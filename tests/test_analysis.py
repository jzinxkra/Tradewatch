import pytest
from collections import deque
from analysis.processor import compute_statistics

def test_compute_statistics_basic():
    trades = deque([
        {"price": 100.0, "quantity": 1.0, "timestamp": 1},
        {"price": 110.0, "quantity": 2.0, "timestamp": 2},
        {"price": 105.0, "quantity": 1.5, "timestamp": 3},
    ])
    stats = compute_statistics(trades)
    assert round(stats["price_change_pct"], 2) == 5.0
    assert round(stats["avg_price"], 2) == 105.0
    assert round(stats["total_volume"], 2) == 4.5
    assert stats["trade_count"] == 3

def test_compute_statistics_empty():
    stats = compute_statistics(deque())
    assert stats == {
        "price_change_pct": 0,
        "avg_price": 0,
        "total_volume": 0,
        "trade_count": 0
    }
