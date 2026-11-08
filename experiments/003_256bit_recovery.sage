import json
import time
from pathlib import Path

# Experiment 003: Coppersmith scaling to RSA-256
# Synthetic RSA keys generated solely for research.

set_random_seed(20261108)

def make_prime(bits):
    lower = ZZ(2) ** (bits - 1)
    upper = ZZ(2) ** bits - 1
    return ZZ(random_prime(upper, lbound=lower))

p = make_prime(128)
q = make_prime(128)

while p == q or (p * q).nbits() != 256:
    q = make_prime(128)

N = p * q
beta = 0.5

# Begin with a small pilot before testing the boundary.
unknown_bits = [16, 32, 48, 56, 60, 62, 64, 66, 68, 72]

results = {
    "experiment": "003_256bit_recovery",
    "modulus_bits": int(N.nbits()),
    "prime_bits": [int(p.nbits()), int(q.nbits())],
    "N": str(N),
    "p": str(p),
    "q": str(q),
    "beta": float(beta),
    "theoretical_N_quarter": str(N.nth_root(4, truncate_mode=True)[0]),
    "trials": []
}

print("Experiment 003: RSA-256 scaling")
print("Modulus size:", N.nbits(), "bits")
print("Prime sizes:", p.nbits(), q.nbits(), "bits")
print("-" * 55)

for k in unknown_bits:
    X = ZZ(2) ** k
    prefix = (p // X) * X
    actual_suffix = p - prefix

    R = PolynomialRing(Zmod(N), 'x')
    x = R.gen()
    f = x + prefix

    start = time.perf_counter()
    candidates = []
    error = None

    try:
        candidates = [
            ZZ(r) for r in f.small_roots(
                X=X,
                beta=beta,
                epsilon=0.03
            )
        ]
    except Exception as exc:
        error = str(exc)

    elapsed = time.perf_counter() - start

    recovered = None
    for root in candidates:
        candidate = prefix + root
        if candidate > 1 and N % candidate == 0:
            recovered = candidate
            break

    success = recovered == p

    trial = {
        "unknown_bits": int(k),
        "X": str(X),
        "actual_suffix": str(actual_suffix),
        "success": bool(success),
        "elapsed_seconds": float(elapsed),
        "candidate_count": len(candidates),
        "error": error
    }

    results["trials"].append(trial)

    print(
        f"k={k:2d} | "
        f"success={str(success):5s} | "
        f"time={elapsed:.4f}s"
    )

output = Path("results/experiment_003.json")
output.write_text(json.dumps(results, indent=2))

print("-" * 55)
print("Saved results to", output)
