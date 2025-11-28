#Author: Ornella Kim Gasková

from src.models.courier import Courier
from src.core.shared import couriers_map

def init_couriers(num_couriers):
    for i in range(1, num_couriers + 1):
        c = Courier(i)
        couriers_map[i] = c