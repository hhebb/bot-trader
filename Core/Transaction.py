class Transaction:
    def __init__(self):
        self.__max_size = 1000
        self.__history = list()

    def SetSnapshot(self, snapshot: list):
        # 최초 snapshot 데이터를 transaction 에 대입.
        # 또는 주기적으로 초기화

        self.__history = list()
        for d in snapshot:
            stamp = d['transaction_date']
            position = d['type']
            price = float(d['price'])
            amount = float(d['units_traded'])
            self.__history.append(MarketOrder(stamp, position, price, amount))

        # print(self.__history)

    def Update(self, data: list):
        # data 갯수만큼 업데이트.
        for d in data:
            stamp = d['contDtm']
            position = 'ask' if d['buySellGb'] == 1 else 'bid'
            price = float(d['contPrice'])
            amount = float(d['contQty'])
            self.__history.append(MarketOrder(stamp, position, price, amount))

        if len(self.__history) > self.__max_size:
            self.__history.pop(0)

        # print(self.__history)

    def GetHistory(self):
        return self.__history


class MarketOrder:
    def __init__(self, timestamp: str, position: str, price: float, amount: float):
        self.timestamp = timestamp
        self.type = position # bid or ask
        self.price = price
        self.amount = amount
