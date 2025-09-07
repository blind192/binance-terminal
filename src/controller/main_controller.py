from PyQt5.QtCore import QTimer
from src.view.main_window import MainWindow
from src.view.control_panel import ControlPanel
from src.view.orders_panel import OrdersPanel
from src.model.binance_model import BinanceModel
from src.model.data_model import DataModel
from src.model.order_model import OrderModel
from src.controller.chart_controller import ChartController
from src.controller.order_controller import OrderController

class MainController:
    def __init__(self):
        self.models = {
            'binance': BinanceModel(),
            'data': DataModel(),
            'order': OrderModel()
        }
        
        self.views = {
            'main_window': MainWindow(self),
            'control_panel': ControlPanel(self),
            'orders_panel': OrdersPanel(self)
        }
        
        self.sub_controllers = {
            'chart': ChartController(self),
            'order': OrderController(self)
        }
        
        self.timer = QTimer()
        self.setup_connections()
    
    def setup_connections(self):
        """Setup timer connections"""
        self.timer.timeout.connect(self.update_plots)
        self.timer.start(5000)  # 5 seconds
    
    def show_window(self):
        """Show main window and initialize UI"""
        main_window = self.views['main_window']
        
        # Start binance sockets
        self.models['binance'].start()
        
        # Initialize data
        self.models['data'].initialize_preferred_symbols()
        
        # Create UI components
        control_panel = self.views['control_panel'].create_panel()
        orders_panel = self.views['orders_panel'].create_panel()
        
        # Add to layout
        main_window.global_layout.addWidget(control_panel, 0, 0)
        main_window.global_layout.addWidget(orders_panel, 2, 0)
        
        # Create initial chart
        first_coin = list(self.models['data'].preferred.keys())[0]
        first_tf = self.models['data'].preferred[first_coin]
        self.sub_controllers['chart'].add_plot(first_coin, first_tf)
        
        # Show window
        main_window.show()
    
    def on_window_close(self):
        """Handle window close event"""
        self.models['binance'].stop()
        self.timer.stop()
    
    def on_timeframe_changed(self):
        """Handle timeframe change"""
        coin = self.views['control_panel'].get_selected_coin()
        timeframe = self.views['control_panel'].get_selected_timeframe()
        self.sub_controllers['chart'].change_plot_data(coin, timeframe)
    
    def on_coin_changed(self):
        """Handle coin change"""
        coin = self.views['control_panel'].get_selected_coin()
        timeframe = self.views['control_panel'].get_selected_timeframe()
        self.sub_controllers['chart'].change_plot_data(coin, timeframe)
    
    def show_order_dialog(self):
        """Show order creation dialog"""
        self.sub_controllers['order'].show_order_dialog()
    
    def update_plots(self):
        """Update all plots"""
        self.sub_controllers['chart'].update_plots()
    
    def ws_response(self, info):
        """Websocket response handler"""
        if self.models['data'].process_websocket_data(info):
            # Data was processed successfully
            pass
