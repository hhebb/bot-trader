from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout


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
        self.show()


class OrderBookWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__orderItems = list()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('lob', self)
        for i in range(5):
            self.__orderItems.append(OrderItem(10, 1.0))
        self.show()


class OrderItem(QWidget):
    def __init__(self, price, amount):
        super().__init__()
        self.__price = price
        self.__amount = amount
        self.InitUI()

    def InitUI(self):
        layout = QHBoxLayout()
        layout.addWidget(QLabel('price'))
        layout.addWidget(QLabel('amount'))
        self.setLayout(layout)
        self.show()


class TransactionWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('transaction', self)
        self.show()


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
        self.show()


class UserStatusPanel(QWidget):
    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        b = QPushButton('user', self)
        self.show()