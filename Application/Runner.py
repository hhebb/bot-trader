import datetime
from Core.Market import Market
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Core.Agent import Agent
import time
from namespace import *


class RunnerWorker(QObject):
    '''
        * signal
        * stepped: simulate step 알림. market GUI 들이 update 되도록 함.
        * transactionSignal: user 체결 알림. user GUI 들이 update 되도록 함.
    '''

    stepped = pyqtSignal()
    # 알고리즘이 step 마다 행동을 취하고 emit.
    transactionSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__market = Market()
        self.__agent = Agent(10000)
        self.__timestamp = datetime.datetime.strptime('2021-09-22 00:36:11', '%Y-%m-%d %H:%M:%S') # 2021-09-09 11:48:43 # 2021-09-22 00:36:11
        self.__market.dbManager.SetCurrentDB(dbName='data')
        self.__market.dbManager.SetCurrentCollection(collectionName=str(self.__timestamp))
        self.__market.dbManager.QueryAllRows()
        self.__agent.transactionSignal.connect(self.transactionSignal.emit)
        # collection 들 표시하고 선택한 후에 DB 연결을 수행하도록 변경하기.
        # self.__pair = self.__market.dbManager.pair
        # self.__timestamp = datetime.datetime.strptime(self.__market.dbManager.timestamp, '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0
        self.ready = True
        self.__simulateState = SimulateState.STOP
        self.__simulateSpeed = 10

    def InitRunner(self):
        self.__market.dbManager.SetCurrentDB(dbName='data')
        self.__market.dbManager.SetCurrentCollection(collectionName=str(self.__timestamp))
        self.__market.dbManager.QueryAllRows()
        self.__market.InitializeMarket()

        self.__agent.InitializeAcount()

        self.step = 0
        self.ready = True
        self.__simulateState = SimulateState.STOP
        self.__simulateSpeed = 10

    def SetStartTime(self, startTime: datetime.datetime):
        self.__timestamp = startTime
        self.__market.dbManager.SetCurrentDB(dbName='data')
        self.__market.dbManager.SetCurrentCollection(collectionName=str(self.__timestamp))
        self.__market.dbManager.QueryAllRows()

    def Simulate(self):
        '''
            thread work.
            Simulate automatically.
            appropriate time delay for rendering sync.
        '''
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while True:
            time.sleep(.4 * 1 / self.__simulateSpeed) #.2
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
        self.__timestamp += datetime.timedelta(seconds=1)
        self.step += 1
        self.stepped.emit()
        # QThread.sleep(2)
        self.ready = False

        # 시장가 get
        primeAskKey = list(self.__market.GetASK().GetLOB().keys())[0]
        askPrice = self.__market.GetASK().GetLOB()[primeAskKey].price  # ->LimitOrder, order[amount], order[count]
        primeBidKey = list(self.__market.GetBID().GetLOB().keys())[-1]
        bidPrice = self.__market.GetBID().GetLOB()[primeBidKey].price  # ->LimitOrder, order[amount], order[count]
        self.__agent.Transact(ask=self.__market.GetASK(), bid=self.__market.GetBID())

        # order test.
        self.__agent.AutoBuy(pair='xrp', price=askPrice, amount=1)
        self.__agent.AutoSell(pair='xrp', price=bidPrice, amount=2)

    def GetSimulateState(self):
        return self.__simulateState

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