from PyQt5.QtWidgets import QGraphicsView, QGridLayout
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QCloseEvent
import ctypes
import finplot as fplt

class MainWindow(QGraphicsView):
    def __init__(self, controller):
        super().__init__()
        self.controller = controller
        self.setup_ui()
    
    def setup_ui(self):
        """Setup the main window UI"""
        self.global_layout = QGridLayout()
        self.setLayout(self.global_layout)
        self.setWindowTitle("Terminal")

        # Background color surrounding the plots
        self.setStyleSheet("background-color:" + fplt.background)
        width = ctypes.windll.user32.GetSystemMetrics(0)
        height = ctypes.windll.user32.GetSystemMetrics(1)
        self.resize(int(width * 0.7), int(height * 0.7))

        # Finplot requires this property
        self.axs = []
        fplt.autoviewrestore()
    
    def closeEvent(self, event: QCloseEvent) -> None:
        """Handle the close event of the main window."""
        self.controller.on_window_close()
        QCoreApplication.quit()
