class Transaction:
    def __init__(self):
        self.__max_size = 1000
        self.__history = list()

    def Update(self, data):
        # data 갯수만큼 업데이트.
        for d in data:
            pass


        if len(self.__history) > self.__max_size:
            self.__history.pop(0)

        datas = [MarketOrder('bid', 0, 1000, 4)]
        self.__history.extend(datas)

    def GetHistory(self):
        return self.__history


class MarketOrder:
    def __init__(self, timestamp, position, price, amount):
        self.timestamp = timestamp
        self.type = position # bid or ask
        self.price = price
        self.amount = amount