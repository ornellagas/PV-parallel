#Author: Ornella Kim Gasková

import queue
import threading

incoming_queue = queue.Queue()
ready_queue = queue.Queue()

orders_map = {}
orders_map_lock = threading.Lock()

couriers_map = {}
couriers_map_lock = threading.Lock()

print_lock = threading.Lock()

stop = False
MAX_ORDERS = 10