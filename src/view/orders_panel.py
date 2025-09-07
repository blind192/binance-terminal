from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QScrollArea, QHBoxLayout, QPushButton
)
from PyQt5.QtCore import Qt

class OrdersPanel:
    def __init__(self, controller):
        self.controller = controller
        self.panel = None
        self.orders_container = None
        self.orders_container_layout = None
    
    def create_panel(self):
        """Create active orders panel"""
        orders_panel = QWidget()
        orders_panel.setMaximumHeight(200)
        
        orders_layout = QVBoxLayout(orders_panel)
        orders_layout.setAlignment(Qt.AlignTop)
        
        # Header
        orders_label = QLabel("Active Orders")
        orders_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 18px;
                font-weight: bold;
                padding: 10px;
                background-color: #1e1e1e;
                border-radius: 6px;
            }
        """)
        orders_label.setAlignment(Qt.AlignCenter)
        orders_layout.addWidget(orders_label)
        
        # Orders container
        orders_container = QWidget()
        self.orders_container_layout = QVBoxLayout(orders_container)
        self.orders_container_layout.setAlignment(Qt.AlignTop)
        
        # Scroll area for orders
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(orders_container)
        scroll_area.setStyleSheet("""
            QScrollArea {
                background-color: #1e1e1e;
                border: 1px solid #555;
                border-radius: 6px;
            }
            QScrollArea > QWidget > QWidget {
                background-color: #1e1e1e;
            }
        """)
        
        orders_layout.addWidget(scroll_area)
        
        self.panel = orders_panel
        self.orders_container = orders_container
        return orders_panel
    
    def add_order_widget(self, order_data, close_callback):
        """Add order widget to panel"""
        order_widget = QWidget()
        order_layout = QHBoxLayout(order_widget)
        order_layout.setContentsMargins(10, 8, 10, 8)
        
        # Order info
        coin = order_data['coin']
        order_type = order_data['type']
        stop_loss = order_data['stop_loss']
        take_profit = order_data['take_profit']
        
        # Color based on order type
        type_color = "#4CAF50" if order_type == "BUY" else "#f44336"
        
        order_info = QLabel(f"{order_type} {coin} | SL: {stop_loss:.4f} | TP: {take_profit:.4f}")
        order_info.setStyleSheet(f"""
            QLabel {{
                color: {type_color};
                font-size: 18px;
                padding: 8px;
                font-weight: bold;
            }}
        """)
        
        # Close button
        close_btn = QPushButton("✕")
        close_btn.setMaximumWidth(40)
        close_btn.setMaximumHeight(30)
        close_btn.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                border: none;
                padding: 8px;
                border-radius: 4px;
                font-weight: bold;
                font-size: 16px;
            }
            QPushButton:hover {
                background-color: #d32f2f;
            }
            QPushButton:pressed {
                background-color: #b71c1c;
            }
        """)
        close_btn.clicked.connect(lambda: close_callback(order_widget, order_data))
        
        order_layout.addWidget(order_info)
        order_layout.addStretch()
        order_layout.addWidget(close_btn)
        
        # Add order to container
        self.orders_container_layout.addWidget(order_widget)
        
        return order_widget
    
    def remove_order_widget(self, order_widget):
        """Remove order widget from panel"""
        self.orders_container_layout.removeWidget(order_widget)
        order_widget.deleteLater()
