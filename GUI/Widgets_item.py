from PyQt5.QtWidgets import *
from PyQt5 import QtGui
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtChart import QChart, QLineSeries, QCandlestickSeries, \
    QCandlestickSet, QChartView, QDateTimeAxis
from datetime import datetime
import namespace
from Application.Runner import RunnerWorker
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

class ControlContainer(QFrame):
    '''
        control toolbax container.
        시뮬레이션 시작, 정지, 속도 조절 등.
    '''
    def __init__(self, runnerWorker, runnerThread):
        super(ControlContainer, self).__init__()
        self.__runnerWorker = runnerWorker
        self.__runnerThread = runnerThread
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__dbselectCombobox = QComboBox()
        self.__startButton = QPushButton('START')
        self.__playButton = QPushButton('PLAY')
        self.__stepButton = QPushButton('STEP')
        self.__speedUpButton = QPushButton('UP')
        self.__speedDownButton = QPushButton('DOWN')

        self.SetCombobox()
        self.__startButton.clicked.connect(self.StartSimulation)
        self.__playButton.clicked.connect(self.ToggleSimulate)
        self.__stepButton.clicked.connect(self.SimulateStep)
        self.__speedUpButton.clicked.connect(self.SpeedUp)
        self.__speedDownButton.clicked.connect(self.SpeedDown)

        self.__layout.addWidget(self.__dbselectCombobox)
        self.__layout.addWidget(self.__startButton)
        self.__layout.addWidget(self.__playButton)
        self.__layout.addWidget(self.__stepButton)
        self.__layout.addWidget(self.__speedUpButton)
        self.__layout.addWidget(self.__speedDownButton)

        self.setLayout(self.__layout)

    def SetStyle(self):
        self.setMinimumSize(100, 100)
        self.setStyleSheet(
            '''
                border-width: 1px;
                border-color: white;
                border-style: solid;
            '''
        )

    def SetCombobox(self):
        dbm = self.__runnerWorker.GetMarket().GetDBManager()
        colls = dbm.GetCollectionNames(dbName='data')
        self.__dbselectCombobox.currentIndexChanged.connect(self.ComboboxChangeHandler)
        for collection in colls:
            self.__dbselectCombobox.addItem(collection)

    def ComboboxChangeHandler(self):
        cur = self.__dbselectCombobox.currentIndex()

    def StartSimulation(self):
        # 시작되면 비활성화 하기.
        # 초기화 버튼 추가하기.
        if self.__runnerWorker.GetSimulateState() == namespace.SimulateState.STOP:
            self.__runnerThread.start()
            self.__runnerWorker.ToggleSimulateState()

    def ToggleSimulate(self):
        self.__runnerWorker.ToggleSimulateState()

    def SimulateStep(self):
        self.__runnerWorker.StopSimulate()
        self.__runnerWorker.SetReady()
        self.__runnerWorker.SimulateStep()

    def SpeedUp(self):
        self.__runnerWorker.SpeedUp()

    def SpeedDown(self):
        self.__runnerWorker.SpeedDown()


class MarketBriefContainer(QFrame):
    def __init__(self):
        super(MarketBriefContainer, self).__init__()
        self.InitUI()
        self.Setstyle()

    def InitUI(self):
        pass

    def Setstyle(self):
        self.setMinimumSize(100, 100)
        self.setStyleSheet(
            '''
                border-width: 1px;
                border-color: white;
                border-style: solid;
            '''
        )


class UserAnalysisContainer(QFrame):
    def __init__(self):
        super(UserAnalysisContainer, self).__init__()
        self.InitUI()
        self.Setstyle()

    def InitUI(self):
        pass

    def Setstyle(self):
        self.setMinimumSize(100, 100)
        self.setStyleSheet(
            '''
                border-width: 1px;
                border-color: white;
                border-style: solid;
            '''
        )


