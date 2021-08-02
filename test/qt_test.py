from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QGridLayout
import sys
from Application.Runner import Runner
from GUI.Widgets import *

class MyApp(QWidget):

    def __init__(self):
        super().__init__()
        self.InitUI()

    def InitUI(self):
        mainHbox = QHBoxLayout()
        marketLayout = QVBoxLayout()
        controlPanelLayout = QVBoxLayout()

        mainHbox.addLayout(marketLayout)
        mainHbox.addLayout(controlPanelLayout)

        marketLayout.addWidget(TickerPanel())
        marketLayout.addWidget(OrderPanel())

        controlPanelLayout.addWidget(ControlPanel())
        controlPanelLayout.addWidget(UserStatusPanel())

        self.setLayout(mainHbox)

        self.setWindowTitle('Box Layout')
        self.setGeometry(300, 300, 300, 200)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    # runner = Runner()
    # runner.Simulate()
    sys.exit(app.exec_())