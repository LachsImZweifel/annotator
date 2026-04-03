from PyQt6.QtWidgets import QGraphicsScene, QMainWindow
from PyQt6.QtGui import QImage, QPixmap, QShortcut
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
        self._view = AnnotationView(self._scene)

        # Layout configuration
        self.setCentralWidget(self._view)

        # Signals
        self._view.point_clicked.connect(self._point_clicked)

        self.frame_obj = None
        self._shortcuts()

    ########### Custom methods ###########
    def display_image(self, image_data: ImageData):
        q_img = QImage(
            image_data.data,
            image_data.width,
            image_data.height,
            image_data.bytes_per_line,
            QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_img)
        self._scene.clear()
        self.frame_obj = self._scene.addPixmap(pixmap)
        self._view._update_image_scale(self.frame_obj)

    ########## Event handlers ##########
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aufruf der Methode in der View
        self._view._update_image_scale(self.frame_obj)

    def _shortcuts(self):
        # RIGHT KEY
        self.next_shortcut = QShortcut(Qt.Key.Key_Right, self)
        self.next_shortcut.activated.connect(self.next_img.emit)

        # LEFT KEY
        self.prev_shortcut = QShortcut(Qt.Key.Key_Left, self)
        self.prev_shortcut.activated.connect(self.prev_img.emit)

    def _point_clicked(self, scene_pos):
        self.point_clicked.emit(scene_pos)