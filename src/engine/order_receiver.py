#Author: Ornella Kim Gasková

import time
import random
from src.models.order import Order
from src.core.shared import orders_map, orders_map_lock, incoming_queue, print_lock, stop, MAX_ORDERS

def order_receiver():
    global stop
    order_id = 1
    while order_id <= MAX_ORDERS and not stop:
        order = Order(
            order_id,
            (random.randint(0, 10), random.randint(0, 10)),
            (random.randint(0, 10), random.randint(0, 10))
        )

        with orders_map_lock:
            orders_map[order_id] = order

        incoming_queue.put(order)

        with print_lock:
            print(f"[Order Receiver] New order {order_id}")

        order_id += 1
        time.sleep(random.uniform(1, 2))

    stop = True
    with print_lock:
        print("[Order Receiver] Max orders reached, stopping order receiver.")