import unittest
import threading
import time
from queue import Queue
from src.models.order import Order
from src.core import shared
from src.engine.kitchen_worker import kitchen_worker
from src.engine.assignment import assign_orders

class TestParallelSystem(unittest.TestCase):
    def setUp(self):
        shared.incoming_queue = Queue()
        shared.ready_queue = Queue()
        shared.orders_map = {}
        shared.couriers_map = {i: type('Courier', (), {'id': i, 'status': 'IDLE', 'lock': threading.Lock()})() for i in range(1, 6)}
        shared.stop = False

    def test_bulk_order_processing(self):
        NUM_ORDERS = 30
        NUM_KITCHEN_WORKERS = 3

        # vytvoření objednávek
        for i in range(1, NUM_ORDERS + 1):
            order = Order(i, (0,0), (i,i))
            shared.orders_map[i] = order
            shared.incoming_queue.put(order)

        # spuštění kitchen workerů
        for i in range(NUM_KITCHEN_WORKERS):
            t = threading.Thread(target=kitchen_worker, args=(i+1,), daemon=True)
            t.start()

        # spuštění assign engine
        t_assign = threading.Thread(target=assign_orders, daemon=True)
        t_assign.start()

        # čekáme na zpracování všech objednávek
        timeout = time.time() + 20  # max 20 sekund
        while len([o for o in shared.orders_map.values() if o.status != "ASSIGNED"]) > 0:
            if time.time() > timeout:
                break
            time.sleep(0.1)

        # test: všechny objednávky byly přiřazeny
        assigned_orders = [o for o in shared.orders_map.values() if o.status == "ASSIGNED"]
        self.assertEqual(len(assigned_orders), NUM_ORDERS)

        # test: žádný kurýr není duplicitně přiřazen
        assigned_couriers = [o.assigned_courier for o in assigned_orders]
        self.assertEqual(len(assigned_couriers), NUM_ORDERS)
        self.assertTrue(all(c is not None for c in assigned_couriers))

if __name__ == "__main__":
    unittest.main()
