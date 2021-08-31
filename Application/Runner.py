import datetime
from Core.Market import Market
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Core.Agent import Agent
import time

class RunnerThread(QThread):
    stepped = pyqtSignal(object, object, object)
    agentInfoSignal = pyqtSignal(object, object, object, object, object)

    def __init__(self):
        super().__init__()
        self.__market = Market()
        self.__agent = Agent(10000)
        self.__timestamp = datetime.datetime.strptime('2021-08-22 15:24:13', '%Y-%m-%d %H:%M:%S')
        self.__market.dbManager.Connect(db='data', collection=str(self.__timestamp))
        # collection 들 표시하고 선택한 후에 DB 연결을 수행하도록 변경하기.
        # self.__pair = self.__market.dbManager.pair
        # self.__timestamp = datetime.datetime.strptime(self.__market.dbManager.timestamp, '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0
        self.ready = True

    def Simulate(self):
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while self.step < 180:
            tmp = 0
            time.sleep(.1)
            while not self.ready:
                tmp += 1
                # print('', end=' ')
                pass
            self.__market.Step(self.__timestamp)
            # self.__agent.Execute()
            ask = self.__market.GetASK()
            bid = self.__market.GetBID()
            trans = self.__market.GetTransaction()
            # print('> trans: ', self.__market.GetTransaction().GetHistoryDiff())
            self.__timestamp += datetime.timedelta(seconds=1)
            self.step += 1
            self.stepped.emit(ask, bid, trans)
            # print('> step', self.step)
            # QThread.sleep(2)
            self.ready = False

            # 시장가 get
            primeAskKey = list(ask.GetLOB().keys())[0]
            askPrice = ask.GetLOB()[primeAskKey].price #->LimitOrder, order[amount], order[count]
            primeBidKey = list(bid.GetLOB().keys())[-1]
            bidPrice = bid.GetLOB()[primeBidKey].price #->LimitOrder, order[amount], order[count]
            self.__agent.Transact(ask=ask, bid=bid)
            self.__agent.Buy(pair='xrp', price=askPrice, amount=1)
            self.__agent.Sell(pair='xrp', price=bidPrice, amount=2)
            marketPrice = trans.GetHistory()[-1].price
            # print(self.__agent.GetEvaluation({'xrp': marketPrice}))
            evaluation = self.__agent.GetEvaluation({'xrp': marketPrice})
            ledger = self.__agent.GetLedger()
            orders = self.__agent.GetOrders()
            history = self.__agent.GetHistory()
            self.agentInfoSignal.emit(self.__agent.GetInitAsset(), evaluation, ledger, orders, history)
        self.step = 0

    def SetReady(self, ready):
        self.ready = True

    def run(self) -> None:
        self.Simulate()

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent