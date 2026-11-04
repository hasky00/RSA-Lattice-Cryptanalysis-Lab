"""Experimental univariate Coppersmith-style lattice construction.

Requires SymPy and fpylll. This is a research/teaching scaffold, not a
proof-producing implementation of all Coppersmith theorem variants.
"""

from dataclasses import dataclass


@dataclass
class SmallRootResult:
    candidates: list[int]
    lattice_dimension: int
    reduced_polynomials: list[str]


def build_univariate_lattice(f, modulus: int, X: int, m: int, t: int):
    """Build a scaled coefficient lattice for a monic univariate polynomial."""
    import sympy as sp

    x = sp.Symbol("x")
    poly = sp.Poly(f, x, domain=sp.ZZ)
    if poly.degree() < 1:
        raise ValueError("f must have positive degree.")
    if poly.LC() != 1:
        raise ValueError("The classical scaffold requires a monic polynomial.")
    if modulus <= 1 or X <= 0 or m < 1 or t < 0:
        raise ValueError("Require modulus > 1, X > 0, m >= 1, t >= 0.")

    delta = poly.degree()
    shifts = []
    for i in range(m):
        for j in range(delta):
            shifts.append(sp.Poly((x ** j) * (poly.as_expr() ** i)
                                  * (modulus ** (m - i)), x, domain=sp.ZZ))
    for j in range(t):
        shifts.append(sp.Poly((x ** j) * (poly.as_expr() ** m),
                              x, domain=sp.ZZ))

    dimension = delta * m + t
    rows = []
    for shift in shifts:
        scaled = sp.Poly(shift.as_expr().subs(x, X * x), x, domain=sp.ZZ)
        rows.append([int(scaled.nth(k)) for k in range(dimension)])

    if len(rows) != dimension:
        raise RuntimeError("Unexpected lattice dimension.")
    return rows


def recover_small_roots(f, modulus: int, X: int, m: int = 2, t: int = 1):
    """Run fpylll LLL and extract integer-root candidates from short rows."""
    import sympy as sp
    from fpylll import IntegerMatrix, LLL

    x = sp.Symbol("x")
    poly = sp.Poly(f, x, domain=sp.ZZ)
    rows = build_univariate_lattice(poly.as_expr(), modulus, X, m, t)
    matrix = IntegerMatrix.from_matrix(rows)
    LLL.reduction(matrix)

    candidates = set()
    reduced_polynomials = []
    dimension = len(rows)

    for i in range(dimension):
        coefficients = []
        for k in range(dimension):
            value = int(matrix[i, k])
            divisor = X ** k
            if value % divisor:
                break
            coefficients.append(value // divisor)
        else:
            if not any(coefficients):
                continue
            h = sp.Poly(sum(coefficients[k] * x ** k
                            for k in range(dimension)), x, domain=sp.ZZ)
            reduced_polynomials.append(str(h.as_expr()))
            for root in h.ground_roots():
                if getattr(root, "is_Integer", False):
                    value = int(root)
                    if abs(value) < X and int(poly.eval(value)) % modulus == 0:
                        candidates.add(value)

    return SmallRootResult(sorted(candidates), dimension, reduced_polynomials)


def root_bound_reference(modulus: int, degree: int, epsilon: float = 0.01):
    """Return an indicative N^(1/delta-epsilon) bound, not a proof checker."""
    if modulus <= 1 or degree < 1 or epsilon <= 0:
        raise ValueError("Invalid bound parameters.")
    return modulus ** (1.0 / degree - epsilon)
