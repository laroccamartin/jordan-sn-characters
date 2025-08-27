from src.jordan_chars.roichman import normalized_character_mc
def sign_character_norm(n:int, mu):
    return (-1)**(n - len(mu))
def standard_character_norm(n:int, mu):
    m1 = sum(1 for x in mu if x==1)
    return (m1 - 1) / (n-1)

def test_trivial_rep_small():
    for n in range(2,8):
        lam = (n,)
        for mu in [(n,), tuple([1]*n)]:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=0, T=2000)
            assert abs(est - 1.0) < 0.15

def test_sign_rep_small():
    for n in range(2,8):
        lam = tuple([1]*n)
        for mu in [(n,), tuple([1]*n)]:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=1, T=2500)
            truth = sign_character_norm(n, mu)
            assert abs(est - truth) < 0.25

def test_standard_rep_small():
    for n in range(4,9):
        lam = (n-1,1)
        for mu in [(n,), (n-1,1), tuple([1]*n)]:
            est = normalized_character_mc(lam, mu, epsilon=0.05, delta=1e-6, seed=2, T=3000)
            truth = standard_character_norm(n, mu)
            assert abs(est - truth) < 0.25
