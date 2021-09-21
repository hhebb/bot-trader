# import list for test
import sys
from PyQt5.QtChart import QCandlestickSeries, QChart, QChartView, QCandlestickSet
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QPointF, QDateTime
from PyQt5 import QtChart as qc
from datetime import datetime
from PyQt5.QtGui import QPainter
from PyQt5.QtGui import QFont, QFontDatabase

import Core.DBManager
import namespace
import pandas as pd
import numpy as np

np.arange(10)


'''
setStyleSheet(QString::fromUtf8("QScrollBar:vertical {"              
    "    border: 1px solid #999999;"
    "    background:white;"
    "    width:10px;    "
    "    margin: 0px 0px 0px 0px;"
    "}"
    "QScrollBar::handle:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130), stop:1 rgb(32, 47, 130));"
    "    min-height: 0px;"
    "}"
    "QScrollBar::add-line:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0 rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
    "    height: 0px;"
    "    subcontrol-position: bottom;"
    "    subcontrol-origin: margin;"
    "}"
    "QScrollBar::sub-line:vertical {"
    "    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,"
    "    stop: 0  rgb(32, 47, 130), stop: 0.5 rgb(32, 47, 130),  stop:1 rgb(32, 47, 130));"
    "    height: 0 px;"
    "    subcontrol-position: top;"
    "    subcontrol-origin: margin;"
    "}"
    ));'''

# app = QApplication(sys.argv)
# w = QWidget()
# w.setGeometry(500, 500, 100, 200)
# bar = QScrollBar(w)
# bar.setGeometry(0, 0, 20, 200)
# bar.setStyleSheet(
# '''QScrollBar:vertical {
#             border: 0px solid #999999;
#             background:white;
#             width:10px;
#             margin: 0px 0px 0px 0px;
#         }
#         QScrollBar::handle:vertical {
#
#             min-height: 0px;
#           	border: 0px solid red;
# 			border-radius: 5px;
# 			background-color: black;
#         }
#         QScrollBar::add-line:vertical {
#             height: 0px;
#             subcontrol-position: bottom;
#             subcontrol-origin: margin;
#         }
#         QScrollBar::sub-line:vertical {
#             height: 0 px;
#             subcontrol-position: top;
#             subcontrol-origin: margin;
#         }'''
# )
