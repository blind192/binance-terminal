import sys
import warnings
from PyQt5.QtWidgets import QApplication

from src.controller.main_controller import MainController
from src.config.styles import apply_theme

warnings.filterwarnings("ignore", category=DeprecationWarning, message="sipPyTypeDict.*")

if __name__ == "__main__":
    app = QApplication([])
    
    # Apply theme
    apply_theme()
    
    # Create main controller
    controller = MainController()
    
    # Show main window
    controller.show_window()
    
    # Start main event loop
    sys.exit(app.exec_())
