import yfinance as yf
import pandas as pd
import numpy as np

class TechnicalIndicators:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = self.fetch_data()

    def fetch_data(self, period="1y"):
        stock = yf.Ticker(self.ticker)
        df = stock.history(period=period)
        if df.empty:
            raise ValueError(f"No data found for {self.ticker}")
        return df

    def calculate_sma(self, window=20):
        return self.data['Close'].rolling(window=window).mean()

    def calculate_rsi(self, periods=14):
        delta = self.data['Close'].diff()
        gain = delta.where(delta > 0, 0).rolling(window=periods).mean()
        loss = -delta.where(delta < 0, 0).rolling(window=periods).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    def calculate_macd(self, slow=26, fast=12, signal=9):
        ema_fast = self.data['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = self.data['Close'].ewm(span=slow, adjust=False).mean()
        macd = ema_fast - ema_slow
        signal_line = macd.ewm(span=signal, adjust=False).mean()
        return macd, signal_line

    def calculate_bollinger_bands(self, window=20, num_std=2):
        sma = self.calculate_sma(window)
        rolling_std = self.data['Close'].rolling(window=window).std()
        upper_band = sma + (rolling_std * num_std)
        lower_band = sma - (rolling_std * num_std)
        return upper_band, lower_band

    def get_fundamental_data(self):
        stock = yf.Ticker(self.ticker)
        info = stock.info
        return {
            'pe_ratio': info.get('trailingPE', 'N/A'),
            'eps': info.get('trailingEps', 'N/A'),
            'revenue_growth': info.get('revenueGrowth', 'N/A') * 100 if info.get('revenueGrowth') else 'N/A',
            'debt_equity': info.get('debtToEquity', 'N/A')
        }

    def generate_recommendation(self):
        latest = self.data.iloc[-1]
        rsi = self.calculate_rsi().iloc[-1]
        macd, signal = self.calculate_macd()
        macd_val, signal_val = macd.iloc[-1], signal.iloc[-1]
        fundamental = self.get_fundamental_data()
        pe_ratio = fundamental['pe_ratio']

        score = 0
        if rsi < 30:
            score += 1  # Oversold
        elif rsi > 70:
            score -= 1  # Overbought
        if macd_val > signal_val:
            score += 1  # Bullish
        elif macd_val < signal_val:
            score -= 1  # Bearish
        if pe_ratio != 'N/A' and pe_ratio < 15:
            score += 1  # Undervalued
        elif pe_ratio != 'N/A' and pe_ratio > 25:
            score -= 1  # Overvalued

        if score > 0:
            return {'action': 'Buy', 'reason': 'Favorable technical and fundamental indicators'}
        elif score < 0:
            return {'action': 'Sell', 'reason': 'Unfavorable technical and fundamental indicators'}
        else:
            return {'action': 'Hold', 'reason': 'Neutral indicators'}