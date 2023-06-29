from helga.polynomial import Polynomial


def make_prime_field(p):
    return make_finite_field(p, 1)


def make_finite_field(p, n, irreducible_polynomial_string=None):
    if n == 1:
        divisor = p
        base_field = None
    else:
        base_field = make_prime_field(p)
        if irreducible_polynomial_string is None:
            raise NotImplementedError("TODO: pick irreducible polynomial")
        else:
            irreducible_polynomial = Polynomial(
                irreducible_polynomial_string, base_field
            )
        divisor = irreducible_polynomial

    class FiniteFieldElement:
        def __init__(self, value):
            self.divisor = divisor
            if n == 1:
                self.base_field = self.__class__
            else:
                self.base_field = base_field
            self.field_characteristic = p

            if n != 1 and type(value) is not Polynomial:
                value = Polynomial(value, self.base_field)

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

            t = Polynomial(0, self.base_field)
            new_t = Polynomial(1, self.base_field)
            r = self.divisor
            new_r = self.value
            while new_r != Polynomial(0, self.base_field):
                quotient = (r / new_r)[0]
                r, new_r = new_r, r - quotient * new_r
                t, new_t = new_t, t - quotient * new_t

            assert r.degree == 0

            return self.__class__(r.coefficients[0].inverse() * t)

        def __repr__(self):
            return f"{self.__class__.__name__}({self.value})"

        def __str__(self):
            return str(self.value)

    FiniteFieldElement.__name__ = f"F_{p ** n}"

    return FiniteFieldElement
