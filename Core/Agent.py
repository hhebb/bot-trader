class Agent:
    def __init__(self, asset):
        self.__initialAsset = asset
        self.__currentAsset = asset
        self.__tradeCount = 0
        self.__fiat = 0
        self.__balance = dict()
        self.__yield = 0
        self.__winRate = 0

    def UpdataStatus(self, market):
        # print("i'm agent")
        for k, v in self.__balance.items():
            # 현재 가격을 받아서 balance 변화, asset 변화
            pass

    def ExecuteStratage(self):
        pass

    def Sell(self, amount=0):
        if amount == 0:
            return

    def Buy(self, amount=0):
        if amount == 0:
            return
