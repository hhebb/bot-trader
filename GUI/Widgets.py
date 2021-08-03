from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QRect

'''
ticker, candle panel
'''
class TickerPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('ticker', self)
        candleChart = CandleStickWidget(self)
        self.show()


class CandleStickWidget(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.InitUI()

    def InitUI(self):
        b = QPushButton('candle', self)
        self.show()


class Candle(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        pass

'''
market data panel
'''
class OrderPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        layout.addWidget(OrderBookWidget())
        layout.addWidget(TransactionWidget())
        self.setLayout(layout)


class OrderBookWidget(QFrame):
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
        askLayout = QVBoxLayout(askFrame)
        bidLayout = QVBoxLayout(bidFrame)

        for i in range(5):
            askLayout.addWidget(OrderItem(10, 1.0))
            bidLayout.addWidget(OrderItem(10, 1.0))

        layout.addWidget(askFrame)
        layout.addWidget(bidFrame)
        self.setLayout(layout)


class OrderItem(QFrame):
    def __init__(self, price, amount):
        super().__init__()
        self.__price = price
        self.__amount = amount
        self.setFixedSize(100, 30)
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel(str(self.__price)))
        layout.addWidget(QLabel(str(self.__amount)))
        self.setObjectName('test')
        self.setStyleSheet(''' #test {
                            background-color: red;
                            border-style: solid;
                            border-width: 2px;
                            } 
                            QWidget{
                            background-color: white;
                            }''')
        self.setLayout(layout)
        # self.setFixedSize(20, 100)
        # self.label = QLabel('test', self)


class TransactionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('transaction', self)
        layout = QVBoxLayout()
        for i in range(5):
            layout.addWidget(TransactionItem('1:0:0', 100, 5))
        self.setLayout(layout)

class TransactionItem(QWidget):
    def __init__(self, time, price, amount):
        super().__init__()
        self.__time = time
        self.__price = price
        self.__amount = amount

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
        b = QPushButton('user', self)
