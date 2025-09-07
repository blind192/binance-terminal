class OrderModel:
    def __init__(self):
        self.active_orders = []
    
    def create_order(self, order_type, coin, timeframe, stop_loss, take_profit):
        """Create a new order"""
        order_data = {
            'type': order_type,
            'coin': coin,
            'timeframe': timeframe,
            'stop_loss': stop_loss,
            'take_profit': take_profit
        }
        self.active_orders.append(order_data)
        return order_data
    
    def close_order(self, order_data):
        """Close an order"""
        if order_data in self.active_orders:
            self.active_orders.remove(order_data)
            return True
        return False
    
    def has_active_orders(self):
        """Check if there are active orders"""
        return len(self.active_orders) > 0
