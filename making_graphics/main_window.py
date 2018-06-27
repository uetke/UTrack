import sys
import time
from random import randint, shuffle

from PyQt5 import uic, QtOpenGL, QtCore, QtGui
from PyQt5.QtCore import Qt, QPropertyAnimation
from PyQt5.QtWidgets import QWidget, QApplication, QGraphicsScene, QMainWindow, QGraphicsTextItem


class Main(QMainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        uic.loadUi('main_window.ui', self)

        self.digits = []
        self.animations = []

        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)

        self.scene.setSceneRect(0, 0, 800, 600)
        self.view.setViewport(QtOpenGL.QGLWidget())
        self.populate()

        self.setWindowState(Qt.WindowMaximized)

        self.animator = QtCore.QTimer()
        self.animator.timeout.connect(self.animate)
        self.animate()

    def populate(self):


        font = QtGui.QFont('White Rabbit')
        font.setPointSize(120)
        self.dot1 = QGraphicsTextItem(':')
        self.dot1.setFont(font)
        self.dot1.setPos(140, 0)
        self.scene.addItem(self.dot1)
        self.dot2 = QGraphicsTextItem(':')
        self.dot2.setFont(font)
        self.dot2.setPos(410, 0)
        self.scene.addItem(self.dot2)
        for i in range(60):
            l = QGraphicsTextItem(str(i % 10))
            l.setFont(font)
            l.setZValue(-100)
            l.setPos(randint(0, 500), randint(150, 300))
            l.setOpacity(.3)
            self.scene.addItem(l)
            self.digits.append(l)

    def animate(self):

        self.animations = [0]*60

        def animate_to(t, item, x, y, angle):
            animation = QPropertyAnimation(item, b'pos')

            # You create a timeline (in this case, it is 1 second long
            # timeline = QtCore.QTimeLine(1000)

            # And it has 100 steps
            # timeline.setFrameRange(0, 100)

            # I want that, at time t, the item be at point x,y
            # animation.setStartValue(item.getPos())
            animation.setEndValue(QtCore.QPointF(x, y))

            # And it should be rotated at angle "angle"
            # animation.setRotationAt(t, angle)

            # It should animate this specific item
            # animation.setItem(item)

            # And the whole animation is this long, and has
            # this many steps as I set in timeline.
            animation.setDuration(1000)

            # Here is the animation, use it.
            return animation

        # Ok, I confess it, this part is a mess, but... a little
        # mistery is good for you. Read this carefully, and tell
        # me if you can do it better. Or try to something nicer!

        offsets = [i for i in range(6)]
        shuffle(offsets)

        # Some items, animate with purpose
        h1, h2 = map(int, '%02d' % time.localtime().tm_hour)
        h1 += offsets[0] * 10
        h2 += offsets[1] * 10
        self.animations[h1] = animate_to(0.2, self.digits[h1], -40, 0, 0)
        self.animations[h2] = animate_to(0.2, self.digits[h2], 50, 0, 0)

        m1, m2 = map(int, '%02d' % time.localtime().tm_min)
        m1 += offsets[2] * 10
        m2 += offsets[3] * 10
        self.animations[m1] = animate_to(0.2, self.digits[m1], 230, 0, 0)
        self.animations[m2] = animate_to(0.2, self.digits[m2], 320, 0, 0)

        s1, s2 = map(int, '%02d' % time.localtime().tm_sec)
        s1 += offsets[4] * 10
        s2 += offsets[5] * 10
        self.animations[s1] = animate_to(0.2, self.digits[s1], 500, 0, 0)
        self.animations[s2] = animate_to(0.2, self.digits[s2], 590, 0, 0)

        # Other items, animate randomly
        for i in range(60):
            l = self.digits[i]
            if i in [h1, h2, m1, m2, s1, s2]:
                l.setOpacity(1)
                continue
            l.setOpacity(.3)
            self.animations[i] = animate_to(1, l, randint(0, 500), randint(0, 300), randint(0, 0))

        [animation.start() for animation in self.animations]

        self.animator.start(5000)

    def viewMousePressEvent(self, event):
        #        QtGui.QGraphicsView.mousePressEvent(self.view, event)
        pos = self.view.mapToScene(event.pos())
        sample, value = self.computePosValue(pos)
        print(value)
        # if self.draw_mode == DRAW_LINE:
        #     source = self.wave_path.path().elementAt(sample)
        #     x2 = sample * 16384
        #     y2 = pow20 - value
        #     self.scene.linedraw.setLine(source.x, source.y, x2, y2)
        #     self.scene.linedraw.setVisible(True)
        #     self.mouse_prev = sample, pow20 - source.y
        # elif self.draw_mode == DRAW_CURVE:
        #     if self.scene.curvepath.isVisible() and self.scene.curve_complete:
        #         return QtGui.QGraphicsView.mousePressEvent(self.view, event)
        #     source = self.wave_path.path().elementAt(sample)
        #     self.scene.setCurveStart(source.x, source.y, sample)
        #     self.scene.curvepath.setVisible(True)
        # #            self.mouse_prev = sample, value
        # else:
        #     self.drawAction.emit(DRAW_FREE, True)
        #     self.valueChanged.emit(sample, value)
        #     self.mouse_prev = sample, value


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Main()
    window.show()
    sys.exit(app.exec_())
