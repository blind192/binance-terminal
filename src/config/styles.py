import finplot as fplt

def apply_theme():
    """Apply TradingView style theme"""
    # TradingView style
    fplt.foreground = "#7a7c85"
    fplt.background = "#131722"
    # Candles
    fplt.candle_bull_color = "#2e7871"
    fplt.candle_bear_color = "#e84752"
    fplt.candle_bull_body_color = fplt.candle_bull_color
    # Cross hair
    fplt.cross_hair_color = "#5e6b78"
    # Volume
    fplt.volume_bull_color = "#265f5e"
    fplt.volume_bear_color = "#7d303a"
    fplt.volume_bull_body_color = fplt.volume_bull_color
