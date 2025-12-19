# Author: Ornella Kim Gasková

import uvicorn
import threading
from engine.api import app
from engine.kitchen_worker import kitchen_worker
from engine.assignment import assign_orders
from engine.init_couriers import init_couriers

def run_logic():
    # 1. Inicializace kurýrů
    init_couriers(5)

    # 2. Spuštění kuchařů (pro jistotu je nastartujeme přímo tady)
    print("Startuji kuchaře...")
    for i in range(1, 4):
        t = threading.Thread(target=kitchen_worker, args=(i,), daemon=True)
        t.start()

    # 3. Spuštění dispečera
    print("Startuji dispečink...")
    t_assign = threading.Thread(target=assign_orders, daemon=True)
    t_assign.start()

if __name__ == "__main__":
    # Nastartujeme logiku v samostatném vlákně, aby neblokovala API
    logic_thread = threading.Thread(target=run_logic, daemon=True)
    logic_thread.start()

    # Spustíme webový server
    print("Spouštím API na http://127.0.0.1:8000")
    uvicorn.run(app, host="127.0.0.1", port=8000)