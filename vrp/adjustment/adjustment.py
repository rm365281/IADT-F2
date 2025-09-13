from solution import Solution
from vehicle import Vehicle
from vrp.adjustment.helper import Helper


class Adjustment:
    def __init__(self, depot_identifier, helper: Helper):
        self.__depot_identifier = depot_identifier
        self.__helper = helper

    def apply(self, solution: Solution):
        """
        Apply adjustments to the solution to ensure that capacity constraints is met.
        Args:
            solution:
                The solution to have the routes adjusted.

        Returns:
            The adjusted solution.

        """
        new_vehicles: list[Vehicle] = []
        for vehicle in solution.vehicles:
            new_route = self.__helper.split_route_by_capacity(vehicle.route, vehicle.capacity)
            final_route = self.__helper.remove_duplicated_sequencial_depots(new_route)
            final_route.distance = self.__helper.calculate_distance(final_route)
            new_vehicle = Vehicle(route=final_route, autonomy=vehicle.autonomy, capacity=vehicle.capacity)
            new_vehicles.append(new_vehicle)

        solution.vehicles = new_vehicles
        return solution
