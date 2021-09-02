import datetime

from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFormLayout, QFrame
from PyQt5.QtCore import QRect, pyqtSignal, QDateTime
from PyQt5.QtChart import QChart, QLineSeries, QCandlestickSeries, \
    QCandlestickSet, QChartView, QDateTimeAxis
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter

'''
ticker, candle panel
'''
class TickerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('ticker', self)
        self.__layout = QVBoxLayout()

        # candle series
        self.__candleSeries = QCandlestickSeries()
        self.__candleSeries.setIncreasingColor(Qt.red)
        self.__candleSeries.setDecreasingColor(Qt.blue)

        # chart
        self.__chart = QChart()
        self.__chart.addSeries(self.__candleSeries)
        self.__chart.createDefaultAxes()
        self.__chart.legend().hide()

        # axis
        axis_x = QDateTimeAxis()
        axis_x.setTickCount(10)
        axis_x.setFormat("mm:ss")
        self.__chart.addAxis(axis_x, Qt.AlignBottom)
        self.__candleSeries.attachAxis(axis_x)

        # displaying chart
        self.__chartView = QChartView(self.__chart)
        self.__chartView.setRenderHint(QPainter.Antialiasing)

        self.__layout.addWidget(self.__chartView)

        self.setLayout(self.__layout)

    def Draw(self, tickChart: list, volumeChart: list):
        # 매 step 마다 함수 실행은 하지만 candle 갯수가 같다면 그냥 pass 한다.
        if self.__candleSeries.count() == len(tickChart):
            return

        # clear
        self.__candleSeries.clear()

        # re draw
        for candle in tickChart:
            self.AppendCandle(candle)

        # axis
        axis_x = QDateTimeAxis()
        axis_x.setTickCount(10)
        axis_x.setFormat("mm:ss")
        self.__chart.addAxis(axis_x, Qt.AlignBottom)
        self.__candleSeries.attachAxis(axis_x)

        self.__chart.removeSeries(self.__candleSeries)
        self.__chart.addSeries(self.__candleSeries)

        self.__chart.createDefaultAxes()
        self.__chart.legend().hide()



    def AppendCandle(self, candleData):
        o, h, l, c = candleData.GetOHLC()
        ts = candleData.GetStamp()
        # time manipulate. 반드시 Qt 초 시간 단위에 맞게 해야만 초단위로 차트 그릴 수 있음.
        format = "%Y-%m-%d %H:%M:%S"
        t = datetime.datetime.fromtimestamp(ts)
        t = t.strftime(format)
        t = QDateTime.fromString(t, "yyyy-MM-dd hh:mm:ss")
        t = t.toMSecsSinceEpoch()
        candle = QCandlestickSet(o, h, l, c, t)

        self.__candleSeries.append(candle)


# class CandleStikcWidget(QCandlestickSet):
#     def __init__(self, parent):
#         super().__init__(parent)
#         self.InitUI()
#
#     def InitUI(self):
#         b = QPushButton('candle', self)
#         self.show()
#
#
# class Candle(QWidget):
#     # candle: Ticker.Ticker.Candle()
#     def __init__(self, candle):
#         super().__init__()
#         self.__candle = candle
#         self.InitUI()
#
#     def InitUI(self):
#         timestamp = self.__candle.GetStamp()
#         ohlc = self.__candle.GetOHLC()
#
#     def MakeCandle(self):
#         pass

'''
market data panel
'''
class OrderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        self.orderbookWidget = OrderBookWidget()
        self.transactionWidget = TransactionWidget()
        layout.addWidget(self.orderbookWidget)
        layout.addWidget(self.transactionWidget)
        self.setLayout(layout)


