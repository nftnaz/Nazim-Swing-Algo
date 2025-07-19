import yfinance as yf
ticker = "RELIANCE.NS"
stock = yf.Ticker(ticker)
df = stock.history(period="1y")
print(df)