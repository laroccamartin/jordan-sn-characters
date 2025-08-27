from typing import List, Tuple
import random

Partition = Tuple[int, ...]

def _col_height(shape: List[int], j: int) -> int:
    return sum(1 for rlen in shape if rlen > j)

def sample_syt(lam: Partition, rng: random.Random) -> List[List[int]]:
    T = [ [None]*lam[i] for i in range(len(lam)) ]
    shape = list(lam)
    row_map = list(range(len(lam)))
    n = sum(lam)
    for label in range(n, 0, -1):
        cells = [(i,j) for i, rlen in enumerate(shape) for j in range(rlen)]
        i, j = rng.choice(cells)
        while True:
            right = shape[i] - 1 - j
            down  = _col_height(shape, j) - 1 - i
            if right == 0 and down == 0:
                break
            if rng.random() < (right / (right + down)):
                j += 1
            else:
                i += 1
        orig_i = row_map[i]
        col_j  = shape[i]-1
        T[orig_i][col_j] = label
        shape[i] -= 1
        if shape[i] == 0:
            del shape[i]; del row_map[i]
    return T
