from PyQt5.QtDesigner import QPyDesignerCustomWidgetPlugin, QExtensionFactory
from PyQt5.QtWidgets import QWidget
from pyqtgraph import ImageView

class VideoWidget(QPyDesignerCustomWidgetPlugin):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.initialized = False
        self.view = ImageView()

    def initialize(self, formEditor):
        if self.initialized:
            return

        manager = formEditor.extensionManager()
        if manager:
            # self.factory = VideoWidgetTaskMenuFactory(manager)
            # manager.registerExtensions(self.factory, 'com.trolltech.Qt.Designer.TaskMenu')
            pass
        
    def createWidget(self, widget):
        return VideoWidget(widget)

    def name(self):
        return "VideoWidget"

    def includeFile(self):
        return "QQ_Widgets.videowidget"

    def update_data(self, data):
        self.view.setImage(data)


class VideoWidgetTaskMenuFactory(QExtensionFactory):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

    def createExtension(self, obj, iid, parent):
        if iid != 'com.trolltech.Qt.Designer.TaskMenu':
            return None

        if isinstance(obj, VideoWidget):
            return True