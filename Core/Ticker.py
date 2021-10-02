from datetime import datetime
import numpy as np

class Ticker:
    '''
        all Series are managed by dictionary like.
        tickSeries: [CandleBar(), ...]
        volumeSeries: [VolumeBar(), ...]
        buffer: [[price, amount], ...]
        CandleBar: [open, high, low, close]
        VolumeBar: timestamp, amount

        series 마다 특화된 class 만들어서 관리해야함!
    '''

    def __init__(self):
        # comprehensive series. 왠만하면 데이터는 해쉬로 관리하는 것이 좋음.
        self.__totalSeries = dict()
        self.__totalSeries['candle'] = CandleSeriesObject()
        self.__totalSeries['volume'] = VolumeSeriesObject()
        self.__totalSeries['ma5'] = MASeriesObject(size=5)
        self.__totalSeries['ma20'] = MASeriesObject(size=20)
        self.__totalSeries['ma60'] = MASeriesObject(size=60)

        # series ############################## to remove
        self.__tickSeries = CandleSeriesObject()
        self.__volumeSeries = VolumeSeriesObject()
        self.__ma5Series = MASeriesObject(size=5)
        self.__ma20Series = MASeriesObject(size=20)
        self.__ma60Series = MASeriesObject(size=60)
        self.__bollingerBandSeries = BollingerBandSeriesObject(size=20)

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
                self.__ma20Series.Feed(timestamp=self.__stamp, closePrice=c)
                self.__bollingerBandSeries.Feed(timestamp=self.__stamp, closePrice=c)
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

    def GetDatas(self) -> dict:
        return self.__totalSeries

    def GetTickSeries(self) -> dict:
        # return self.__tickSeries
        return self.__tickSeries.GetSeries()

    def GetVolumeSeries(self) -> dict:
        return self.__volumeSeries.GetSeries()

    def GetMA5Series(self) -> dict:
        return self.__ma5Series.GetSeries()

    def GetMA20Series(self) -> dict:
        return self.__ma20Series.GetSeries()

    def GetBollingerBandSeries(self) -> dict:
        return self.__bollingerBandSeries.GetSeries()

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

        * series
            * tick data series
        * maxSize
            * limit of max tick data
    '''

    def __init__(self):
        self._series = dict()
        self._maxSize = 60

    def Feed(self):
        '''
            append data.
        '''
        if len(self._series) > self._maxSize:
            self._series.pop(list(self._series.keys())[0])
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
        super().Feed()
        timestamp = kargs['timestamp']
        ohlc = kargs['ohlc']
        # candle = CandleBar(timestamp=timestamp, ohlc=ohlc)
        self._series[timestamp] = ohlc


class VolumeSeriesObject(BaseSeriesObject):
    def __init__(self):
        super().__init__()

    def Feed(self, **kargs):
        super().Feed()
        timestamp = kargs['timestamp']
        vol = kargs['volume']
        # volume = VolumeBar(timestamp=timestamp, amount=vol)
        self._series[timestamp] = vol


class MASeriesObject(BaseSeriesObject):
    def __init__(self, size=5):
        super().__init__()
        self.__size = size
        self.__bucket = list()

    def Feed(self, **kargs):
        super().Feed()
        timestamp = kargs['timestamp']
        price = kargs['closePrice']
        self.__bucket.append(price)
        if len(self.__bucket) > self.__size:
            self.__bucket.pop(0)

        mean = np.mean(self.__bucket)
        # mAverage = MA5Bar(timestamp=timestamp, c=mean)
        self._series[timestamp] = mean


class MACDSeriesObject(BaseSeriesObject):
    def __init__(self, short=12, long=26, size=9):
        super().__init__()
        self.__priceBucketSize = long
        self.__macdBucketSize = size
        self.__priceBucket = list()
        self.__macdBucket = list()

    def Feed(self, **kargs):
        super().Feed()
        timestamp = kargs['timestamp']
        price = kargs['closePrice']
        self.__priceBucket.append(price)
        if len(self.__priceBucket) > self.__bucketSize:
            self.__priceBucket.pop(0)

        maShort = np.mean(self.__priceBucket[-12:])
        maLong = np.mean(self.__priceBucket)
        macd = maShort - maLong

        self.__macdBucket.append(macd)
        if len(self.__macdBucket) > self.__macdBucketSize:
            self.__macdBucket.pop(0)

        # signal = np.mean(self.__macdBucket)
        # mAverage = MA5Bar(timestamp=timestamp, c=mean)
        # self._series[timestamp] = mAverage


class BollingerBandSeriesObject(BaseSeriesObject):
    def __init__(self, size=20):
        super().__init__()
        self.__size = size
        self.__bucket = list()

    def Feed(self, **kargs):
        super().Feed()
        timestamp = kargs['timestamp']
        price = kargs['closePrice']
        self.__bucket.append(price)
        if len(self.__bucket) > self.__size:
            self.__bucket.pop(0)

        mean = np.mean(self.__bucket)
        std = np.std(self.__bucket)
        upper = mean + 2 * std
        lower = mean - 2 * std

        self._series[timestamp] = (upper, lower)


class RSISeriesObject(BaseSeriesObject):
    def __init__(self, size=14):
        super().__init__()
        self.__size = size
        self.__bucket = list()

    def Feed(self, **kargs):
        super().Feed()
        timestamp = kargs['timestamp']
        price = kargs['closePrice']
        self.__bucket.append(price)


        if len(self.__bucket) > self.__size:


            self.__bucket.pop(0)

        mean = np.mean(self.__bucket)
        std = np.std(self.__bucket)
        upper = mean + 2 * std
        lower = mean - 2 * std

        self._series[timestamp] = (upper, lower)

