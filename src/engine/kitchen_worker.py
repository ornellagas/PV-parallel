import time
import random
from src.core.shared import incoming_queue, ready_queue, print_lock, stop

def kitchen_worker(worker_id):
    while not stop or not incoming_queue.empty():
        try:
            order = incoming_queue.get(timeout=1)
        except Exception:
            continue

        order.status = "PREPARING"
        with print_lock:
            print(f"[Kitchen Worker {worker_id}] Preparing order {order.id}")

        time.sleep(random.uniform(1, 2))  # simulace vaření

        order.status = "READY"
        ready_queue.put(order)
        with print_lock:
            print(f"[Kitchen Worker {worker_id}] Order {order.id} ready")

        incoming_queue.task_done()

    with print_lock:
        print(f"[Kitchen Worker {worker_id}] Exiting, no more orders.")