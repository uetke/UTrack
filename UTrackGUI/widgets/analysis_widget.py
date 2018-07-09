from PyQt5.QtWidgets import QWidget, QHBoxLayout
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg


class AnalysisWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()

        self.plot_histogram = pg.PlotItem()
        self.layout.addItem(self.plot_histogram)
        self.setLayout(self.layout)