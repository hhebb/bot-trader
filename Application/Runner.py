import datetime
from Core.Market import Market
from PyQt5.QtCore import pyqtSignal, QObject
from Core.Agent import Agent
import time

class RunnerWorker(QObject):
    stepped = pyqtSignal(object, object, object, object)
    # 알고리즘이 step 마다 행동을 취하고 emit.
    agentStepSignal = pyqtSignal(object, object, object, object, object)
    # 수동으로 조작할 때마다 agent 에서부터 연쇄적으로 emit 함. connect 는 top level GUI 에서.
    # manualOrderSignal = pyqtSignal(object, object) # order, ledger

    def __init__(self):
        super().__init__()
        self.__market = Market()
        self.__agent = Agent(10000)
        self.__timestamp = datetime.datetime.strptime('2021-08-22 15:24:13', '%Y-%m-%d %H:%M:%S')
        self.__market.dbManager.Connect(db='data', collection=str(self.__timestamp))
        # self.__agent.GetManualOrderThread().manualOrderSignal.connect(self.manualOrderSignal.emit)
        # collection 들 표시하고 선택한 후에 DB 연결을 수행하도록 변경하기.
        # self.__pair = self.__market.dbManager.pair
        # self.__timestamp = datetime.datetime.strptime(self.__market.dbManager.timestamp, '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0
        self.ready = True

    def Simulate(self):
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while True: #self.step < 180:
            # print(self.step)
            time.sleep(.02)
            while not self.ready:
                time.sleep(.0001)
                pass
            self.__market.Step(self.__timestamp)
            # self.__agent.Execute()
            ask = self.__market.GetASK()
            bid = self.__market.GetBID()
            trans = self.__market.GetTransaction()
            ticker = self.__market.GetTicker()
            # print('> trans: ', self.__market.GetTransaction().GetHistoryDiff())
            self.__timestamp += datetime.timedelta(seconds=1)
            self.step += 1
            self.stepped.emit(ask, bid, trans, ticker)
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
            self.__agent.CancelAll()
            marketPrice = trans.GetHistory()[-1].price
            # print(self.__agent.GetEvaluation({'xrp': marketPrice}))
            evaluation = self.__agent.GetEvaluation({'xrp': marketPrice})
            ledger = self.__agent.GetLedger()
            orders = self.__agent.GetOrders()
            history = self.__agent.GetHistory()
            self.agentStepSignal.emit(self.__agent.GetInitAsset(), evaluation, ledger, orders, history)
        self.step = 0

    def SetReady(self):
        self.ready = True

    # def run(self) -> None:
    #     self.Simulate()

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent