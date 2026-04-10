from PyQt6.QtCore import Qt, pyqtSignal, QPointF
from PyQt6.QtGui import QImage, QPixmap, QColor, QPen, QBrush, QPainterPath, QPolygonF
from PyQt6.QtWidgets import QGraphicsView, QGraphicsPathItem

from src.utils.types_and_dataclasses import ImageGUI, KeypointsCOCO
from src.config import KEYPOINT_COLORS, KEYPOINT_SIZE


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
        self._scene.clear()
        self.frame_obj = self._scene.addPixmap(pixmap)
        self.setSceneRect(self.frame_obj.boundingRect())
        self.update_image_scale(self.frame_obj)

    def draw_keypoints(self, keypoints: KeypointsCOCO):
        for keypoint_list in keypoints:
            for i, keypoint in enumerate(keypoint_list):
                self._scene.addItem(self._get_symbol(i, keypoint))

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
        if not self.frame_obj:
            return 1.0
        viewport = self.viewport().size()
        scene_rect = self.frame_obj.boundingRect()
        scale_x = viewport.width() / scene_rect.width()
        scale_y = viewport.height() / scene_rect.height()
        return min(scale_x, scale_y)


    @staticmethod
    def _get_symbol(index, keypoint: tuple[int, int, int]):

        color_code = "#FFFFFF"
        for color, indices in KEYPOINT_COLORS.items():
            if index in indices:
                color_code = color

        color = QColor(color_code)
        size = KEYPOINT_SIZE
        path = QPainterPath()

        x, y, visibility = keypoint
        match visibility:
            case 0:
                # Not labeled / hidden: draw an X marker.
                path.moveTo(x - size, y - size)
                path.lineTo(x + size, y + size)
                path.moveTo(x + size, y - size)
                path.lineTo(x - size, y + size)
            case 1:
                # Labeled but not visible: triangle pointing down.
                triangle = QPolygonF([
                    QPointF(x, y + size),
                    QPointF(x - size, y - size),
                    QPointF(x + size, y - size),
                ])
                path.addPolygon(triangle)
                path.closeSubpath()
            case 2:
                # Visible and labeled: triangle pointing up.
                triangle = QPolygonF([
                    QPointF(x, y - size),
                    QPointF(x - size, y + size),
                    QPointF(x + size, y + size),
                ])
                path.addPolygon(triangle)
                path.closeSubpath()
            case _:
                raise ValueError(f"Wrong visibility value for keypoint: {visibility}")

        symbol_item = QGraphicsPathItem(path)
        if visibility in (1, 2):
            symbol_item.setPen(QPen(Qt.PenStyle.NoPen))
            symbol_item.setBrush(QBrush(color))
        else:
            pen = QPen(color)
            pen.setWidth(2)
            symbol_item.setPen(pen)
        return symbol_item

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
