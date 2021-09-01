from  namespace import *
from collections import defaultdict
from copy import copy

class Agent:
    '''
        ledger: {pair: amount, ...}
        orders: {id: {pair: '', position: '', price: '', amount: ''}, ...}
        history: [{pair: '', position: '', price: '', amount: ''}, ...]
        
        필요한거 - *총자산평가, -승률, 순이익, 잔고(현금, 주식 별로)
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

    def AppendHistory(self, pair: str, position: int, price: float, amount: float):
        item = {'pair': pair, 'position': position, 'price': price, 'amount': amount}
        self.__history.append(item)

    def ExecuteStratage(self):
        pass

    def Sell(self, pair: str, price: float, amount: float):
        # 팔 때. ledger 주식 차감, order 추가. 주문만 들어간 상태로, 체결은 다음 틱부터 가능.
        print(self.__ledger[pair], amount)
        if self.__ledger[pair] < amount:
            return
        order = {'pair': pair, 'position': EPostion.SELL, 'price': price, 'amount': amount}
        self.__ledger[pair] -= amount
        self.__orders[self.__orderId] = order
        self.__orderId += 1

    def Buy(self, pair: str, price: float, amount: float):
        # 살 때. ledger 현금 차감, order 추가. 주문만 들어간 상태로, 체결은 다음 틱부터 가능.
        if self.__ledger['fiat'] < price * amount:
            return
        order = {'pair': pair, 'position': EPostion.BUY, 'price': price, 'amount': amount}
        self.__ledger['fiat'] -= price * amount
        self.__orders[self.__orderId] = order
        self.__orderId += 1

    def Cancel(self, orderId: int):
        # 취소 주문. ledger 복원. order 삭제.
        order = self.__orders[orderId]
        pair = order['pair']
        amount = order['amount']
        price = order['price']
        position = order['position']

        if position == EPostion.BUY:
            # buy 주문 취소할 때 현금 복원
            self.__ledger['fiat'] += price * amount
        else:
            # sell 주문 취소할 때 수량 복원
            self.__ledger[pair] += amount

        del self.__orders[orderId]

    def CancelAll(self):
        orderIds = list(self.__orders.keys())
        for orderId in orderIds:
            self.Cancel(orderId)

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
                # buy 체결될 때. ledger 주식 추가. order 삭제. history 추가. 체결 조건.
                if price >= min(ask.keys()):
                    transPrice = min(ask.keys())
                    # 0, 1 주 같은 낚시 물량 걸러내려는 의도.
                    if ask[transPrice].amount >= amount:
                        self.__ledger[order['pair']] += amount
                        self.__history.append(order)
                        toRemove.append(orderId)
            elif order['position'] == EPostion.SELL:
                # sell 체결될 때. ledger 현금 추가. order 삭제. history 추가. 체결 조건.
                if price <= max(bid.keys()):
                    transPrice = max(bid.keys())
                    if bid[transPrice].amount >= amount:
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
                # print(amount, pair)
                totalAsset += amount * currentPrices[pair]

        for key, order in self.__orders.items():
            if order['position'] == EPostion.BUY:
                price = order['price']
                amount = order['amount']
                totalAsset += price * amount
            if order['position'] == EPostion.SELL:
                pair = order['pair']
                price = currentPrices[pair]
                amount = order['amount']
                totalAsset += price * amount
        return totalAsset

    def GetInitAsset(self):
        return self.__initialAsset

    def GetFiat(self) -> dict:
        # {amount, status}
        return self.__ledger['fiat'][FIAT_PRICE]

    def GetLedger(self, pair=None) -> dict:
        if pair is not None:
            return self.__ledger[pair]
        else:
            return self.__ledger

    def GetHistory(self) -> list:
        return self.__history

    def GetOrders(self) -> dict:
        return self.__orders