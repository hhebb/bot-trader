from  namespace import *

class Agent:
    def __init__(self, asset):
        self.__ledger = dict()
        self.__history = list()
        self.__tradeCount = 0
        self.__initialAsset = asset

        self.__yield = 0
        self.__winRate = 0

        self.__initializeAcount()

    def __initializeAcount(self):
        self.UpdateLedger(pair='fiat', price=FIAT_PRICE,
                          amount=self.__initialAsset, status=EOrderStatus.COMPLETE)
        self.__history = list()
        self.__tradeCount = 0

    def UpdateLedger(self, pair: str, price: float, amount: float, status: int):
        # ledger[pair][price] = {amount, status}. 무조건 실행. 조건 안걸리면 넘어감.
        if pair not in self.__ledger:
            self.__ledger[pair] = dict()
            if price not in self.__ledger[pair]:
                self.__ledger[pair][price] = dict()
        else:
            if price not in self.__ledger[pair]:
                self.__ledger[pair][price] = dict()
            else:
                pass

        self.__ledger[pair][price] = {'amount': amount, 'status': status}

    def AppendHistory(self, pair: str, position: int, price: float, amount: float):
        item = {'pair': pair, 'position': position, 'price': price, 'amount': amount}
        self.__history.append(item)

    def ExecuteStratage(self):
        pass

    def Sell(self, pair: str, price: float, amount: float):
        self.UpdateLedger(pair=pair, price=price, amount=-amount, status=EOrderStatus.WAIT)
        self.AppendHistory(pair=pair, position=EPostion.SELL, price=price, amount=amount)

    def Buy(self, pair: str, price: float, amount: float):
        self.UpdateLedger(pair=pair, price=price, amount=amount, status=EOrderStatus.WAIT)
        self.AppendHistory(pair=pair, position=EPostion.BUY, price=price, amount=amount)

    def Cancle(self, pair: str, price: float):
        # 취소 주문. 해당 ledger 걍 삭제. 현금 복원.
        _amount = self.__ledger[pair][price]['amount']
        _price = self.__ledger[pair][price]['price']
        del self.__ledger[pair][price]
        self.__ledger['fiat'][FIAT_PRICE] += _amount * _price


    def Evaluation(self, currentPrices: dict):
        # 현재 자산가치 평가. ledger 에서 완전히 체결이 이루어진 상태 기준으로 asset 평가
        totalAsset = 0
        for pair in self.__ledger.keys():
            for price in pair.keys():
                if pair == 'fiat':
                    # 현금일 땐 걍 더해줌.
                    totalAsset += self.__ledger[pair][FIAT_PRICE]['amount']
                else:
                    # 주식일 땐 현재가로 계산
                    status = self.__ledger[pair][price]['status']
                    _amount = self.__ledger[pair][price]['amount']
                    _price = self.__ledger[pair][price]['price']
                    if status == EOrderStatus.WAIT:
                        # 체결되지 않았을 때 그만큼 현금으로 더함.
                        totalAsset += _amount * _price
                    elif status == EOrderStatus.COMPLETE:
                        # 체결되었을 때, 그만큼 현재가 반영해서 더함.
                        totalAsset += _amount * currentPrices[pair]
        return totalAsset


    def GetFiat(self) -> dict:
        # {amount, status}
        return self.__ledger['fiat'][FIAT_PRICE]

    def GetLedger(self, pair=None) -> dict:
        if pair is not None:
            return self.__ledger[pair]
        else:
            return self.__ledger
