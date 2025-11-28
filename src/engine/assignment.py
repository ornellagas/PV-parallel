#Author: Ornella Kim Gasková

import time
from src.core.shared import ready_queue, couriers_map, couriers_map_lock, print_lock, stop

def assign_orders():
    while not stop or not ready_queue.empty():
        try:
            order = ready_queue.get(timeout=1)
        except Exception:
            continue

        assigned = False
        with couriers_map_lock:
            for courier in couriers_map.values():
                if courier.status == "IDLE":
                    courier.status = "DELIVERING"
                    order.status = "ASSIGNED"
                    order.assigned_courier = courier.id
                    assigned = True
                    with print_lock:
                        print(f"[Assignment] Order {order.id} assigned to Courier {courier.id}")
                    break

        if not assigned:
            ready_queue.put(order)
            time.sleep(1)
        else:
            # simulace doručení
            time.sleep(2)  # doba doručení
            order.status = "DELIVERED"
            with couriers_map_lock:
                courier.status = "IDLE"
            with print_lock:
                print(f"[Assignment] Order {order.id} delivered by Courier {courier.id}")

        ready_queue.task_done()

    with print_lock:
        print("[Assignment] Exiting, no more orders.")