import random
from unittest.mock import Mock

import pytest

from vrp.selection import parents_selection


@pytest.mark.parametrize("population_size", [3, 5, 10])
def test_parents_choice(population_size):
    population = []
    for _ in range(population_size):
        solution = Mock()
        solution.fitness = float(random.randint(1, 100))
        population.append(solution)

    parent1, parent2 = parents_selection(population)
    assert parent1 != parent2

def test_parents_choice_with_one_individual():
    population = [Mock(fitness=10.0)]
    with pytest.raises(ValueError):
        parents_selection(population)