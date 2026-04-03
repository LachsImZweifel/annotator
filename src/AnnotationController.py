import sys
from PyQt6.QtWidgets import QApplication

from src.data_handler import DataHandler
from src.gui import Gui

class AnnotationController:
    def __init__(self, data_path:str, video_mode:bool=False):
        self._app = QApplication([])
        self._data_handler = DataHandler(data_path, video_mode)
        self._gui = Gui()

        # Signals
        self._gui.next_img.connect(self._next_image)
        self._gui.prev_img.connect(self._previous_image)

        self._next_image()
        self._run_gui()

    def _run_gui(self):
        self._gui.show()
        sys.exit(self._app.exec())

    def _next_image(self):
        image = self._data_handler.next_image()
        if image is not None:
            self._gui.display_image(image)

    def _previous_image(self):
        image = self._data_handler.previous_image()
        if image is not None:
            self._gui.display_image(image)






