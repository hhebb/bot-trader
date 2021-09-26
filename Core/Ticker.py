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
        self.__tickSeries = CandleSeriesObject()
        self.__volumeSeries = VolumeSeriesObject()
        self.__ma5Series = MASeriesObject(size=5)
        self.__ma20Series = MASeriesObject(size=20)
        self.__ma60Series = MASeriesObject(size=60)

        # self.__tickSeries = list()
        # self.__volumeSeries = list()
        # self.__ma5Series = list()
        # self.__ma20Series = list()
        # self.__ma60Series = list()

        self.__buffer = list()
        self.__candleGap = 60
        self.__timeBucket = 0
        self.__seriesCount = 0

        self.__stamp = None
        self.__lastData = None

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
                # candle = self.__lastCandle if self.__lastCandle else CandleBar(self.__stamp, [0, 0, 0, 0])
                # volume = 0
                o, h, l, c, totalVolume = self.__lastData if self.__lastData else (0, 0, 0, 0, 0)
            else:
                # stamp = self.__buffer[0][0]
                o, h, l, c = self.__buffer[0][0], \
                             max(self.__buffer, key=lambda x: x[0])[0], \
                             min(self.__buffer, key=lambda x: x[0])[0], \
                             self.__buffer[-1][0]
                totalVolume = self.CalcTotalVolume()


                ######################################################
                # new series
                self.__tickSeries.Feed(timestamp=self.__stamp, ohlc=[o, h, l, c])
                self.__volumeSeries.Feed(timestamp=self.__stamp, volume=totalVolume)
                self.__ma5Series.Feed(timestamp=self.__stamp, closePrice=c)
                # self.__ma20Series.Feed(timestamp=self.__stamp, closePrice=c)
                # self.__ma60Series.Feed(timestamp=self.__stamp, closePrice=c)

                ######################################################

                # series item 생성
                # candle = CandleBar(self.__stamp, [o, h, l, c])
                # volume = VolumeBar(self.__stamp, totalVolume)
                # ma20 = MA20Bar(self.__stamp, average20)
                # ma60 = MA60Bar(self.__stamp, average60)

            # series 에 추가
            # self.__tickSeries.append(candle)
            # self.__volumeSeries.append(volume)

            self.__buffer.clear()
            self.__timeBucket = 0
            self.__lastData = (o, h, l, c, totalVolume)
            self.__stamp = None
            self.__seriesCount += 1

        self.__timeBucket += 1

    def GetTickSeries(self) -> dict:
        # return self.__tickSeries
        return self.__tickSeries.GetSeries()

    def GetVolumeSeries(self) -> dict:
        return self.__volumeSeries.GetSeries()

    def GetMA5Series(self) -> dict:
        return self.__ma5Series.GetSeries()

    def CalcTotalVolume(self):
        vol = 0
        for buf in self.__buffer:
            vol += buf[1]
        return vol

    def GetSeriesCount(self):
        return self.__seriesCount


#################################################
# 공통 클래스를 만들어야 할 듯.

class BaseSeriesObject:
    '''
        series: {timestamp: data}
    '''

    def __init__(self):
        self._series = dict()

    def Feed(self):
        pass

    def GetStamp(self):
        return self.__timestamp

    def GetSeries(self) -> dict:
        return self._series

    def GetDatapoint(self, timestamp):
        return self._series[timestamp]


class CandleSeriesObject(BaseSeriesObject):
    def __init__(self):
        super().__init__()

    def Feed(self, **kargs):
        timestamp = kargs['timestamp']
        ohlc = kargs['ohlc']
        candle = CandleBar(timestamp=timestamp, ohlc=ohlc)
        self._series[timestamp] = candle


class VolumeSeriesObject(BaseSeriesObject):
    def __init__(self):
        super().__init__()

    def Feed(self, **kargs):
        timestamp = kargs['timestamp']
        vol = kargs['volume']
        volume = VolumeBar(timestamp=timestamp, amount=vol)
        self._series[timestamp] = volume


class MASeriesObject(BaseSeriesObject):
    def __init__(self, size=5):
        super().__init__()
        self.__size = size
        self.__bucket = list()

    def Feed(self, **kargs):
        timestamp = kargs['timestamp']
        price = kargs['closePrice']
        self.__bucket.append(price)
        if len(self.__bucket) > self.__size:
            self.__bucket.pop(0)

        mean = np.mean(self.__bucket)
        mAverage = MA5Bar(timestamp=timestamp, c=mean)
        self._series[timestamp] = mAverage



###################################################



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