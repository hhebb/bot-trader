class Ticker:
    def __init__(self):
        self.tick_chart = list()
        self.volume_chart = list()
        self.ma5 = list()
        self.ma20 = list()
        self.ma60 = list()

    def Parse(self):
        candle = Candle(0, [0, 0, 0, 0])
        volume = TradingVolume(0, 10)
        self.tick_chart.append(candle)
        self.volume_chart.append(volume)

    def GetTickChart(self):
        return self.tick_chart

    def GetVolumeChart(self):
        return self.volume_chart


class Candle:
    def __init__(self, timestamp, ohlc):
        self.timestamp = timestamp
        self.timestamp, self.open, self.high, self.low, self.close = ohlc


class TradingVolume:
    def __init__(self, timestamp, amount):
        self.timestamp = timestamp
        self.amount = amount