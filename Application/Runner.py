import datetime
from Core.Market import Market
# from ..Core import Agent

class Runner:
    def __init__(self):
        self.__market = Market()
        # self.__agent = Agent.Agent()
        self.__timestamp = datetime.datetime.strptime('2021-08-01 18:35:05', '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0

    def Simulate(self):
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.

        while self.step < 120:
            self.__market.Step(self.__timestamp)
            # self.__agent.Execute()
            trans = self.__market.GetTransaction()
            # print('> trans: ', trans)
            self.__timestamp += datetime.timedelta(seconds=1)
            self.step += 1

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent