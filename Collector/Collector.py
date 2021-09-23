import asyncio
import websockets
import json
import datetime
import requests
from Core.DBManager import DBManager

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
            result = manager.QueryRow(stamp)

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
                result = manager.QueryRow(stamp)
                if result is not None:
                    if 'transaction' in result.keys():
                        # print('> trans, document exist, trans exist')
                        # transaction 형태때문에 어쩔 수 없이 복잡해짐.
                        for t in trans:
                            manager.PushTransaction(stamp, t)
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
    manager.WriteLOBSnapshot(stamp, [j['data']['bids'], j['data']['asks']])

def TransactionSnapshotSaver(manager, stamp):
    url = 'https://api.bithumb.com/public/transaction_history/XRP_KRW'
    params = {'count': 5}
    result = requests.get(url=url, params=params)
    j = result.json()
    manager.WriteTransactionSnapshot(stamp, j['data'])

async def main():
    manager = DBManager()
    now = str(datetime.datetime.now().replace(microsecond=0))
    print(now)
    # manager.Connect('data', now)
    manager.SetCurrentDB('data')
    manager.SetCurrentCollection(now)


    # task 로 만들어서 event loop 에 한 번에 등록해도 됨.
    savers = [TransactionSaver(manager), LOBSaver(manager)]
    await asyncio.gather(*savers)


asyncio.run(main())
