from unittest import TestCase
from vrp.route_spliter import RouteSplitter
from route import Route


class TestRouteSpliter(TestCase):
    route_spliter = RouteSplitter(depot_identifier=0, number_vehicles=4)

    def test_split(self):
        route = Route([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20])
        split_routes = self.route_spliter.split(route)

        self.assertEqual(len(split_routes), 4)
        self.assertEqual(split_routes[0].customers, [0, 1, 2, 3, 4, 5, 0])
        self.assertEqual(split_routes[1].customers, [0, 6, 7, 8, 9, 10, 0])
        self.assertEqual(split_routes[2].customers, [0, 11, 12, 13, 14, 15, 0])
        self.assertEqual(split_routes[3].customers, [0, 16, 17, 18, 19, 20, 0])
