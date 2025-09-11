import random

from solution import Solution


def parents_choice(population: list[Solution]) -> tuple[Solution, Solution]:
    if len(population) < 5:
        return population[0], population[1]
    tournament_size = 5
    tournament = random.sample(population, tournament_size)
    tournament = sorted(tournament, key=lambda ind: ind.fitness)
    return tournament[0], tournament[1]

def choose_two_different_indices(length: int) -> tuple[int, int]:
    idx1 = random.randint(0, length - 1)
    idx2 = random.randint(idx1 + 1, length)
    return idx1, idx2