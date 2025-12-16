import json
import asyncio
import pandas as pd
import websockets
from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware

from data_store import store
import analytics as qa

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BINANCE_WS = "wss://stream.binance.com:9443/stream"

# ---------------------------
# Binance WebSocket Listener
# ---------------------------
async def binance_listener(symbols):
    streams = "/".join([f"{s}@trade" for s in symbols])
    url = f"{BINANCE_WS}?streams={streams}"

    async with websockets.connect(url) as ws:
        while True:
            msg = await ws.recv()
            data = json.loads(msg)["data"]

            tick = {
                "timestamp": pd.to_datetime(data["T"], unit="ms"),
                "price": float(data["p"]),
                "qty": float(data["q"]),
            }

            store.add_tick(data["s"].lower(), tick)

# ---------------------------
# WebSocket → Frontend
# ---------------------------
@app.websocket("/ws")
async def websocket_endpoint(ws: WebSocket):
    await ws.accept()
    await ws.send_json({"status": "connected"})

    try:
        while True:
            await asyncio.sleep(1)

            payload = {}

            for symbol in store.ticks:
                df = pd.DataFrame(store.get_ticks(symbol))
                if df.empty:
                    continue

                df.set_index("timestamp", inplace=True)

                prices = df["price"]
                returns = qa.log_returns(prices)

                payload[symbol] = {
                    "last_price": prices.iloc[-1],
                    "volatility": returns.std() if not returns.empty else 0,
                }

            await ws.send_json(payload)

    except Exception:
        await ws.close()

# ---------------------------
# Start Binance Stream
# ---------------------------
@app.post("/start")
async def start_stream(symbols: list[str]):
    asyncio.create_task(binance_listener(symbols))
    return {"status": "stream started", "symbols": symbols}

# ---------------------------
# Analytics REST API
# ---------------------------
@app.get("/analytics/spread")
def spread_api(sym1: str, sym2: str, window: int = 50):
    df1 = pd.DataFrame(store.get_ticks(sym1))
    df2 = pd.DataFrame(store.get_ticks(sym2))

    if df1.empty or df2.empty:
        return {"error": "not enough data"}

    df1.set_index("timestamp", inplace=True)
    df2.set_index("timestamp", inplace=True)

    merged = df1.join(df2, lsuffix="_1", rsuffix="_2", how="inner")

    hedge = qa.hedge_ratio(merged["price_1"], merged["price_2"])
    spread = qa.spread(merged["price_1"], merged["price_2"], hedge)
    z = qa.zscore(spread, window)

    return {
        "hedge_ratio": hedge,
        "spread": spread.dropna().tolist(),
        "zscore": z.dropna().tolist()
    }

@app.get("/analytics/adf")
def adf_api(symbol: str):
    df = pd.DataFrame(store.get_ticks(symbol))
    df.set_index("timestamp", inplace=True)
    return qa.adf_test(df["price"])
