import random

from domain import Solution


def parents_selection(population: list[Solution]) -> tuple[Solution, Solution]:
    """
    Selects two parents from the population using tournament selection.
    If a population with only two individuals is provided, those two individuals are returned as parents.

    Args:
        population: List of solutions representing the population.

    Returns:
        A tuple containing two selected parent solutions.
    Raises:
        ValueError: If the population has less than two individuals.

    """
    if len(population) < 2:
        raise ValueError("Population must have at least two individuals to select parents.")

    if len(population) == 2:
        return population[0], population[1]

    tournament_size = 5
    if len(population) < 5:
        tournament_size = len(population)

    selected = []
    for _ in range(2):
        tournament = random.sample(range(len(population)), tournament_size)
        winner = max(tournament, key=lambda i: population[i].fitness)
        selected.append(population[winner])
        population.remove(population[winner])
        if len(population) < tournament_size:
            tournament_size = len(population)
    return selected[0], selected[1]