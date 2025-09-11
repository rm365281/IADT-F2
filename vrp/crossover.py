import random

from solution import Solution


def choose_two_different_indices(length: int) -> tuple[int, int]:
    idx1 = random.randint(0, length - 1)
    idx2 = random.randint(idx1 + 1, length)
    return idx1, idx2