from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsView


class AnnotationView(QGraphicsView):
    point_clicked : pyqtSignal = pyqtSignal(QPointF)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._scene = scene
        self._frame_obj = None
        self._click_task = self._zoom

    def set_image(self, image_data):
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
        self.update_image_scale(self.frame_obj)

    def _zoom(self, coordinates: QPointF, factor=5):
        self.scale(factor, factor)
        self.centerOn(coordinates)
        self._click_task = self._emit_click

    def _emit_click(self, coordinates: QPointF):
        self.point_clicked.emit(coordinates)

    def update_image_scale(self, frame_obj):
        if frame_obj:
            self.fitInView(
                frame_obj,
                Qt.AspectRatioMode.KeepAspectRatio
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._click_task(self.mapToScene(event.pos()))

        super().mousePressEvent(event)