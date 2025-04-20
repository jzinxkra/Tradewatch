from fastapi import FastAPI, HTTPException
from ingest.binance_ws import get_trade_buffers
from analysis.processor import analyze_all_symbols, compute_statistics
import uvicorn

app = FastAPI(title="TradeWatch API")

@app.get("/summary")
def get_all_summaries():
    buffers = get_trade_buffers()
    summary = analyze_all_symbols(buffers)
    return summary

@app.get("/summary/{symbol}")
def get_summary_for_symbol(symbol: str):
    buffers = get_trade_buffers()
    symbol = symbol.lower()
    if symbol not in buffers:
        raise HTTPException(status_code=404, detail="Symbol not found or no data yet.")
    stats = compute_statistics(buffers[symbol])
    return {symbol: stats}

if __name__ == "__main__":
    uvicorn.run("api.main:app", host="0.0.0.0", port=8000, reload=True)
