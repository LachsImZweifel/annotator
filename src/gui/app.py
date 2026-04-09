from PyQt6.QtWidgets import QGraphicsScene, QMainWindow
from PyQt6.QtGui import QShortcut
from PyQt6.QtCore import Qt, pyqtSignal, QPointF

from src.data_handler import ImageData
from src.gui.annotation_view import AnnotationView


class App(QMainWindow):
    next_img: pyqtSignal = pyqtSignal()
    prev_img: pyqtSignal = pyqtSignal()
    point_clicked: pyqtSignal = pyqtSignal(QPointF)

    def __init__(self):
        super().__init__()
        # Window configuration
        self.setWindowTitle("Annotator")
        self.resize(800, 600)

        # Graphics Scene configuration
        self._scene = QGraphicsScene()
        self._annotation_view = AnnotationView(self._scene)

        # Layout configuration
        self.setCentralWidget(self._annotation_view)

        # Signals
        self._annotation_view.point_clicked.connect(self._point_clicked)

        self.frame_obj = None
        self._shortcuts()

    ########## Event handlers ##########
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aufruf der Methode in der View
        self._annotation_view.update_image_scale(self.frame_obj)

    def _shortcuts(self):
        # RIGHT KEY
        self.next_shortcut = QShortcut(Qt.Key.Key_Right, self)
        self.next_shortcut.activated.connect(self.next_img.emit)
        self.next_shortcut.activated.connect(lambda: self._annotation_view.switch_task("zoom"))

        # LEFT KEY
        self.prev_shortcut = QShortcut(Qt.Key.Key_Left, self)
        self.prev_shortcut.activated.connect(self.prev_img.emit)
        self.next_shortcut.activated.connect(lambda: self._annotation_view.switch_task("zoom"))

    ########### Signal handlers ##########
    def _point_clicked(self, scene_pos):
        self.point_clicked.emit(scene_pos)

    ########### Function Calls ##########
    def set_image(self, image_data: ImageData):
        self._annotation_view.set_image(image_data)