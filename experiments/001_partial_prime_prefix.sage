"""Experiment 001: recover a toy RSA prime from its known high-bit prefix.

Run with:
    sage experiments/001_partial_prime_prefix.sage

This uses SageMath's implementation of univariate Coppersmith small_roots
for an unknown divisor of N. Parameters are intentionally tiny and public.
Never use against real keys or systems.
"""

import json
import time
from pathlib import Path

p = next_prime(2^31 + 12345)
q = next_prime(2^31 + 98765)
N = p * q

unknown_bits = 8
X = 2^unknown_bits
known_prefix = (p >> unknown_bits) << unknown_bits

R.<x> = PolynomialRing(Zmod(N))
f = x + known_prefix

started = time.perf_counter()
roots = f.small_roots(X=X, beta=0.5)
elapsed = time.perf_counter() - started

recovered = []
for root in roots:
    candidate = ZZ(known_prefix + ZZ(root))
    if 0 <= ZZ(root) < X and N % candidate == 0:
        recovered.append({"root": int(root), "factor": int(candidate)})

success = any(item["factor"] in (int(p), int(q)) for item in recovered)
result = {
    "experiment": "001_partial_prime_prefix",
    "description": "Toy RSA factor recovery from known high bits of one prime",
    "N": int(N),
    "public_exponent": 65537,
    "prime_bits": int(p.nbits()),
    "unknown_low_bits": unknown_bits,
    "root_bound_X": int(X),
    "known_prefix": int(known_prefix),
    "beta": 0.5,
    "polynomial": "f(x) = x + known_prefix",
    "lattice_method": "SageMath Coppersmith small_roots (unknown divisor)",
    "elapsed_seconds": elapsed,
    "candidates": recovered,
    "success": bool(success),
    "verification": "Every reported factor is checked by exact divisibility N % factor == 0",
    "ground_truth_for_validation_only": {"p": int(p), "q": int(q)},
}

out = Path("results/experiment_001.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
if not success:
    raise SystemExit("Experiment did not recover the ground-truth factor; inspect Sage version/parameters.")
