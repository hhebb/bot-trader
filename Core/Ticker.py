from datetime import datetime
import numpy as np

class Ticker:
    '''
        tickSeries: [CandleBar(), ...]
        volumeSeries: [VolumeBar(), ...]
        buffer: [[price, amount], ...]
        CandleBar: [open, high, low, close]
        VolumeBar: timestamp, amount

        series 마다 특화된 class 만들어서 관리해야함!
    '''

    def __init__(self):
        # series
        self.__tickSeries = list()
        self.__volumeSeries = list()
        self.__ma5Series = list()
        self.__ma20Series = list()
        self.__ma60Series = list()

        self.__buffer = list()
        self.__candleGap = 60
        self.__timeBucket = 0
        self.__priceQueue = list()

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
                self.__priceQueue.append(c)
                if len(self.__priceQueue) > 60:
                    self.__priceQueue.pop(0)

                average5 = np.mean(self.__priceQueue[-5:])
                average20 = np.mean(self.__priceQueue[-20:])
                average60 = np.mean(self.__priceQueue[-60:])

                # series item 생성
                candle = CandleBar(self.__stamp, [o, h, l, c])
                volume = VolumeBar(self.__stamp, totalVolume)
                ma5 = MA5Bar(self.__stamp, average5)
                # ma20 = MA20Bar(self.__stamp, average20)
                # ma60 = MA60Bar(self.__stamp, average60)

            # series 에 추가
            self.__tickSeries.append(candle)
            self.__volumeSeries.append(volume)
            self.__ma5Series.append(ma5)

            self.__buffer.clear()
            self.__timeBucket = 0
            self.__lastCandle = candle
            self.__stamp = None
        self.__timeBucket += 1

    def GetTickSeries(self) -> list:
        return self.__tickSeries

    def GetVolumeSeries(self) -> list:
        return self.__volumeSeries

    def GetMA5Series(self) -> list:
        return self.__ma5Series

    def CalcTotalVolume(self):
        vol = 0
        for buf in self.__buffer:
            vol += buf[1]
        return vol


#################################################
# 공통 클래스를 만들어야 할 듯.

class CandleBar:
    def __init__(self, timestamp: datetime.timestamp, ohlc: list):
        self.__timestamp = timestamp
        self.__open, self.__high, self.__low, self.__close = ohlc

    def GetStamp(self):
        return self.__timestamp

    def GetOHLC(self):
        return self.__open, self.__high, self.__low, self.__close


class VolumeBar:
    def __init__(self, timestamp: datetime.timestamp, amount: float):
        self.__timestamp = timestamp
        self.__amount = amount

    def GetStamp(self):
        return self.__timestamp

    def GetAmount(self):
        return self.__amount


class MA5Bar:
    def __init__(self, timestamp: datetime.timestamp, c: float):
        self.__timestamp = timestamp
        self.__price = c

    def GetStamp(self):
        return self.__timestamp

    def GetPrice(self):
        return self.__price