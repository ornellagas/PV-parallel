import time
from src.core.shared import orders_map, orders_map_lock, print_lock, stop

def monitor_thread():
    while True:
        with orders_map_lock, print_lock:
            total_orders = len(orders_map)
            completed_orders = sum(1 for o in orders_map.values() if o.status in ("ASSIGNED", "DELIVERED"))

            incoming = sum(1 for o in orders_map.values() if o.status == "NEW")
            preparing = sum(1 for o in orders_map.values() if o.status == "PREPARING")
            ready = sum(1 for o in orders_map.values() if o.status == "READY")
            assigned = sum(1 for o in orders_map.values() if o.status == "ASSIGNED")
            delivered_orders = sum(1 for o in orders_map.values() if o.status == "DELIVERED")

            print(f"[Monitor] New: {incoming}, Preparing: {preparing}, Ready: {ready}, "
                  f"Assigned: {assigned}, Completed: {completed_orders}/{total_orders}")

        if stop and total_orders > 0 and delivered_orders == total_orders:
            with print_lock:
                print("[Monitor] All orders processed, stopping monitor.")
            break

        time.sleep(1)