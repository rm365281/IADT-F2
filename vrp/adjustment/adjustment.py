from itinerary import Itinerary
from solution import Solution
from vehicle import Vehicle
from vrp.adjustment.helper import Helper


class Adjustment:
    def __init__(self, graph, depot_identifier):
        self.__graph = graph
        self.__depot_identifier = depot_identifier
        self.__helper = Helper(graph, depot_identifier)

    def apply(self, solution: Solution):
        new_vehicles: list[Vehicle] = []
        for vehicle in solution.vehicles:
            new_route = self.__helper.split_route_by_capacity(vehicle)
            final_itinerary = self.__helper.remove_duplicated_sequencial_depots(new_route)

            new_vehicle = Vehicle(itinerary=Itinerary(final_itinerary), autonomy=vehicle.autonomy,
                                  capacity=vehicle.capacity)
            new_vehicles.append(new_vehicle)

        solution.vehicles = new_vehicles
        return solution