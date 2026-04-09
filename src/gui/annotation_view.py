from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QImage, QPixmap, QMouseEvent
from PyQt6.QtWidgets import QGraphicsView


class AnnotationView(QGraphicsView):
    point_clicked : pyqtSignal = pyqtSignal(QPointF)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self._scene = scene
        self._frame_obj = None
        self._click_task = self._zoom

    ####### Custom methods #######
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
        self.setSceneRect(self.frame_obj.boundingRect())
        self.update_image_scale(self.frame_obj)

    def _zoom(self, coordinates: QPointF, factor=10):
        self.scale(factor, factor)
        self.centerOn(coordinates)

    def update_image_scale(self, frame_obj):
        if frame_obj:
            self.fitInView(
                frame_obj,
                Qt.AspectRatioMode.KeepAspectRatio
            )

    ####### Signal handlers #######
    def _emit_click(self, coordinates: QPointF):
        self.point_clicked.emit(coordinates)

    ####### Event handlers #######
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                # Set Keypoint
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
                self._emit_click(self.mapToScene(event.pos()))  # TODO redundant? Use signal directly?
            else:
                if self.transform().m11() < 1.01: self._zoom(self.mapToScene(event.pos()))
                self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
                super().mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        # Sobald die Taste losgelassen wird, deaktivieren wir den Drag-Modus wieder
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)
