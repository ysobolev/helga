from fractions import Fraction
from helga.algos import gcd
import re


def parse_polynomial_string(s, var="x"):
    """Parse string representation of polynomial into coefficients.

    Returns dictionary mapping degree to coefficient.
    """

    s = s.replace(" ", "")
    s = s.strip()
    if not s:
        return {0: 0}

    # the first term does not need to have a sign, but add one for uniformity of parsing
    if s[0] not in "+-":
        s = "+" + s

    coefficients = {}
    while s:
        match = re.match("[+-]+[\d\./]*", s)
        if match is None:
            coefficient = None
        else:
            s = s[len(match.group(0)) :]
            coefficient_string = match.group(0)
            if coefficient_string.startswith("+-") or coefficient_string.startswith(
                "-+"
            ):
                coefficient_string = "-" + coefficient_string[2:]
            try:
                coefficient = Fraction(coefficient_string)
                if coefficient.denominator == 1:
                    coefficient = coefficient.numerator
            except ValueError:
                coefficient = int(coefficient_string + "1")

        match = re.match(var, s)
        if match is None:
            coefficients[0] = coefficients.setdefault(0, 0) + coefficient
            continue
        else:
            s = s[len(match.group(0)) :]

        match = re.match("\^", s)
        if match is None:
            coefficients[1] = coefficients.setdefault(1, 0) + coefficient
            continue
        else:
            s = s[len(match.group(0)) :]

        match = re.match("\d+", s)
        if match is None:
            raise ValueError("Dangling exponent")
        s = s[len(match.group(0)) :]
        degree = int(match.group(0))
        coefficients[degree] = coefficients.setdefault(degree, 0) + coefficient

    return coefficients


def polynomial(coefficients=None, ring=None):
    """Create a polynomial.

    Coefficients can be a string, list, or dictionary mapping degree to value.

    If the ring is not provided, it is inferred. If it is provided, all terms are cast to it.
    """

    if coefficients is None:
        coefficients = {}

    if isinstance(coefficients, str):
        coefficients = parse_polynomial_string(coefficients)
    elif isinstance(coefficients, (list, tuple)):
        coefficients = {i: value for i, value in enumerate(coefficients)}
    elif not isinstance(coefficients, dict):
        coefficients = {0: coefficients}

    if ring is None and not coefficients:
        ring = int

    if ring is None and coefficients:
        types = [type(coefficient) for coefficient in coefficients.values()]
        if Fraction in types:
            ring = Fraction
        else:
            ring = types[0]

    return make_polynomial_ring(ring)(coefficients)


RINGS = {}


