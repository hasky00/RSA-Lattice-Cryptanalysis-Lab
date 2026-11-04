"""Command-line demonstrations for the RSA Lattice Cryptanalysis Lab."""

import argparse
from fractions import Fraction

from .rsa import generate_toy_key, encrypt, decrypt, validate_key
from .lll import lll_reduce


def demo_rsa():
    key = generate_toy_key(bits=32)
    message = 12345
    ciphertext = encrypt(message, key.n, key.e)
    recovered = decrypt(ciphertext, key)
    print("Toy RSA arithmetic demonstration")
    print(f"N = {key.n}")
    print(f"e = {key.e}")
    print(f"p, q are retained as experimental ground truth: {key.p}, {key.q}")
    print(f"d = {key.d}")
    print(f"message = {message}")
    print(f"ciphertext = {ciphertext}")
    print(f"decrypted = {recovered}")
    print(f"key invariants valid = {validate_key(key)}")
    print("WARNING: textbook RSA and tiny parameters are not secure.")


def demo_lll():
    basis = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    print("Input basis:")
    for row in basis:
        print(" ", row)
    reduced = lll_reduce(basis, delta=Fraction(3, 4))
    print("LLL-reduced basis:")
    for row in reduced:
        print(" ", row)


def demo_coppersmith():
    try:
        import sympy as sp
        from .coppersmith import recover_small_roots, root_bound_reference
    except ImportError as exc:
        raise SystemExit("Install project dependencies first: python -m pip install -e .") from exc

    x = sp.Symbol("x")
    p, q, secret_root = 101, 113, 7
    N = p * q
    f = x - secret_root
    X = 10

    print("Toy univariate small-root experiment")
    print(f"N = {N}; polynomial = {f}; root bound X = {X}")
    print(f"Verified ground-truth root: {int(f.subs(x, secret_root)) % N == 0}")
    print(f"Indicative monic linear-root bound: {root_bound_reference(N, 1):.2f}")

    try:
        result = recover_small_roots(f, N, X, m=2, t=1)
    except ImportError as exc:
        raise SystemExit("fpylll is required for this experiment. See README.") from exc

    print(f"Lattice dimension: {result.lattice_dimension}")
    print(f"Recovered candidates: {result.candidates}")
    print(f"Ground truth recovered: {secret_root in result.candidates}")
    print("A negative result is an experimental outcome, not a theorem counterexample.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("experiment", choices=("rsa", "lll", "coppersmith"))
    args = parser.parse_args()
    {"rsa": demo_rsa, "lll": demo_lll, "coppersmith": demo_coppersmith}[args.experiment]()


if __name__ == "__main__":
    main()
