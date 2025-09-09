from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QListView, QPushButton, QLabel, QMessageBox
)
from PySide6.QtCore import Qt, QStringListModel
import logging

from client.utils.api_client import APIClient

logger = logging.getLogger(__name__)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.api_client = APIClient()
        self.init_ui()
        self.setup_connections()
    
    def init_ui(self):
        self.setWindowTitle("Client Application")
        self.setGeometry(100, 100, 600, 400)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout(central_widget)
        
        # Input section
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.setPlaceholderText("Enter request text...")
        input_layout.addWidget(self.input_field)
        
        self.send_button = QPushButton("Send Request")
        input_layout.addWidget(self.send_button)
        
        layout.addLayout(input_layout)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        self.get_requests_button = QPushButton("Get Requests")
        self.clear_button = QPushButton("Clear")
        buttons_layout.addWidget(self.get_requests_button)
        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addStretch()
        
        layout.addLayout(buttons_layout)
        
        # List view section
        self.list_view = QListView()
        self.list_model = QStringListModel()
        self.list_view.setModel(self.list_model)
        
        layout.addWidget(QLabel("Requests:"))
        layout.addWidget(self.list_view)
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def setup_connections(self):
        self.send_button.clicked.connect(self.on_send_clicked)
        self.get_requests_button.clicked.connect(self.on_get_requests_clicked)
        self.clear_button.clicked.connect(self.on_clear_clicked)
    
    def on_send_clicked(self):
        text = self.input_field.text().strip()
        if not text:
            QMessageBox.warning(self, "Warning", "Please enter some text")
            return
        
        self.statusBar().showMessage("Sending request...")
        
        response = self.api_client.send_request(text)
        if response:
            self.statusBar().showMessage(f"Request sent successfully (ID: {response['id']})")
            self.input_field.clear()
        else:
            self.statusBar().showMessage("Failed to send request")
            QMessageBox.critical(self, "Error", "Failed to send request to server")
    
    def on_get_requests_clicked(self):
        self.statusBar().showMessage("Fetching requests...")
        
        response = self.api_client.get_requests()
        if response and response.get("items"):
            requests = response["items"]
            display_texts = []
            
            for req in requests:
                text = f"[{req['id']}] {req['text']} (Clicks: {req['click_count']}, Date: {req['request_date']})"
                display_texts.append(text)
            
            self.list_model.setStringList(display_texts)
            self.statusBar().showMessage(f"Loaded {len(requests)} requests")
        else:
            self.statusBar().showMessage("No requests found or server error")
            self.list_model.setStringList(["No requests available"])
    
    def on_clear_clicked(self):
        self.input_field.clear()
        self.list_model.setStringList([])
        self.api_client.reset_click_count()
        self.statusBar().showMessage("Cleared")
    
    def closeEvent(self, event):
        """Handle application close."""
        reply = QMessageBox.question(
            self,
            "Confirm Exit",
            "Are you sure you want to exit?",
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No
        )
        
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()