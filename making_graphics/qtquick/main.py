#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtQml import QQmlApplicationEngine
from PyQt5.QtGui import QScreen

if __name__ == "__main__":
    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()
    engine.load('basic.qml')
    view = engine.rootObjects()[0]
    # view.setSource(QUrl('basic.qml'))
    view.show()
    print(QScreen().physicalDotsPerInch())
    sys.exit(app.exec_())