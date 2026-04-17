from PyQt6.QtWidgets import QGraphicsScene, QMainWindow
from PyQt6.QtGui import QShortcut
from PyQt6.QtCore import Qt, pyqtSignal

from src.utils.types_and_dataclasses import ImageGUI, SkeletonsData, Keypoint
from src.gui.annotation_view import AnnotationView


class App(QMainWindow):
    next_img: pyqtSignal = pyqtSignal()
    prev_img: pyqtSignal = pyqtSignal()
    get_img: pyqtSignal = pyqtSignal(int) #TODO implement
    set_kp: pyqtSignal = pyqtSignal(object)
    next_kp: pyqtSignal = pyqtSignal()
    prev_kp: pyqtSignal = pyqtSignal()
    remove_kp: pyqtSignal = pyqtSignal()
    skeleton_index: pyqtSignal = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        # Window configuration
        self.setWindowTitle("Annotator")
        self.resize(800, 600)

        # Graphics Scene configuration
        self._scene = QGraphicsScene()
        self._annotation_view = AnnotationView(self._scene)

        # Layout configuration
        self.setCentralWidget(self._annotation_view)

        # Signals
        self._annotation_view.point_clicked.connect(self._point_clicked)

        self.frame_obj = None
        self._shortcuts()

    ########## Event handlers ##########
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Aufruf der Methode in der View
        self._annotation_view.update_image_scale(self.frame_obj)

    def _shortcuts(self):
        # RIGHT KEY -> NEXT IMAGE
        self.next_img_shortcut = QShortcut(Qt.Key.Key_Right, self)
        self.next_img_shortcut.activated.connect(self.next_img.emit)

        # LEFT KEY -> PREV IMAGE
        self.prev_img_shortcut = QShortcut(Qt.Key.Key_Left, self)
        self.prev_img_shortcut.activated.connect(self.prev_img.emit)

        # E Key -> NEXT KEYPOINT
        self.next_keypoint_shortcut = QShortcut(Qt.Key.Key_E, self)
        self.next_keypoint_shortcut.activated.connect(self.next_kp.emit)

        # Q KEY -> PREV KEYPOINT
        self.next_keypoint_shortcut = QShortcut(Qt.Key.Key_Q, self)
        self.next_keypoint_shortcut.activated.connect(self.prev_kp.emit)

        # R Key -> Remove Keypoint
        self.remove_kp_shortcut = QShortcut(Qt.Key.Key_R, self)
        self.remove_kp_shortcut.activated.connect(self.remove_kp.emit)

        # W KEY -> ENABLE SET KEYPOINTS = keyPressEvent

        # 1 - 9 -> SET TRACKING ID / NAVIGATE SKELETONS

    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self._annotation_view.set_kp_mode(True)
        if Qt.Key.Key_1 <= event.key() <= Qt.Key.Key_9:
            number = (event.key() - Qt.Key.Key_0) -1
            self.skeleton_index.emit(number)

    def keyReleaseEvent(self, event):
        if event.key() == Qt.Key.Key_W:
            self._annotation_view.set_kp_mode(False)

    ########### Signal handlers ##########
    def _point_clicked(self, keypoint: Keypoint):
        self.set_kp.emit(keypoint)

    ########### Function Calls ##########
    def new_image(self, image_data: ImageGUI):
        self._annotation_view.set_image(image_data)

    def new_data(self, keypoints: SkeletonsData):
        self._annotation_view.draw_keypoints(keypoints)