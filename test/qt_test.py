from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
import sys
from Application.Runner import RunnerThread
from GUI.Widgets import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.InitUI()
        self.runner = RunnerThread()
        self.market = self.runner.GetMarket()
        self.runner.stepped.connect(self.Recv)
        self.startButton.clicked.connect(self.clickedHandler)
        self.orderPanel.orderbookWidget.drawFinished.connect(self.runner.SetReady)

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


    def Recv(self, ask, bid, trans):
        # print(ask, bid, trans)
        # print(ask.GetLOB())
        self.orderPanel.orderbookWidget.Update(ask.GetLOB())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    # runner = Runner()
    # runner.Simulate()
    sys.exit(app.exec_())
