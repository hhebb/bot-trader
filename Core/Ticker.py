class Ticker:
    def __init__(self):
        self.__tick_chart = list()
        self.__volume_chart = list()
        self.__ma5 = list()
        self.__ma20 = list()
        self.__ma60 = list()

    def Update(self):
        candle = Candle(0, [0, 0, 0, 0])
        volume = TradingVolume(0, 10)
        self.__tick_chart.append(candle)
        self.__volume_chart.append(volume)

    def GetTickChart(self):
        return self.__tick_chart

    def GetVolumeChart(self):
        return self.__volume_chart

    def GetMA5(self):
        return self.__ma5


class Candle:
    def __init__(self, timestamp, ohlc):
        self.timestamp = timestamp
        self.timestamp, self.open, self.high, self.low, self.close = ohlc


class TradingVolume:
    def __init__(self, timestamp, amount):
        self.timestamp = timestamp
        self.amount = amount