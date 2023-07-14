from unittest import TestCase
from helga.projective_geometry import ProjectivePoint
from fractions import Fraction


class TestProjectivePoint(TestCase):
    def test_construction(self):
        point = ProjectivePoint([Fraction(1, 2), Fraction(2, 3)])
        point2 = ProjectivePoint([3, 4], field=Fraction)
        self.assertEqual(point.field, Fraction)
        self.assertEqual(point2.field, Fraction)

    def test_eq(self):
        point = ProjectivePoint([Fraction(1, 2), Fraction(2, 3)])
        point2 = ProjectivePoint([3, 4], field=Fraction)
        self.assertEqual(point, point2)
