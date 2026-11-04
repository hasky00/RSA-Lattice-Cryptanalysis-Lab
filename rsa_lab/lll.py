"""Educational LLL reduction for small integer row-bases.

This implementation uses exact Fraction arithmetic. It is deliberately simple,
not optimized, and intended for learning and small experiments only.
"""

from fractions import Fraction
from math import floor


def _dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def _nearest_integer(value: Fraction) -> int:
    """Nearest integer; ties are rounded away from zero."""
    if value >= 0:
        return floor(value + Fraction(1, 2))
    return -floor(-value + Fraction(1, 2))


def gram_schmidt(basis):
    """Return (orthogonal vectors, mu coefficients, squared norms)."""
    n = len(basis)
    orthogonal = []
    mu = [[Fraction(0) for _ in range(n)] for _ in range(n)]
    norms = []

    for i, row in enumerate(basis):
        v = [Fraction(x) for x in row]
        for j in range(i):
            if norms[j] == 0:
                raise ValueError("Basis is linearly dependent.")
            mu[i][j] = _dot(row, orthogonal[j]) / norms[j]
            v = [v[k] - mu[i][j] * orthogonal[j][k]
                 for k in range(len(row))]
        orthogonal.append(v)
        norms.append(_dot(v, v))

    return orthogonal, mu, norms


def lll_reduce(basis, delta=Fraction(3, 4)):
    """Return an LLL-reduced copy of an integer row-basis."""
    if not basis:
        return []
    if not (Fraction(1, 4) < delta < 1):
        raise ValueError("delta must satisfy 1/4 < delta < 1.")
    width = len(basis[0])
    if any(len(row) != width for row in basis):
        raise ValueError("All basis rows must have the same length.")

    b = [[int(x) for x in row] for row in basis]
    if len(b) > width:
        raise ValueError("This implementation expects an independent row-basis.")

    _, mu, norms = gram_schmidt(b)
    k = 1

    while k < len(b):
        for j in range(k - 1, -1, -1):
            _, mu, norms = gram_schmidt(b)
            q = _nearest_integer(mu[k][j])
            if q:
                b[k] = [b[k][r] - q * b[j][r] for r in range(width)]

        _, mu, norms = gram_schmidt(b)
        if norms[k] >= (delta - mu[k][k - 1] ** 2) * norms[k - 1]:
            k += 1
        else:
            b[k], b[k - 1] = b[k - 1], b[k]
            _, mu, norms = gram_schmidt(b)
            k = max(k - 1, 1)

    return b
