import threading
import numpy as np
import pyqtgraph as pg
import h5py
import os
import trackpy as tp

from PyQt5 import uic, QtGui, QtCore
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QMainWindow, QFileDialog
from Resources import resources
from widgets import VideoWidget, OptionsWidget

class MyCircleOverlay(pg.EllipseROI):
    def __init__(self, pos, size, **args):
        pg.ROI.__init__(self, pos, size, **args)
        self.aspectLocked = True

pen = QtGui.QPen(QtCore.Qt.red, 0.1)


class TrackMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'Resources/main_window.ui'), self)

        self.layout = self.centralwidget.layout()

        self.video_widget = VideoWidget(self)
        # self.analysis_widget = pg.PlotWidget(self)
        self.options_widget = OptionsWidget(self)
        self.layout.addWidget(self.video_widget, 0, 0, 2, 2)
        # self.layout.addWidget(self.analysis_widget, 0, 2, 2, -1)
        self.layout.addWidget(self.options_widget, 2, 0, -1, 0)

        self.action_open.triggered.connect(self.open_file)
        self.action_locate_particles.triggered.connect(self.locate_particles)
        # self.video_widget.imv.sigTimeChanged.connect(self.locate_particles)
        self.data = None
        self.circles = []

    def open_file(self):
        filename = QFileDialog.getOpenFileName(self, 'Select File', '')
        print(filename)
        with h5py.File(filename[0]) as file:
            data = np.swapaxes(file['Basler data'][:, :, :], 1, 2)
        self.data = data
        self.video_widget.imv.setImage(data)
        # t = threading.Thread(target=load_data, args=(self.video_widget, filename))
        # t.start()

    def locate_particles(self):
        self.centroids = tp.locate(self.data[self.video_widget.imv.currentIndex, :,:], 9, minmass=250)

        x, y = self.centroids['x'].tolist(), self.centroids['y'].tolist()
        imv_view = self.video_widget.imv.getView()

        for c in self.circles:
            imv_view.removeItem(c)

        for i in range(len(x)):
            self.circles.append(MyCircleOverlay(pos=(y[i]-5, x[i]-5), size=10, pen=pen, movable=False))
            imv_view.addItem(self.circles[-1])


def load_data(video_widget, filename):
    with h5py.File(filename) as file:
        data = file['Basler data'][:, :, :]
    video_widget.imv.setImage(data)



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    w = TrackMainWindow()
    w.show()
    sys.exit(app.exec())