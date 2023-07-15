from helga.finite_field import make_finite_field
from helga.elliptic_curve import make_elliptic_curve

from unittest import TestCase


class TestEllipticCurve(TestCase):
    def test_addition_identity(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, F_101)
        point = EC((13, 2, 1))
        self.assertEqual(point + EC.identity(), point)
    
    def test_addition_negative(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, F_101)
        point1 = EC((13, 2, 1))
        point2 = EC((13, -2, 1))
        self.assertEqual(point1 + point2, EC.identity())
    
    def test_addition_secant(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, F_101)
        point1 = EC((13, 2, 1))
        point2 = EC((3, 95, 1))
        self.assertEqual(point1 + point2, EC((21, 32, 1)))
    
    def test_addition_tangent(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, F_101)
        point = EC((13, 2, 1))
        self.assertEqual(point + point, EC((76, 36, 1)))
