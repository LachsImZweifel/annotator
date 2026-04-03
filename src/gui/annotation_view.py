from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtWidgets import QGraphicsView


class AnnotationView(QGraphicsView):
    point_clicked : pyqtSignal = pyqtSignal(QPointF)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)

    def _zoom_in(self, factor=5):
        self.scale(factor, factor)

    def _update_image_scale(self, frame_obj):
        if frame_obj:
            self.fitInView(
                frame_obj,
                Qt.AspectRatioMode.KeepAspectRatio
            )

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            # Umrechnung von Monitor-Pixel zu Bild-Pixel
            scene_pos = self.mapToScene(event.pos())
            self.point_clicked.emit(scene_pos)

        super().mousePressEvent(event)