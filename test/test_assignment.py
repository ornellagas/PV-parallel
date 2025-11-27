import unittest
import threading
from src.models.order import Order
from src.core import shared
from src.engine.assignment import assign_orders

class TestAssignmentEngine(unittest.TestCase):
    def setUp(self):
        shared.ready_queue = shared.ready_queue or []
        shared.couriers_map = {i: type('Courier', (), {'id': i, 'status': 'IDLE', 'lock': threading.Lock()})() for i in range(1, 4)}

    def test_assignment(self):
        order = Order(1, (0,0), (5,5))
        shared.ready_queue.put(order)

        t = threading.Thread(target=assign_orders, daemon=True)
        t.start()

        # čekáme chvíli na přiřazení
        t.join(timeout=2)
        self.assertEqual(order.status, "ASSIGNED")
        self.assertIsNotNone(order.assigned_courier)

if __name__ == "__main__":
    unittest.main()
