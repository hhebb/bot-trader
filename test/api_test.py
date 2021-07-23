import asyncio
import websockets
import json
import datetime
import pymongo

class DBManager:
    def __init__(self):
        self.conn: pymongo.MongoClient = None
        self.db = None
        self.collection = None

    def Connect(self, db='test', coll='tmp'):
        self.conn = pymongo.MongoClient('localhost', 27017)
        self.db = self.conn.get_database(db)
        self.collection = self.db.get_collection(coll)

    def GetData(self):
        # cursor 는 generator 혹은 iterator.
        result = self.collection.find()
        for res in result:
            print(res, type(res))

    def Write(self, data):
        self.collection.insert_one(data)

    def Clear(self):
        self.collection.drop()


async def bithumb_ws_client():
    uri = "wss://pubwss.bithumb.com/pub/ws"
    manager = DBManager()
    async with websockets.connect(uri, ping_interval=None) as websocket:
        manager.Connect()

        greeting = await websocket.recv()
        print('greeting: ', greeting)

        subscribe_fmt = {
        "type":"orderbookdepth",
        "symbols": ["XRP_KRW"],
        "tickTypes": ["12H"]
        }
        subscribe_data = json.dumps(subscribe_fmt)
        await websocket.send(subscribe_data)

        status = await websocket.recv()
        status = json.loads(status)
        if status['status'] == '0000':
            pass

        stamp = 0

        while True:
            data = await websocket.recv()
            data = json.loads(data)

            ##################
            # transaction
            # data = data['content']['list']
            # trs = [(tr['contDtm'], tr['buySellGb'], tr['contPrice'], tr['contQty']) for tr in data]
            # print(trs)

            #############
            # ticker
            # t = data['content']['time']
            # close, open = data['content']['closePrice'], data['content']['openPrice']
            # power = data['content']['volumePower']
            # print(t, close, open, power)

            #############
            # orderbook
            # stamp = float(data['content']['datetime'][:-6] + '.' + data['content']['datetime'][-6:])
            # stamp = datetime.datetime.fromtimestamp(stamp)
            # print(stamp)
            data = data['content']['list']
            orders = [(order['orderType'], order['price'], order['quantity'], order['total']) for order in data]
            print(orders)

            row = {'timestamp' : stamp, 'data' : orders}
            manager.Write(row)
            stamp += 1



async def main():
     await bithumb_ws_client()

asyncio.run(main())