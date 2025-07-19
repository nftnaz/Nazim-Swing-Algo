import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from TechnicalIndicator import TechnicalIndicators

st.set_page_config(page_title="Stock Analysis Bot (Indian Market)", layout="wide")

st.title("Stock Analysis Bot (Indian Market)")
st.write("Analyze Indian stocks with fundamental and technical insights")

# Input for stock ticker
ticker = st.text_input("Enter NSE Stock Ticker (e.g., RELIANCE.NS)", value="RELIANCE.NS").upper()

if st.button("Analyze"):
    try:
        # Initialize technical indicators
        ti = TechnicalIndicators(ticker)
        df = ti.data

        # Fundamental Analysis
        st.header("Fundamental Analysis")
        fundamental_data = ti.get_fundamental_data()
        fundamental_df = pd.DataFrame({
            'Metric': ['P/E Ratio', 'EPS', 'Revenue Growth (%)', 'Debt/Equity'],
            'Value': [
                fundamental_data['pe_ratio'],
                fundamental_data['eps'],
                fundamental_data['revenue_growth'],
                fundamental_data['debt_equity']
            ]
        })
        st.table(fundamental_df)

        # Technical Analysis
        st.header("Technical Analysis")
        sma = ti.calculate_sma()
        rsi = ti.calculate_rsi()
        macd, signal = ti.calculate_macd()
        upper_band, lower_band = ti.calculate_bollinger_bands()

        technical_df = pd.DataFrame({
            'Metric': ['SMA (20)', 'RSI', 'MACD', 'Signal Line'],
            'Value': [
                round(sma.iloc[-1], 2) if not pd.isna(sma.iloc[-1]) else 'N/A',
                round(rsi.iloc[-1], 2) if not pd.isna(rsi.iloc[-1]) else 'N/A',
                round(macd.iloc[-1], 2) if not pd.isna(macd.iloc[-1]) else 'N/A',
                round(signal.iloc[-1], 2) if not pd.isna(signal.iloc[-1]) else 'N/A'
            ]
        })
        st.table(technical_df)

        # Recommendation
        st.header("Recommendation")
        recommendation = ti.generate_recommendation()
        st.write(f"**Action**: {recommendation['action']}")
        st.write(f"**Reason**: {recommendation['reason']}")

        # Price Chart
        st.header("Price Chart")
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close Price', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=df.index, y=sma, name='SMA (20)', line=dict(color='green')))
        fig.add_trace(go.Scatter(x=df.index, y=upper_band, name='Upper Bollinger Band', line=dict(color='red', dash='dash')))
        fig.add_trace(go.Scatter(x=df.index, y=lower_band, name='Lower Bollinger Band', line=dict(color='red', dash='dash')))
        fig.update_layout(
            title=f"{ticker} Price and Indicators",
            xaxis_title="Date",
            yaxis_title="Price (INR)",
            template="plotly_dark"
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Sidebar for additional info
st.sidebar.header("About")
st.sidebar.write("This bot analyzes Indian stocks using fundamental and technical indicators, providing buy/sell/hold recommendations.")
st.sidebar.write("Data Source: Yahoo Finance (yfinance)")
st.sidebar.write("Built with Streamlit and Python")