class OrderBookWidget(QFrame):
    drawFinished = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.__orderItems = list()
        self.setObjectName('order')
        self.setStyleSheet(''' #order {
                                        background: rgb(45, 45, 45);
                                        border-style: solid;
                                        border-width: 5px;
                                        border-color: rgb(45, 245, 245);
                                        } ''')
        self.InitUI()

    def InitUI(self):
        b = QPushButton('orderbook', self)
        layout = QVBoxLayout()
        bidFrame = QFrame()
        askFrame = QFrame()
        # askFrame.setObjectName('ask')
        # bidFrame.setObjectName('bid')
        askFrame.setStyleSheet(""" background-color: rgb(128, 128, 255); """)
        bidFrame.setStyleSheet(""" background-color: rgb(128, 128, 255); """)
        self.askLayout = QVBoxLayout(askFrame)
        self.bidLayout = QVBoxLayout(bidFrame)

        layout.addWidget(askFrame)
        layout.addWidget(bidFrame)
        self.setLayout(layout)

    def Draw(self, askData: dict, bidData: dict):
        # clear
        for i in reversed(range(self.askLayout.count())):
            rm = self.askLayout.itemAt(i).widget()
            self.askLayout.removeWidget(rm)
            rm.setParent(None)

        # clear
        for i in reversed(range(self.bidLayout.count())):
            rm = self.bidLayout.itemAt(i).widget()
            self.bidLayout.removeWidget(rm)
            rm.setParent(None)

        for price, order in askData.items():
            if self.askLayout.count() >= 5:
                break
            item = OrderItem(order.price, order.amount)
            self.askLayout.addWidget(item)

        for price, order in bidData.items():
            if self.bidLayout.count() >= 5:
                break
            item = OrderItem(order.price, order.amount)
            self.bidLayout.addWidget(item)

    # deprecated!
    # def Update(self, askData: dict, bidData: dict):
    #     # print('> ui update', bidData)
    #     for price, order in askData.items():
    #         i, targetItem = self.FindItem(price)
    #         # print(targetItem)
    #         # 기존에 없는 호가이면 추가.
    #         if not targetItem:
    #             idx = self.FindInsertIndex(str(price))
    #             newItem = OrderItem(order.price, order.amount)
    #             # print('insert index', idx)
    #             self.askLayout.insertWidget(idx, newItem)
    #             if self.askLayout.count() > 10:
    #                 delete = self.askLayout.itemAt(self.askLayout.count()-1).widget()
    #                 self.askLayout.removeWidget(delete)
    #         else:
    #             idx = self.askLayout.indexOf(targetItem)
    #             # print('exist')
    #             if order.amount == 0.0:
    #                 # print('zero')
    #                 self.askLayout.removeWidget(targetItem)
    #             else:
    #                 # print('change', targetItem.amount, order.amount)
    #                 # targetItem.widget = OrderItem(order.price, -100)
    #                 self.ReplaceItem(i, order.price, order.amount)
    #
    #     for price, order in bidData.items():
    #         i, targetItem = self.FindItem(price)
    #         if not targetItem:
    #             idx = self.FindInsertIndex(str(price))
    #             newItem = OrderItem(order.price, order.amount)
    #             self.bidLayout.insertWidget(idx, newItem)
    #             if self.bidLayout.count() > 10:
    #                 delete = self.bidLayout.itemAt(self.bidLayout.count()-1).widget()
    #                 self.bidLayout.removeWidget(delete)
    #         else:
    #             idx = self.bidLayout.indexOf(targetItem)
    #             if order.amount == 0.0:
    #                 self.bidLayout.removeWidget(targetItem)
    #             else:
    #                 self.ReplaceItem(i, order.price, order.amount)

    def FindInsertIndex(self, p):
        idx = 0
        for i in range(self.askLayout.count()):
            idx = i
            w = self.askLayout.itemAt(i).widget()
            if float(w.objectName()) >= float(p):
                break
        return idx

    def FindItem(self, p):
        for i in range(self.askLayout.count()):
            w = self.askLayout.itemAt(i).widget()
            if float(w.objectName()) == float(p):
                return i, w
        return None, None

    def ReplaceItem(self, i, price, amount):
        self.askLayout.removeWidget(self.askLayout.itemAt(i).widget())
        self.askLayout.insertWidget(i, OrderItem(price, amount))


