import os

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow
from Resources import resources
from .video_widget import VideoWidget

class TrackMainWindow(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        p = os.path.dirname(__file__)
        uic.loadUi(os.path.join(p, 'Resources/main_window.ui'), self)
        self.widget_video



if __name__ == "__main__":
    import sys
    from PyQt5.QtWidgets import QApplication
    app = QApplication([])
    w = TrackMainWindow()
    w.show()
    sys.exit(app.exec())