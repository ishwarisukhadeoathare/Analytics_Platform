# Quant Analytics Dashboard - Binance Real-time

## Overview

The **Quant Analytics Dashboard** is a real-time financial data visualization and analytics web application built to monitor Binance Futures trading data. It provides traders, analysts, and enthusiasts with instant insights into price movements, trading volumes, spreads, correlations, and Z-scores of selected trading pairs. This dashboard is designed for educational purposes and not as financial advice.

The project consists of a **frontend** built with HTML, CSS, and JavaScript (Plotly.js for charts) and a **backend** in Python for data processing and analytics.

---

## Features

1. **Real-time WebSocket Integration**
   - Connects to Binance Futures WebSocket API.
   - Streams live trading data for multiple symbols.
   - Displays connection status with visual indicators.

2. **Control Panel**
   - Configure trading symbols (e.g., BTCUSDT, ETHUSDT, SOLUSDT).
   - Select resampling timeframe (1s, 5s, 30s, 1m, 5m, 15m).
   - Set rolling window size for analytics (20, 50, 100, 200 periods).
   - Choose analytics type: 
     - Price & Volume  
     - Spread & Z-Score  
     - Correlation Matrix  
     - Hedge Ratio (OLS)
   - Start/Stop streaming data.
   - Run Augmented Dickey-Fuller (ADF) stationarity tests.
   - Export or clear data.

3. **Stats Dashboard**
   - Displays key metrics in real-time:
     - Total Ticks
     - Average Spread
     - Current Z-Score
     - BTC/ETH Correlation
     - Total Volume
     - Active Alerts

4. **Interactive Charts**
   - **Price Chart:** Live price movement for selected symbols.
   - **Spread & Z-Score Chart:** Track spread and standardized deviations.
   - **Correlation Matrix:** Shows interrelationships between selected symbols.
   - Toggle chart types, thresholds, and refresh correlation dynamically.

5. **Alerts & Notifications**
   - Configurable Z-score and price change alerts.
   - Alerts displayed with timestamps and severity indicators (info, critical).
   - Ability to remove individual alerts.

6. **Data Table**
   - Displays latest tick data including timestamp, symbol, price, size, volume, % change, spread, and Z-score.
   - Search symbols and refresh table dynamically.

7. **Backend Analytics**
   - Python scripts for advanced statistical calculations:
     - OHLC resampling (`resample_ohlc`)
     - Log returns (`log_returns`)
     - Rolling volatility (`rolling_volatility`)
     - Hedge ratio calculation (`hedge_ratio`)
     - Spread and Z-score computation (`spread`, `zscore`)
     - Rolling correlation (`rolling_corr`)
     - Augmented Dickey-Fuller test (`adf_test`)

---

## Project Structure