class OrderItem(QFrame):
    def __init__(self, price, amount):
        super().__init__()
        self.__price = price
        self.__amount = amount
        self.amount = amount
        self.setFixedSize(100, 30)
        self.setObjectName(str(price))
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(str(self.__price)))
        layout.addWidget(QLabel(str(self.__amount)))
        # self.setObjectName('test')
        # self.setStyleSheet(''' #test {
        #                     background-color: red;
        #                     border-style: solid;
        #                     border-width: 2px;
        #                     }
        #                     QWidget{
        #                     background-color: white;
        #                     }''')
        self.setLayout(layout)
        # self.setFixedSize(20, 100)
        # self.label = QLabel('test', self)


class TransactionWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('root')
        self.setStyleSheet(''' #root {background-color: rgb(45, 45, 45);}''')
        self.InitUI()

    def InitUI(self):
        b = QPushButton('transaction', self)
        self.transLayout = QVBoxLayout() # just container
        frame = QFrame()
        frame.setStyleSheet(''' QFrame {background-color: rgb(128, 128, 255);} ''')
        self.transactionLayout = QVBoxLayout(frame) # contain transaction
        self.transLayout.addWidget(frame)
        self.setLayout(self.transLayout)

    def Draw(self, data: list):
        # remove
        for i in reversed(range(self.transactionLayout.count())):
            rm = self.transactionLayout.itemAt(i).widget()
            self.transactionLayout.removeWidget(rm)
            rm.setParent(None)

        for trans in data:
            if self.transactionLayout.count() >= 10:
                break
            stamp = str(trans.timestamp)
            price = str(trans.price)
            amount = str(trans.amount)
            order = str(trans.order)
            w = TransactionItem(stamp, price, amount, order)
            self.transactionLayout.addWidget(w)

    # deprecated
    # def Update(self, data: list, reset: bool):
    #     if reset:
    #         self.ResetWidgets()
    #
    #     for trans in data:
    #         if self.FindItem(trans.order):
    #             continue
    #         # print(trans.order, trans.timestamp)
    #
    #         stamp = str(trans.timestamp)
    #         price = str(trans.price)
    #         amount = str(trans.amount)
    #         order = str(trans.order)
    #         w = TransactionItem(stamp, price, amount, order)
    #         # print(stamp, order)
    #         self.transactionLayout.insertWidget(self.transactionLayout.count(), w)
    #
    #         if self.transactionLayout.count() > 10:
    #             toRemove = self.transactionLayout.itemAt(0)
    #             # print('> remove: ', toRemove.widget().objectName())
    #             self.transactionLayout.removeWidget(toRemove.widget())
    #
    #         ##############
    #         # if not self.FindItem(trans.timestamp):
    #             # stamp = str(trans.timestamp)
    #             # price = str(trans.price)
    #             # amount = str(trans.amount)
    #             # w = TransactionItem(stamp, price, amount)
    #             # print(stamp)
    #             # self.transLayout.insertWidget(self.transactionLayout.count(), w)
    #             #
    #             # if self.transLayout.count() > 10:
    #             #     toRemove = self.transLayout.itemAt(0)
    #             #     self.transLayout.removeWidget(toRemove.widget())

    def FindItem(self, order):
        for i in range(self.transactionLayout.count()):
            if self.transactionLayout.itemAt(i).widget().objectName() == str(order):
                return True

        return False

    def ResetWidgets(self):
        for i in range(self.transactionLayout.count()):
            self.transactionLayout.removeWidget(self.transactionLayout.itemAt(0).widget())
            pass

