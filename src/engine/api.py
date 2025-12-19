# Author: Ornella Kim Gasková

import threading
from contextlib import asynccontextmanager
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

# Importy upraveny tak, aby fungovaly z 'src' jako kořenové složky
from core.shared import incoming_queue, orders_map, orders_map_lock, ws_manager, emit_event
from models.order import Order

# Importujeme workery pro automatický start (pokud je chceš spouštět z API)
from engine.kitchen_worker import kitchen_worker
from engine.assignment import assign_orders
from engine.init_couriers import init_couriers

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Tato část zajistí, že se paralelní procesy spustí spolu s API
    # Inicializace kurýrů
    init_couriers(5)
    # Spuštění kuchařů
    for i in range(1, 4):
        threading.Thread(target=kitchen_worker, args=(i,), daemon=True).start()
    # Spuštění dispečera
    threading.Thread(target=assign_orders, daemon=True).start()

    print("Logistický engine byl nastartován v paralelních vláknech.")
    yield
    print("Systém se vypíná.")

# Vytvoření aplikace s lifespanem
app = FastAPI(title="Real-time Logistics System", lifespan=lifespan)

class OrderRequest(BaseModel):
    items: list[str]
    address: str

@app.post("/orders")
async def create_order(data: OrderRequest):
    # Přijme reálnou objednávku a vloží ji do systému
    with orders_map_lock:
        new_id = len(orders_map) + 1
        order = Order(new_id, "Main Kitchen", data.address)

        # Dynamické přidání položky do objektu
        order.items = data.items
        orders_map[new_id] = order

    incoming_queue.put(order)
    # Oznámení dispečinku
    emit_event("ORDER_CREATED", new_id, "NEW", f"Items: {', '.join(data.items)}")
    return {"status": "received", "order_id": new_id}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Endpoint pro real-time komunikaci s dashboardem
    await ws_manager.connect(websocket)
    try:
        while True:
            # Čekání na zprávu (udržuje spojení)
            await websocket.receive_text()
    except WebSocketDisconnect:
        ws_manager.disconnect(websocket)


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    # HTML Dashboard s připojením k WebSocketu
    return """
    <html>
        <head>
            <title>Logistics Dashboard</title>
            <style>
                body { font-family: 'Segoe UI', sans-serif; background: #121212; color: white; padding: 20px; }
                .grid { display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }
                .card { background: #1e1e1e; padding: 20px; border-radius: 12px; border: 1px solid #333; }
                #log { height: 500px; overflow-y: auto; background: #000; padding: 15px; border-radius: 8px; font-family: 'Consolas', monospace; font-size: 14px; }
                .msg { margin-bottom: 10px; padding: 8px; border-left: 4px solid #444; background: #252525; }
                .status-NEW { border-left-color: #3498db; color: #3498db; }
                .status-PREPARING { border-left-color: #e67e22; color: #e67e22; }
                .status-READY { border-left-color: #f1c40f; color: #f1c40f; }
                .status-ASSIGNED { border-left-color: #9b59b6; color: #9b59b6; }
                .status-DELIVERED { border-left-color: #2ecc71; color: #2ecc71; }
                h1 { color: #2ecc71; }
            </style>
        </head>
        <body>
            <h1>Real-time Dispatch Control</h1>
            <div class="grid">
                <div class="card">
                    <h2>Live Activity Feed</h2>
                    <div id="log"></div>
                </div>
                <div class="card">
                    <h2>System Overview</h2>
                    <p>Orders processed: <strong id="total">0</strong></p>
                    <p>Connection: <span id="status" style="color: gray;">Connecting...</span></p>
                    <hr style="border:0; border-top: 1px solid #333">
                    <p><small>Waiting for incoming POST requests to /orders...</small></p>
                </div>
            </div>
            <script>
                // Automatická detekce adresy (localhost vs 127.0.0.1)
                const wsUrl = `ws://${window.location.host}/ws`;
                console.log("Connecting to:", wsUrl);

                const ws = new WebSocket(wsUrl);
                const statusLabel = document.getElementById('status');
                let total = 0;

                ws.onopen = () => {
                    statusLabel.innerText = "● Online";
                    statusLabel.style.color = "#2ecc71";
                    console.log("✅ WebSocket Connected");
                };

                ws.onclose = () => {
                    statusLabel.innerText = "○ Offline";
                    statusLabel.style.color = "red";
                };

                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    const log = document.getElementById('log');
                    const line = document.createElement('div');
                    line.className = `msg status-${data.status}`;
                    line.innerHTML = `<strong>[${data.type}]</strong> Order #${data.id}: ${data.status} <br> 
                                      <small style="color: #888;">${data.detail}</small>`;
                    log.prepend(line);

                    if(data.type === 'ORDER_CREATED') {
                        total++;
                        document.getElementById('total').innerText = total;
                    }
                };
            </script>
        </body>
    </html>
    """