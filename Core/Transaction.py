import datetime

class Transaction:
    '''
        history: [MarketOrder, ...]
        MarketOrder: type, price, amount, order
    '''
    def __init__(self):
        self.__max_size = 1000
        self.__history = list()
        self.__historyDiff = list()
        self.order = 0
        self.orderReset = False

    def SetSnapshot(self, snapshot: list):
        # 최초 snapshot 데이터를 transaction 에 대입.
        # 또는 주기적으로 초기화

        self.__history = list()
        self.order = 0
        for d in snapshot:
            stamp = d['transaction_date']
            position = d['type']
            price = float(d['price'])
            amount = float(d['units_traded'])
            self.__history.append(MarketOrder(stamp, position, price, amount, self.order))
            self.order += 1

        self.orderReset = True

    def Update(self, data: list):
        # data 갯수만큼 업데이트.
        self.__historyDiff = list()
        for d in data:
            seconds = datetime.datetime.strptime(d['contDtm'].split('.')[0], '%Y-%m-%d %H:%M:%S')
            stamp = str(seconds)
            position = 'ask' if d['buySellGb'] == 1 else 'bid'
            price = float(d['contPrice'])
            amount = float(d['contQty'])
            self.__history.append(MarketOrder(stamp, position, price, amount, self.order))
            self.__historyDiff.append(MarketOrder(stamp, position, price, amount, self.order))
            self.order += 1

        if len(self.__history) > self.__max_size:
            self.__history.pop(0)


    def GetHistory(self):
        return self.__history

    def GetHistoryDiff(self):
        return self.__historyDiff

    def GetIsReset(self):
        return self.orderReset

    def UnSet(self):
        self.orderReset = False


class MarketOrder:
    def __init__(self, timestamp: str, position: str, price: float, amount: float, order: int):
        self.timestamp = timestamp
        self.type = position # bid or ask
        self.price = price
        self.amount = amount
        self.order = order
