import asyncio
import websockets
import json
from collections import defaultdict, deque

COINS = ['btcusdt', 'ethusdt', 'bnbusdt', 'solusdt', 'xrpusdt', 'lrcusdt']
STREAM_URL = "wss://stream.binance.com:9443/stream?streams=" + "/".join(f"{coin}@trade" for coin in COINS)
TRADE_BUFFERS = defaultdict(lambda: deque(maxlen=1000))

def get_trade_buffers():
    return TRADE_BUFFERS

async def handle_trade_message(msg):
    stream = msg.get("stream")
    data = msg.get("data")
    if not stream or not data:
        return

    symbol = data.get("s", "").lower()
    price = float(data.get("p", 0))
    quantity = float(data.get("q", 0))
    trade_time = data.get("T")

    trade = {
        "price": price,
        "quantity": quantity,
        "timestamp": trade_time
    }

    TRADE_BUFFERS[symbol].append(trade)
    print(f"[{symbol}] Price: {price}, Qty: {quantity}")

async def binance_ws_listener():
    async with websockets.connect(STREAM_URL) as ws:
        print("Connected to Binance WebSocket")
        async for message in ws:
            msg = json.loads(message)
            await handle_trade_message(msg)

if __name__ == "__main__":
    try:
        asyncio.run(binance_ws_listener())
    except KeyboardInterrupt:
        print("Interrupted by user")
