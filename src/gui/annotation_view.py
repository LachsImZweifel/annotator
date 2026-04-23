from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGraphicsView, QGraphicsItem, QGraphicsItemGroup

from src.utils.types_and_dataclasses import ImageGUI, SkeletonsData
from src.utils.gui_toolkit import draw_keypoint
from src.config import KEYPOINT_SIZE


class AnnotationView(QGraphicsView):
    point_clicked : pyqtSignal = pyqtSignal(object)

    def __init__(self, scene, parent=None):
        super().__init__(scene, parent)
        self._scene = scene
        self._frame_obj = None

        # navigation & controls
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self._click_task = self._zoom
        self._pan_start = None
        self._enable_keypoints = False

        # visual
        self.setCursor(Qt.CursorShape.CrossCursor)
        self._kp_group = None

    ####### Custom methods #######
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

    def draw_keypoints(self, skeletons_data: SkeletonsData):
        self._prepare_keypoints()

        for skeleton_data in skeletons_data:
            for i, keypoint in enumerate(skeleton_data):
                item = draw_keypoint(
                    i,
                    (keypoint[0], keypoint[1]),
                    visibility=keypoint[2],
                    size=KEYPOINT_SIZE
                )
                self._kp_group.addToGroup(item)

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


    def _handle_keypoint_click(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self._emit_click(event.pos(), 2)
        elif event.button() == Qt.MouseButton.RightButton:
            self._emit_click(event.pos(), 1)

    def _handle_navigation(self, event):
        if self.transform().m11() < self._get_fit_scale() * 1.01:
            self._zoom(self.mapToScene(event.pos()))
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        super().mousePressEvent(event)

    def _prepare_keypoints(self):
        if self._kp_group is not None:
            self._scene.removeItem(self._kp_group)
            self._kp_group = None
        self._kp_group = QGraphicsItemGroup()
        self._kp_group.setZValue(10)
        self._scene.addItem(self._kp_group)

    ####### Signal handlers #######
    def _emit_click(self, event_pos: QPointF, visibility=None):
        scene_pos = self.mapToScene(event_pos)
        self.point_clicked.emit((scene_pos.x() , scene_pos.y(), visibility))

    ####### Event handlers #######
    def mousePressEvent(self, event):
        if self._enable_keypoints:
            self._handle_keypoint_click(event)
        elif event.button() == Qt.MouseButton.LeftButton:
            self._handle_navigation(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_in_factor = 1.25
        zoom_out_factor = 1 / zoom_in_factor

        if event.angleDelta().y() > 0:
            self.scale(zoom_in_factor, zoom_in_factor)
        else:
            self.scale(zoom_out_factor, zoom_out_factor)

    def set_kp_mode(self, kp_mode: bool):
        self._enable_keypoints = kp_mode
