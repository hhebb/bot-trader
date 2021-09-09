from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QLineSeries, QCandlestickSeries, \
    QCandlestickSet, QChartView, QDateTimeAxis
from datetime import datetime
import namespace
from Application.Runner import RunnerThread
from Core import Agent

'''
    [GUI 분류 체계]
    > 범위별 분류, 기능별 분류 2 가지 방법.
    1. 단일 widget 은 기본 widget 으로 사용한다.
        * 스타일, 서식 등은 QWidget 단에서 모두 지원 가능하기 때문.
    2. 2 개 이상 widget 이 조합되면 새로운 class 를 만든다.
        * 웬만하면 frame 단위로 만들어서 frame 꾸미기 쉽도록 만들 수 있음.
        * 대부분 기본 widget 이 frame 직계자손.
        * 새로 정의되는 기능(메서드)과 새로 추가된 데이터 입출력(signal, slot) 을 커스텀하기 쉽도록 만듬.
        * 각 내부 아이템(widget, frame) 들은 layout 혹은 splitter 에 의해 배치 조정 되도록 함.
    3. [2] 에서 이미 정의한 클래스 안에 widget 을 더 추가하고 싶을 땐 상속을 한다.
        * base class 를 만들어서 상속을 한다.
    4. [2] 에서 이미 정의한 클래스와 비슷한데 기능의 차이가 있다면 한 단계 추상화 한다.
        * base class 를 만들어서 각각 상속을 한다.
        * 웬만하면 base class 는 인스턴스를 만들지 않고 abc 를 사용.
    5. 하나의 아이템으로 독립성을 띌 수 있으면 이름에 container 를 붙인다.
        * 여러 아이템들을 감싸고 기능들을 포함하는 하나의 모듈로서 인식.
        * panel 이나 도구모음 등에 사용하기에 적합하다.
        * 어디까지 widget 이고 어디까지 container 라고 할 지 모호함이 있다.
        * 기능은 제외하고 배치에 관한 영역이라고만 생각하면 될 듯.
    
    
    [설계]
    * 시각적으로 bottom-up 설계.
    * 작은 아이템부터 쌓아 올리는 방법.
    * 먼저 가장 작은 item 을 정의하고 점점 살을 붙여가며 정의함.
    * GUI 도 변동성이 적은 core widget, 변동성이 빈번한 배치(container)나 상속받은 widget 계층이 있음.
    * 크게 3 종류의 클래스
        1. base
        2. base 들의 조합, 그 조합들의 조합. 일반 widget
        3. container
    * 용도에 맞게 클래스 분류하도록 하기.
        * 굳이 나누지 않아도 되는, 나눠서 쓸 일이 없는 것은 그냥 거대하게 만들어도 됨.
        * 재활용하지도 않을거 나누어봤자 복잡도만 증가함.
        * 혹시 필요하게 된다면 그때가서 나눠도 문제없음. 그 때는 손쉽게 나누기 가능.
        * 나누지 않아서 불편하면 그냥 나눠도 됨.
    * 전체적으로 유연한 개발에 초점을 맞춰야 함.
        * 위 법칙들은 가이드로써만 이용하고 유동적으로 개발해야 함.  
        
'''

class LOBContainer(QFrame):
    '''
        호가창 통쨰로 가지고 있는 container.
        크게 ask, bid 2 개의 ListView 를 포함함.
    '''

    def __init__(self):
        super(LOBContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('OrderBook')
        self.__header = self.CreateHeader()
        self.__askListWidget = LOBListWidget()
        self.__bidListWidget = LOBListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__askListWidget)
        self.__layout.addWidget(self.__bidListWidget)
        self.setLayout(self.__layout)


    def SetProperty(self):
        pass

    def CreateHeader(self):
        header = QFrame()
        headerLayout = QHBoxLayout()
        headerLayout.addWidget(QLabel('price'))
        headerLayout.addSpacerItem(QSpacerItem(50, 20)) # w h
        headerLayout.addWidget(QLabel('amount'))
        header.setLayout(headerLayout)
        return header

    def Update(self, askData: dict, bidData: dict):
        # 최소한의 전처리를 하고 보내줄까??
        self.__askListWidget.Update(askData)
        self.__bidListWidget.Update(bidData)


