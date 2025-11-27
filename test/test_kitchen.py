import unittest
from queue import Queue
from unittest.mock import patch
from io import StringIO
import sys
import threading

from src.models.order import Order
from src.core import shared
from src.engine.kitchen_worker import kitchen_worker

class TestKitchenWorker(unittest.TestCase):
    def setUp(self):
        # Reset shared resources
        shared.incoming_queue = Queue()
        shared.ready_queue = Queue()
        shared.print_lock = threading.Lock()
        shared.stop = False

        # Přidáme několik objednávek
        for i in range(1, 4):
            order = Order(i, (0,0), (i,i))
            shared.incoming_queue.put(order)

    @patch("time.sleep", return_value=None)  # odstraní reálné čekání
    def test_kitchen_worker_processing(self, mock_sleep):
        old_stdout = sys.stdout
        sys.stdout = StringIO()  # zachytí printy

        # Spustíme worker vlákno
        t = threading.Thread(target=kitchen_worker, args=(1,), daemon=True)
        t.start()
        t.join(timeout=2)  # join s timeoutem, aby test neblokoval

        output = sys.stdout.getvalue()
        sys.stdout = old_stdout

        # Ověření: všechny objednávky jsou READY
        ready_orders = list(shared.ready_queue.queue)
        self.assertEqual(len(ready_orders), 3)
        for order in ready_orders:
            self.assertEqual(order.status, "READY")

        # Ověření výpisů
        self.assertIn("Preparing order", output)
        self.assertIn("Order 1 ready", output)
        self.assertIn("Exiting, no more orders", output)

if __name__ == "__main__":
    unittest.main()
