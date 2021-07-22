import heapq

class OrderBook:
    def __init__(self, position):
        self.__type = position
        self.__LOB = dict()
        self.__LOB_list = list()
        self.__init_size = 10

    def SetSnapshot(self, snapshot):
        # 최초 snapshot 데이터를 orderbook 에 대입.
        self.__LOB = snapshot

    def Update(self, data):
        # 신규 호가는 append, 기존 호가는 change.
        self.__LOB[10000] = LimitOrder(10000, 10, 1)
        self.__LOB_list = list(self.__LOB)
        heapq.heapify(self.__LOB_list)
        self.__LOB = dict(self.__LOB_list)

    def GetLOB(self):
        return self.__LOB


class LimitOrder:
    def __init__(self, price, amount, count):
        self.price = price
        self.amount = amount
        self.count = count
