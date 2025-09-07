import finplot as fplt
import pyqtgraph as pg
from PyQt5.QtWidgets import QVBoxLayout, QWidget
from PyQt5.QtCore import Qt

class ChartView:
    def __init__(self, main_window):
        self.main_window = main_window
        self.plots = {}
    
    def create_chart_container(self):
        """Create container for chart"""
        plot_container = QWidget()
        plot_container.setSizePolicy(pg.QtWidgets.QSizePolicy.Expanding, pg.QtWidgets.QSizePolicy.Expanding)
        
        # Create layout for container with center alignment
        container_layout = QVBoxLayout(plot_container)
        container_layout.setAlignment(Qt.AlignTop)
        container_layout.setContentsMargins(50, 10, 50, 50)
        
        return plot_container, container_layout
    
    def create_plot_axes(self, rows=2):
        """Create plot axes"""
        ax, ax_secondary = fplt.create_plot_widget(self.main_window, rows=rows, init_zoom_periods=100)
        ax.showGrid(True, True)
        return ax, ax_secondary
    
    def add_candlestick_plot(self, df, ax, symbol):
        """Add candlestick plot to axis"""
        plot = fplt.candlestick_ochl(df[["Open", "Close", "High", "Low"]], ax=ax)
        fplt.add_legend(symbol, ax=ax)
        return plot
    
    def add_price_highlight(self, df, ax):
        """Add price highlight elements"""
        current_price = df["Close"].iloc[-1]
        old_price = df["Close"].iloc[-2]
        
        # Define color of rectangle
        if current_price > old_price:
            rec_color = "#2e7871"
        elif current_price == old_price:
            rec_color = "#4a4e59"
        else:
            rec_color = "#e84752"

        # Add current price line
        price_line = pg.InfiniteLine(
            angle=0,
            movable=False,
            pen=fplt._makepen(fplt.candle_bull_body_color, style="--"),
        )
        price_line.setPos(current_price)
        ax.addItem(price_line, ignoreBounds=True)

        # Price text
        text = pg.TextItem(
            html=(
                '<b style="color:white; background-color:'
                + rec_color
                + '";>'
                + str(current_price)
                + "</b>"
            ),
            anchor=(0, 0.5),
        )
        text.setPos(len(df.index), current_price)
        ax.addItem(text, ignoreBounds=True)
        
        return price_line, text, rec_color
