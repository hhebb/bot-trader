import datetime
from Core.Market import Market
# from ..Core import Agent

class Runner:
    def __init__(self):
        self.__market = Market()
        # self.__agent = Agent.Agent()
        self.__timestamp = None
        self.speed = 1

    def Simulate(self):
        # collection total count 로 loop 돌려야 함.
        # initial timestamp 지정해야 함.
        while True:
            self.__market.Step(self.__timestamp)
            # self.__agent.Execute()
            self.__timestamp = datetime.timedelta(seconds=1)
            break

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent