import finplot as fplt
import pyqtgraph as pg
from src.view.chart_view import ChartView

class ChartController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.chart_view = ChartView(main_controller.views['main_window'])
    
    def add_plot(self, symbol, timeframe):
        """Add a plot to the screen"""
        main_window = self.main_controller.views['main_window']
        data_model = self.main_controller.models['data']
        binance_model = self.main_controller.models['binance']
        
        # Create chart container
        plot_container, container_layout = self.chart_view.create_chart_container()
        
        # Create plot axes
        ax, ax_secondary = self.chart_view.create_plot_axes(rows=2)
        
        main_window.axs.append(ax)
        main_window.axs.append(ax_secondary)
        
        data_model.axs_dict[symbol] = [ax, ax_secondary]
        
        # Add chart to container
        container_layout.addWidget(ax.ax_widget)
        
        # Add container to layout
        main_window.global_layout.addWidget(plot_container, 1, 0)
        
        # Start websocket and get historical data
        binance_model.start_kline_socket(
            symbol=symbol, 
            interval=timeframe, 
            callback=self.main_controller.ws_response
        )
        
        self.update_plot(symbol, timeframe)
    
    def update_plot(self, symbol, timeframe):
        """Update plot with historical data"""
        data_model = self.main_controller.models['data']
        binance_model = self.main_controller.models['binance']
        
        # Get historical data
        df = binance_model.get_historical_data(symbol, timeframe)
        
        # Get axes
        ax = data_model.axs_dict[symbol][0]
        
        # Add candlestick plot
        plot = self.chart_view.add_candlestick_plot(df, ax, symbol)
        data_model.plots[symbol + " price"] = plot
        
        # Save data
        data_model.symbol_data_dict[symbol] = df
        
        # Add price highlight
        price_line, text, rec_color = self.chart_view.add_price_highlight(df, ax)
        
        # Store references for later updates
        ax.price_line = price_line
        ax.text = text
        ax.rec_color = rec_color
    
    def change_plot_data(self, coin, timeframe):
        """Change plot data based on coin and timeframe"""
        data_model = self.main_controller.models['data']
        binance_model = self.main_controller.models['binance']
        
        if not binance_model.supported_symbols:
            return
        
        if coin not in binance_model.supported_symbols:
            print(f"Symbol {coin} is not supported")
            return
        
        # Update only if coin or timeframe changed
        if coin not in data_model.preferred or data_model.preferred.get(coin) != timeframe:
            # Clear old data
            if coin in data_model.axs_dict:
                ax_list = data_model.axs_dict[coin]
                # Remove axis widgets from layout
                for ax in ax_list:
                    if hasattr(ax, 'ax_widget'):
                        main_window = self.main_controller.views['main_window']
                        main_window.global_layout.removeWidget(ax.ax_widget)
                        ax.ax_widget.setParent(None)
                
                # Remove from lists
                for ax in ax_list:
                    if ax in main_window.axs:
                        main_window.axs.remove(ax)
                
                data_model.plots.pop(coin + " price", None)
            
            # Clear all previous data
            data_model.preferred.clear()
            data_model.symbol_data_dict.clear()
            data_model.axs_dict.clear()
            data_model.plots.clear()
            
            # Add new pair
            data_model.preferred[coin] = timeframe
            
            # Create new plot
            self.add_plot(coin, timeframe)
            
            fplt.refresh()
    
    def update_plots(self):
        """Update all plots"""
        data_model = self.main_controller.models['data']
        
        # If call is too early
        if not data_model.symbol_data_dict:
            return
        
        # Update all plots
        for key in list(data_model.plots.keys()):
            symbol = key.split()[0]
            df = data_model.symbol_data_dict.get(symbol)
            
            if df is None or df.empty:
                continue
            
            # Get correct ax
            axs = data_model.axs_dict.get(symbol)
            if not axs:
                continue
            
            ax = axs[0]
            
            if key.split()[1] == "price":
                # OCHL for some reason
                data_model.plots[key].update_data(df[["Open", "Close", "High", "Low"]])
            
            current_price = df["Close"].iloc[-1]
            old_price = df["Close"].iloc[-2]
            
            if current_price > old_price:
                rec_color = "#2e7871"
            elif current_price == old_price:
                rec_color = "#4a4e59"
            else:
                rec_color = "#e84752"
            
            # Update price line and text if they exist
            if hasattr(ax, 'price_line') and hasattr(ax, 'text'):
                # Color of line
                ax.price_line.setPen(pg.mkPen(rec_color, style=pg.QtCore.Qt.DashLine))
                
                # Position of line
                ax.price_line.setPos(current_price)
                
                # Position of text
                ax.text.setPos(len(df.index), current_price)
                
                countdown = data_model.countdown
                if "-" in countdown:
                    countdown = "0:00:00"
                
                ax.text.setHtml(
                    (
                        '<b style="color:white; background-color:'
                        + rec_color
                        + '";>'
                        + str(current_price)
                        + '</b> <body style="color:white; background-color:'
                        + rec_color
                        + '";>'
                        + countdown
                        + "</body>"
                    )
                )
