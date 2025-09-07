# Binance Terminal - Paper Trading Platform

![Python](https://img.shields.io/badge/Python-3.9.13-blue.svg)
![PyQt5](https://img.shields.io/badge/GUI-PyQt5-green.svg)
![Binance](https://img.shields.io/badge/Exchange-Binance-orange.svg)
![MVC](https://img.shields.io/badge/Architecture-MVC-purple.svg)

A professional paper trading terminal with Binance integration, built with Python and PyQt5, featuring real-time market data, technical charts, and simulated trading capabilities.

> 🚀 **Project developed with assistance from DeepSeek AI**

## 📸 Interface Overview

### Main Trading Interface
![Main Interface](https://raw.githubusercontent.com/blind192/binance-terminal/main/assets/images/main-interface.png)

*Real-time candlestick charts with trading controls and market data*

### Order Creation Dialog  
![Order Dialog](https://raw.githubusercontent.com/blind192/binance-terminal/main/assets/images/order-dialog.png)

*Order creation window with stop-loss and take-profit settings*

## ✨ Features

### 📊 Real-time Market Data
- Live candlestick charts with multiple timeframes (1m to 1M)
- Real-time price updates via Binance WebSocket API
- Volume indicators and price highlights
- TradingView-style dark theme

### 🎯 Paper Trading
- Simulated BUY/SELL orders with stop-loss and take-profit
- Virtual balance management ($15,000 starting capital)
- Active orders panel with one-click closing
- Risk-free trading practice environment

### 📈 Technical Analysis
- Multiple chart support
- Customizable timeframes and symbols
- Price countdown to next candle
- Professional TradingView-inspired styling

### 🏗️ Architecture
- **MVC Pattern** - Clean separation of concerns
- **Modular Design** - Easy maintenance and extensibility
- **Real-time Updates** - WebSocket-based data streaming
- **Responsive UI** - Professional desktop application

## 🛠️ Installation

### Prerequisites
- Python 3.9.13
- pip (Python package manager)

### Quick Start
```bash
# Install dependencies
pip install -r requirements.txt

# Launch the application
python main.py
```

## 🎮 Usage

### Getting Started
1. **Launch the application**: Run `python main.py`
2. **Select a symbol**: Choose from popular cryptocurrencies  
3. **Choose timeframe**: Select from 1m to 1M intervals
4. **Monitor markets**: Watch real-time price movements

### Placing Orders
1. Click **"Create Order"** button
2. Select order type (BUY/SELL)
3. Set stop-loss and take-profit levels
4. Confirm to place simulated order

## ⚠️ Important Notes

### Paper Trading Only
- This is a **simulation platform** only
- No real funds are involved
- Perfect for learning and strategy testing

### Binance API
- Uses public Binance API endpoints
- No API key required for market data
- Read-only access to market information

---

**Disclaimer**: This is a paper trading simulation. Never trade with real money without proper understanding of risks.
