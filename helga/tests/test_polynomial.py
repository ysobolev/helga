import unittest

from helga.polynomial import parse_polynomial_string, Polynomial
from helga.finite_field import make_prime_field


class TestParsePolynomialString(unittest.TestCase):
    def test_constants(self):
        self.assertEqual(parse_polynomial_string("1"), {0: 1})
        self.assertEqual(parse_polynomial_string("-1"), {0: -1})
        self.assertEqual(parse_polynomial_string("5"), {0: 5})
        self.assertEqual(parse_polynomial_string("-5"), {0: -5})
        self.assertEqual(parse_polynomial_string("0"), {0: 0})

    def test_empty(self):
        self.assertEqual(parse_polynomial_string(""), {0: 0})

    def test_linear_term(self):
        self.assertEqual(parse_polynomial_string("x"), {1: 1})
        self.assertEqual(parse_polynomial_string("-x"), {1: -1})
        self.assertEqual(parse_polynomial_string("2x"), {1: 2})
        self.assertEqual(parse_polynomial_string("-2x"), {1: -2})
        self.assertEqual(parse_polynomial_string("3 x"), {1: 3})
        self.assertEqual(parse_polynomial_string("- 3 x"), {1: -3})

    def test_monomial(self):
        self.assertEqual(parse_polynomial_string("x^2"), {2: 1})
        self.assertEqual(parse_polynomial_string("-x^2"), {2: -1})
        self.assertEqual(parse_polynomial_string("2x^3"), {3: 2})
        self.assertEqual(parse_polynomial_string("-2x^3"), {3: -2})
        self.assertEqual(parse_polynomial_string("3 x^4"), {4: 3})
        self.assertEqual(parse_polynomial_string("- 3 x ^ 4"), {4: -3})

    def test_polynomial(self):
        self.assertEqual(parse_polynomial_string("x^2 - x + 5x^3"), {1: -1, 2: 1, 3: 5})
        self.assertEqual(parse_polynomial_string("x^2 - 4 + 5x^3"), {0: -4, 2: 1, 3: 5})
        self.assertEqual(parse_polynomial_string("5x^3 + 4"), {0: 4, 3: 5})

    def test_duplicate(self):
        self.assertEqual(parse_polynomial_string("0 + 2 + 3"), {0: 5})
        self.assertEqual(parse_polynomial_string("2 + x^2 - 3"), {0: -1, 2: 1})

    def test_malformed(self):
        self.assertEqual(parse_polynomial_string("x + -1"), {0: -1, 1: 1})
        self.assertEqual(parse_polynomial_string("5 + x + -1"), {0: 4, 1: 1})
        self.assertEqual(parse_polynomial_string("5 + x - +1"), {0: 4, 1: 1})
        self.assertEqual(parse_polynomial_string("5 + - x"), {0: 5, 1: -1})
        self.assertEqual(parse_polynomial_string("5 - + x"), {0: 5, 1: -1})


