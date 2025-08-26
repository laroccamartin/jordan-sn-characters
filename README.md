# jordan-sn-characters

**Additive approximation of normalized symmetric-group characters**  
via **Roichman’s formula** and **uniform SYT sampling (GNW hook-walk)**, following Jordan (2008).  
This is the *classical* part of Jordan’s result—no quantum circuits needed.

χ̂_λ(μ) = χ_λ(μ) / d_λ = E_{Λ∼SYT(λ)}[ W_μ(Λ) ],  
with W_μ(Λ) ∈ {−1, 0, 1} computed from relative positions of consecutive labels.

- Sampling Λ ∼ SYT(λ): Greene–Nijenhuis–Wilf **hook-walk**, expected O(n²).
- Monte-Carlo: T = Θ(ε⁻² log(1/δ)) gives additive ε with prob ≥ 1−δ (Hoeffding).

## Quickstart
~~~bash
python -m venv .venv && source .venv/bin/activate
pip install -U pip && pip install -r requirements.txt

# Example: λ=(5,3), μ=(3,2,2,1) in S_8
python -m src.jordan_chars.estimate --lambda 5,3 --mu 3,2,2,1 --epsilon 0.03 --delta 1e-4 --seed 0
~~~

## Tests
~~~bash
pytest -q
~~~

## Reference
- Jordan (2008): additive approximation for S_n characters via Roichman + GNW.
- GNW hook-walk for uniform SYT.
