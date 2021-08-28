from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
import sys
from Application.Runner import RunnerThread
from GUI.Widgets import *
from PyQt5 import QtGui
from PyQt5.QtCore import Qt

class MyApp(QWidget):
    drawed = pyqtSignal(bool)
    stepRequest = pyqtSignal(bool)
    def __init__(self):
        super().__init__()
        self.InitUI()
        self.runner = RunnerThread()
        self.market = self.runner.GetMarket()
        self.runner.stepped.connect(self.Recv)
        self.startButton.clicked.connect(self.clickedHandler)
        # self.orderPanel.orderbookWidget.drawFinished.connect(self.runner.SetReady)
        self.drawed.connect(self.runner.SetReady)
        self.stepRequest.connect(self.runner.SetReady)

    def clickedHandler(self):
        self.runner.start()
        # print('click!!')

    def InitUI(self):
        self.startButton = QPushButton('loop!', self)
        mainHbox = QHBoxLayout()
        marketLayout = QVBoxLayout()
        controlPanelLayout = QVBoxLayout()

        mainHbox.addLayout(marketLayout)
        mainHbox.addLayout(controlPanelLayout)

        marketLayout.addWidget(TickerPanel())
        self.orderPanel = OrderPanel()
        marketLayout.addWidget(self.orderPanel)

        controlPanelLayout.addWidget(ControlPanel())
        controlPanelLayout.addWidget(UserStatusPanel())

        self.setLayout(mainHbox)

        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


    # slot. step by synchronized signal.
    def Recv(self, ask, bid, trans):
        # print(ask, bid, trans)
        # print(ask.GetLOB())
        # self.orderPanel.orderbookWidget.Update(ask.GetLOB(), bid.GetLOB())
        self.orderPanel.orderbookWidget.Draw(ask.GetLOB(), bid.GetLOB())
        # self.orderPanel.transactionWidget.Update(trans.GetHistory(), trans.GetIsReset())
        self.orderPanel.transactionWidget.Draw(trans.GetHistory())
        # self.drawed.emit(True)

    # step by manual control
    def keyPressEvent(self, e: QtGui.QKeyEvent) -> None:
        if e.key() == Qt.Key_S:
            self.stepRequest.emit(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    # runner = Runner()
    # runner.Simulate()
    sys.exit(app.exec_())
