import pandas as pd
from datetime import datetime
from src.utils.constants import DEFAULT_PREFERRED_SYMBOLS

class DataModel:
    def __init__(self):
        self.plots = {}
        self.preferred = {}
        self.axs_dict = {}
        self.symbol_data_dict = {}
        self.countdown = ""
        self.selected_coins = []
        self.timeframes = []
    
    def initialize_preferred_symbols(self, nr_charts=4):
        """Initialize preferred symbols and timeframes"""
        self.preferred = {k: DEFAULT_PREFERRED_SYMBOLS[k] for k in list(DEFAULT_PREFERRED_SYMBOLS)[:nr_charts]}
    
    def process_websocket_data(self, info):
        """Process websocket response data"""
        try:
            sym = info["s"]
            tf = info["k"]["i"]

            # Skip response if symbol is not in preferred
            if sym not in self.preferred or tf != self.preferred[sym]:
                return False

            # Get or create dataframe for this symbol
            if sym not in self.symbol_data_dict:
                self.symbol_data_dict[sym] = pd.DataFrame()
            
            df = self.symbol_data_dict[sym]

            close = float(info["k"]["c"])
            high = float(info["k"]["h"])
            low = float(info["k"]["l"])
            volume = float(info["k"]["v"])

            # t is the timestamp in ms
            t = int(info["k"]["t"])

            # Use int(info['k']['T']) - current time to calculate time until next candle
            d1 = int(info["k"]["T"])
            converted_d1 = datetime.fromtimestamp(round(d1 / 1000))
            current_time = datetime.now()
            td = converted_d1 - current_time
            self.countdown = str(td).split(".")[0]

            # PROTECTED TIMESTAMP EXTRACTION
            if len(df) >= 2:
                t0 = int(df.index[-2].timestamp()) * 1000
                t1 = int(df.index[-1].timestamp()) * 1000
            elif len(df) == 1:
                t1 = int(df.index[-1].timestamp()) * 1000
                t0 = t1 - 60000  # minus 1 minute (60000 ms)
            else:
                current_time_ms = int(datetime.now().timestamp()) * 1000
                t1 = current_time_ms
                t0 = current_time_ms - 60000

            t2 = t1 + (t1 - t0)

            # Update line corresponding with symbol
            if t < t2:
                # update last candle
                i = df.index[-1]
                df.loc[i, "Close"] = close
                df.loc[i, "High"] = high
                df.loc[i, "Low"] = low
                df.loc[i, "Volume"] = volume
            else:
                # Add it all together, OCHLV
                data = [t] + [float(info["k"]["o"])] + [close] + [high] + [low] + [volume]
                candle = pd.DataFrame(
                    [data], columns="Time Open Close High Low Volume".split()
                ).astype({"Time": "datetime64[ms]"})
                candle.set_index("Time", inplace=True)

                # Add to dataframe
                df = pd.concat([df, candle])

            # Symbol_dict consists of all ohlcv data
            self.symbol_data_dict[sym] = df
            return True

        except Exception as e:
            print(f"Error processing websocket data: {e}")
            return False
