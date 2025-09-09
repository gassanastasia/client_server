import sys
import os
import logging
from PySide6.QtWidgets import QApplication

# Добавляем путь для импортов
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .ui.main_window import MainWindow

def setup_logging():
    """Setup application logging."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler(sys.stdout)]
    )

def main():
    """Main application entry point."""
    setup_logging()
    logging.info("Starting client application...")
    
    # Create Qt application
    app = QApplication(sys.argv)
    app.setApplicationName("Client Application")
    app.setApplicationVersion("1.0.0")
    
    # Create and show main window
    window = MainWindow()
    window.show()
    
    logging.info("Client application started successfully")
    
    # Start event loop
    sys.exit(app.exec())

if __name__ == "__main__":
    main()