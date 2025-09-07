from PyQt5.QtWidgets import QMessageBox
from src.view.order_dialog import OrderDialog

class OrderController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
    
    def show_order_dialog(self):
        """Show order creation dialog"""
        order_model = self.main_controller.models['order']
        
        # Check if there are active orders
        if order_model.has_active_orders():
            QMessageBox.warning(None, "Warning", "Please close your current order before creating a new one.")
            return
        
        dialog = OrderDialog()
        result = dialog.exec_()
        
        if result == OrderDialog.Accepted:
            order_data = dialog.get_order_data()
            self.create_order(order_data)
    
    def create_order(self, order_data):
        """Create a new order"""
        order_model = self.main_controller.models['order']
        control_panel = self.main_controller.views['control_panel']
        orders_panel = self.main_controller.views['orders_panel']
        
        coin = control_panel.get_selected_coin()
        timeframe = control_panel.get_selected_timeframe()
        
        # Create order in model
        order_data = order_model.create_order(
            order_data['type'],
            coin,
            timeframe,
            order_data['stop_loss'],
            order_data['take_profit']
        )
        
        # Create order widget in view
        order_widget = orders_panel.add_order_widget(
            order_data,
            self.close_order
        )
        
        # Store widget reference
        order_data['widget'] = order_widget
        
        print(f"Order created - Type: {order_data['type']}, SL: {order_data['stop_loss']}, TP: {order_data['take_profit']}")
    
    def close_order(self, order_widget, order_data):
        """Close an order"""
        order_model = self.main_controller.models['order']
        orders_panel = self.main_controller.views['orders_panel']
        
        # Remove from view
        orders_panel.remove_order_widget(order_widget)
        
        # Remove from model
        if order_model.close_order(order_data):
            print(f"Order closed - Type: {order_data['type']}, SL: {order_data['stop_loss']}, TP: {order_data['take_profit']}")
