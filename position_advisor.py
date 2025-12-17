def position_recommendation(
    current_price,
    buy_price,
    daily_ema20,
    daily_atr,
    final_signal
):
    # --- FORCE SCALARS ---
    current_price = float(current_price)
    daily_ema20 = float(daily_ema20)
    daily_atr = float(daily_atr)

    recommendation = final_signal
    reason = "Trend aligned with model"

    stop_loss = buy_price - (2 * daily_atr)
    target = buy_price + (3 * daily_atr)

    if (current_price < stop_loss) or (current_price < daily_ema20):
        recommendation = "SELL"
        reason = "Stop-loss hit or daily trend broken"

    elif current_price >= target:
        recommendation = "HOLD"
        reason = "Target achieved — book partial profits"

    elif (current_price - buy_price) / buy_price > 0.08:
        recommendation = "HOLD"
        reason = "Price extended from buy zone"

    return {
        "recommendation": recommendation,
        "stop_loss": round(stop_loss, 2),
        "target": round(target, 2),
        "reason": reason
    }