class TransactionItem(QFrame):
    def __init__(self, time, price, amount, order):
        super().__init__()
        self.__time = time
        self.__price = price
        self.__amount = amount
        self.setObjectName(order)
        # self.setStyleSheet(''' #trans {background-color: red;} ''')
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(str(self.__time)))
        layout.addWidget(QLabel(str(self.__price)))
        layout.addWidget(QLabel(str(self.__amount)))
        self.setLayout(layout)

'''
user data, control panel
'''
class ControlPanel(QWidget):
    '''
        simulation speed, layout set..
        수동 진행, 자동 진행 switch.
    '''

    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('control', self)


class UserStatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        # b = QPushButton('user', self)
        self.outer = QVBoxLayout()
        frame = QFrame()
        self.outer.addWidget(frame)
        self.userLayout = QFormLayout(frame)

        # labels
        self.nameLabel = QLabel('name')
        self.initialAssetLabel = QLabel('initial asset')
        self.totalAssetLabel = QLabel('total asset')
        self.netProfitLabel = QLabel('net profit')

        # fields
        self.name = QLabel('minsu')
        self.initAsset = QLabel('')
        self.totalAsset = QLabel('')
        self.netProfit = QLabel('')

        self.userLayout.addRow(self.nameLabel, self.name)
        self.userLayout.addRow(self.initialAssetLabel, self.initAsset)
        self.userLayout.addRow(self.totalAssetLabel, self.totalAsset)
        self.userLayout.addRow(self.netProfitLabel, self.netProfit)

        self.dataListLayout = QHBoxLayout()
        self.orderLayout = QVBoxLayout()
        self.ledgerLayout = QVBoxLayout()
        self.historyLayout = QVBoxLayout()
        self.dataListLayout.addLayout(self.orderLayout)
        self.dataListLayout.addLayout(self.ledgerLayout)
        self.dataListLayout.addLayout(self.historyLayout)

        self.outer.addLayout(self.dataListLayout)

        self.setLayout(self.outer)

    def Recv(self, initAsset, totalAsset, ledger, orders, history):
        self.initAsset.setText((str(initAsset)))
        self.totalAsset.setText(str(totalAsset))
        self.netProfit.setText(str(float(totalAsset) - float(self.initAsset.text())))

        # agent order clear
        for i in reversed(range(self.orderLayout.count())):
            rm = self.orderLayout.itemAt(i).widget()
            self.orderLayout.removeWidget(rm)
            rm.setParent(None)

        for i in reversed(range(self.ledgerLayout.count())):
            rm = self.ledgerLayout.itemAt(i).widget()
            self.ledgerLayout.removeWidget(rm)
            rm.setParent(None)

        for i in reversed(range(self.historyLayout.count())):
            rm = self.historyLayout.itemAt(i).widget()
            self.historyLayout.removeWidget(rm)
            rm.setParent(None)

        for key, order in orders.items():
            self.orderLayout.addWidget(AgentOrderItem(order))

        for key, ledger in ledger.items():
            self.ledgerLayout.addWidget(LedgerItem(key, ledger))

        for info in history:
            self.historyLayout.addWidget(HistoryItem(info))

class AgentOrderItem(QWidget):
    def __init__(self, order: dict):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(order['pair']))
        self.layout.addWidget(QLabel(str(order['position'])))
        self.layout.addWidget(QLabel(str(order['price'])))
        self.layout.addWidget(QLabel(str(order['amount'])))

        self.setLayout(self.layout)

class LedgerItem(QWidget):
    def __init__(self, key, ledger):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(key))
        self.layout.addWidget(QLabel(str(ledger)))

        self.setLayout(self.layout)

class HistoryItem(QWidget):
    def __init__(self, info: list):
        super().__init__()
        self.layout = QHBoxLayout()
        self.layout.addWidget(QLabel(info['pair']))
        self.layout.addWidget(QLabel(str(info['position'])))
        self.layout.addWidget(QLabel(str(info['price'])))
        self.layout.addWidget(QLabel(str(info['amount'])))

        self.setLayout(self.layout)