import numpy as np

from domain import Route


class RouteSplitter:
    def __init__(self, depot_identifier: int, number_vehicles: int) -> None:
        if number_vehicles <= 0:
            raise ValueError("Number of vehicles must be greater than zero.")
        self.number_vehicles = number_vehicles
        self.depot_identifier = depot_identifier

    def split(self, route: Route) -> list[Route]:
        """
        Splits a single route into multiple routes based on the number of vehicles.
        Args:
            route: a Route object representing the complete route to be split.

        Returns:
            a list of Route objects, each representing a split route.
        """
        chunks = np.array_split(route.customers, self.number_vehicles)

        return [Route([self.depot_identifier] + chunk.tolist() + [self.depot_identifier]) for chunk in chunks]