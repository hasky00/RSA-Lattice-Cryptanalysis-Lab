import pytest


def test_coppersmith_lattice_builder_has_expected_dimension():
    sp = pytest.importorskip("sympy")
    pytest.importorskip("fpylll")
    from rsa_lab.coppersmith import build_univariate_lattice
    x = sp.Symbol("x")
    rows = build_univariate_lattice(x - 7, modulus=101 * 113, X=10, m=2, t=1)
    assert len(rows) == 3
    assert all(len(row) == 3 for row in rows)
