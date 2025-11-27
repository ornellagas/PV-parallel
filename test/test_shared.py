import unittest
import queue
from src.core import shared

class TestSharedResources(unittest.TestCase):
    def test_queues_initially_empty(self):
        self.assertEqual(shared.incoming_queue.qsize(), 0)
        self.assertEqual(shared.ready_queue.qsize(), 0)

    def test_orders_map_lock(self):
        with shared.orders_map_lock:
            shared.orders_map[1] = "test"
            self.assertIn(1, shared.orders_map)
            del shared.orders_map[1]

if __name__ == "__main__":
    unittest.main()
