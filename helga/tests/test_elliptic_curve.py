from helga.finite_field import make_finite_field
from helga.projective_geometry import ProjectivePoint
from helga.elliptic_curve import make_elliptic_curve

from unittest import TestCase


class TestEllipticCurve(TestCase):
    def test_addition_identity(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, field=F_101)
        point = EC((13, 2, 1))
        self.assertEqual(point + EC.identity(), point)
    
    def test_addition_negative(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, field=F_101)
        point1 = EC((13, 2, 1))
        point2 = EC((13, -2, 1))
        self.assertEqual(point1 + point2, EC.identity())
    
    def test_addition_secant(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, field=F_101)
        point1 = EC((13, 2, 1))
        point2 = EC((3, 95, 1))
        self.assertEqual(point1 + point2, EC((21, 32, 1)))
    
    def test_addition_tangent(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, field=F_101)
        point = EC((13, 2, 1))
        self.assertEqual(point + point, EC((76, 36, 1)))

    def test_negation(self):
        F_101 = make_finite_field(101, 1)
        EC = make_elliptic_curve(2, 3, field=F_101)
        point = EC((13, 2, 1))
        self.assertEqual(-point, EC((13, 99, 1)))

    def test_multiplication(self):
        F_101 = make_finite_field(101, 1)
        generator = ProjectivePoint((52, 74, 1), F_101)
        EC = make_elliptic_curve(2, 3, generator, field=F_101)
        point = EC((13, 2, 1))
        self.assertEqual(point * -1, EC((13, 99, 1)))
        self.assertEqual(point * 0, EC((0, 1, 0)))
        self.assertEqual(point * 1, point)
        self.assertEqual(point * 5, EC((81, 89, 1)))

