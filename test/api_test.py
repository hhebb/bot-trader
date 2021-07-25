import asyncio
import websockets
import json
import datetime
import pymongo
import requests

class DBManager:
    def __init__(self):
        self.conn: pymongo.MongoClient = None
        self.db = None
        self.collection = None

    def Connect(self, db='test', coll='tmp'):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn.get_database(db)
        self.collection = self.db.get_collection(coll)

    def GetRow(self, timestamp):
        # find 는 cursor 반환. cursor 는 generator 혹은 iterator.
        # find_one 은 dict 반환
        query = {'timestamp' : {'$eq':timestamp}}
        result = self.collection.find_one(query)
        # for res in result:
        #     print(res, type(res))
        return result

    def WriteLOB(self, stamp, lob):
        self.collection.update_one({'timestamp': stamp}, {'$set': {'lob': lob}}, upsert=True)

    def PushLOB(self, stamp, lob):
        self.collection.update_one({'timestamp': stamp}, {'$push': {'lob': lob}}, upsert=True)

    def WriteTransaction(self, stamp, transaction):
        self.collection.update_one({'timestamp': stamp}, {'$set': {'transaction': transaction}}, upsert=True)

    def PushTransaction(self, stamp, transaction):
        self.collection.update_one({'timestamp': stamp}, {'$push': {'transaction': transaction}}, upsert=True)

    def WriteLOBSnapshot(self, stamp, snapshot):
        self.collection.update_one({'timestamp': stamp}, {'$set': {'snapshot_lob': snapshot}}, upsert=True)

    def WriteTransactionSnapshot(self, stamp, snapshot):
        self.collection.update_one({'timestamp': stamp}, {'$set': {'snapshot_transaction': snapshot}}, upsert=True)

    def Clear(self):
        self.collection.drop()


async def LOBSaver(manager):
    uri = "wss://pubwss.bithumb.com/pub/ws"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        greeting = await websocket.recv()
        print('> LOB saver connected: ', greeting)

        subscribe_fmt = {
            "type": "orderbookdepth",
            "symbols": ["XRP_KRW"],
            "tickTypes": ["12H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        status = await websocket.recv()
        status = json.loads(status)
        if status['status'] == '0000':
            pass

        # initial stamp save.
        now = datetime.datetime.now().replace(microsecond=0)
        LOBSnapshotSaver(manager, now)
        count = 0

        while True:
            # orderbook
            data = await websocket.recv()
            data = json.loads(data)
            stamp = float(data['content']['datetime'][:-6])
            stamp = datetime.datetime.fromtimestamp(stamp)
            orderData = data['content']['list']

            # row = {'timestamp' : stamp, 'lob' : orderData}
            result = manager.GetRow(stamp)

            if result is not None:
                # document 가 이미 있으며 lob 가 이미 있을 땐 확장 후 update.
                if 'lob' in result.keys():
                    # print('> lob, document exist, lob exist')
                    # result['lob'].extend(orderData)
                    # manager.WriteLOB(stamp, result['lob'])
                    manager.PushLOB(stamp, orderData)
                # document 는 있는데 lob 가 없으면 field 만 update.
                else:
                    # print('> lob, document exist')
                    manager.WriteLOB(stamp, orderData)
            # document 가 없을 땐, 신규 생성 insert.
            else:
                # print('> lob, no document')
                manager.WriteLOB(stamp, orderData)

            # snapshot save
            if count % 5 == 0:
                LOBSnapshotSaver(manager, stamp)
                # print('> snapshot save')

            count += 1

async def TransactionSaver(manager):
    uri = "wss://pubwss.bithumb.com/pub/ws"
    async with websockets.connect(uri, ping_interval=None) as websocket:
        greeting = await websocket.recv()
        print('> transaction saver connected: ', greeting)

        subscribe_fmt = {
        "type":"transaction",
        "symbols": ["XRP_KRW"],
        "tickTypes": ["12H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        status = await websocket.recv()
        status = json.loads(status)
        if status['status'] == '0000':
            pass

        # initial stamp save.
        now = datetime.datetime.now().replace(microsecond=0)
        TransactionSnapshotSaver(manager, now)
        count = 0

        while True:
            # transaction
            data = await websocket.recv()
            data = json.loads(data)
            transactionData = data['content']['list']

            separated = dict()
            for trans in transactionData:
                # print(trans['contDtm'])
                stamp = trans['contDtm']
                stamp = datetime.datetime.strptime(stamp.split('.')[0], '%Y-%m-%d %H:%M:%S')
                if stamp not in separated.keys():
                    separated[stamp] = list()
                separated[stamp].append(trans)
                # row = {'timestamp': stamp, 'data': trans}
                # print('> trans: ', row)
                # manager.Write(row)

            for stamp, trans in separated.items():
                result = manager.GetRow(stamp)
                if result is not None:
                    if 'transaction' in result.keys():
                        # print('> trans, document exist, lob exist')
                        manager.PushTransaction(stamp, trans)
                    else:
                        # print('> trans, document exist')
                        manager.WriteTransaction(stamp, trans)
                else:
                    # print('> trans, no document')
                    manager.WriteTransaction(stamp, trans)

            # snapshot save
            if count % 5 == 0:
                TransactionSnapshotSaver(manager, stamp)
                # print('> transaction snapshot save', count)

            # print(count)
            count += 1

def LOBSnapshotSaver(manager, stamp):
    url = 'https://api.bithumb.com/public/orderbook/XRP_KRW'
    params = {'count': 5}
    result = requests.get(url=url, params=params)
    j = result.json()
    manager.WriteLOBSnapshot(stamp, j['data'])

def TransactionSnapshotSaver(manager, stamp):
    url = 'https://api.bithumb.com/public/transaction_history/XRP_KRW'
    params = {'count': 5}
    result = requests.get(url=url, params=params)
    j = result.json()
    manager.WriteTransactionSnapshot(stamp, j['data'])

async def main():
    manager = DBManager()
    manager.Connect()

    # task 로 만들어서 event loop 에 한 번에 등록해도 됨.
    savers = [TransactionSaver(manager), LOBSaver(manager)]
    await asyncio.gather(*savers)


asyncio.run(main())