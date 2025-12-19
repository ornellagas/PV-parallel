# Author: Ornella Kim Gasková

import queue
import threading
import asyncio

# SDÍLENÉ ZDROJE (Producer-Consumer Pattern) ---
# incoming_queue: Objednávky čekající na kuchaře
incoming_queue = queue.Queue()
# ready_queue: Hotová jídla čekající na kurýra
ready_queue = queue.Queue()

# Sdílené mapy pro sledování stavu v reálném čase
orders_map = {}
orders_map_lock = threading.Lock()  # Ošetření Race Condition u objednávek

couriers_map = {}
couriers_map_lock = threading.Lock()  # Ošetření Race Condition u kurýrů

# Globální signál pro ukončení všech vláken
stop = False


# --- WEBSOCKET MANAGER ---
class ConnectionManager:
    # Spravuje aktivní WebSocket spojení pro real-time dashboard

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Odešle JSON zprávu všem připojeným klientům (dashboardům)
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                # Automatický úklid neaktivních spojení
                if connection in self.active_connections:
                    self.active_connections.remove(connection)


ws_manager = ConnectionManager()


# --- BRIDGE: SYNCHRONNÍ VLÁKNA -> ASYNCHRONNÍ WEBSOCKET ---
def emit_event(event_type: str, order_id: int, status: str, detail: str = ""):

   #  Bezpečně předá událost z paralelního vlákna (Thread) do
   #  asynchronní smyčky (FastAPI/Uvicorn), která obsluhuje WebSockety.
    message = {
        "type": event_type,
        "id": order_id,
        "status": status,
        "detail": detail
    }

    try:
        # Pokusíme se získat běžící smyčku (tu, ve které běží FastAPI)
        loop = asyncio.get_event_loop()

        if loop.is_running():
            # Most: Naplánujeme odeslání zprávy do hlavní asynchronní smyčky
            asyncio.run_coroutine_threadsafe(ws_manager.broadcast(message), loop)
        else:
            # Pokud smyčka není spuštěná, zkusíme ji pro tento výpis spustit
            loop.run_until_complete(ws_manager.broadcast(message))

    except RuntimeError:
        # Toto nastane, pokud vlákno (např. KitchenWorker) nemá přiřazenou smyčku.
        # Vytvoříme dočasnou smyčku pro odeslání zprávy.
        try:
            new_loop = asyncio.new_event_loop()
            asyncio.set_event_loop(new_loop)
            new_loop.run_until_complete(ws_manager.broadcast(message))
            new_loop.close()
        except Exception as e:
            print(f"Kritická chyba při odesílání události: {e}")