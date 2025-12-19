# Author: Ornella Kim Gasková

from core.shared import couriers_map, couriers_map_lock
from models.courier import Courier

def init_couriers(count: int):
    # Vytvoří počáteční sadu kurýrů v systému
    with couriers_map_lock:
        for i in range(1, count + 1):
            courier = Courier(i, f"Courier-{i}", "IDLE")
            couriers_map[i] = courier
    print(f"Inicializováno {count} kurýrů pro rozvoz.")