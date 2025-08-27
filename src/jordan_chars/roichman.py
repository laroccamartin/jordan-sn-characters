from typing import Tuple, List, Dict
import math, random
import numpy as np
from .partitions import Partition, partition_size, dim_hook_length
from .gnw import sample_syt

def _positions(tableau: List[List[int]]) -> Dict[int, Tuple[int,int]]:
    pos = {}
    for r, row in enumerate(tableau):
        for c, v in enumerate(row):
            pos[v] = (r, c)
    return pos

def _partial_sums(mu: Partition) -> set:
    s = 0; S = set()
    for part in mu:
        s += part; S.add(s)
    return S

def roichman_weight(mu: Partition, tableau: List[List[int]]) -> int:
    n = sum(len(r) for r in tableau)
    pos = _positions(tableau)
    B = _partial_sums(mu)
    P = 1
    for i in range(1, n):
        if i in B:
            continue
        (ri, ci) = pos[i]
        (r1, c1) = pos[i+1]
        def is_sw(a, b):  # strictly SW?
            (ra, ca), (rb, cb) = a, b
            return ra > rb and ca < cb
        def is_ne(a, b):  # strictly NE?
            (ra, ca), (rb, cb) = a, b
            return ra < rb and ca > cb
        if is_sw((r1,c1), (ri,ci)):
            f = -1
        else:
            if (i+1) not in B and (i+2) in pos:
                (r2, c2) = pos[i+2]
                if is_ne((r1,c1), (ri,ci)) and is_sw((r2,c2), (r1,c1)):
                    f = 0
                else:
                    f = 1
            else:
                f = 1
        P *= f
        if P == 0:
            break
    return P

def normalized_character_mc(lam: Partition, mu: Partition, epsilon: float=0.02,
                            delta: float=1e-3, seed: int=0, T: int=None,
                            early_zero: bool=True) -> float:
    n = partition_size(lam)
    if sum(mu) != n:
        raise ValueError("lambda and mu must partition the same n")
    if T is None:
        T = math.ceil((2.0 / (epsilon**2)) * math.log(2.0/delta))
    rng = random.Random(seed)
    acc = 0.0
    for _ in range(T):
        tab = sample_syt(lam, rng)
        w = roichman_weight(mu, tab)
        acc += w
    return acc / T

def unnormalized_from_normalized(lam: Partition, normalized_value: float) -> float:
    return dim_hook_length(lam) * normalized_value
