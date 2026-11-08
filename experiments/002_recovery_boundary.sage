"""Experiment 002: Coppersmith recovery vs unknown suffix bits.

Uses only a deterministic, synthetic toy RSA modulus.
"""

import json
import time
from pathlib import Path

p = next_prime(2^31 + 98765)
q = next_prime(2^31 + 12345)
N = p * q

R.<x> = PolynomialRing(Zmod(N))

trials = []

for k in range(4, 21, 2):
    X = 2^k
    prefix = (p >> k) << k
    f = x + prefix

    started = time.perf_counter()
    try:
        roots = f.small_roots(X=X, beta=0.5)
        elapsed = time.perf_counter() - started

        recovered = []
        for root in roots:
            candidate = ZZ(prefix + ZZ(root))
            if 0 <= ZZ(root) < X and N % candidate == 0:
                recovered.append({
                    "root": int(root),
                    "factor": int(candidate)
                })

        success = any(
            item["factor"] == int(p)
            for item in recovered
        )
        error = None

    except Exception as exc:
        elapsed = time.perf_counter() - started
        recovered = []
        success = False
        error = str(exc)

    trial = {
        "unknown_bits": int(k),
        "X": int(X),
        "known_prefix": int(prefix),
        "elapsed_seconds": float(elapsed),
        "success": bool(success),
        "candidates": recovered,
        "error": error
    }

    trials.append(trial)

    print(
        f"k={k:2d} | "
        f"success={success} | "
        f"time={elapsed:.4f}s"
    )

result = {
    "experiment": "002_recovery_boundary",
    "description": "Toy RSA partial-prime recovery boundary",
    "sage_method": "small_roots",
    "beta": float(0.5),
    "N": int(N),
    "p_for_validation_only": int(p),
    "q_for_validation_only": int(q),
    "trials": trials
}

out = Path("results/experiment_002.json")
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(result, indent=2) + "\n")

print(f"\nSaved results to {out}")
