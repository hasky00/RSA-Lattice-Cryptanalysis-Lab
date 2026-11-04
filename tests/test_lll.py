from fractions import Fraction
from rsa_lab.lll import lll_reduce, gram_schmidt


def test_lll_returns_integer_basis_same_rank():
    basis = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    reduced = lll_reduce(basis, delta=Fraction(3, 4))
    assert len(reduced) == len(basis)
    assert all(len(row) == 3 for row in reduced)
    assert all(isinstance(x, int) for row in reduced for x in row)
    _, _, norms = gram_schmidt(reduced)
    assert all(norm > 0 for norm in norms)


def test_lll_reduction_is_not_longer_first_vector():
    basis = [[1, 1, 1], [-1, 0, 2], [3, 5, 6]]
    reduced = lll_reduce(basis)
    norm = lambda row: sum(x*x for x in row)
    assert norm(reduced[0]) <= norm(basis[0])
