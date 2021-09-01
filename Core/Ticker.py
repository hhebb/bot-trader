class Ticker:
    '''
        tickChart: [CandleBar(), ...]
        volumeChart: [VolumeBar(), ...]
        buffer: [[stamp, price, amount], ...]
    '''

    def __init__(self):
        self.__tickChart = list()
        self.__volumeChart = list()
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

            candle = CandleBar(stamp, [o, h, l, c])
            volume = VolumeBar(stamp, totalVolume)
            self.__tickChart.append(candle)
            self.__volumeChart.append(volume)

            self.__buffer.clear()

        self.__timeBucket += 1


    def GetTickChart(self):
        return self.__tickChart

    def GetVolumeChart(self):
        return self.__volumeChart

    def GetMA5(self):
        return self.__ma5

    def CalcTotalVolume(self):
        vol = 0
        for buf in self.__buffer:
            vol += buf[2]
        return vol


class CandleBar:
    def __init__(self, timestamp, ohlc):
        self.__timestamp = timestamp
        self.__open, self.__high, self.__low, self.__close = ohlc

    def GetStamp(self):
        return self.__timestamp

    def GetOHLC(self):
        return self.__open, self.__high, self.__low, self.__close


class VolumeBar:
    def __init__(self, timestamp, amount):
        self.__timestamp = timestamp
        self.__amount = amount

    def GetStamp(self):
        return self.__timestamp

    def GetAmount(self):
        return self.__amount