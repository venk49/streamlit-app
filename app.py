import streamlit as st
from data_loader import load_data
from analysis_engine import analyze_timeframe, score_to_signal, final_decision
from position_advisor import position_recommendation

st.set_page_config(page_title="Swing Trading Analyzer", layout="wide")
st.title("📈 Multi-Timeframe Swing Trading Analyzer")

symbol = st.text_input("Stock Symbol", value="AAPL")
buy_price = st.number_input("Your Buy Price (Optional)", min_value=0.0, step=0.1)

if st.button("Analyze"):
    with st.spinner("Analyzing charts..."):
        timeframes = {
            "4H": ("4h", "60d"),
            "DAILY": ("1d", "1y"),
            "WEEKLY": ("1wk", "5y")
        }

        tf_signals = {}
        for tf, (interval, period) in timeframes.items():
            df = load_data(symbol, interval, period)
            score = analyze_timeframe(df)
            signal, strength = score_to_signal(score)
            tf_signals[tf] = {"signal": signal, "strength": strength}

        final_signal, confidence = final_decision(tf_signals)

    st.subheader("📊 Timeframe Signals")
    for tf, data in tf_signals.items():
        st.write(f"**{tf}:** {data['signal']} (Strength: {data['strength']})")

    st.subheader("✅ Model Recommendation")
    st.metric("Action", final_signal, delta=f"Confidence: {confidence}")

    if buy_price > 0:
        daily_df = load_data(symbol, "1d", "1y")
        pos = position_recommendation(
            daily_df["Close"].iloc[-1],
            buy_price,
            daily_df["ema20"].iloc[-1],
            daily_df["atr"].iloc[-1],
            final_signal
        )

        st.subheader("📌 Position-Based Guidance")
        st.metric("Adjusted Action", pos["recommendation"])
        col1, col2 = st.columns(2)
        col1.metric("Suggested Stop Loss", pos["stop_loss"])
        col2.metric("Suggested Target", pos["target"])
        st.info(f"🧠 Reason: {pos['reason']}")