import math
from src.jordan_chars.partitions import parse_partition, dim_hook_length, count_fixed_points, partition_size
from src.jordan_chars.roichman import normalized_character_mc

def sign_character_norm(n:int, mu):
    # sign rep (1^n): χ(μ) = (-1)^{n-ℓ(μ)}, d=1
    l = len(mu)
    return (-1)**(n - l)

def standard_character_norm(n:int, mu):
    # (n-1,1): χ̂ = (m1 - 1)/(n-1)
    m1 = sum(1 for x in mu if x==1)
    return (m1 - 1) / (n-1)

def test_trivial_rep_small():
    for n in range(2,9):
        lam = (n,)
        for mu in [(n,), tuple([1]*n)]:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=0, T=2000)
            assert abs(est - 1.0) < 0.1

def test_sign_rep_small():
    for n in range(2,9):
        lam = tuple([1]*n)
        mus = [(n,), tuple([1]*n)]
        for mu in mus:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=1, T=3000)
            truth = sign_character_norm(n, mu)  # already normalized (d=1)
            assert abs(est - truth) < 0.2

def test_standard_rep_small():
    for n in range(4,9):
        lam = (n-1,1)
        # a couple of mu's
        for mu in [(n,), (n-1,1), tuple([1]*n)]:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=2, T=4000)
            truth = standard_character_norm(n, mu)
            assert abs(est - truth) < 0.2
