from helga.projective_geometry import ProjectivePoint
from helga.ring import get_base_ring, is_field, get_characteristic, Q


def make_elliptic_curve(a, b, generator=None, field=None):
    """Create an elliptic curve of the form y^2=x^3+ax+b.
    
    The field characteristic must not be 2 or 3.
    """

    if field is None:
        field = Q

    assert is_field(field)
    assert get_characteristic(field) not in (2, 3)

    point_at_infinity = ProjectivePoint((0, 1, 0), field)

    class EllipticCurvePoint:
        def __init__(self, point):
            self.a = field(a)
            self.b = field(b)

            if isinstance(point, self.__class__):
                self.point = point.point
            elif isinstance(point, ProjectivePoint):
                self.point = point
            elif isinstance(point, (tuple, list)):
                self.point = ProjectivePoint(point, field)
            else:
                raise ValueError("no known conversions")

        @classmethod
        def identity(cls):
            return cls(point_at_infinity)
        
        @classmethod
        def generator(cls):
            return cls(generator)

        def is_inf(self):
            # Return if this point is the point at infinity
            return self.point == point_at_infinity

        def __eq__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented
            
            return self.point == rhs.point

        def __neg__(self):
            if self.is_inf():
                return self

            return self.__class__(ProjectivePoint((self.point[0], -self.point[1], self.point[2]), field))

        def __add__(self, rhs):
            if not isinstance(rhs, self.__class__):
                return NotImplemented

            if self.is_inf():
                return rhs

            if rhs.is_inf():
                return self

            if self.point[0] == rhs.point[0]:
                if self.point[1] == -rhs.point[1]:
                    return self.__class__(point_at_infinity)

                # tangent line
                m = (field(3)*self.point[0]**2 + self.a) / (field(2) * self.point[1])
            else:
                # secant line
                m = (self.point[1] - rhs.point[1]) / (self.point[0] - rhs.point[0])

            x = m**2 - self.point[0] - rhs.point[0]
            y = -self.point[1] + m*(self.point[0] - x)

            return self.__class__(ProjectivePoint((x, y, field(1)), field))

        def __mul__(self, n):
            n = int(n)

            if n < 0:
                return -self * -n
            elif n == 0:
                return self.__class__.identity()
            elif n % 2 == 0:
                return (self + self) * (n / 2)
            else:
                return self + self * (n - 1)

        def __rmul__(self, n):
            return self * n

        def __repr__(self):
            return f"{self.__class__.__name__}({self.point})"

    return EllipticCurvePoint