def make_polynomial_ring(base_ring):
    name = f"{base_ring.__name__}[x]"
    if name in RINGS:
        return RINGS[name]

    class RingElement:
        def __init__(self, coefficients=None):
            if coefficients is None:
                coefficients = {}

            for key, value in coefficients.items():
                if not isinstance(value, base_ring):
                    coefficients[key] = base_ring(value)

            coefficients = {
                degree: coefficient
                for degree, coefficient in coefficients.items()
                if coefficient != base_ring(0)
            }

            self.coefficients = coefficients
            self.ring = base_ring
            self.indeterminate = "x"

        def __reduce__(self):
            # This allows the class to be pickled.
            return (polynomial, (self.coefficients,))

        def __eq__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            return self.coefficients == rhs.coefficients

        def __add__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            coefficients = self.coefficients.copy()
            for degree, coefficient in rhs.coefficients.items():
                coefficients[degree] = (
                    coefficients.setdefault(degree, self.ring(0)) + coefficient
                )

            return self.__class__(coefficients)

        def __iadd__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            self.coefficients = (self + rhs).coefficients
            return self

        def __neg__(self):
            coefficients = {
                degree: -coefficient
                for degree, coefficient in self.coefficients.items()
            }
            return self.__class__(coefficients)

        def __sub__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            return self + -rhs

        def __isub__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            self.coefficients = (self - rhs).coefficients
            return self

        def __mul__(self, rhs):
            if type(rhs).__name__ == self.ring.__name__:
                coefficients = {
                    degree: coefficient * rhs
                    for degree, coefficient in self.coefficients.items()
                }
                return self.__class__(coefficients)
            elif isinstance(rhs, self.__class__):
                coefficients = {}
                for degree1, coefficient1 in self.coefficients.items():
                    for degree2, coefficient2 in rhs.coefficients.items():
                        degree = degree1 + degree2
                        coefficient = coefficient1 * coefficient2
                        coefficients[degree] = (
                            coefficients.setdefault(degree, self.ring(0)) + coefficient
                        )

                return self.__class__(coefficients)

            return NotImplemented

        def __imul__(self, rhs):
            if (
                isinstance(rhs, self.__class__)
                or type(rhs).__name__ == self.ring.__name__
            ):
                self.coefficients = (self * rhs).coefficients
                return self

            return NotImplemented

        def __rmul__(self, lhs):
            if type(lhs).__name__ != self.ring.__name__:
                return NotImplemented

            return self * lhs

        def __truediv__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            assert rhs.degree >= 0

            if self.ring is int and rhs.coefficients[rhs.degree] != self.ring(1):
                raise ValueError("divisor is not monic")

            quotient = self.__class__({})
            remainder = self.__class__(self.coefficients.copy())

            while remainder.degree >= rhs.degree:
                s = self.__class__(
                    {
                        remainder.degree
                        - rhs.degree: remainder.coefficients[remainder.degree]
                        / rhs.coefficients[rhs.degree]
                    }
                )
                quotient += s
                remainder -= s * rhs
            return quotient, remainder

        def __floordiv__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            quotient, remainder = self / rhs
            return quotient

        def __ifloordiv__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            self.coefficients = (self // rhs).coefficients
            return self

        def __mod__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            return (self / rhs)[1]

        def __imod__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            self.coefficients = (self % rhs).coefficients
            return self

        def evaluate(self, point):
            assert type(point).__name__ == self.ring.__name__

            accum = self.ring(0)
            for degree, coefficient in self.coefficients.items():
                accum += coefficient * point**degree

            return accum

        @property
        def degree(self):
            if len(self.coefficients) == 0:
                return -1
            return max(self.coefficients.keys())

        def content(self):
            if self.ring is int:
                coefficients = list(self.coefficients.values())
                if len(coefficients) == 0:
                    return 0

                if len(coefficients) == 1:
                    return coefficients[0]

                accum = coefficients[0]
                for i in range(1, len(coefficients)):
                    accum = gcd(accum, coefficients[i])

                return accum

            elif self.ring is Fraction:
                max_denom = max(x.denominator for x in self.coefficients.values())
                int_poly = polynomial(
                    {
                        degree: (coefficient * max_denom).numerator
                        for degree, coefficient in self.coefficients.items()
                    },
                    ring=int,
                )
                return Fraction(int_poly.content()) / Fraction(max_denom)

            return self.ring(1)

        def primitive_part(self):
            if self.ring is not int and self.ring is not Fraction:
                return self

            content = self.content()
            coefficients = {
                degree: coefficient / content
                for degree, coefficient in self.coefficients.items()
            }
            return polynomial(coefficients, int)

        def __repr__(self):
            def make_var_str(degree):
                if degree == 0:
                    return ""
                elif degree == 1:
                    return self.indeterminate
                else:
                    return f"{self.indeterminate}^{degree}"

            def make_coefficient_str(coefficient, degree):
                value = str(coefficient)
                if value == "1":
                    if degree != 0:
                        value = " + "
                    else:
                        value = " + 1"
                elif value == "-1":
                    if degree != 0:
                        value = " - "
                    else:
                        value = " - 1"
                elif value.startswith("-"):
                    value = " - " + value[1:]
                else:
                    value = " + " + value
                return value

            polynomial_string = (
                "".join(
                    make_coefficient_str(coefficient, degree) + make_var_str(degree)
                    for degree, coefficient in self.coefficients.items()
                )
                .strip()
                .strip("+")
                .strip()
            )

            if self.ring == int:
                return f'polynomial("{polynomial_string}")'

            return f'polynomial("{polynomial_string}", {self.ring.__name__})'

    RingElement.__name__ = name
    RINGS[name] = RingElement

    return RingElement