class LOBListWidget(QFrame):
    '''
        listWidget 을 포함하는 base class 로 만들어야 할 듯.
    '''
    def __init__(self):
        super(LOBListWidget, self).__init__()
        self.InitUI()

    def InitUI(self):
        # self.setFixedSize(200, 500)
        self.__layout = QVBoxLayout()
        self.__listWidget = QListWidget()
        self.__layout.addWidget(self.__listWidget)
        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow(0, 0)

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def AddRow(self, price, amount):
        item = QListWidgetItem()
        custom_widget = LOBItem(price, amount)
        item.setSizeHint(custom_widget.sizeHint())
        self.__listWidget.addItem(item)
        self.__listWidget.setItemWidget(item, custom_widget)

    def Clear(self):
        # 루프 돌면서 하나하나 지워야 하는가?
        self.__listWidget.clear()

    def Update(self, data: dict):
        # clear
        self.Clear()

        # for i in reversed(range(self.askLayout.count())):
        #     rm = self.askLayout.itemAt(i).widget()
        #     self.askLayout.removeWidget(rm)
        #     rm.setParent(None)

        for price, order in data.items():
            if self.__listWidget.count() >= 5:
                break
            self.AddRow(order.price, order.amount)


class LOBItem(QFrame):
    def __init__(self, price, amount):
        super(LOBItem, self).__init__()
        self.__price = price
        self.__amount = amount
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__priceLabel = QLabel(str(self.__price))
        self.__bar = BaseBar()
        self.__amountLabel = QLabel(str(self.__amount))
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__bar)
        self.__layout.addWidget(self.__amountLabel)
        self.setLayout(self.__layout)


class BaseBar(QFrame):
    '''
        LOB item 에 amount 수량 시각화하는 bar.
    '''
    def __init__(self):
        super(BaseBar, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        self.Draw(a0, qp, 40)
        qp.end()

    def Draw(self, event, qp, w):
        qp.setPen(QtGui.QColor(168, 34, 3))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawRect(0, 0, w, 20) # x y w h


class TransactionContainer(QFrame):
    def __init__(self):
        super(TransactionContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('Transaction')
        self.__header = self.CreateHeader()
        self.__transactionListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__transactionListWidget)

        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow(0, 0, 0, 0)

    def CreateHeader(self):
        header = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('stamp'))
        layout.addWidget(QLabel('price'))
        layout.addWidget(QLabel('position'))
        layout.addWidget(QLabel('amount'))
        header.setLayout(layout)
        return header

    def AddRow(self, stamp, price, amount, order):
        item = QListWidgetItem()
        custom_widget = TransactionItem(stamp, price, amount, order)
        item.setSizeHint(custom_widget.sizeHint())
        self.__transactionListWidget.addItem(item)
        self.__transactionListWidget.setItemWidget(item, custom_widget)

    def Update(self, transaction: list):
        # remove
        self.__transactionListWidget.clear()
        # for i in reversed(range(self.transactionLayout.count())):
        #     rm = self.transactionLayout.itemAt(i).widget()
        #     self.transactionLayout.removeWidget(rm)
        #     rm.setParent(None)

        for trans in transaction:
            if self.__transactionListWidget.count() >= 10:
                break

            stamp = str(trans.timestamp)
            price = str(trans.price)
            amount = str(trans.amount)
            order = str(trans.order)
            self.AddRow(stamp, price, amount, order)

            # w = TransactionItem(stamp, price, amount, order)
            # self.transactionLayout.addWidget(w)


class TransactionItem(QFrame):
    clicked = pyqtSignal()
    def __init__(self, stamp, price, amount, order):
        super(TransactionItem, self).__init__()
        self.__stamp = stamp
        self.__price = price
        self.__amount = amount
        self.__order = order
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(QLabel(str(self.__stamp)))
        self.__layout.addWidget(QLabel(str(self.__price)))
        self.__layout.addWidget(QLabel(str(self.__amount)))
        self.__layout.addWidget(QLabel(str(self.__order)))

        # self.setStyleSheet('background: white')
        self.setLayout(self.__layout)

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        print('clicked')
        self.clicked.emit()
        
        
