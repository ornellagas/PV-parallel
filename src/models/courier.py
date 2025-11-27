import threading

class Courier:
    def __init__(self, courier_id):
        self.id = courier_id
        self.status = "IDLE"     # IDLE, DELIVERING
        self.assigned_order = None
        self.lock = threading.Lock()