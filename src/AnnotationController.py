import sys
from PyQt6.QtWidgets import QApplication

from src.data_handler import DataHandler
from src.gui import Gui

class AnnotationController:
    def __init__(self, data_path:str, video_mode:bool=False):
        self.current_frame_index = 0
        self.app = QApplication([])
        self.data_handler = DataHandler(data_path, video_mode)
        self.gui = Gui()

        self.next_frame()
        self.run_gui()

    def run_gui(self):
        self.gui.show()
        sys.exit(self.app.exec())

    def next_frame(self):
        frame = self.data_handler.get_image()
        if frame is not None:
            self.gui.display_image(frame)






