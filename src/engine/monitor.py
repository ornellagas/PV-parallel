# Author: Ornella Kim Gasková

import time
from core.shared import incoming_queue, ready_queue, stop

def monitor_queues():
    # Vypisuje stav front do terminálu pro kontrolu paralelního běhu
    while not stop:
        # qsize() nám řekne, kolik věcí čeká ve frontě
        print(f"--- MONITOR: Čeká na kuchyni: {incoming_queue.qsize()} | Čeká na rozvoz: {ready_queue.qsize()} ---")
        time.sleep(5)