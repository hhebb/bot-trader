import sys
from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QCandlestickSet
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import Qt, QPointF, QDateTime
from PyQt5 import QtChart as qc
from datetime import datetime
from PyQt5.QtGui import QPainter

from GUI.Widgets_item import *

app = QApplication(sys.argv)

window = QMainWindow()
w = Window()
window.setCentralWidget(w)
window.show()

sys.exit(app.exec_())