class CandleChartContainer(QFrame):
    '''
        hover 이벤트 등 추가.
        MA, MACD 등 보조지표 추가.
    '''
    def __init__(self):
        super(CandleChartContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__title = QLabel('CandleChart')
        # candle series
        self.__candleSeries = QCandlestickSeries()
        self.__candleSeries.setIncreasingColor(Qt.red)
        self.__candleSeries.setDecreasingColor(Qt.blue)

        # chart
        self.__chart = QChart()
        self.__chart.addSeries(self.__candleSeries)
        self.__chart.createDefaultAxes()
        self.__chart.legend().hide()

        # displaying chart
        self.__chartView = QChartView(self.__chart)
        self.__chartView.setRenderHint(QPainter.Antialiasing)

        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__chartView)
        self.setLayout(self.__layout)

    def Draw(self, tickChart: list, volumeChart: list):
        # 매 step 마다 함수 실행은 하지만 candle 갯수가 같다면 그냥 pass 한다.
        if self.__candleSeries.count() == len(tickChart):
            return

        # clear all previous candles.
        self.__candleSeries.clear()

        # re-draw all candles.
        for candle in tickChart:
            self.AppendCandle(candle)

        # axis
        # axis_x = QDateTimeAxis()
        # axis_x.setTickCount(10)
        # axis_x.setFormat("mm:ss")
        # self.__chart.addAxis(axis_x, Qt.AlignBottom)
        # self.__candleSeries.attachAxis(axis_x)

        self.__chart.removeSeries(self.__candleSeries)
        self.__chart.addSeries(self.__candleSeries)

        self.__chart.createDefaultAxes()
        self.__chart.legend().hide()

    def AppendCandle(self, candleData):
        o, h, l, c = candleData.GetOHLC()
        ts = candleData.GetStamp()
        # time manipulate. 반드시 Qt 초 시간 단위에 맞게 해야만 분단위 이하로 차트 그릴 수 있음.
        format = "%Y-%m-%d %H:%M:%S"
        t = datetime.fromtimestamp(ts)
        t = t.strftime(format)
        t = QDateTime.fromString(t, "yyyy-MM-dd hh:mm:ss")
        t = t.toMSecsSinceEpoch()
        candle = QCandlestickSet(o, h, l, c, t)

        self.__candleSeries.append(candle)


class OrderListContainer(QFrame):
    def __init__(self, ):
        super(OrderListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('Order')
        self.__header = self.CreateHeader()
        self.__orderListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__orderListWidget)
        self.setLayout(self.__layout)

        # for i in range(5):
        #     self.AddRow()

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def CreateHeader(self):
        header = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('pair'))
        layout.addWidget(QLabel('position'))
        layout.addWidget(QLabel('price'))
        layout.addWidget(QLabel('amount'))
        header.setLayout(layout)
        return header

    def AddRow(self, pair, position, price, amount):
        item = QListWidgetItem()
        custom_widget = OrderItem(pair, position, price, amount)
        item.setSizeHint(custom_widget.sizeHint())
        self.__orderListWidget.addItem(item)
        self.__orderListWidget.setItemWidget(item, custom_widget)


    def Update(self, data: dict):
        # print('order', len(data))
        self.__orderListWidget.clear()
        for orderId, order in data.items():
            print('rendering order', orderId)
            pair = order['pair']
            position = order['position']
            price = order['price']
            amount = order['amount']
            self.AddRow(pair, position, price, amount)


class OrderItem(QFrame):
    orderCanceled = pyqtSignal()
    def __init__(self, pair, position, price, amount):
        super(OrderItem, self).__init__()
        self.__pair = pair
        self.__position = position
        self.__price = price
        self.__amount = amount
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__pairLabel = QLabel(str(self.__pair))
        self.__positionLabel = QLabel(str(self.__position))
        self.__priceLabel = QLabel(str(self.__price))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__cancelButton = QPushButton('cancel')
        self.__layout.addWidget(self.__pairLabel)
        self.__layout.addWidget(self.__positionLabel)
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.__layout.addWidget(self.__cancelButton)
        self.setLayout(self.__layout)


    def CancelOrder(self):
        pass


class LedgerListContainer(QFrame):
    def __init__(self):
        super(LedgerListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('Ledger')
        self.__header = self.CreateHeader()
        self.__ledgerListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__ledgerListWidget)
        self.setLayout(self.__layout)

        # for i in range(5):
        #     self.AddRow()

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def CreateHeader(self):
        header = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('pair'))
        layout.addWidget(QLabel('amount'))
        header.setLayout(layout)
        return header

    def AddRow(self, pair, amount):
        item = QListWidgetItem()
        custom_widget = LedgerItem(pair, amount)
        item.setSizeHint(custom_widget.sizeHint())
        self.__ledgerListWidget.addItem(item)
        self.__ledgerListWidget.setItemWidget(item, custom_widget)

    def Update(self, data: dict):
        # print('ledger :', data)
        self.__ledgerListWidget.clear()
        for pair, amount in data.items():
            pair = pair
            amount = amount
            self.AddRow(pair, amount)


class LedgerItem(QFrame):
    def __init__(self, pair, amount):
        super(LedgerItem, self).__init__()
        self.__pair = pair
        self.__amount = amount
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__pairLabel = QLabel(str(self.__pair))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__layout.addWidget(self.__pairLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.setLayout(self.__layout)


class HistoryListContainer(QFrame):
    def __init__(self):
        super(HistoryListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('History')
        self.__header = self.CreateHeader()
        self.__historyListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__historyListWidget)
        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow()

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def CreateHeader(self):
        header = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('pair'))
        layout.addWidget(QLabel('position'))
        layout.addWidget(QLabel('price'))
        layout.addWidget(QLabel('amount'))
        header.setLayout(layout)
        return header

    def AddRow(self):
        item = QListWidgetItem()
        custom_widget = HistoryItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.__historyListWidget.addItem(item)
        self.__historyListWidget.setItemWidget(item, custom_widget)


class HistoryItem(QFrame):
    def __init__(self):
        super(HistoryItem, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(QLabel('pair'))
        self.__layout.addWidget(QLabel('position'))
        self.__layout.addWidget(QLabel('price'))
        self.__layout.addWidget(QLabel('amount'))
        self.setLayout(self.__layout)


class ManualOrderContainer(QFrame):
    sellRequest = pyqtSignal(str, float, float)
    buyRequest = pyqtSignal(str, float, float)
    cancelRequest = pyqtSignal(str, float, float)
    '''
        수동 주문 창.
    '''
    def __init__(self, manualOrderThread: Agent.ManualOrderThread):
        super(ManualOrderContainer, self).__init__()
        self.__manualOrderThread = manualOrderThread
        self.InitUI()
        self.SignalConnect()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__title = QLabel('Manual Order')
        self.__pairLabel = QLabel('pair')
        self.__priceLabel = QLabel('price')
        self.__amountLabel = QLabel('amount')
        self.__pairText = QLineEdit()
        self.__priceText = QLineEdit()
        self.__amountText = QLineEdit()
        self.__sellButton = QPushButton('sell')
        self.__buyButton = QPushButton('buy')

        self.__layout.addWidget(self.__title, 0, 0)
        self.__layout.addWidget(self.__pairLabel, 1, 0)
        self.__layout.addWidget(self.__priceLabel, 1, 1)
        self.__layout.addWidget(self.__amountLabel, 1, 2)
        self.__layout.addWidget(self.__pairText, 2, 0)
        self.__layout.addWidget(self.__priceText, 2, 1)
        self.__layout.addWidget(self.__amountText, 2, 2)
        self.__layout.addWidget(self.__sellButton, 1, 3)
        self.__layout.addWidget(self.__buyButton, 1, 4)

        self.setLayout(self.__layout)


    def SignalConnect(self):
        self.__sellButton.clicked.connect(self.SellRequestHandler)
        self.__buyButton.clicked.connect(self.BuyRequestHandler)
        # self.__cancelButton.clicked.connect(self.CancelRequestHandler)

        self.sellRequest.connect(self.__manualOrderThread.ManualSell)
        self.buyRequest.connect(self.__manualOrderThread.ManualBuy)
        self.cancelRequest.connect(self.__manualOrderThread.ManualCancel)

    def SellRequestHandler(self):
        self.sellRequest.emit(self.__pairText.text(), float(self.__priceText.text()),
                              float(self.__amountText.text()))

    def BuyRequestHandler(self):
        self.buyRequest.emit('xrp', 1000, 1)

        # self.buyRequest.emit(self.__pairText.text(), float(self.__priceText.text()),
        #                       float(self.__amountText.text()))

    # def CancelRequestHandler(self):
    #     self.cancelRequest.emit(self.__pairText.text(), float(self.__priceText.text()),
    #                           float(self.__amountText.text()))



class UserStatusContainer(QFrame):
    def __init__(self):
        super(UserStatusContainer, self).__init__()
        self.InitUI()
        self.InitializeData()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__title = QLabel('Status')
        self.__nameLabel = QLabel('User: ')
        self.__assetLabel = QLabel('Initial asset: ')
        self.__evalLabel = QLabel('Evaluation: ')
        self.__countLabel = QLabel('Trade count: ')
        self.__nameText = QLabel()
        self.__assetText = QLabel()
        self.__evalText = QLabel()
        self.__countText = QLabel()

        self.__layout.addWidget(self.__title, 0, 0)
        self.__layout.addWidget(self.__nameLabel, 1, 0)
        self.__layout.addWidget(self.__nameText, 1, 1)
        self.__layout.addWidget(self.__assetLabel, 2, 0)
        self.__layout.addWidget(self.__assetText, 2, 1)
        self.__layout.addWidget(self.__evalLabel, 3, 0)
        self.__layout.addWidget(self.__evalText, 3, 1)
        self.__layout.addWidget(self.__countLabel, 4, 0)
        self.__layout.addWidget(self.__countText, 5, 1)

        self.setLayout(self.__layout)

    def InitializeData(self):
        self.__nameText.setText('minsu')
        self.__assetText.setText('10000')
        self.__evalText.setText('10000')
        self.__countText.setText('')


# assembly. Top level.
class Window(QFrame):
    stepRequest = pyqtSignal(bool)

    def __init__(self):
        super(Window, self).__init__()

        # right method using QThread??
        self.__runnerThread = QThread()
        self.__runnerWorker = RunnerThread()
        self.__runnerWorker.moveToThread(self.__runnerThread)
        self.__runnerThread.started.connect(self.__runnerWorker.Simulate)
        self.__runnerWorker.stepped.connect(self.Recv)
        # self.__runnerWorker.agentStepSignal.connect(self.RecvAgentInfo)
        self.stepRequest.connect(self.__runnerWorker.SetReady)
        #


        # self.__runnerThread = RunnerThread()
        self.__manualOrderThread = Agent.ManualOrderThread(
            agent=self.__runnerWorker.GetAgent())
        # self.__runnerThread.stepped.connect(self.Recv)
        # self.__runnerThread.agentStepSignal.connect(self.RecvAgentInfo)
        # self.__manualOrderThread.manualOrderSignal.connect(self.RecvManualOrder)
        #
        # self.__runnerThread.manualOrderSignal.connect(self.RecvManualOrder)
        # self.startButton.clicked.connect(self.clickedHandler)
        # self.stepRequest.connect(self.__runnerThread.SetReady)
        self.InitUI()

    def InitUI(self):
        button = QPushButton('simulate', self)
        button.clicked.connect(self.start)

        self.__mainLayout = QHBoxLayout()

        self.__marketLayout = QVBoxLayout()
        self.__chart = CandleChartContainer()
        self.__lob = LOBContainer()
        self.__transaction = TransactionContainer()
        self.__marketLayout.addWidget(self.__chart)
        self.__marketLayout.addWidget(self.__lob)
        self.__marketLayout.addWidget(self.__transaction)

        self.__userLayout = QVBoxLayout()
        self.__manualOrder = ManualOrderContainer(self.__manualOrderThread)

        self.__userBalanceLayout = QHBoxLayout()
        self.__order = OrderListContainer()
        self.__ledger = LedgerListContainer()
        self.__history = HistoryListContainer()
        self.__userBalanceLayout.addWidget(self.__order)
        self.__userBalanceLayout.addWidget(self.__ledger)
        self.__userBalanceLayout.addWidget(self.__history)

        self.__userStatus = UserStatusContainer()
        self.__userLayout.addWidget(self.__manualOrder)
        self.__userLayout.addLayout(self.__userBalanceLayout)
        self.__userLayout.addWidget(self.__userStatus)

        self.__mainLayout.addLayout(self.__marketLayout)
        self.__mainLayout.addLayout(self.__userLayout)

        self.setLayout(self.__mainLayout)

        #
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_BACKGROUND.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           'color: white'
                           )

    # slot. step by synchronized signal.
    def Recv(self, ask, bid, trans, ticker):
        # lob recv
        # self.orderPanel.orderbookWidget.Draw(ask.GetLOB(), bid.GetLOB())
        self.__lob.Update(ask.GetLOB(), bid.GetLOB())

        # transaction recv
        # self.orderPanel.transactionWidget.Draw(trans.GetHistory())
        self.__transaction.Update(trans.GetHistory())

        # tick recv
        tickChart = ticker.GetTickChart()
        volumeChart = ticker.GetVolumeChart()
        # self.tickerPanel.Draw(tickChart, volumeChart)
        self.__chart.Draw(tickChart, volumeChart)

    def RecvManualOrder(self, orders: dict, ledger: dict):
        self.__order.Update(orders)
        print('orders update')
        # self.__ledger.Update(ledger)
        print('ledger update')

    def RecvAgentInfo(self, initAsset, totalAsset, ledger, orders, history):
        #self.userStatusPanel.Recv(initAsset, totalAsset, ledger, orders, history)
        pass

    # step by manual control
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_S:
            self.stepRequest.emit(True)

    def start(self):
        # simulate start button
        self.__runnerThread.start()