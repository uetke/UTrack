from PyQt5.QtCore import QPointF, pyqtSignal, pyqtProperty, QUrl
from PyQt5.QtGui import QColor, QGuiApplication
from PyQt5.QtQml import qmlRegisterType
from PyQt5.QtQuick import QQuickItem, QSGGeometryNode, QSGGeometry, QSGFlatColorMaterial, QSGNode, QQuickView


class BezierCurve(QQuickItem):
    # Signals
    p1_changed = pyqtSignal('QPointF')
    p2_changed = pyqtSignal('QPointF')
    p3_changed = pyqtSignal('QPointF')
    p4_changed = pyqtSignal('QPointF')
    segment_count_changed = pyqtSignal(int)

    #Properties
    @pyqtProperty(QPointF, notify=p1_changed)
    def p1(self):
        return self.m_p1

    @p1.setter
    def p1(self, p):
        if self.m_p1 != p:
            self.m_p1 = p
            self.p1_changed.emit(p)
            self.update()

    @pyqtProperty(QPointF, notify=p2_changed)
    def p2(self):
        return self.m_p2

    @p2.setter
    def p2(self, p):
        if self.m_p2 != p:
            self.m_p2 = p
            self.p2_changed.emit(p)
            self.update()

    @pyqtProperty(QPointF, notify=p3_changed)
    def p3(self):
        return self.m_p3

    @p3.setter
    def p3(self, p):
        if self.m_p3 != p:
            self.m_p3 = p
            self.p3_changed.emit(p)
            self.update()

    @pyqtProperty(QPointF, notify=p4_changed)
    def p4(self):
        return self.m_p4

    @p4.setter
    def p4(self, p):
        if self.m_p4 != p:
            self.m_p4 = p
            self.p4_changed.emit(p)
            self.update()

    @pyqtProperty(int, notify=segment_count_changed)
    def segment_count(self):
        return self.m_segment_count

    @segment_count.setter
    def segment_count(self, s):
        if self.m_segment_count != s:
            self.m_segment_count = s
            self.segment_count_changed.emit(s)
            self.update()

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.m_p1 = QPointF(0, 0)
        self.m_p2 = QPointF(1, 0)
        self.m_p3 = QPointF(0, 1)
        self.m_p4 = QPointF(1, 1)
        self.m_segment_count = 16
        self.setFlag(QQuickItem.ItemHasContents, True)
        self.node = None

    def updatePaintNode(self, old_node, _):
        if not old_node:
            self.node = QSGGeometryNode()
            geometry = QSGGeometry(QSGGeometry.defaultAttributes_Point2D(), self.m_segment_count)
            geometry.setLineWidth(2)
            geometry.setDrawingMode(QSGGeometry.DrawLineStrip)
            self.node.setGeometry(geometry)
            self.node.setFlag(QSGNode.OwnsGeometry)
            material = QSGFlatColorMaterial()
            material.setColor(QColor(255, 0, 0))
            self.node.setMaterial(material)
            self.node.setFlag(QSGNode.OwnsMaterial)
        else:
            geometry = self.node.geometry()
            geometry.allocate(self.m_segment_count)

        w = self.width()
        h = self.height()
        vertices = geometry.vertexDataAsPoint2D()
        for i in range(self.m_segment_count):
            t = i/(self.m_segment_count-1)
            invt = 1-t
            pos = invt * invt * invt * self.m_p1 \
                  + 3 * invt * invt * t * self.m_p2 \
                  + 3 * invt * t * t * self.m_p3 \
                  + t * t * t * self.m_p4

            vertices[i].set(pos.x()*w, pos.y()*h)

        self.node.markDirty(QSGNode.DirtyGeometry)

        return self.node


if __name__ == '__main__':
    import sys


    app = QGuiApplication(sys.argv)

    qmlRegisterType(BezierCurve, "CustomGeometry", 1, 0, "BezierCurve")
    view = QQuickView()
    format = view.format()
    format.setSamples(16)
    view.setFormat(format)
    view.setSource(QUrl('main.qml'))
    view.show()
    view.showMaximized()

    sys.exit(app.exec_())
