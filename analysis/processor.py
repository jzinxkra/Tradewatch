from collections import deque
from typing import Dict

def compute_statistics(trades: deque) -> Dict:
    if not trades:
        return {
            "price_change_pct": 0,
            "avg_price": 0,
            "total_volume": 0,
            "trade_count": 0
        }

    prices = [trade["price"] for trade in trades]
    quantities = [trade["quantity"] for trade in trades]

    first_price = prices[0]
    last_price = prices[-1]
    price_change_pct = ((last_price - first_price) / first_price) * 100 if first_price > 0 else 0

    total_volume = sum(quantities)
    avg_price = sum(prices) / len(prices)

    return {
        "price_change_pct": round(price_change_pct, 2),
        "avg_price": round(avg_price, 4),
        "total_volume": round(total_volume, 4),
        "trade_count": len(trades)
    }

def analyze_all_symbols(buffers: Dict[str, deque]) -> Dict[str, Dict]:
    summary = {}
    for symbol, trades in buffers.items():
        stats = compute_statistics(trades)
        summary[symbol] = stats
    return summary
