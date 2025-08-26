from typing import Tuple, List, Dict
import math, random
import numpy as np

from .partitions import Partition, partition_size, dim_hook_length
from .gnw import sample_syt

def _positions(tableau: List[List[int]]) -> Dict[int, Tuple[int,int]]:
    """Map entry -> (row, col) 0-based."""
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
    """
    Compute W_mu(Λ) ∈ {−1,0,1} product per Roichman’s formula.
    B(mu) = {μ1, μ1+μ2, ...}; multiply f_mu(i,Λ) for i=1..n-1 with i∉B(mu).
    f_mu depends on relative positions of i, i+1, i+2 (see Jordan’s summary).
    """
    n = sum(len(r) for r in tableau)
    pos = _positions(tableau)
    B = _partial_sums(mu)
    P = 1
    for i in range(1, n):
        if i in B:  # skip border indices
            continue
        (ri, ci)   = pos[i]
        (r1, c1)   = pos[i+1]
        # helper relations
        def is_sw(a, b):  # a strictly southwest of b?
            (ra, ca), (rb, cb) = a, b
            return ra > rb and ca < cb
        def is_ne(a, b):  # a strictly northeast of b?
            (ra, ca), (rb, cb) = a, b
            return ra < rb and ca > cb

        if is_sw((r1,c1), (ri,ci)):
            f = -1
        else:
            # 0-case: (i+1) NE of i, and (i+2) SW of (i+1), and (i+1) ∉ B(mu)
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
    """
    Jordan’s classical estimator: E_Λ W_mu(Λ) over uniform SYT(λ).
    Returns additive-ε estimate of χ̂_λ(μ)=χ_λ(μ)/d_λ with prob ≥ 1-δ
    using T = Θ(ε^{-2} log(1/δ)) samples. (Hoeffding.)
    """
    n = partition_size(lam)
    if sum(mu) != n:
        raise ValueError("lambda and mu must partition the same n")
    if T is None:
        # Hoeffding: T >= (1/2ε^2) ln(2/δ); use factor 2 for comfort
        T = math.ceil((2.0 / (epsilon**2)) * math.log(2.0/delta))
    rng = random.Random(seed)
    acc = 0.0
    for t in range(T):
        tab = sample_syt(lam, rng)
        w = roichman_weight(mu, tab)
        acc += w
        if early_zero and w == 0:
            # nothing prevents early zeros; keep counting samples anyway
            pass
    return acc / T

def unnormalized_from_normalized(lam: Partition, normalized_value: float) -> float:
    """Return χ_λ(μ) = d_λ * χ̂_λ(μ)."""
    return dim_hook_length(lam) * normalized_value
