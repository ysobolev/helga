import unittest

from helga.finite_field import make_finite_field, make_prime_field
from helga.polynomial import polynomial


class TestPrimeField(unittest.TestCase):
    def test_construction_from_int(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3).value, 3)
        self.assertEqual(F_7(30).value, 2)
        self.assertEqual(F_7(-4).value, 3)

    def test_eq(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3), F_7(3))

    def test_eq_duplicate_field(self):
        F_7 = make_prime_field(7)
        F_7a = make_prime_field(7)
        self.assertEqual(F_7(3), F_7a(3))

    def test_add(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3) + F_7(2), F_7(5))
        self.assertEqual(F_7(3) + F_7(4), F_7(0))
        self.assertEqual(F_7(3) + F_7(5), F_7(1))

    def test_iadd(self):
        F_7 = make_prime_field(7)
        x = F_7(3)
        x += F_7(5)
        self.assertEqual(x, F_7(1))

    def test_neg(self):
        F_7 = make_prime_field(7)
        self.assertEqual(-F_7(3), F_7(4))

    def test_sub(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3) - F_7(2), F_7(1))
        self.assertEqual(F_7(3) - F_7(4), F_7(6))

    def test_isub(self):
        F_7 = make_prime_field(7)
        x = F_7(3)
        x -= F_7(5)
        self.assertEqual(x, F_7(5))

    def test_mul(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(2) * F_7(3), F_7(6))
        self.assertEqual(F_7(3) * F_7(4), F_7(5))

    def test_imul(self):
        F_7 = make_prime_field(7)
        x = F_7(3)
        x *= F_7(4)
        self.assertEqual(x, F_7(5))

    def test_inverse(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3).inverse(), F_7(5))

    def test_div(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3) / F_7(4), F_7(6))

    def test_idiv(self):
        F_7 = make_prime_field(7)
        x = F_7(3)
        x /= F_7(4)
        self.assertEqual(x, F_7(6))

    def test_pow(self):
        F_7 = make_prime_field(7)
        self.assertEqual(F_7(3) ** 5, F_7(5))

    def test_exceptions(self):
        F_3 = make_prime_field(3)
        F_7 = make_prime_field(7)
        with self.assertRaises(TypeError):
            F_3(2) + F_7(4)
        with self.assertRaises(TypeError):
            F_3(2) - F_7(4)
        with self.assertRaises(TypeError):
            F_3(2) * F_7(4)
        with self.assertRaises(TypeError):
            F_3(2) / F_7(4)

        with self.assertRaises(TypeError):
            x = F_3(2)
            x += F_7(4)
        with self.assertRaises(TypeError):
            x = F_3(2)
            x -= F_7(4)
        with self.assertRaises(TypeError):
            x = F_3(2)
            x *= F_7(4)
        with self.assertRaises(TypeError):
            x = F_3(2)
            x /= F_7(4)


class TestNonPrimeField(unittest.TestCase):
    def test_construction_from_poly(self):
        F_7 = make_prime_field(7)
        F_343 = make_finite_field(7, 3, "x^3 - 3")
        self.assertEqual(
            F_343(polynomial("x^2 + 1", F_7)).value, polynomial("x^2 + 1", F_7)
        )
        self.assertEqual(F_343("x^2 + 1").value, polynomial("x^2 + 1", F_7))
        self.assertEqual(F_343("x^3 - 3").value, polynomial(0, F_7))
        self.assertEqual(F_343("x^4 + 2").value, polynomial("3x + 2", F_7))

    def test_inverse(self):
        F_7 = make_prime_field(7)
        F_343 = make_finite_field(7, 3, "x^3 - 3")
        self.assertEqual(F_343("x^2 + 1").inverse(), F_343("2x^2 + x + 5"))

    def test_pow(self):
        F_7 = make_prime_field(7)
        F_343 = make_finite_field(7, 3, "x^3 - 3")
        self.assertEqual(F_343("x^2 + 1") ** 2, F_343("2x^2 + 3x + 1"))
