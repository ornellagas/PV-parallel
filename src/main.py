#Author: Ornella Kim Gasková

import threading
import time
from core.shared import orders_map, orders_map_lock
from engine.order_receiver import order_receiver
from engine.kitchen_worker import kitchen_worker
from engine.assignment import assign_orders
from engine.monitor import monitor_thread
from engine.init_couriers import init_couriers


def main():
    NUM_KITCHEN_WORKERS = 3
    NUM_COURIERS = 5
    MAX_ORDERS = 10

    init_couriers(NUM_COURIERS)

    # start vláken
    threads = []

    # kitchen workers
    for i in range(NUM_KITCHEN_WORKERS):
        t = threading.Thread(target=kitchen_worker, args=(i+1,))
        t.start()
        threads.append(t)

    # assignment engine
    t_assign = threading.Thread(target=assign_orders)
    t_assign.start()
    threads.append(t_assign)

    # order receiver
    t_receiver = threading.Thread(target=order_receiver)
    t_receiver.start()
    threads.append(t_receiver)

    # monitor
    t_monitor = threading.Thread(target=monitor_thread)
    t_monitor.start()
    threads.append(t_monitor)

    for t in threads:
        t.join()

    global stop
    while True:
        with orders_map_lock:
            total_orders = len(orders_map)
            delivered_orders = sum(1 for o in orders_map.values() if o.status == "DELIVERED")
        if total_orders >= MAX_ORDERS and delivered_orders == MAX_ORDERS:
            break
        time.sleep(1)

        # počkáme na ukončení všech vláken
    for t in threads:
        t.join()

    print("System finished all orders.")

if __name__ == "__main__":
    main()