import datetime
from Core.Market import Market
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Core.Agent import Agent
import time

class RunnerThread(QThread):
    stepped = pyqtSignal(object, object, object)

    def __init__(self):
        super().__init__()
        self.__market = Market()
        self.__agent = Agent(100)
        self.__timestamp = datetime.datetime.strptime('2021-08-07 15:56:49', '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0
        self.ready = True

    def Simulate(self):
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while self.step < 180:
            tmp = 0
            time.sleep(.15)
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

            # agent act
            self.__agent.UpdataStatus(self.__market)

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