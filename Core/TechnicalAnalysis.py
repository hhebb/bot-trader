from Core.Ticker import *

class TechnicalAnalyzer:
    '''
        기술적 분석 모듈.
        Analyzer 모듈이 사용함.

        -------------------------------

        tickData: [CandleBar(), ...]
        CandleBar: [open, high, low, close]

        volData: [VolumeBar(), ...]
        VolumeBar: amount

        --------------------------------

        * MA5, MA20
        * MACD
        * RSI
        * Stochastic
        * BB

    '''

    def __init__(self, tickData: list, volData: list):
        self.__tickData = tickData
        self.__volData = volData
        self.MakeDataframe()

    def MakeDataframe(self):
        for candle in self.__tickData:
            print(candle.GetOHLC())

        for vol in self.__volData:
            print(vol.GetAmount())

    def GetMA5(self):
        pass