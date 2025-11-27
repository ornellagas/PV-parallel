class Order:
    def __init__(self, order_id, restaurant_location, customer_location):
        self.id = order_id
        self.restaurant_location = restaurant_location
        self.customer_location = customer_location
        self.status = "NEW"  # NEW, PREPARING, READY, ASSIGNED, DELIVERED
        self.assigned_courier = None