class LOBContainer(QFrame):
    '''
        호가창 통쨰로 가지고 있는 container.
        크게 ask, bid 2 개의 ListView 를 포함함.
    '''

    def __init__(self):
        super(LOBContainer, self).__init__()
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.CreateHeader()
        self.__layout = QVBoxLayout()
        self.__title = QLabel('ORDERBOOK')
        # self.__header = self.CreateHeader()
        self.__askListWidget = LOBListWidget(lobType=namespace.LOBType.ASK)
        self.__bidListWidget = LOBListWidget(lobType=namespace.LOBType.BID)
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__askListWidget)
        self.__layout.addWidget(self.__bidListWidget)
        self.setLayout(self.__layout)


    def SetStyle(self):
        self.setObjectName(self.__class__.__name__)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        self.__header.setObjectName('header')
        self.__header.setStyleSheet(
            f'''
                border-style: none none solid none;
                border-width: 1px;
                border-color: white;
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 0px;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )

    def CreateHeader(self):
        self.__header = QFrame()
        self.__priceLabel = QLabel('PRICE')
        self.__amountLabel = QLabel('AMOUNT')

        headerLayout = QHBoxLayout()
        headerLayout.addWidget(self.__priceLabel)
        headerLayout.addSpacerItem(QSpacerItem(50, 20)) # w h
        headerLayout.addWidget(self.__amountLabel)
        self.__header.setLayout(headerLayout)

    def Update(self, askData: dict, bidData: dict):
        # 최소한의 전처리를 하고 보내줄까??
        self.__askListWidget.Update(askData)
        self.__bidListWidget.Update(bidData)


class LOBListWidget(QFrame):
    '''
        listWidget 을 포함하는 base class 로 만들어야 할 듯.
    '''
    def __init__(self, lobType: namespace.LOBType):
        super(LOBListWidget, self).__init__()
        self.__type = lobType
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        # self.setFixedSize(200, 500)
        self.__layout = QVBoxLayout()
        self.__listWidget = QListWidget()
        self.__layout.addWidget(self.__listWidget)
        self.setLayout(self.__layout)

    def SetStyle(self):
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = 40, 40, 40#namespace.ColorCode.DARK_MIDDLE.value
        self.setStyleSheet(
            f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
            'border-radius: 5px;'
                           )

        bar = QScrollBar()
        bar.setStyleSheet(
            f'''QScrollBar:vertical {{
                        border: 0px solid #999999;
                        border-radius: 10px;
                        background-color: white;
                        width:10px;    
                        margin: 0px 0px 0px 0px;
                    }}
                    QScrollBar::handle:vertical {{         
    
                        min-height: 0px;
                          border: 0px solid red;
                        border-radius: 5px;
                        background-color: black;
                    }}
                    QScrollBar::add-line:vertical {{       
                        height: 0px;
                        subcontrol-position: bottom;
                        subcontrol-origin: margin;
                    }}
                    QScrollBar::sub-line:vertical {{
                        height: 0 px;
                        subcontrol-position: top;
                        subcontrol-origin: margin;
                    }}
            '''
        )
        self.__listWidget.setVerticalScrollBar(bar)


    def AddRow(self, price, amount, rowCount):
        # item 의 사이즈는 꼭 여기서 지정?
        item = QListWidgetItem()
        custom_widget = LOBItem(price, amount)
        item.setSizeHint(QSize(0, 30))#(custom_widget.sizeHint())
        self.__listWidget.insertItem(rowCount, item)
        self.__listWidget.setItemWidget(item, custom_widget)

    def Clear(self):
        # 루프 돌면서 하나하나 지워야 하는가?
        self.__listWidget.clear()

    def Update(self, data: dict):
        '''
            lob 는 오름차순으로 들어옴.
            ASK 는 데이터는 그대로, 추가는 역으로 해줘야함.
            BID 는 데이터는 역으로, 추가는 그대로 해줘야함.
        '''
        # clear
        self.Clear()

        if self.__type.value == namespace.LOBType.ASK.value:
            for price, order in data.items():
                if self.__listWidget.count() >= 5:
                    break
                self.AddRow(order.price, order.amount, 0)

        elif self.__type.value == namespace.LOBType.BID.value:
            for price, order in reversed(data.items()):
                if self.__listWidget.count() >= 5:
                    break
                self.AddRow(order.price, order.amount, self.__listWidget.count())

        # for price, order in items:
        #     if self.__listWidget.count() >= 5:
        #         break
        #     self.AddRow(order.price, order.amount)


class LOBItem(QFrame):
    def __init__(self, price, amount):
        super(LOBItem, self).__init__()
        self.__price = price
        self.__amount = amount
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__priceLabel = QLabel(str(self.__price))
        self.__bar = BaseBar(self.__amount)
        self.__amountLabel = QLabel(str(self.__amount))
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__bar)
        self.__layout.addWidget(self.__amountLabel)
        self.setLayout(self.__layout)

    def SetStyle(self):
        self.setObjectName('LOBItem')
        self.setStyleSheet(
            f'''
                border-style: none none solid none;
                border-color: rgb(50, 50, 50);
                border-width: 1px;
                border-radius: 0px;
                margin: 0px 0px;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__bar.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )


class BaseBar(QFrame):
    '''
        LOB item 에 amount 수량 시각화하는 bar.
    '''
    def __init__(self, amount):
        super(BaseBar, self).__init__()
        self.__amount = amount
        self.InitUI()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.setLayout(self.__layout)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        length = self.__amount / 1000
        self.Draw(a0, qp, length)
        qp.end()

    def Draw(self, event, qp, w):
        qp.setPen(QtGui.QColor(200, 100, 3))
        qp.setBrush(QBrush(Qt.red, Qt.SolidPattern))
        qp.drawRect(0, 0, w, 100) # x y w h


class TransactionContainer(QFrame):
    def __init__(self):
        super(TransactionContainer, self).__init__()
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.CreateHeader()
        self.__layout = QVBoxLayout()
        self.__title = QLabel('TRANSACTION')
        self.__transactionListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__transactionListWidget)

        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        self.__header.setStyleSheet(
            f'''
                        border-style: none none solid none;
                        border-width: 1px;
                        border-color: white;
                        background-color: rgb({str(r)}, {str(g)}, {str(b)});
                        border-radius: 0px;
                    '''
        )

        bar = QScrollBar()
        bar.setStyleSheet(
            f'''QScrollBar:vertical {{
                           border: 0px solid #999999;
                           border-radius: 10px;
                           background-color: white;
                           width:10px;    
                           margin: 0px 0px 0px 0px;
                       }}
                       QScrollBar::handle:vertical {{         

                           min-height: 0px;
                             border: 0px solid red;
                           border-radius: 5px;
                           background-color: black;
                       }}
                       QScrollBar::add-line:vertical {{       
                           height: 0px;
                           subcontrol-position: bottom;
                           subcontrol-origin: margin;
                       }}
                       QScrollBar::sub-line:vertical {{
                           height: 0 px;
                           subcontrol-position: top;
                           subcontrol-origin: margin;
                       }}
               '''
        )
        self.__stampLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__positionLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__transactionListWidget.setVerticalScrollBar(bar)

    def CreateHeader(self):
        self.__header = QFrame()
        self.__stampLabel = QLabel('STAMP')
        self.__priceLabel = QLabel('PRICE')
        self.__positionLabel = QLabel('POSITION')
        self.__amountLabel = QLabel('AMOUNT')
        layout = QHBoxLayout()
        layout.addWidget(self.__stampLabel)
        layout.addWidget(self.__priceLabel)
        layout.addWidget(self.__positionLabel)
        layout.addWidget(self.__amountLabel)
        self.__header.setLayout(layout)
        # return header

    def AddRow(self, stamp, price, amount, order):
        item = QListWidgetItem()
        custom_widget = TransactionItem(stamp, price, amount, order)
        item.setSizeHint(QSize(0, 30))  # (custom_widget.sizeHint())
        self.__transactionListWidget.addItem(item)
        self.__transactionListWidget.setItemWidget(item, custom_widget)

    def Update(self, transaction: list):
        # remove
        self.__transactionListWidget.clear()

        for trans in reversed(transaction):
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
        self.SetStyle()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__stampLabel = QLabel(str(self.__stamp))
        self.__priceLabel = QLabel(str(self.__price))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__orderLabel = QLabel(str(self.__order))

        self.__layout.addWidget(self.__stampLabel)
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.__layout.addWidget(self.__orderLabel)

        # self.setStyleSheet('background: white')
        self.setLayout(self.__layout)

    def SetStyle(self):
        self.setStyleSheet(
            f'''
                border-style: none none solid none;
                font-size: 10px;
                border-color: rgb(50, 50, 50);
                border-width: 1px;
                margin: 0px 0px;
                border-radius: 0px;
            '''
        )
        self.__stampLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__orderLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )

        # self.setStyleSheet(
        #     f'''
        #                 border-radius: 0px;
        #                 margin: 0px 0px;
        #             '''
        # )

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
        self.SetStyle()

    def InitUI(self):
        self.__layout = QVBoxLayout()
        self.__title = QLabel('CANDLE CHART')

        # candle series
        self.__candleSeries = QCandlestickSeries()
        self.__candleSeries.setIncreasingColor(Qt.red)
        self.__candleSeries.setDecreasingColor(Qt.blue)

        # chart
        self.__chart = QChart()
        self.__chart.setTitle('XRP')
        self.__chart.addSeries(self.__candleSeries)
        self.__chart.createDefaultAxes()
        self.__chart.legend().hide()

        # displaying chart
        self.__chartView = QChartView(self.__chart)
        self.__chartView.setRenderHint(QPainter.Antialiasing)

        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__chartView)
        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        # self.__chart.setBackgroundPen(QColor(255, 0, 0))
        self.__chart.setBackgroundBrush(QColor(30, 30, 30))

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
    def __init__(self, manualOrderWorker: Agent.ManualOrderWorker):
        super(OrderListContainer, self).__init__()
        self.__manualOrderWorker = manualOrderWorker
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.CreateHeader()
        self.__layout = QVBoxLayout()
        self.__title = QLabel('ORDER')
        self.__orderListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__orderListWidget)
        self.setLayout(self.__layout)

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        self.__header.setObjectName('header')
        self.__header.setStyleSheet(
            f'''
                        border-style: none none solid none;
                        border-width: 1px;
                        border-color: white;
                        background-color: rgb({str(r)}, {str(g)}, {str(b)});
                        border-radius: 0px;
                    '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__positionLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__orderListWidget.setStyleSheet(
            f'''
                border-radius: 0px;
            '''
        )

    def CreateHeader(self):
        self.__header = QFrame()
        self.__pairLabel = QLabel('PAIR')
        self.__positionLabel = QLabel('POSITION')
        self.__priceLabel = QLabel('PRICE')
        self.__amountLabel = QLabel('AMOUNT')
        layout = QHBoxLayout()
        layout.addWidget(self.__pairLabel)
        layout.addWidget(self.__positionLabel)
        layout.addWidget(self.__priceLabel)
        layout.addWidget(self.__amountLabel)
        self.__header.setLayout(layout)
        # return header

    def AddRow(self, parentContainer, orderId, pair, position, price, amount):
        '''
            signal connect.
        '''
        item = QListWidgetItem()
        custom_widget = OrderItem(parentContainer, orderId, pair, position, price, amount)
        item.setSizeHint(QSize(0, 40))
        self.__orderListWidget.addItem(item)
        self.__orderListWidget.setItemWidget(item, custom_widget)


    def Update(self, data: dict):
        # print('order', len(data))
        self.__orderListWidget.clear()
        for orderId, order in data.items():
            # print('rendering order', orderId)
            pair = order['pair']
            position = order['position']
            price = order['price']
            amount = order['amount']
            self.AddRow(self, orderId, pair, position, price, amount)

    def GetWorker(self):
        return self.__manualOrderWorker


class OrderItem(QFrame):
    '''
        CancelOrderRequestHandler: 취소 버튼을 누르면 worker 의 cancel 함수 직접 호출.
    '''
    def __init__(self, parentContainer, orderId, pair, position, price, amount):
        super(OrderItem, self).__init__()
        self.__parentContainer = parentContainer
        self.__orderId = orderId
        self.__pair = pair
        self.__position = position
        self.__price = price
        self.__amount = amount
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__pairLabel = QLabel(str(self.__pair))
        self.__positionLabel = QLabel(str(self.__position))
        self.__priceLabel = QLabel(str(self.__price))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__cancelButton = QPushButton('X')
        self.__cancelButton.clicked.connect(self.CancelOrderRequestHandler)
        self.__layout.addWidget(self.__pairLabel)
        self.__layout.addWidget(self.__positionLabel)
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.__layout.addWidget(self.__cancelButton)
        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_MIDDLE.value
        self.setStyleSheet(
            f'''
                border-style: none none solid none;
                font-size: 10px;
                border-color: rgb(50, 50, 50);
                border-width: 1px;
                margin: 1px 0px;
            '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__positionLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__cancelButton.setFixedSize(25, 25)
        self.__cancelButton.setStyleSheet(
            '''
                background-color: red;
                color: black;
                padding: 5px;
                border-radius: 5px;
            '''
        )

    def GetOrderID(self):
        return self.__orderId

    def CancelOrderRequestHandler(self):
        # print(self.__orderId)
        self.__parentContainer.GetWorker().ManualCancel(self.__orderId)


class LedgerListContainer(QFrame):
    def __init__(self):
        super(LedgerListContainer, self).__init__()
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.CreateHeader()
        self.__layout = QVBoxLayout()
        self.__title = QLabel('LEDGER')
        self.CreateHeader()
        self.__ledgerListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__ledgerListWidget)
        self.setLayout(self.__layout)

        #
        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                        background-color: rgb({str(r)}, {str(g)}, {str(b)});
                        border-radius: 10px;
                        margin: 5px;
                    '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        self.__header.setObjectName('header')
        self.__header.setStyleSheet(
            f'''
                        border-style: none none solid none;
                        border-width: 1px;
                        border-color: white;
                        background-color: rgb({str(r)}, {str(g)}, {str(b)});
                        border-radius: 0px;
                    '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__ledgerListWidget.setStyleSheet(
            f'''
                border-radius: 0px;
            '''
        )

    def CreateHeader(self):
        self.__header = QFrame()
        self.__pairLabel = QLabel('PAIR')
        self.__amountLabel = QLabel('AMOUNT')
        layout = QHBoxLayout()
        layout.addWidget(self.__pairLabel)
        layout.addWidget(self.__amountLabel)
        self.__header.setLayout(layout)
        # return header

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
        self.SetStyle()

    def InitUI(self):
        self.__layout = QHBoxLayout()
        self.__pairLabel = QLabel(str(self.__pair))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__layout.addWidget(self.__pairLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_MIDDLE.value
        self.setStyleSheet(
            f'''
                border-style: none none solid none;
                font-size: 10px;
                border-color: rgb(50, 50, 50);
                border-width: 1px;
                margin: 1px 0px;
            '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )


class HistoryListContainer(QFrame):
    def __init__(self):
        super(HistoryListContainer, self).__init__()
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.CreateHeader()
        self.__layout = QVBoxLayout()
        self.__title = QLabel('HISTORY')
        self.__historyListWidget = QListWidget()
        self.__layout.addWidget(self.__title)
        self.__layout.addWidget(self.__header)
        self.__layout.addWidget(self.__historyListWidget)
        self.setLayout(self.__layout)

        # self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        # self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-color: red;'
                           )

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        self.__header.setObjectName('header')
        self.__header.setStyleSheet(
            f'''
                border-style: none none solid none;
                border-width: 1px;
                border-color: white;
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 0px;
            '''
        )
        bar = QScrollBar()
        bar.setStyleSheet(
            f'''QScrollBar:vertical {{
                                   border: 0px solid #999999;
                                   border-radius: 10px;
                                   background-color: white;
                                   width:10px;    
                                   margin: 0px 0px 0px 0px;
                               }}
                               QScrollBar::handle:vertical {{         

                                   min-height: 0px;
                                     border: 0px solid red;
                                   border-radius: 5px;
                                   background-color: black;
                               }}
                               QScrollBar::add-line:vertical {{       
                                   height: 0px;
                                   subcontrol-position: bottom;
                                   subcontrol-origin: margin;
                               }}
                               QScrollBar::sub-line:vertical {{
                                   height: 0 px;
                                   subcontrol-position: top;
                                   subcontrol-origin: margin;
                               }}
                       '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__positionLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                font-size: 10px;
                border: none;
            '''
        )
        self.__historyListWidget.setVerticalScrollBar(bar)

    def CreateHeader(self):
        self.__header = QFrame()
        self.__pairLabel = QLabel('PAIR')
        self.__positionLabel = QLabel('POSITION')
        self.__priceLabel = QLabel('PRICE')
        self.__amountLabel = QLabel('AMOUNT')
        layout = QHBoxLayout()
        layout.addWidget(self.__pairLabel)
        layout.addWidget(self.__positionLabel)
        layout.addWidget(self.__priceLabel)
        layout.addWidget(self.__amountLabel)
        self.__header.setLayout(layout)
        # return header

    def AddRow(self, pair, position, price, amount):
        item = QListWidgetItem()
        custom_widget = HistoryItem(pair, position, price, amount)
        item.setSizeHint(custom_widget.sizeHint())
        self.__historyListWidget.addItem(item)
        self.__historyListWidget.setItemWidget(item, custom_widget)

    def Clear(self):
        # 루프 돌면서 하나하나 지워야 하는가?
        self.__historyListWidget.clear()

    def Update(self, data: list):
        self.Clear()
        self.__historyListWidget.clear()
        for order in reversed(data):
            if self.__historyListWidget.count() >= 5:
                break
            # print('rendering order', orderId)
            pair = order['pair']
            position = order['position']
            price = order['price']
            amount = order['amount']
            self.AddRow(pair, position, price, amount)


