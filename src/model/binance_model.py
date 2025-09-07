import pandas as pd
from binance.client import Client
from binance import ThreadedWebsocketManager

class BinanceModel:
    def __init__(self):
        self.client = Client()
        self.twm = ThreadedWebsocketManager()
        self.supported_symbols = self._get_supported_symbols()
    
    def _get_supported_symbols(self):
        """Get list of currently supported symbols"""
        return [d["symbol"] for d in self.client.get_exchange_info().get("symbols")]
    
    def start_kline_socket(self, symbol, interval, callback):
        """Start kline websocket for symbol"""
        self.twm.start_kline_socket(symbol=symbol, callback=callback, interval=interval)
    
    def get_historical_data(self, symbol, interval, limit=120):
        """Get historical kline data"""
        hist_candles = self.client.get_klines(symbol=symbol, interval=interval, limit=limit)
        df = pd.DataFrame(hist_candles)
        
        # Only the columns contain the OHLCV data
        df.drop(columns=[6, 7, 8, 9, 10, 11], axis=1, inplace=True)
        
        # OHLCV
        df = df.rename(
            columns={0: "Time", 1: "Open", 2: "High", 3: "Low", 4: "Close", 5: "Volume"}
        )
        
        # Convert time in ms to datetime
        df["Time"] = pd.to_datetime(df["Time"], unit='ms')
        
        # Convert other columns to float
        df = df.astype({
            "Open": float,
            "High": float,
            "Low": float,
            "Close": float,
            "Volume": float,
        })
        
        df.set_index("Time", inplace=True)
        return df
    
    def stop(self):
        """Stop all websockets"""
        self.twm.stop()
    
    def start(self):
        """Start websocket manager"""
        self.twm.start()
