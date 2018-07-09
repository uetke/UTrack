from PyQt5.QtWidgets import QWidget, QHBoxLayout
from pyqtgraph import GraphicsLayoutWidget
import pyqtgraph as pg

class VideoWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.layout = QHBoxLayout(self)

        # Settings for the image
        self.imv = pg.ImageView()

        # Add everything to the widget
        self.layout.addWidget(self.imv)
        self.setLayout(self.layout)