class HistoryItem(QFrame):
    def __init__(self, pair, position, price, amount):
        super(HistoryItem, self).__init__()
        self.__pair = pair
        self.__position = position
        self.__price = price
        self.__amount = amount
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.__pairLabel = QLabel(str(self.__pair))
        self.__positionLabel = QLabel(str(self.__position))
        self.__priceLabel = QLabel(str(self.__price))
        self.__amountLabel = QLabel(str(self.__amount))
        self.__layout = QHBoxLayout()
        self.__layout.addWidget(self.__pairLabel)
        self.__layout.addWidget(self.__positionLabel)
        self.__layout.addWidget(self.__priceLabel)
        self.__layout.addWidget(self.__amountLabel)
        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_MIDDLE.value
        self.setStyleSheet(
            f'''
                border-style: none none solid none;
                font-size: 10px;
                border-color: rgb(50, 50, 50);
                border-width: 1px;
                border-radius: 0px;
                margin: 0px 0px;
            '''
        )
        self.__pairLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__positionLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__priceLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )
        self.__amountLabel.setStyleSheet(
            '''
                border-style: none;
            '''
        )


class ManualOrderContainer(QFrame):
    '''
        * signal
            * sellRequest
            * buyRequest
    '''
    sellRequest = pyqtSignal(str, float, float)
    buyRequest = pyqtSignal(str, float, float)
    '''
        수동 주문 창.
    '''
    def __init__(self, manualOrderWorker: Agent.ManualOrderWorker):
        super(ManualOrderContainer, self).__init__()
        self.__manualOrderWorker = manualOrderWorker
        self.InitUI()
        self.SetStyle()
        self.SignalConnect()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__title = QLabel('MANUAL ORDER')
        self.__pairLabel = QLabel('PAIR')
        self.__priceLabel = QLabel('PRICE')
        self.__amountLabel = QLabel('AMOUNT')
        self.__pairText = QLineEdit()
        self.__priceText = QLineEdit()
        self.__amountText = QLineEdit()
        self.__sellButton = QPushButton('SELL')
        self.__buyButton = QPushButton('BUY')

        self.__layout.addWidget(self.__title, 0, 0, 1, -1)
        self.__layout.addWidget(self.__pairLabel, 1, 0)
        self.__layout.addWidget(self.__priceLabel, 1, 1)
        self.__layout.addWidget(self.__amountLabel, 1, 2)
        self.__layout.addWidget(self.__pairText, 2, 0)
        self.__layout.addWidget(self.__priceText, 2, 1)
        self.__layout.addWidget(self.__amountText, 2, 2)
        self.__layout.addWidget(self.__sellButton, 1, 3, 2, 1)
        self.__layout.addWidget(self.__buyButton, 1, 4, 2, 1)
        self.__layout.setRowStretch(0, 1)
        self.__layout.setRowStretch(1, 4)
        self.__layout.setRowStretch(2, 4)

        self.setLayout(self.__layout)

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )
        r, g, b = namespace.ColorCode.DARK_MIDDLE.value
        self.__pairText.setPlaceholderText('enter pair')
        self.__pairText.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 5px;
                padding: 5px;
            '''
        )
        self.__priceText.setPlaceholderText('enter price')
        self.__priceText.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 5px;
                padding: 5px;
            '''
        )
        self.__amountText.setPlaceholderText('enter amount')
        self.__amountText.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 5px;
                padding: 5px;
            '''
        )
        self.__sellButton.setMinimumSize(QSize(80, 100))
        self.__sellButton.setStyleSheet(
            '''
                background-color: red;
                border-radius: 10px;
                padding: 5px;
                color: black;
            '''
        )
        self.__buyButton.setMinimumSize(QSize(80, 100))
        self.__buyButton.setStyleSheet(
            '''
                background-color: green;
                border-radius: 10px;
                padding: 5px;
                color: black;
            '''
        )

    def SignalConnect(self):
        self.__sellButton.clicked.connect(self.SellRequestHandler)
        self.__buyButton.clicked.connect(self.BuyRequestHandler)

        self.sellRequest.connect(self.__manualOrderWorker.ManualSell)
        self.buyRequest.connect(self.__manualOrderWorker.ManualBuy)

    def SellRequestHandler(self):
        self.__manualOrderWorker.ManualSell('xrp', 1000, 1)
        # self.sellRequest.emit(self.__pairText.text(), float(self.__priceText.text()),
        #                       float(self.__amountText.text()))

    def BuyRequestHandler(self):
        # self.buyRequest.emit('xrp', 1000, 1)
        self.__manualOrderWorker.ManualBuy('xrp', 1000, 1)
        # self.buyRequest.emit(self.__pairText.text(), float(self.__priceText.text()),
        #                       float(self.__amountText.text()))



class UserStatusContainer(QFrame):
    def __init__(self):
        super(UserStatusContainer, self).__init__()
        self.InitUI()
        self.SetStyle()
        self.InitializeData()

    def InitUI(self):
        self.__layout = QGridLayout()
        self.__title = QLabel('STATUS')
        self.__nameLabel = QLabel('USER: ')
        self.__assetLabel = QLabel('INITIAL ASSET: ')
        self.__evalLabel = QLabel('EVALUATION: ')
        self.__countLabel = QLabel('TRADE COUNT: ')
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

    def SetStyle(self):
        r, g, b = namespace.ColorCode.DARK_PANEL.value
        self.setStyleSheet(
            f'''
                background-color: rgb({str(r)}, {str(g)}, {str(b)});
                border-radius: 10px;
                margin: 5px;
            '''
        )
        self.__title.setStyleSheet(
            '''
                border-style: none none solid none;
                border-color: white;
                border-width: 0px;
                font-size: 20px;
                border-radius: 0px;
                margin: 20px 0px 20px 10px;
            '''
        )

    def InitializeData(self):
        self.__nameText.setText('minsu')
        self.__assetText.setText('10000')
        self.__evalText.setText('10000')
        self.__countText.setText('')

    def Update(self, initAsset, totalAsset, ledger, orders, history):
        self.__evalText.setText(str(totalAsset))


# assembly. Top level.
class Window(QFrame):
    '''
        * object
            * runnerWorker: simulator thread worker
            * manualOrderWorker: 수동 주문 처리 thread worker
        * slot
            * RecvMarketData: simulator step 을 통해 market data 수신.
            * RecvAgentData: 수동 주문, 자동 주문, 주문 체결 을 통해 agent data 수신.
            * RecvAgentInfo: agent 의 자산 상태 등 data 를 수신.

        * manual order 를 worker 로 보낼 땐 함수 직접 호출, worker 에서 데이터 받을 땐 signal.
        * automatic order signal 은 worker 에서 step signal 과 통합함.
    '''
    # stepRequest = pyqtSignal()

    def __init__(self):
        super(Window, self).__init__()
        # right method using QThread??
        self.__runnerThread = QThread()
        self.__manualOrderThread = QThread()

        self.__runnerWorker = RunnerWorker()
        self.__manualOrderWorker = Agent.ManualOrderWorker(
            agent=self.__runnerWorker.GetAgent())

        self.__runnerWorker.moveToThread(self.__runnerThread)
        self.__manualOrderWorker.moveToThread(self.__manualOrderThread)

        self.__runnerThread.started.connect(self.__runnerWorker.Simulate)
        self.__runnerWorker.stepped.connect(self.RecvMarketData)
        self.__runnerWorker.agentStepSignal.connect(self.RecvAgentInfo) # ??
        self.__runnerWorker.transactionSignal.connect(self.RecvAgentTransactData)
        # 시스템에 의해 만들어지는 자동 주문 처리.ㄱ
        # self.__runnerWorker.automaticOrderSignal.connect(self.RecvAgentData)

        self.__manualOrderThread.started.connect(self.__manualOrderWorker.run)
        self.__manualOrderWorker.manualOrderSignal.connect(self.RecvAgentData)

        # self.stepRequest.connect(self.__runnerWorker.SetReady)
        #


        # self.__runnerThread = RunnerThread()
        # self.__manualOrderThread = Agent.ManualOrderThread(
        #     agent=self.__runnerWorker.GetAgent())
        # self.__runnerThread.stepped.connect(self.Recv)
        # self.__runnerThread.agentStepSignal.connect(self.RecvAgentInfo)
        # self.__manualOrderThread.manualOrderSignal.connect(self.RecvManualOrder)
        #
        # self.__runnerThread.manualOrderSignal.connect(self.RecvManualOrder)
        # self.startButton.clicked.connect(self.clickedHandler)
        # self.stepRequest.connect(self.__runnerThread.SetReady)
        self.InitUI()
        self.SetStyle()

    def InitUI(self):
        self.__mainLayout = QGridLayout()

        self.__sidebarLayout = QGridLayout()
        self.__controlContainer = ControlContainer(self.__runnerWorker,
                                                   self.__runnerThread)
        self.__marketBriefContainer = MarketBriefContainer()
        self.__userAnalysisContainer = UserAnalysisContainer()
        self.__sidebarLayout.addWidget(self.__controlContainer)
        self.__sidebarLayout.addWidget(self.__marketBriefContainer)
        self.__sidebarLayout.addWidget(self.__userAnalysisContainer)

        self.__marketLayout = QVBoxLayout()
        self.__chart = CandleChartContainer()
        self.__lob = LOBContainer()
        self.__transaction = TransactionContainer()

        self.__marketDataLayout = QHBoxLayout()
        self.__marketDataLayout.addWidget(self.__lob)
        self.__marketDataLayout.addWidget(self.__transaction)

        self.__marketLayout.addWidget(self.__chart)
        self.__marketLayout.addLayout(self.__marketDataLayout)

        self.__userLayout = QGridLayout()
        self.__manualOrder = ManualOrderContainer(self.__manualOrderWorker)

        self.__userBalanceLayout = QHBoxLayout()
        self.__order = OrderListContainer(self.__manualOrderWorker)
        self.__ledger = LedgerListContainer()
        self.__history = HistoryListContainer()
        self.__userBalanceLayout.addWidget(self.__order)
        self.__userBalanceLayout.addWidget(self.__ledger)
        self.__userBalanceLayout.addWidget(self.__history)

        self.__userStatus = UserStatusContainer()
        self.__userLayout.addWidget(self.__userStatus, 0, 0, 1, 1)
        self.__userLayout.addWidget(self.__manualOrder, 0, 1, 1, 1)
        self.__userLayout.addLayout(self.__userBalanceLayout, 1, 0, 1, 2)
        self.__userLayout.setRowStretch(0, 1)
        self.__userLayout.setRowStretch(1, 2)


        self.__mainLayout.addLayout(self.__sidebarLayout, 0, 2)
        self.__mainLayout.addLayout(self.__marketLayout, 0, 0)
        self.__mainLayout.addLayout(self.__userLayout, 0, 1)

        self.__mainLayout.setColumnStretch(0, 2)
        self.__mainLayout.setColumnStretch(1, 2)
        self.__mainLayout.setColumnStretch(2, 1)

        self.setLayout(self.__mainLayout)

    def SetStyle(self):
        self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
        self.setLineWidth(3)
        r, g, b = namespace.ColorCode.DARK_BACKGROUND.value
        self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
                           'border-style: hidden;'
                           # 'border-radius: 20px;'
                           # 'margin: 1px;'
                           # 'padding: 5px'
                           )

    # def SetGlobalStyle(self):
    #     '''
    #         global style setting.
    #     '''
    #
    #     self.setFrameStyle(QFrame.Panel | QFrame.Sunken)
    #     self.setLineWidth(3)
    #     r, g, b = namespace.ColorCode.DARK_BACKGROUND.value
    #     self.setStyleSheet(f'background-color: rgb({str(r)}, {str(g)}, {str(b)});'
    #                        'border-color: red;'
    #                        'color: white;'
    #                        # f"font: 8pt '{namespace.Fonts.SEBANG_BOLD.value}';"
    #                        # 'font-weight: bold;'
    #                        # 'letter-spacing: 1.0px;'
    #                        'border-style: hidden;'
    #                        # 'border-radius: 20px;'
    #                        # 'margin: 5px;'
    #                        # 'padding: 5px'
    #                        )

    # slot. step by synchronized signal.
    def RecvMarketData(self, ask, bid, trans, ticker):
        '''
            Market data Recv.
        '''
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

    def RecvAgentTransactData(self, orders: dict, ledger: dict, history: list):
        '''
            Agent data Recv.
        '''
        self.__order.Update(orders)
        self.__ledger.Update(ledger)
        self.__history.Update(history)

    def RecvAgentData(self, orders: dict, ledger: dict):
        '''
            Agent data Recv.
        '''
        self.__order.Update(orders)
        self.__ledger.Update(ledger)

    def RecvAgentInfo(self, initAsset, totalAsset, ledger, orders, history):
        '''
            Agent Status Recv.
        '''
        self.__userStatus.Update(initAsset, totalAsset, ledger, orders, history)
        pass

    # control
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_A:
            # start simulation, and run.
            self.__runnerThread.start()
            self.__runnerWorker.ToggleSimulateState()
        if e.key() == Qt.Key_S:
            # toggle run/stop
            self.__runnerWorker.ToggleSimulateState()
        elif e.key() == Qt.Key_D:
            # stepping
            self.__runnerWorker.StopSimulate()
            self.__runnerWorker.SetReady()
            self.__runnerWorker.SimulateStep()
        elif e.key() == Qt.Key_BracketRight:
            # speed up
            self.__runnerWorker.SpeedUp()
        elif e.key() == Qt.Key_BracketLeft:
            # speed down
            self.__runnerWorker.SpeedDown()

