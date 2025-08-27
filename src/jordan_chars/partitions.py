from typing import List, Tuple
import math

Partition = Tuple[int, ...]  # nonincreasing

def parse_partition(s: str) -> Partition:
    parts = tuple(int(x) for x in s.strip().replace(' ', '').split(',') if x)
    if any(p <= 0 for p in parts): raise ValueError("parts must be positive")
    if any(parts[i] < parts[i+1] for i in range(len(parts)-1)):
        raise ValueError("partition must be nonincreasing (e.g., 4,2,1)")
    return parts

def partition_size(lam: Partition) -> int:
    return sum(lam)

def hook_lengths(lam: Partition) -> List[List[int]]:
    rows = len(lam)
    HL = []
    def col_height(j:int)->int:
        return sum(1 for r in lam if r > j)
    for i in range(rows):
        row = []
        for j in range(lam[i]):
            right = lam[i] - 1 - j
            down  = col_height(j) - 1 - i
            row.append(1 + right + down)
        HL.append(row)
    return HL

def dim_hook_length(lam: Partition) -> int:
    n = partition_size(lam)
    HL = hook_lengths(lam)
    prod = 1
    for row in HL:
        for h in row: prod *= h
    return math.factorial(n) // prod

def count_fixed_points(mu: Partition) -> int:
    return sum(1 for x in mu if x == 1)
