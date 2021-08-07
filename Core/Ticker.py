class Ticker:
    def __init__(self):
        self.__tick_chart = list()
        self.__volume_chart = list()
        self.__ma5 = list()
        self.__ma20 = list()
        self.__ma60 = list()
        self.__buffer = list()
        self.__candleGap = 60
        self.__timeBucket = 0

    def Update(self, transaction):
        for trans in transaction:
            self.__buffer.append(trans)

        if len(self.__timeBucket) == self.__candleGap:
            stamp = self.__buffer[0][0]
            o, h, l, c = self.__buffer[0][1], \
                         max(self.__buffer, key=lambda x: x[1]), \
                         min(self.__buffer, key=lambda x: x[1]), \
                         self.__buffer[-1][1]
            totalVolume = self.CalcTotalVolume()

            candle = Candle(stamp, [o, h, l, c])
            volume = TradingVolume(stamp, totalVolume)
            self.__tick_chart.append(candle)
            self.__volume_chart.append(volume)

            self.__buffer.clear()

        self.__timeBucket += 1


    def GetTickChart(self):
        return self.__tick_chart

    def GetVolumeChart(self):
        return self.__volume_chart

    def GetMA5(self):
        return self.__ma5

    def CalcTotalVolume(self):
        vol = 0
        for buf in self.__buffer:
            vol += buf[2]
        return vol


class Candle:
    def __init__(self, timestamp, ohlc):
        self.timestamp = timestamp
        self.timestamp, self.open, self.high, self.low, self.close = ohlc


class TradingVolume:
    def __init__(self, timestamp, amount):
        self.timestamp = timestamp
        self.amount = amount