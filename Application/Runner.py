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
        while True:
            self.__market.Step(self.__timestamp)
            # self.__agent.Execute()
            break

    def Pause(self):
        pass

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent