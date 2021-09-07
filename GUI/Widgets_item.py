from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QLineSeries, QCandlestickSeries, \
    QCandlestickSet, QChartView, QDateTimeAxis
from datetime import datetime

import namespace

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
        self.__header = self.CreateHeader()
        self.__askListWidget = LOBListWidget()
        self.__bidListWidget = LOBListWidget()
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
            self.AddRow()

        #
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.GRAY_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def AddRow(self):
        item = QListWidgetItem()
        custom_widget = LOBItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.__listWidget.addItem(item)
        self.__listWidget.setItemWidget(item, custom_widget)

    def Clear(self):
        # 루프 돌면서 하나하나 지워야 하는가?
        self.__listWidget.clear()


class LOBItem(QFrame):
    def __init__(self):
        super(LOBItem, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__price = QLabel('price')
        self.__bar = BaseBar()
        self.__amount = QLabel('amount')
        self.__layout.addWidget(self.__price)
        self.__layout.addWidget(self.__bar)
        self.__layout.addWidget(self.__amount)
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
        self.__header = self.CreateHeader()
        self.__transactionListWidget = QListWidget()
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__transactionListWidget)

        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow()

    def CreateHeader(self):
        header = QFrame()
        layout = QHBoxLayout()
        layout.addWidget(QLabel('stamp'))
        layout.addWidget(QLabel('price'))
        layout.addWidget(QLabel('position'))
        layout.addWidget(QLabel('amount'))
        header.setLayout(layout)
        return header

    def AddRow(self):
        item = QListWidgetItem()
        custom_widget = TransactionItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.__transactionListWidget.addItem(item)
        self.__transactionListWidget.setItemWidget(item, custom_widget)


class TransactionItem(QFrame):
    clicked = pyqtSignal()
    def __init__(self):
        super(TransactionItem, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(QLabel('right now'))
        self.__layout.addWidget(QLabel('1000'))
        self.__layout.addWidget(QLabel('buy'))
        self.__layout.addWidget(QLabel('10'))

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
    def __init__(self):
        super(OrderListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__header = self.CreateHeader()
        self.__orderListWidget = QListWidget()
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__orderListWidget)
        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow()

        #
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.GRAY_PANEL.value
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
        custom_widget = OrderItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.__orderListWidget.addItem(item)
        self.__orderListWidget.setItemWidget(item, custom_widget)


class OrderItem(QFrame):
    orderCanceled = pyqtSignal()
    def __init__(self):
        super(OrderItem, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(QLabel('pair'))
        self.__layout.addWidget(QLabel('position'))
        self.__layout.addWidget(QLabel('price'))
        self.__layout.addWidget(QLabel('amount'))
        self.__layout.addWidget(QPushButton('cancel'))
        self.setLayout(self.__layout)


    def CancelOrder(self):
        pass


class LedgerListContainer(QFrame):
    def __init__(self):
        super(LedgerListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__header = self.CreateHeader()
        self.__ledgerListWidget = QListWidget()
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__ledgerListWidget)
        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow()

        #
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.GRAY_PANEL.value
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

    def AddRow(self):
        item = QListWidgetItem()
        custom_widget = LedgerItem()
        item.setSizeHint(custom_widget.sizeHint())
        self.__ledgerListWidget.addItem(item)
        self.__ledgerListWidget.setItemWidget(item, custom_widget)


class LedgerItem(QFrame):
    def __init__(self):
        super(LedgerItem, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(QLabel('pair'))
        self.__layout.addWidget(QLabel('amount'))
        self.setLayout(self.__layout)


class HistoryListContainer(QFrame):
    def __init__(self):
        super(HistoryListContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__header = self.CreateHeader()
        self.__historyListWidget = QListWidget()
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__historyListWidget)
        self.setLayout(self.__layout)

        for i in range(5):
            self.AddRow()

        #
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.GRAY_PANEL.value
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
    '''
        수동 주문 창.
    '''
    def __init__(self):
        super(ManualOrderContainer, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__pairLabel = QLabel('pair')
        self.__priceLabel = QLabel('price')
        self.__amountLabel = QLabel('amount')
        self.__pairText = QLineEdit()
        self.__priceText = QLineEdit()
        self.__amountText = QLineEdit()
        self.__sellButton = QPushButton('sell')
        self.__buyButton = QPushButton('buy')

        self.__layout.addWidget(self.__pairLabel, 0, 0)
        self.__layout.addWidget(self.__priceLabel, 0, 1)
        self.__layout.addWidget(self.__amountLabel, 0, 2)
        self.__layout.addWidget(self.__pairText, 1, 0)
        self.__layout.addWidget(self.__priceText, 1, 1)
        self.__layout.addWidget(self.__amountText, 1, 2)
        self.__layout.addWidget(self.__sellButton, 0, 3)
        self.__layout.addWidget(self.__buyButton, 0, 4)

        self.setLayout(self.__layout)


class UserStatusContainer(QFrame):
    def __init__(self):
        super(UserStatusContainer, self).__init__()
        self.InitUI()
        self.InitializeData()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__nameLabel = QLabel('User: ')
        self.__assetLabel = QLabel('Initial asset: ')
        self.__evalLabel = QLabel('Evaluation: ')
        self.__countLabel = QLabel('Trade count: ')
        self.__nameText = QLabel()
        self.__assetText = QLabel()
        self.__evalText = QLabel()
        self.__countText = QLabel()

        self.__layout.addWidget(self.__nameLabel, 0, 0)
        self.__layout.addWidget(self.__nameText, 0, 1)
        self.__layout.addWidget(self.__assetLabel, 1, 0)
        self.__layout.addWidget(self.__assetText, 1, 1)
        self.__layout.addWidget(self.__evalLabel, 2, 0)
        self.__layout.addWidget(self.__evalText, 2, 1)
        self.__layout.addWidget(self.__countLabel, 3, 0)
        self.__layout.addWidget(self.__countText, 4, 1)

        self.setLayout(self.__layout)

    def InitializeData(self):
        self.__nameText.setText('minsu')
        self.__assetText.setText('10000')
        self.__evalText.setText('10000')
        self.__countText.setText('')


# assembly
class Window(QFrame):
    def __init__(self):
        super(Window, self).__init__()
        self.InitUI()

    def InitUI(self):
        self.__mainLayout = QHBoxLayout()

        self.__marketLayout = QVBoxLayout()
        self.__chart = CandleChartContainer()
        self.__lob = LOBContainer()
        self.__marketLayout.addWidget(self.__chart)
        self.__marketLayout.addWidget(self.__lob)

        self.__userLayout = QVBoxLayout()
        self.__manualOrder = ManualOrderContainer()

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
        r, g, b = [100 for i in range(3)]
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )
