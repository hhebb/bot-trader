from datetime import datetime

class Ticker:
    '''
        tickChart: [CandleBar(), ...]
        volumeChart: [VolumeBar(), ...]
        buffer: [[price, amount], ...]
    '''

    def __init__(self):
        self.__tickChart = list()
        self.__volumeChart = list()
        self.__ma5 = list()
        self.__ma20 = list()
        self.__ma60 = list()
        self.__buffer = list()
        self.__candleGap = 10
        self.__timeBucket = 0

        self.__stamp = None
        self.__lastCandle = None

    def Update(self, timestamp: datetime, transactions: list):
        if not self.__stamp:
            self.__stamp = timestamp.timestamp()

        # transactions 는 Transaction.MarketOrder() 이므로 변환.
        for trans in transactions:
            tick = [float(trans.price), float(trans.amount)]
            self.__buffer.append(tick)

        if self.__timeBucket == self.__candleGap:
            # bucket time 동안 거래가 한 번도 이뤄지지 않았을 때 처리.
            if len(self.__buffer) == 0:
                candle = self.__lastCandle if self.__lastCandle else CandleBar(self.__stamp, [0, 0, 0, 0])
                volume = 0
            else:
                # stamp = self.__buffer[0][0]
                o, h, l, c = self.__buffer[0][0], \
                             max(self.__buffer, key=lambda x: x[0])[0], \
                             min(self.__buffer, key=lambda x: x[0])[0], \
                             self.__buffer[-1][0]
                totalVolume = self.CalcTotalVolume()

                candle = CandleBar(self.__stamp, [o, h, l, c])
                volume = VolumeBar(self.__stamp, totalVolume)
            self.__tickChart.append(candle)
            self.__volumeChart.append(volume)

            self.__buffer.clear()
            self.__timeBucket = 0
            self.__lastCandle = candle
            self.__stamp = None
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
            vol += buf[1]
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