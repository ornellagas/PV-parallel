# Author: Ornella Kim Gasková

import time
from core.shared import incoming_queue, ready_queue, stop, emit_event, couriers_map, couriers_map_lock

def assign_orders():
    # Logika dispečinku: Hlídá frontu hotových jídel ahledá pro ně dostupné kurýry

    while not stop or not ready_queue.empty():
        try:
            # Čekáme na hotovou objednávku z kuchyně
            order = ready_queue.get(timeout=1)
        except Exception:
            continue

        assigned = False

        # Musíme zamknout mapu kurýrů, abychom bezpečně našli volného
        with couriers_map_lock:
            for courier in couriers_map.values():
                if courier.status == "IDLE":
                    # Našli jsme zdroj (kurýra) - označíme ho jako obsazeného
                    courier.status = "DELIVERING"
                    courier.assigned_order = order.id

                    order.status = "ASSIGNED"
                    order.assigned_courier = courier.id
                    assigned = True

                    # Oznámení na dashboard
                    emit_event("ORDER_ASSIGNED", order.id, "ASSIGNED",
                               f"Courier {courier.id} is picking up the order.")
                    break

        if not assigned:
            # Pokud není volný kurýr, vrátíme objednávku zpět do fronty
            # a chvíli počkáme, než to zkusíme znovu (prevence starvation)
            ready_queue.put(order)
            time.sleep(2)
        else:
            # Simulace cesty ke klientovi
            # V reálném světě by zde bylo čekání na potvrzení z mobilní aplikace kurýra
            time.sleep(5)
            order.status = "DELIVERED"
            # Po doručení uvolníme kurýra pro další práci
            with couriers_map_lock:
                courier.status = "IDLE"
                courier.assigned_order = None

            emit_event("ORDER_DELIVERED", order.id, "DELIVERED",
                       f"Delivered by Courier {courier.id} successfully.")

        ready_queue.task_done()