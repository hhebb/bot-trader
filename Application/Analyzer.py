import datetime
from PyQt5.QtCore import pyqtSignal, QObject, QThread
from Core.Market import Market
from Core.Agent import Agent
import time

class AnalyzerWorker:
    '''
        rendering 제외하여 빠르게 데이터 분석을 하는 모듈.

        * example *
        analyzer = AnalyzerWorker()
        analyzer.Simulate()
        res = analyzer.GetResult()

    '''

    def __init__(self):
        self.__market = Market()
        self.__agent = Agent(100)
        self.__timestamp = datetime.datetime.strptime('2021-09-09 11:48:43', '%Y-%m-%d %H:%M:%S')
        self.__market.dbManager.SetCurrentDB(dbName='data')
        self.__market.dbManager.SetCurrentCollection(collectionName=str(self.__timestamp))
        self.__dataCount = self.GetRowCount()
        # collection 들 표시하고 선택한 후에 DB 연결을 수행하도록 변경하기.
        # self.__pair = self.__market.dbManager.pair
        # self.__timestamp = datetime.datetime.strptime(self.__market.dbManager.timestamp, '%Y-%m-%d %H:%M:%S')
        self.speed = 1
        self.step = 0

    def Simulate(self):
        '''
            market 분석을 위한 데이터 처리.
        '''

        while self.step < self.__dataCount:
            self.__market.Step(self.__timestamp)
            # ask = self.__market.GetASK()
            # bid = self.__market.GetBID()
            # trans = self.__market.GetTransaction()
            # ticker = self.__market.GetTicker()
            self.__timestamp += datetime.timedelta(seconds=1)
            self.step += 1
            # self.stepped.emit(ask, bid, trans, ticker)

            # agent act
            # self.__agent.UpdataStatus(self.__market)

        self.step = 0

    def GetRowCount(self):
        '''
            collection 의 rows 갯수를 반환.
        '''
        col = self.__market.GetDBManager().GetCurrentCollection()
        return col.count()

    def GetResult(self):
        '''
            collection 에 있는 모든 처리된 rows 를 분석을 위해 반환.
        '''
        ask = self.__market.GetASK()
        bid = self.__market.GetBID()
        trans = self.__market.GetTransaction()
        ticker = self.__market.GetTicker()

        candles = ticker.GetTickChart()
        for candle in candles:
            print(candle.GetOHLC())
        return ask, bid, trans, ticker


    def run(self) -> None:
        self.Simulate()

    def GetMarket(self):
        return self.__market

    def GetAgent(self):
        return self.__agent
