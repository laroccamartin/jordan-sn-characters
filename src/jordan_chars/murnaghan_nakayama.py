from functools import lru_cache
from typing import List, Tuple, Iterable, Dict
from .partitions import dim_hook_length

Partition = Tuple[int, ...]

# ---------- helpers on shapes ----------
def _col_height(lam: Partition, j: int) -> int:
    return sum(1 for r in lam if r > j)

def _is_corner(lam: Partition, i: int, j: int) -> bool:
    # corner = no cell to the right and no cell below
    right = lam[i] - 1 - j
    down  = _col_height(lam, j) - 1 - i
    return right == 0 and down == 0

def _rim_path(lam: Partition) -> List[Tuple[int,int]]:
    """Return the rim path cells from top-right to bottom-left (inclusive)."""
    if not lam: return []
    i, j = 0, lam[0]-1
    path = []
    last_row = len(lam) - 1
    while True:
        path.append((i, j))
        if i == last_row and j == 0:
            break
        # if below is outside, go left; else go down
        if i+1 >= len(lam) or lam[i+1] <= j:
            j -= 1
        else:
            i += 1
    return path

def _remove_segment(lam: Partition, seg: List[Tuple[int,int]]) -> Partition:
    """Remove a contiguous rim segment, return new partition (Non-increasing)."""
    # count removed cells per row
    rm: Dict[int,int] = {}
    for (i, _j) in seg:
        rm[i] = rm.get(i, 0) + 1
    new = []
    for i, rlen in enumerate(lam):
        keep = rlen - rm.get(i, 0)
        if keep < 0:  # invalid
            return ()
        if keep > 0:
            new.append(keep)
    # ensure non-increasing
    for a, b in zip(new, new[1:]):
        if a < b:
            return ()
    return tuple(new)

def _rim_hooks_of_length(lam: Partition, r: int) -> List[Tuple[Partition, int]]:
    """All ways to remove a border strip (rim hook) of size r.
       Returns (new_lambda, height) for each removal."""
    if r <= 0: return []
    path = _rim_path(lam)
    # find corner indices along the path
    corners = [k for k,(i,j) in enumerate(path) if _is_corner(lam, i, j)]
    out = []
    # segments must start and end at corners; length exactly r
    corner_set = set(corners)
    for s in corners:
        t = s + r - 1
        if t < len(path) and t in corner_set:
            seg = path[s:t+1]
            new_lam = _remove_segment(lam, seg)
            if new_lam != ():
                rows_touched = len({i for (i,_j) in seg})
                height = rows_touched - 1
                out.append((new_lam, height))
    return out

# ---------- Murnaghan–Nakayama recursion ----------
@lru_cache(maxsize=None)
def _mn_char(lam: Partition, mu: Partition) -> int:
    n_lam = sum(lam)
    n_mu  = sum(mu)
    if n_lam != n_mu:
        return 0
    if n_lam == 0:
        return 1  # both empty
    if not mu:
        return 0
    # pick the first cycle length (mu sorted nonincreasing expected)
    r = mu[0]
    rest = mu[1:]
    total = 0
    for lam2, h in _rim_hooks_of_length(lam, r):
        total += ((-1)**h) * _mn_char(lam2, rest)
    return total

def character_exact(lam: Partition, mu: Partition) -> int:
    """Unnormalized character χ_λ(μ) using Murnaghan–Nakayama."""
    # ensure canonical forms (sorted, nonincreasing)
    lam = tuple(sorted(lam, reverse=True))
    mu  = tuple(sorted(mu,  reverse=True))
    return _mn_char(lam, mu)

def normalized_character_exact(lam: Partition, mu: Partition) -> float:
    """χ̂_λ(μ) = χ_λ(μ) / d_λ."""
    from .partitions import dim_hook_length
    return character_exact(lam, mu) / dim_hook_length(lam)
