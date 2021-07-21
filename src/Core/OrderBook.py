import heapq

class OrderBook:
    def __init__(self, position):
        self.type = position
        self.LOB = dict()
        self.LOB_list = list()
        self.init_size = 10

    def Parse(self):
        # db parse + heap 조작 logic
        self.LOB[10000] = LimitOrder(10000, 10, 1)
        # heapq.heappush(self.LOB, Order(10000, 10, 1))
        self.LOB[10000].Update(100, 2)
        self.LOB_list = list(self.LOB)
        heapq.heapify(self.LOB_list)
        self.LOB = dict(self.LOB_list)

    def GetLOB(self):
        return self.LOB


class LimitOrder:
    def __init__(self, price, amount, count):
        self.price = price
        self.amount = amount
        self.count = count

    def Update(self, amount, count):
        # 해당 price 의 수량이 변하면 업데이트
        self.amount = amount
        self.count = count