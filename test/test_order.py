import unittest
from src.models.order import Order

class TestOrder(unittest.TestCase):
    def test_order_initialization(self):
        order = Order(1, (0,0), (5,5))
        self.assertEqual(order.id, 1)
        self.assertEqual(order.status, "NEW")
        self.assertIsNone(order.assigned_courier)
        self.assertEqual(order.restaurant_location, (0,0))
        self.assertEqual(order.customer_location, (5,5))

    def test_order_status_change(self):
        order = Order(2, (1,1), (2,2))
        order.status = "PREPARING"
        self.assertEqual(order.status, "PREPARING")

if __name__ == "__main__":
    unittest.main()