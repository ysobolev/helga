from fractions import Fraction


def infer_ring(values):
    if not len(values):
        return int

    return type(next(iter(values)))


def rings_equal(lhs, rhs):
    return lhs.__name__ == rhs.__name__


def is_polynomial_ring(ring):
    return ring.__name__.endswith("[x]")


def get_base_ring(ring):
    assert is_polynomial_ring(ring)

    return ring.base_ring


def is_field(ring):
    return ring is Fraction or ring.__name__.startswith("F")


def field_of_fractions(ring):
    if ring is not int:
        raise NotImplementedError

    return Fraction


def is_euclidean_domain(ring):
    if ring is int:
        return True

    if is_field(ring):
        return True

    if is_polynomial_ring(ring) and is_field(get_base_ring(ring)):
        return True

    return False


def is_ufd(ring):
    if ring in [int, Fraction]:
        return True

    if is_field(ring):
        return True

    if is_polynomial_ring(ring) and is_ufd(get_base_ring(ring)):
        return True

    return False
