class OrderBook:
    def __init__(self, position):
        self.__type = position
        self.__LOB = dict()
        # self.__LOB_list = list()
        self.__init_size = 20

    def SetSnapshot(self, snapshot: list):
        # 최초 snapshot 데이터를 orderbook 에 대입.
        # 또는 주기적으로 초기화

        self.__LOB = dict()
        for d in snapshot:
            price = float(d['price'])
            amount = float(d['quantity'])
            count = -1
            self.__LOB[price] = LimitOrder(price, amount, count)

        print(self.__LOB)

    def Update(self, data: list):
        # data 갯수만큼 업데이트 적용
        for d in data:
            price = float(d['price'])
            amount = float(d['quantity'])
            count = int(d['total'])

            # 기존 price
            if price in self.__LOB.keys():
                # print('> exist price')
                # 잔량 소멸
                if count == 0:
                    # print('> zero quantity')
                    del d['price']
                # 잔량 변경
                else:
                    self.__LOB[price].amount = amount
                    self.__LOB[price].count = count
                    # print('> change amount')
            # 신규 price
            else:
                order = LimitOrder(price, amount, count)
                self.__LOB[price] = order
                # print('> new price')

        self.__LOB = dict(sorted(self.__LOB.items()))
        print(self.__LOB)

    def GetLOB(self):
        return self.__LOB


class LimitOrder:
    def __init__(self, price: float, amount: float, count: int):
        self.price = price
        self.amount = amount
        self.count = count
