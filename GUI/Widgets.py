from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout, QFrame
from PyQt5.QtCore import QRect, pyqtSignal

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
        self.orderbookWidget = OrderBookWidget()
        layout.addWidget(self.orderbookWidget)
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
        self.askLayout = QVBoxLayout(askFrame)
        self.bidLayout = QVBoxLayout(bidFrame)

        for i in range(5):
            self.askLayout.addWidget(OrderItem(10, 1.0))
            self.bidLayout.addWidget(OrderItem(10, 1.0))

        layout.addWidget(askFrame)
        layout.addWidget(bidFrame)
        self.setLayout(layout)

    def Update(self, data: dict):
        for price, order in data.items():
            # 기존에 없는 호가이면 추가.
            targetItem = self.askLayout.findChild(OrderItem, str(price))
            if not targetItem:
                idx = self.FindInsertIndex(targetItem)
                self.askLayout.insertWidget(idx, OrderItem(order.price, order.amount))
            else:
                idx = self.askLayout.indexOf(targetItem)
                if order.amount == 0:
                    targetItem.deleteLater()
                else:
                    targetItem.widget = OrderItem(order.price, order.amount)

    def FindInsertIndex(self, p):
        idx = 0
        for i, w in enumerate(self.askLayout.children()):
            if float(w.objectName()) > p:
                idx = i
                break

        return idx


class OrderItem(QFrame):
    def __init__(self, price, amount):
        super().__init__()
        self.__price = price
        self.__amount = amount
        self.setFixedSize(100, 30)
        self.setObjectName(str(price))
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


class TransactionWidget(QFrame):
    def __init__(self):
        super().__init__()
        self.setObjectName('root')
        self.setStyleSheet(''' #root {background-color: rgb(45, 45, 45);}''')
        self.InitUI()

    def InitUI(self):
        b = QPushButton('transaction', self)
        layout = QVBoxLayout()
        frame = QFrame()
        frame.setStyleSheet(''' QFrame {background-color: rgb(128, 128, 255);} ''')
        self.transactionLayout = QVBoxLayout(frame)
        for i in range(5):
            self.transactionLayout.addWidget(TransactionItem('1:0:0', 100, 5))
        layout.addWidget(frame)
        self.setLayout(layout)

    def Update(self, data: list):
        for trans in data:
            targetItem = self.transactionLayout.findChild('trans.timestamp')
            if targetItem:
                continue
            else:
                ts = trans.timestamp
                type = trans.type
                price = trans.price
                amount = trans.amount
                newItem = TransactionItem(ts, price, amount)
                self.transactionLayout.addWidget(newItem)

class TransactionItem(QFrame):
    def __init__(self, time, price, amount):
        super().__init__()
        self.__time = time
        self.__price = price
        self.__amount = amount
        self.setObjectName('trans')
        self.setStyleSheet(''' #trans {background-color: red;} ''')
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
