from config import SIGNAL_MAP, TIMEFRAME_WEIGHTS, FINAL_THRESHOLDS

def analyze_timeframe(df):
    score = 0
    score += 1 if df["ema20"].iloc[-1] > df["ema50"].iloc[-1] else -1

    rsi = df["rsi"].iloc[-1]
    if rsi > 55:
        score += 1
    elif rsi < 45:
        score -= 1

    score += 1 if df["macd"].iloc[-1] > df["macd_signal"].iloc[-1] else -1
    return score

def score_to_signal(score):
    if score >= 2:
        return "BUY", min(score / 3, 1)
    elif score <= -2:
        return "SELL", min(abs(score) / 3, 1)
    else:
        return "HOLD", 0.5

def final_decision(tf_signals):
    final_score = 0
    for tf, data in tf_signals.items():
        s = SIGNAL_MAP[data["signal"]]
        final_score += s * data["strength"] * TIMEFRAME_WEIGHTS[tf]

    if final_score >= FINAL_THRESHOLDS["BUY"]:
        return "BUY", round(final_score, 2)
    elif final_score <= FINAL_THRESHOLDS["SELL"]:
        return "SELL", round(final_score, 2)
    else:
        return "HOLD", round(final_score, 2)