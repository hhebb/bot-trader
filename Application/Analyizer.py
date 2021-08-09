import datetime
from Core.Market import Market
from Core.Agent import Agent
import time

class Analyzer:
    def __init__(self):
        self.__market = Market()
        self.__agent = Agent(100)
        self.__timestamp = datetime.datetime.strptime('2021-08-07 15:56:49', '%Y-%m-%d %H:%M:%S')
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
            self.__market.Step(self.__timestamp)
            ask = self.__market.GetASK()
            bid = self.__market.GetBID()
            trans = self.__market.GetTransaction()
            self.__timestamp += datetime.timedelta(seconds=1)
            self.step += 1

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

if __name__ == '__main__':
    analyzer = Analyzer()
    analyzer.Simulate()