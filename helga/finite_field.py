from helga.polynomial import polynomial
from helga.algos import is_irreducible

FIELDS = {}


def pick_irreducible_polynomial(p, n):
    F_p = make_prime_field(p)
    if p == 2:
        if n == 2:
            return polynomial("x^2 + x + 1", F_p)
        else:
            for k in range(1, n):
                poly = polynomial({n: 1, k: 1, 0: 1}, F_p)
                if is_irreducible(poly):
                    return poly
            for a in range(3, n):
                for b in range(2, a):
                    for c in range(1, b):
                        poly = polynomial({n: 1, a: 1, b: 1, c: 1, 0: 1}, F_p)
                        if is_irreducible(poly):
                            return poly
            raise RuntimeError("Could not find irreducible polynomial")
    else:
        for a in range(p):
            for b in range(p):
                poly = polynomial({n: 1, 1: a, 0: b}, F_p)
                if is_irreducible(poly):
                    return poly

    raise RuntimeError("Could not find irreducible polynomial")


def make_prime_field(p):
    return make_finite_field(p, 1)


def make_finite_field(p, n, irreducible_polynomial=None):
    name = f"F_{p ** n}"
    if name in FIELDS:
        return FIELDS[name]

    if n == 1:
        divisor = p
        base_field = None
    else:
        base_field = make_prime_field(p)
        if irreducible_polynomial is None:
            irreducible_polynomial = pick_irreducible_polynomial(p, n)
        divisor = irreducible_polynomial

    class FiniteFieldElement:
        def __init__(self, value):
            self.divisor = divisor
            if n == 1:
                self.base_field = self.__class__
            else:
                self.base_field = base_field
            self.field_characteristic = p

            # TODO: clean up this type check
            if n != 1 and not type(value).__name__.endswith("[x]"):
                value = polynomial(value, self.base_field)

            value = value % divisor
            if n == 1 and value < 0:
                value += self.divisor

            self.value = value

        def __eq__(self, rhs):
            return self.value == rhs.value

        def __bool__(self):
            return self.value != 0

        def __neg__(self):
            return self.__class__(-self.value)

        def __add__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            return self.__class__(self.value + rhs.value)

        def __iadd(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            self.value = (self + rhs).value
            return self

        def __sub__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            return self.__class__(self.value - rhs.value)

        def __isub__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            self.value = (self - rhs).value
            return self

        def __mul__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            return self.__class__(self.value * rhs.value)

        def __imul__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            self.value = (self * rhs).value
            return self

        def __truediv__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            return self * rhs.inverse()

        def __itruediv__(self, rhs):
            if self.__class__.__name__ != type(rhs).__name__:
                return NotImplemented

            self.value = (self / rhs).value
            return self

        def __pow__(self, power):
            if n == 1:
                return self.__class__(pow(self.value, power, self.field_characteristic))

            if power < 0:
                return self.inverse() ** -power
            elif power == 0:
                return self.__class__(1)
            elif power % 2 == 0:
                return (self * self) ** (power / 2)
            else:
                return self * (self * self) ** ((power - 1) / 2)

        def inverse(self):
            if n == 1:
                return self.__class__(pow(self.value, -1, self.field_characteristic))

            t = polynomial(0, self.base_field)
            new_t = polynomial(1, self.base_field)
            r = self.divisor
            new_r = self.value
            while new_r != polynomial(0, self.base_field):
                quotient = (r / new_r)[0]
                r, new_r = new_r, r - quotient * new_r
                t, new_t = new_t, t - quotient * new_t

            assert r.degree == 0

            return self.__class__(r.coefficients[0].inverse() * t)

        def __repr__(self):
            return f"{self.__class__.__name__}({self.value})"

        def __str__(self):
            return str(self.value)

    FiniteFieldElement.__name__ = name
    FiniteFieldElement.characteristic = p
    FIELDS[name] = FiniteFieldElement

    return FiniteFieldElement
