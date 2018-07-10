from PyQt5.QtWidgets import QWidget, QHBoxLayout
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg


class AnalysisWidget(pg.PlotWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        print('here')
        # self.layout = QHBoxLayout()

        self.histogram_item = self.getPlotItem()
        self.histogram = pg.PlotCurveItem([0, 1], [0], stepMode=True, fillLevel=0, brush=(0, 0, 255, 80))
        self.histogram_item.addItem(self.histogram)
        # self.plot_histogram_item.addItem(self.histogram)
        # self.layout.addItem(self.histogram)
        # self.setLayout(self.layout)