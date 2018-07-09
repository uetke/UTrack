import os

from PyQt5 import uic
from PyQt5.QtWidgets import QWidget


class OptionsWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, '../Resources/options_widget.ui'), self)