class TestPolynomial(unittest.TestCase):
    def test_construction_from_dict(self):
        poly = Polynomial({0: 1, 2: 4, 3: 5}, int)
        self.assertEqual(poly.coefficients, {0: 1, 2: 4, 3: 5})
        self.assertEqual(poly.ring, int)

    def test_construction_from_list(self):
        poly = Polynomial([1, 0, 4, 5], int)
        self.assertEqual(poly.coefficients, {0: 1, 2: 4, 3: 5})
        self.assertEqual(poly.ring, int)

    def test_construction_from_tuple(self):
        poly = Polynomial((1, 0, 4, 5), int)
        self.assertEqual(poly.coefficients, {0: 1, 2: 4, 3: 5})
        self.assertEqual(poly.ring, int)

    def test_construction_from_string(self):
        poly = Polynomial("1 + 4x^2 + 5x^3", int)
        self.assertEqual(poly.coefficients, {0: 1, 2: 4, 3: 5})
        self.assertEqual(poly.ring, int)

    def test_construction_from_constant(self):
        poly = Polynomial(1, int)
        self.assertEqual(poly.coefficients, {0: 1})
        self.assertEqual(poly.ring, int)

    def test_construction_with_cast(self):
        F_3 = make_prime_field(3)
        poly = Polynomial({0: 1, 2: 4, 3: 5}, F_3)
        self.assertEqual(poly.coefficients, {0: F_3(1), 2: F_3(1), 3: F_3(2)})
        self.assertEqual(poly.ring, F_3)

    def test_construction_with_inference(self):
        F_3 = make_prime_field(3)
        poly = Polynomial({0: F_3(1), 2: F_3(1), 3: F_3(2)})
        self.assertEqual(poly.coefficients, {0: F_3(1), 2: F_3(1), 3: F_3(2)})
        self.assertEqual(poly.ring, F_3)

    def test_polynomial_degree(self):
        self.assertEqual(Polynomial("1 + 4x^2 + 5x^3").degree, 3)
        self.assertEqual(Polynomial("1").degree, 0)
        self.assertEqual(Polynomial("0").degree, -1)
        self.assertEqual(Polynomial("").degree, -1)

    def test_evaluate(self):
        poly = Polynomial("1 + 4x^2 + 5x^3")
        self.assertEqual(poly.evaluate(2), 57)

    def test_evaluate_finite_field(self):
        F_11 = make_prime_field(11)
        poly = Polynomial("1 + 4x^2 + 5x^3", F_11)
        self.assertEqual(poly.evaluate(F_11(2)), F_11(2))

    def test_polynomial_eq(self):
        poly1 = Polynomial("x + x^3")
        poly2 = Polynomial("x + x^3")
        self.assertEqual(poly1, poly2)

    def test_polynomial_add(self):
        poly1 = Polynomial("x + x^3")
        poly2 = Polynomial("x^2 - 2x^3")
        self.assertEqual(poly1 + poly2, Polynomial("x + x^2 - x^3"))

    def test_polynomial_iadd(self):
        poly = Polynomial("x + x^3")
        poly += Polynomial("x^2 - 2x^3")
        self.assertEqual(poly, Polynomial("x + x^2 - x^3"))

    def test_polynomial_neg(self):
        poly = Polynomial("x + x^3")
        self.assertEqual(-poly, Polynomial("- x - x^3"))

    def test_polynomial_sub(self):
        poly1 = Polynomial("x + x^3")
        poly2 = Polynomial("x^2 - 2x^3")
        self.assertEqual(poly1 - poly2, Polynomial("x - x^2 + 3x^3"))

    def test_polynomial_isub(self):
        poly = Polynomial("x + x^3")
        poly -= Polynomial("x^2 - 2x^3")
        self.assertEqual(poly, Polynomial("x - x^2 + 3x^3"))

    def test_polynomial_mul(self):
        poly1 = Polynomial("1 + x^2")
        poly2 = Polynomial("x^2 - 2x^4")
        self.assertEqual(poly1 * poly2, Polynomial("x^2 - x^4 - 2x^6"))

    def test_polynomial_imul(self):
        poly = Polynomial("1 + x^2")
        poly *= Polynomial("x^2 - 2x^4")
        self.assertEqual(poly, Polynomial("x^2 - x^4 - 2x^6"))

    def test_polynomial_scalar_mul(self):
        poly = Polynomial("1 + x^2")
        self.assertEqual(poly * 5, Polynomial("5 + 5x^2"))

    def test_polynomial_scalar_imul(self):
        poly = Polynomial("1 + x^2")
        poly *= 5
        self.assertEqual(poly, Polynomial("5 + 5x^2"))

    def test_polynomial_scalar_rmul(self):
        poly = Polynomial("1 + x^2")
        self.assertEqual(5 * poly, Polynomial("5 + 5x^2"))

    def test_polynomial_div(self):
        poly1 = Polynomial("- 1 + x^2")
        poly2 = Polynomial("x")
        quotient, remainder = poly1 / poly2
        self.assertEqual(quotient, Polynomial("x"))
        self.assertEqual(remainder, Polynomial("- 1"))

        F_7 = make_prime_field(7)
        poly3 = Polynomial("- 1 + x^2", F_7)
        poly4 = Polynomial("3", F_7)
        quotient, remainder = poly3 / poly4
        self.assertEqual(quotient, Polynomial("5x^2 + 2", F_7))
        self.assertEqual(remainder, Polynomial("0", F_7))

    def test_polynomial_mod(self):
        poly1 = Polynomial("- 1 + x^2")
        poly2 = Polynomial("x")
        self.assertEqual(poly1 % poly2, Polynomial("- 1"))

    def test_polynomial_imod(self):
        poly = Polynomial("- 1 + x^2")
        poly %= Polynomial("x")
        self.assertEqual(poly, Polynomial("- 1"))

    def test_exceptions(self):
        with self.assertRaises(TypeError):
            Polynomial("x") + "foo"
        with self.assertRaises(TypeError):
            Polynomial("x") - "foo"
        with self.assertRaises(TypeError):
            Polynomial("x") * "foo"
        with self.assertRaises(TypeError):
            Polynomial("x") / "foo"
        with self.assertRaises(TypeError):
            Polynomial("x") % "foo"

        with self.assertRaises(TypeError):
            poly = Polynomial("x")
            poly += "foo"
        with self.assertRaises(TypeError):
            poly = Polynomial("x")
            poly -= "foo"
        with self.assertRaises(TypeError):
            poly = Polynomial("x")
            poly *= "foo"
        with self.assertRaises(TypeError):
            poly = Polynomial("x")
            poly /= "foo"
        with self.assertRaises(TypeError):
            poly = Polynomial("x")
            poly %= "foo"

        F_3 = make_prime_field(3)
        F_7 = make_prime_field(7)
        with self.assertRaises(TypeError):
            Polynomial("x") + Polynomial("x", F_3)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) + Polynomial("x", F_7)
        with self.assertRaises(TypeError):
            Polynomial("x") - Polynomial("x", F_3)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) - Polynomial("x", F_7)
        with self.assertRaises(TypeError):
            Polynomial("x") * Polynomial("x", F_3)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) * Polynomial("x", F_7)
        with self.assertRaises(TypeError):
            Polynomial("x") / Polynomial("x", F_3)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) / Polynomial("x", F_7)
        with self.assertRaises(TypeError):
            Polynomial("x") % Polynomial("x", F_3)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) % Polynomial("x", F_7)

        with self.assertRaises(TypeError):
            Polynomial("x") * F_3(2)
        with self.assertRaises(TypeError):
            Polynomial("x", F_3) * F_7(2)
