from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QMainWindow
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtCore import Qt

from src.utils.image_data import ImageData

class Gui(QMainWindow):
    def __init__(self):
        super().__init__()
        # Window configuration
        self.setWindowTitle("Annotator")
        self.resize(800, 600)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.setCentralWidget(self.view)

        self.frame_obj = None

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

