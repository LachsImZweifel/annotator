from PyQt6.QtCore import Qt, QPointF
from PyQt6.QtGui import QColor, QPen, QBrush, QPainterPath, QPolygonF, QFont
from PyQt6.QtWidgets import QGraphicsPathItem

from src.utils.types_and_dataclasses import Shapes
from src.config import KEYPOINT_COLORS
#TODO: Refactor to toolkit with flexible shapes and colors

def draw_symbol(coordinates: tuple[float, float], shape: Shapes,
                size: int, color_code: str, text: str = "") -> QGraphicsPathItem:

    color = QColor(color_code)
    path = QPainterPath()
    x, y, = coordinates

    match shape:
        case "x":
            path.moveTo(x - size, y - size)
            path.lineTo(x + size, y + size)
            path.moveTo(x + size, y - size)
            path.lineTo(x - size, y + size)
        case "triangle_down":
            triangle = QPolygonF([
                QPointF(x, y + size),
                QPointF(x - size, y - size),
                QPointF(x + size, y - size),
            ])
            path.addPolygon(triangle)
            path.closeSubpath()
        case "triangle_up":
            triangle = QPolygonF([
                QPointF(x, y - size),
                QPointF(x - size, y + size),
                QPointF(x + size, y + size),
            ])
            path.addPolygon(triangle)
            path.closeSubpath()
        case "text":
            font = QFont("Arial", size * 2)
            font.setBold(True)
            text_to_draw = text[:3]
            offset = size * 2
            path.addText(x + offset, y - offset, font, text_to_draw)
        case _:
            raise ValueError("Unknown shape: {}".format(shape))

    symbol_item = QGraphicsPathItem(path)
    if shape in ["x"]:
        pen = QPen(color)
        pen.setWidth(2)
        symbol_item.setPen(pen)
    else:
        symbol_item.setPen(QPen(Qt.PenStyle.NoPen))
        symbol_item.setBrush(QBrush(color))
    return symbol_item

def draw_keypoint(skeleton_index: int, coordinates: tuple[float, float], visibility: int, size: int):
    shapes: dict[int, Shapes] = {
        0 : "x",
        1 : "triangle_down",
        2 : "triangle_up",
    }
    color_code = "#FFFFFF"
    for color, indices in KEYPOINT_COLORS.items():
        if skeleton_index in indices:
            color_code = color
            break

    shape = shapes.get(visibility, "x")
    return draw_symbol(coordinates, shape, size, color_code)