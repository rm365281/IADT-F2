from graph import Node
from vehicle import Vehicle


def calculate_distance_penality(full_itinerary: float, vehicle: Vehicle) -> float:
    penalty = 0
    if full_itinerary > vehicle.autonomy:
        penalty = 100000 #(full_itinerary - vehicle.autonomy) * 1000
    return penalty

def calculate_priority_violation_penality(depot: Node, from_node: Node, has_non_priority_customer_before_priority_customer_in_itinerary: bool) -> \
tuple[bool, int]:
    penalty = 0
    if from_node.priority == 1 and has_non_priority_customer_before_priority_customer_in_itinerary:
        penalty = 50

    if from_node.priority == 0 and depot != from_node:
        has_non_priority_customer_before_priority_customer_in_itinerary = True

    return has_non_priority_customer_before_priority_customer_in_itinerary, penalty

def calculate_vehicle_unbalanced_distance_penality(vehicles: list[Vehicle]) -> float:
    penalty = 0
    total_distance = sum(vehicle.distance() for vehicle in vehicles)
    average_distance = total_distance / len(vehicles) if vehicles else 0

    for vehicle in vehicles:
        penalty += abs(vehicle.distance() - average_distance)

    return penalty