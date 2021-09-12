import sys
from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QCandlestickSet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPointF, QDateTime
from PyQt5 import QtChart as qc
from datetime import datetime
from PyQt5.QtGui import QPainter

from GUI.Widgets_item import *


def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 200, 400)
    window.setStyleSheet(
        f"font: 8pt '{namespace.Fonts.SEBANG_BOLD.value}';"
        'font-weight: bold;'
        'letter-spacing: 1.0px;'
        'color: white;'
                         )
    # window.setWindowFlags(Qt.WindowType.Popup)

    # central widget
    w = Window()
    window.setCentralWidget(w)
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
