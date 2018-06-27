import sys

from PyQt5 import Qt
from PyQt5.QtCore import QMetaObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView, QApplication


class ImageView(QGraphicsView):
    def __init__(self, parent=None, pixmap=None):
        super(ImageView, self).__init__(parent)
        self.pixmap = pixmap
        # QMetaObject.connectSlotsByName(self)

        # self.resized().connect(self.resized)

    def resized(self, *args):
        print(args)

    def resizeEvent(self, event):
        size = event.size()
        item = self.items()[0]
        pixmap = self.pixmap.scaled(size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        item.setPixmap(pixmap)


app = QApplication(sys.argv)
pic = QPixmap('pixmap.jpg')
grview = ImageView(pixmap=pic)
scene = QGraphicsScene()
grview.setScene(scene)
grview.show()
sys.exit(app.exec_())


