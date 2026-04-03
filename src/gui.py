from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMainWindow
from PyQt6.QtGui import QPixmap, QImage, QKeySequence, QShortcut
from PyQt6.QtCore import Qt, pyqtSignal

from src.utils.image_data import ImageData

class Gui(QMainWindow):
    next_requested: pyqtSignal = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.configure_window()

        self.frame_obj = None

        self.shortcuts()


    ########### Custom methods ###########
    def configure_window(self):
        self.setWindowTitle("Annotator")
        self.resize(800, 600)
        self.setCentralWidget(self.view)

    def display_image(self, image_data: ImageData):
        q_img = QImage(
            image_data.data,
            image_data.width,
            image_data.height,
            image_data.bytes_per_line,
            QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_img)
        self.scene.clear()
        self.frame_obj = self.scene.addPixmap(pixmap)

    ########## Event handlers ##########
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.update_image_scale()

    def update_image_scale(self):
        if self.frame_obj:
            self.view.fitInView(
                self.frame_obj,
                Qt.AspectRatioMode.KeepAspectRatio
            )

    def shortcuts(self):
        # RIGHT KEY
        self.next_shortcut = QShortcut(Qt.Key.Key_Right, self)
        self.next_shortcut.activated.connect(lambda: print("GUI-Shortcut: RECHTS erkannt!"))
        self.next_shortcut.activated.connect(self.next_requested.emit)
