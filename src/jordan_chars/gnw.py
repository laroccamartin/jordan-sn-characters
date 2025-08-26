from typing import List, Tuple
import random

Partition = Tuple[int, ...]

def _col_height(shape: List[int], j: int) -> int:
    return sum(1 for rlen in shape if rlen > j)

def _is_corner(shape: List[int], i: int, j: int) -> bool:
    right = shape[i] - 1 - j
    down  = _col_height(shape, j) - 1 - i
    return right == 0 and down == 0

def sample_syt(lam: Partition, rng: random.Random) -> List[List[int]]:
    """
    Uniform SYT via GNW hook-walk.
    Returns a ragged list of rows of shape lam containing numbers 1..n.
    Expected O(n^2) time. Suitable for n up to a few thousand.
    """
    # tableau to fill (fixed target shape)
    T = [ [None]*lam[i] for i in range(len(lam)) ]

    # mutable shape + mapping from current row index -> original row index
    shape = list(lam)
    row_map = list(range(len(lam)))

    n = sum(lam)
    for label in range(n, 0, -1):
        # list all current cells
        cells = [(i,j) for i, rlen in enumerate(shape) for j in range(rlen)]
        i, j = rng.choice(cells)

        # hook-walk until corner
        while True:
            right = shape[i] - 1 - j
            down  = _col_height(shape, j) - 1 - i
            if right == 0 and down == 0:
                break
            # move right with prob right/(right+down), else down
            if rng.random() < (right / (right + down)):
                j += 1
            else:
                i += 1

        # place label at (original_row, current_rightmost_col)
        orig_i = row_map[i]
        col_j  = shape[i]-1
        T[orig_i][col_j] = label

        # remove that corner cell from shape
        shape[i] -= 1
        if shape[i] == 0:
            del shape[i]
            del row_map[i]

    # convert Nones to int (should be none left)
    return T
