# Author: Ornella Kim Gasková

import time
import random
from core.shared import incoming_queue, ready_queue, stop, emit_event

# Reprezentuje kuchaře. Konzumuje objednávky z incoming_queue a produkuje hotová jídla do ready_queue
def kitchen_worker(worker_id):
    while not stop:
        try:
            # Čekání na objednávku (timeout zajistí, že thread může skončit při stop=True)
            order = incoming_queue.get(timeout=2)
        except Exception:
            continue

        # Změna stavu a oznámení dashboardu
        order.status = "PREPARING"
        emit_event("KITCHEN_BUSY", order.id, "PREPARING", f"Chef {worker_id} is cooking...")

        # Simulace reálné práce (každé jídlo trvá jinak dlouho)
        time.sleep(random.uniform(3, 6))

        order.status = "READY"
        ready_queue.put(order)
        emit_event("KITCHEN_DONE", order.id, "READY", f"Chef {worker_id} finished.")

        incoming_queue.task_done()