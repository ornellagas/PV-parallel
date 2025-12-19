# Author: Ornella Kim Gasková

import threading

class Courier:
    def __init__(self, courier_id, name, status="IDLE"):
        self.id = courier_id
        self.name = name
        self.status = status
        self.assigned_order = None
        self.lock = threading.Lock()