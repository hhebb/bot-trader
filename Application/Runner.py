import datetime
from Core.Market import Market
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Core.Agent import Agent
import time
from namespace import *

class RunnerWorker(QObject):
    stepped = pyqtSignal(object, object, object, object)
    # 알고리즘이 step 마다 행동을 취하고 emit.
    agentStepSignal = pyqtSignal(object, object, object, object, object)
    transactionSignal = pyqtSignal(object, object) # orders, ledger
    automaticOrderSignal = pyqtSignal()

    # 수동으로 조작할 때마다 agent 에서부터 연쇄적으로 emit 함. connect 는 top level GUI 에서.
    # manualOrderSignal = pyqtSignal(object, object) # order, ledger
    '''
        * signal
            * stepped: simulate step 이후 market ask, bid, transaction, ticker 전달.
            * agentStepSignal: simulate step 이후 asset, eval, ledger, orders, history 전달.
            * transactionSignal: 거래가 체결되면 GUI 갱신을 위해 user orders, ledger 를 전달.
    '''
    def __init__(self):
        super().__init__()
        self.__market = Market()
        self.__agent = Agent(10000)
        self.__timestamp = datetime.datetime.strptime('2021-08-22 15:24:13', '%Y-%m-%d %H:%M:%S')
        self.__market.dbManager.Connect(db='data', collection=str(self.__timestamp))
        self.__agent.transactionSignal.connect(self.transactionSignal.emit)
        # collection 들 표시하고 선택한 후에 DB 연결을 수행하도록 변경하기.
        # self.__pair = self.__market.dbManager.pair
        # self.__timestamp = datetime.datetime.strptime(self.__market.dbManager.timestamp, '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0
        self.ready = True
        self.__simulateState = SimulateState.STOP
        self.__simulateSpeed = 10

    def Simulate(self):
        '''
            Simulate automatically.
            appropriate time delay for rendering sync.
        '''
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while True:
            time.sleep(.2 * 1 / self.__simulateSpeed)
            while self.__simulateState == SimulateState.STOP:
                time.sleep(.001)
                pass

            # instantly simulate single step.
            self.SimulateStep()
        self.step = 0

    def SimulateStep(self):
        '''
            1 single step.
            For manual step simulation.
        '''
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
        askPrice = ask.GetLOB()[primeAskKey].price  # ->LimitOrder, order[amount], order[count]
        primeBidKey = list(bid.GetLOB().keys())[-1]
        bidPrice = bid.GetLOB()[primeBidKey].price  # ->LimitOrder, order[amount], order[count]
        self.__agent.Transact(ask=ask, bid=bid)

        self.__agent.AutoBuy(pair='xrp', price=askPrice, amount=1)
        self.__agent.AutoSell(pair='xrp', price=bidPrice, amount=2)

        marketPrice = trans.GetHistory()[-1].price
        # print(self.__agent.GetEvaluation({'xrp': marketPrice}))
        evaluation = self.__agent.GetEvaluation({'xrp': marketPrice})
        ledger = self.__agent.GetLedger()
        orders = self.__agent.GetOrders()
        history = self.__agent.GetHistory()
        self.agentStepSignal.emit(self.__agent.GetInitAsset(), evaluation, ledger, orders, history)

    def ToggleSimulateState(self):
        if self.__simulateState == SimulateState.STOP:
            self.__simulateState = SimulateState.RUNNING
        else:
            self.__simulateState = SimulateState.STOP

    def StopSimulate(self):
        if self.__simulateState == SimulateState.RUNNING:
            self.__simulateState = SimulateState.STOP

    def SetReady(self):
        self.ready = True

    def SpeedUp(self):
        if self.__simulateSpeed >= SimulateSpeedLimit.UPPER_BOUND.value:
            return
        self.__simulateSpeed += 1

    def SpeedDown(self):
        if self.__simulateSpeed <= SimulateSpeedLimit.LOWER_BOUND.value:
            return
        self.__simulateSpeed -= 1

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent