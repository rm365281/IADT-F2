from vrp.crossover import choose_two_different_indices


def test_choose_two_different_indices():
    length = 10
    idx1, idx2 = choose_two_different_indices(length)
    assert 0 <= idx1 < idx2 <= length