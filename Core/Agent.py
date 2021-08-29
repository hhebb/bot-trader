from  namespace import *
from collections import defaultdict

class Agent:
    '''
        ledger: {pair: amount, ...}
        orders: {id: {pair: '', position: '', price: '', amount: ''}, ...}
        history: [{pair: '', position: '', price: '', amount: ''}, ...]

    '''
    def __init__(self, asset):
        self.__ledger = defaultdict(float)
        self.__orders = dict()
        self.__history = list()
        self.__tradeCount = 0
        self.__initialAsset = asset
        self.__orderId = 0

        self.__yield = 0
        self.__winRate = 0

        self.__initializeAcount()

    def __initializeAcount(self):
        self.__orderId = 0
        self.__ledger['fiat'] = self.__initialAsset
        self.__history = list()
        self.__tradeCount = 0

    # def UpdateLedger(self, pair: str, price: float, amount: float, status: int):
    #     # ledger[pair][price] = {amount, status}. 무조건 실행. 조건 안걸리면 넘어감.
    #     if pair not in self.__ledger:
    #         self.__ledger[pair] = dict()
    #         if price not in self.__ledger[pair]:
    #             self.__ledger[pair][price] = dict()
    #     else:
    #         if price not in self.__ledger[pair]:
    #             self.__ledger[pair][price] = dict()
    #         else:
    #             pass
    #
    #     self.__ledger[pair][price] = {'amount': amount, 'status': status}
    #
    #     # buy 로 인해 주문이 생기면 반드시 그만큼 fiat 를 빼야함.
    #     if amount > 0:
    #         self.__ledger['fiat'][FIAT_PRICE]['amount'] -= price * amount


    def AppendHistory(self, pair: str, position: int, price: float, amount: float):
        item = {'pair': pair, 'position': position, 'price': price, 'amount': amount}
        self.__history.append(item)

    def ExecuteStratage(self):
        pass

    def Sell(self, pair: str, price: float, amount: float):
        # 팔 때는 order 에만 변화가 일어남. 주문만 들어간 상태로, 체결은 다음 틱부터 가능.
        order = {'pair': pair, 'position': EPostion.SELL, 'price': price, 'amount': amount}
        self.__ledger[pair] -= amount
        self.__orders[self.__orderId] = order
        self.__orderId += 1

    def Buy(self, pair: str, price: float, amount: float):
        # 살 때는 ledger[fiat], order 에만 변화가 일어남. 주문만 들어간 상태로, 체결은 다음 틱부터 가능.
        order = {'pair': pair, 'position': EPostion.BUY, 'price': price, 'amount': amount}
        self.__ledger['fiat'] -= price * amount
        self.__orders[self.__orderId] = order
        self.__orderId += 1

    def Cancle(self, pair: str, price: float):
        # 취소 주문. 해당 ledger 걍 삭제. 현금 복원.
        _amount = self.__ledger[pair][price]['amount']
        _price = self.__ledger[pair][price]['price']
        del self.__ledger[pair][price]
        self.__ledger['fiat'][FIAT_PRICE] += _amount * _price

    def Transact(self, ask, bid):
        # 체결되는 조건 - 시장가 범위 내에 위치 + 주문 가격에 잔량 존재.
        toRemove = list()
        ask = ask.GetLOB()
        bid = bid.GetLOB()
        for orderId in self.__orders.keys():
            order = self.__orders[orderId]
            price = order['price']
            amount = order['amount']
            if order['position'] == EPostion.BUY:
                # buy 체결될 때. ledger 추가. history 추가.
                if price in ask.keys():
                    if ask[price].amount >= amount:
                        self.__ledger[order['pair']] += amount
                        self.__history.append(order)
                        toRemove.append(orderId)
            elif order['position'] == EPostion.SELL:
                # sell 체결될 때. 체결된 만큼 현금으로 돌아옴. history 추가.
                if price in bid.keys():
                    if bid[price].amount >= amount:
                        self.__ledger['fiat'] += price * amount
                        self.__history.append(order)
                        toRemove.append(orderId)

        # closed order remove from orders
        for key in toRemove:
            del self.__orders[key]


    def GetEvaluation(self, currentPrices: dict):
        # 현재 자산가치 평가. ledger 에서 완전히 체결이 이루어진 상태 기준으로 asset 평가
        totalAsset = 0
        for pair in self.__ledger.keys():
            if pair == 'fiat':
                # 현금일 땐 걍 더해줌.
                totalAsset += self.__ledger[pair]
            else:
                # 주식일 땐 현재가로 계산
                amount = self.__ledger[pair]
                totalAsset += amount * currentPrices[pair]

        return totalAsset


    def GetFiat(self) -> dict:
        # {amount, status}
        return self.__ledger['fiat'][FIAT_PRICE]

    def GetLedger(self, pair=None) -> dict:
        if pair is not None:
            return self.__ledger[pair]
        else:
            return self.__ledger

    def GetHistory(self):
        return self.__history

    def GetOrders(self):
        return self.__orders