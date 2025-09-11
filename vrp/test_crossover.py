from unittest.mock import Mock

from solution import Solution
from vrp.crossover import parents_choice, choose_two_different_indices


def test_parents_choice():
    solution1 = Mock()
    solution1.fitness = 1.0
    solution2 = Mock()
    solution2.fitness = 2.0
    solution3 = Mock()
    solution3.fitness = 3.0
    solution4 = Mock()
    solution4.fitness = 4.0
    solution5 = Mock()
    solution5.fitness = 5.0
    solution6 = Mock()
    solution6.fitness = 6.0
    population: list[Solution] = [
        solution1,
        solution2,
        solution3,
        solution4,
        solution5,
        solution6,
    ]

    parent1, parent2 = parents_choice(population)
    assert parent1 != parent2

def test_choose_two_different_indices():
    length = 10
    idx1, idx2 = choose_two_different_indices(length)
    assert 0 <= idx1 < idx2 <= length