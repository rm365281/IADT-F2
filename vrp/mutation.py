import random

import solution
from graph import Node
from itinerary import Itinerary
from solution import Solution
from vehicle import Vehicle
from itertools import groupby

def mutate_vehicle_itinerary(vehicle: Vehicle, mutation_probability: float) -> None:
    itinerary = vehicle.itinerary
    customer_ids = itinerary.customers[1:-1]
    for j in range(len(customer_ids) - 1):
        if random.random() <= mutation_probability:
            customer_ids[j], customer_ids[j + 1] = customer_ids[j + 1], customer_ids[j]
    vehicle.itinerary = Itinerary([key for key, _ in groupby([0] + customer_ids + [0])])

def mutate_itinerary_between_vehicles(solution: Solution) -> None:
    if len(solution.vehicles) < 2:
        return
    v1, v2 = random.sample(solution.vehicles, 2)
    _swap_customers_between_vehicles(solution, v1, v2)

def _swap_customers_between_vehicles(solution: Solution, v1, v2):
    v1_ids = v1.customers()[1:-1]
    new_vehicles = []
    if v1_ids and len(v1_ids) > 1:
        c = random.choice(v1_ids)
        v1_new_ids = [key for key, _ in groupby([x for x in v1_ids if x != c])]
        v2_new_ids = [key for key, _ in groupby(v2.customers() + [c])]
        new_vehicles.append(Vehicle(itinerary=Itinerary([0] + v1_new_ids + [0]), autonomy=v1.autonomy, capacity=v1.capacity))
        new_vehicles.append(Vehicle(itinerary=Itinerary([0] + v2_new_ids + [0]), autonomy=v2.autonomy, capacity=v2.capacity))
        solution.vehicles = new_vehicles