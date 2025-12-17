import yfinance as yf
from indicators import ema, rsi, macd, atr

def load_data(symbol, interval, period):
    df = yf.download(symbol, interval=interval, period=period)
    df.columns = [c[0] if isinstance(c, tuple) else c for c in df.columns]
    df.dropna(inplace=True)

    df["ema20"] = ema(df["Close"], 20)
    df["ema50"] = ema(df["Close"], 50)
    df["rsi"] = rsi(df["Close"])
    df["macd"], df["macd_signal"] = macd(df["Close"])
    df["atr"] = atr(df)

    return df