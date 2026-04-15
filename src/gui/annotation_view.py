from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsItemGroup

from src.utils.types_and_dataclasses import ImageGUI, KeypointsCOCO, SkeletonCOCO
from src.utils.gui_toolkit import draw_keypoint
from src.config import KEYPOINT_SIZE


class AnnotationView(QGraphicsView):
    point_clicked : pyqtSignal = pyqtSignal(QPointF)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)

        self._scene = scene
        self._frame_obj = None
        self._click_task = self._zoom
        self._pan_start = None

        # courser design
        self.cursor_follower = None
        self.setCursor(Qt.CursorShape.CrossCursor)

    ####### Custom methods #######
    def new_image(self, image_data: ImageGUI, keypoints: KeypointsCOCO):
        self.set_image(image_data)
        self.draw_keypoints(keypoints)

    def set_image(self, image_data: ImageGUI):
        q_img = QImage(
            image_data.data,
            image_data.width,
            image_data.height,
            image_data.bytes_per_line,
            QImage.Format.Format_RGB888
        )
        pixmap = QPixmap.fromImage(q_img)
        if self._frame_obj is None: self._frame_obj = self._scene.addPixmap(pixmap)
        else: self._frame_obj.setPixmap(pixmap)
        self.setSceneRect(self._frame_obj.boundingRect())
        self.update_image_scale(self._frame_obj)

    def draw_keypoints(self, keypoints: KeypointsCOCO):
        for keypoint_list in keypoints:
            for i, keypoint in enumerate(keypoint_list):
                self._scene.addItem(draw_keypoint(
                    i,
                    (keypoint[0], keypoint[1]),
                    visibility=keypoint[2],
                    size=KEYPOINT_SIZE
                ))

    def _zoom(self, coordinates: QPointF, factor=10):
        self.scale(factor, factor)
        self.centerOn(coordinates)

    def update_image_scale(self, frame_obj):
        if frame_obj:
            self.fitInView(
                frame_obj,
                Qt.AspectRatioMode.KeepAspectRatio
            )

    def _get_fit_scale(self) -> float:
        if not self._frame_obj:
            return 1.0
        viewport = self.viewport().size()
        scene_rect = self._frame_obj.boundingRect()
        scale_x = viewport.width() / scene_rect.width()
        scale_y = viewport.height() / scene_rect.height()
        return min(scale_x, scale_y)

    ####### Signal handlers #######
    def _emit_click(self, coordinates: QPointF):
        self.point_clicked.emit(coordinates)

    ####### Event handlers #######
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
            # Set Keypoints
            if event.modifiers() & Qt.KeyboardModifier.ControlModifier:
                self._emit_click(self.mapToScene(event.pos()))  # TODO redundant? Use signal directly?
            else:
                if self.transform().m11() < self._get_fit_scale() * 1.01:
                    self._zoom(self.mapToScene(event.pos()))
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
