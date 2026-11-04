# RSA Lattice Cryptanalysis Lab

A reproducible Python laboratory for studying RSA number theory, lattice reduction, and univariate Coppersmith-style small-root experiments using **toy parameters**.

> **Research/education only.** This project is not a production cryptographic implementation. It deliberately uses textbook RSA in demonstrations and small, artificial parameters. Never use it to generate, store, attack, or validate real private keys.

## What is included

- `rsa_lab/rsa.py` — toy RSA key generation, encryption/decryption, and parameter checks.
- `rsa_lab/lll.py` — a compact educational LLL implementation using exact rational arithmetic.
- `rsa_lab/coppersmith.py` — univariate monic polynomial lattice construction and an experimental reduction/root-candidate pipeline using `fpylll` and SymPy.
- `rsa_lab/experiments.py` — runnable demonstrations.
- `tests/` — unit tests for arithmetic and LLL; the Coppersmith test is optional if `fpylll` is installed.

## Setup

Python 3.10 or newer is recommended.

```bash
python -m venv .venv
# macOS/Linux:
source .venv/bin/activate
# Windows PowerShell:
# .venv\\Scripts\\Activate.ps1

python -m pip install -e ".[dev]"
```

The core RSA and educational LLL modules use only the Python standard library. The Coppersmith experiment additionally uses SymPy and `fpylll`.

If `fpylll` installation is inconvenient on your platform, use a SageMath environment and adapt the lattice reduction call to Sage's `Matrix(ZZ, ...).LLL()`.

## Run the demonstrations

```bash
python -m rsa_lab.experiments rsa
python -m rsa_lab.experiments lll
python -m rsa_lab.experiments coppersmith
```

Run tests:

```bash
pytest -q
```

## Research workflow

1. Run the RSA demonstration and inspect the public/private parameter relationships.
2. Run the exact-arithmetic LLL demonstration and compare the input and reduced bases.
3. Run the Coppersmith experiment on the included toy polynomial.
4. Change the root bound `X`, polynomial degree, and lattice parameters `m` and `t`.
5. Record success/failure, lattice dimension, coefficient bit lengths, and runtime.
6. Keep a record of the theorem assumptions separately from experimental outcomes.

## Important mathematical scope

For a monic univariate polynomial of degree `delta`, the classical Coppersmith small-root result gives a polynomial-time recovery guarantee for roots below approximately `N^(1/delta)`; rigorous statements use a fixed margin such as `N^(1/delta - epsilon)`. The implementation here is an **experimental lattice builder**, not a complete proof-producing implementation of every theorem variant. A failed experiment does not disprove the theorem, and a recovered candidate must always be checked against the original modular equation and the stated size bound.

The included LLL implementation is intended for small educational examples. It uses exact `Fraction` arithmetic and recomputes Gram–Schmidt data frequently; it is not optimized for large cryptographic lattices.

## Suggested next milestones

- Add experiment metadata output (JSON/CSV).
- Add reproducible parameter sweeps.
- Compare the educational LLL implementation with `fpylll`.
- Add a carefully documented unknown-divisor prime-prefix experiment.
- Add a research notebook with plots of success rate versus root size and lattice dimension.
- Add a reference bibliography with DOI/publisher links verified against the originals.

## Project structure

```text
rsa-lattice-cryptanalysis-lab/
├── README.md
├── pyproject.toml
├── rsa_lab/
│   ├── __init__.py
│   ├── rsa.py
│   ├── lll.py
│   └── coppersmith.py
└── tests/
    ├── test_rsa.py
    ├── test_lll.py
    └── test_coppersmith.py
```

## Experiment 001: partial prime-prefix recovery

The first research experiment is implemented as a SageMath script:

```bash
sage experiments/001_partial_prime_prefix.sage
```

It models a prime as `p = p0 + x`, where `p0` is the known high-bit prefix and `x` is an unknown low-bit suffix. Since `p | N`, the monic linear polynomial `f(x) = p0 + x` has a small root modulo an unknown divisor of `N`. SageMath's `small_roots` routine applies the unknown-divisor Coppersmith method with `beta=0.5` for a balanced toy modulus. The script verifies recovered factors using exact integer divisibility and records the run in `results/experiment_001.json`.

The script is deliberately limited to toy parameters. The theoretical `N^(1/4-epsilon)` scale is an asymptotic guide under theorem assumptions, not a claim that all parameter choices or all implementations succeed. See [`experiments/README.md`](experiments/README.md) for the derivation.
