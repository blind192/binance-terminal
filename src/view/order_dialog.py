from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, 
    QDoubleSpinBox, QPushButton, QMessageBox
)

class OrderDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
    
    def setup_ui(self):
        """Setup order dialog UI"""
        self.setWindowTitle("Create Order")
        self.setModal(True)
        self.setFixedSize(600, 400)
        
        layout = QVBoxLayout(self)
        
        # Order Type (BUY/SELL)
        type_layout = QHBoxLayout()
        type_layout.addWidget(QLabel("Order Type:"))
        self.order_type = QComboBox()
        self.order_type.addItems(["BUY", "SELL"])
        self.order_type.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 4px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                selection-background-color: #4CAF50;
            }
        """)
        type_layout.addWidget(self.order_type)
        layout.addLayout(type_layout)
        
        # Stop Loss
        sl_layout = QHBoxLayout()
        sl_layout.addWidget(QLabel("Stop Loss:"))
        self.sl_input = QDoubleSpinBox()
        self.sl_input.setDecimals(4)
        self.sl_input.setMinimum(0.0001)
        self.sl_input.setMaximum(999999.9999)
        sl_layout.addWidget(self.sl_input)
        layout.addLayout(sl_layout)
        
        # Take Profit
        tp_layout = QHBoxLayout()
        tp_layout.addWidget(QLabel("Take Profit:"))
        self.tp_input = QDoubleSpinBox()
        self.tp_input.setDecimals(4)
        self.tp_input.setMinimum(0.0001)
        self.tp_input.setMaximum(999999.9999)
        tp_layout.addWidget(self.tp_input)
        layout.addLayout(tp_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.create_btn = QPushButton("Create")
        self.create_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.clicked.connect(self.reject)
        
        self.cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        button_layout.addWidget(self.create_btn)
        button_layout.addWidget(self.cancel_btn)
        layout.addLayout(button_layout)
        
        self.setStyleSheet("""
            QDialog {
                background-color: #2c2c2c;
            }
            QLabel {
                color: white;
                font-size: 16px;
                min-width: 80px;
            }
            QDoubleSpinBox {
                background-color: white;
                border: 1px solid #555;
                padding: 5px;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
    
    def get_order_data(self):
        """Get order data from dialog"""
        return {
            'type': self.order_type.currentText(),
            'stop_loss': self.sl_input.value(),
            'take_profit': self.tp_input.value()
        }
