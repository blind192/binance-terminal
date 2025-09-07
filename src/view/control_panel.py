from PyQt5.QtWidgets import (
    QComboBox, QWidget, QPushButton, QLabel, QHBoxLayout, QVBoxLayout
)
from PyQt5.QtCore import Qt
from src.utils.constants import SUPPORTED_COINS, TIMEFRAMES

class ControlPanel:
    def __init__(self, controller):
        self.controller = controller
        self.panel = None
        self.timeframe_combo = None
        self.asset_combo = None
        self.order_btn = None
    
    def create_panel(self):
        """Create control panel"""
        panel = QWidget()
        
        # Use vertical layout to push elements to top
        main_layout = QVBoxLayout(panel)
        main_layout.setAlignment(Qt.AlignTop)
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Create horizontal layout for controls
        controls_layout = QHBoxLayout()
        controls_layout.setAlignment(Qt.AlignLeft)
        controls_layout.setSpacing(10)
        
        # Add elements
        self._create_balance_label(controls_layout)
        self._create_timeframe_combobox(controls_layout)
        self._create_coin_combobox(controls_layout)
        self._create_order_button(controls_layout)
        
        # Add horizontal layout to vertical
        main_layout.addLayout(controls_layout)
        
        self.panel = panel
        return panel
    
    def _create_balance_label(self, layout):
        """Create balance label"""
        balance_label = QLabel("Balance: <span style='color: #4CAF50;'>15 000$</span>")
        balance_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 8px 16px;
                background-color: #1e1e1e;
                border-radius: 6px;
                min-width: 150px;
            }
        """)
        balance_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(balance_label)
        layout.addSpacing(20)
    
    def _create_timeframe_combobox(self, layout):
        """Create timeframe combobox"""
        self.timeframe_combo = QComboBox()
        
        for timeframe in TIMEFRAMES:
            self.timeframe_combo.addItem(timeframe)
            
        self.timeframe_combo.setCurrentIndex(0)  # 1m as default
        self.timeframe_combo.setMinimumWidth(120)
        
        self.timeframe_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                selection-background-color: #4CAF50;
                min-width: 120px;
            }
        """)
        
        self.timeframe_combo.currentTextChanged.connect(self.controller.on_timeframe_changed)
        layout.addWidget(self.timeframe_combo)
    
    def _create_coin_combobox(self, layout):
        """Create coin combobox"""
        self.asset_combo = QComboBox()
        
        for coin in SUPPORTED_COINS:
            self.asset_combo.addItem(coin)
        
        self.asset_combo.setCurrentIndex(0)  # BTCUSDT as default
        self.asset_combo.setMinimumWidth(200)
        self.asset_combo.currentTextChanged.connect(self.controller.on_coin_changed)
        self.asset_combo.setStyleSheet("""
            QComboBox {
                background-color: #1e1e1e;
                color: white;
                border: 1px solid #555;
                padding: 8px 12px;
                border-radius: 4px;
                min-width: 100px;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #1e1e1e;
                color: white;
                selection-background-color: #4CAF50;
                min-width: 120px;
            }
        """)
        layout.addWidget(self.asset_combo)
    
    def _create_order_button(self, layout):
        """Create order button"""
        layout.addStretch()
        
        self.order_btn = QPushButton("Create Order")
        self.order_btn.setMaximumWidth(200)
        self.order_btn.setStyleSheet("""
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
        self.order_btn.clicked.connect(self.controller.show_order_dialog)
        layout.addWidget(self.order_btn)
    
    def get_selected_coin(self):
        """Get currently selected coin"""
        return self.asset_combo.currentText() if self.asset_combo else "BTCUSDT"
    
    def get_selected_timeframe(self):
        """Get currently selected timeframe"""
        return self.timeframe_combo.currentText() if self.timeframe_combo else "15m"
