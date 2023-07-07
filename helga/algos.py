from helga.ring import is_euclidean_domain, is_polynomial_ring, get_base_ring
from helga.polynomial import make_polynomial_ring, polynomial
from fractions import Fraction


def extended_ea(a, b, ring=int):
    (old_r, r) = (a, b)
    (old_s, s) = (ring(1), ring(0))
    (old_t, t) = (ring(0), ring(1))

    while r != ring(0):
        q = old_r // r
        (old_r, r) = (r, old_r - q * r)
        (old_s, s) = (s, old_s - q * s)
        (old_t, t) = (t, old_t - q * t)

    return (old_s, old_t)


def gcd(a, b, ring=int):
    if is_euclidean_domain(ring):
        u, v = extended_ea(a, b, ring=ring)
        return a * u + b * v

    if is_polynomial_ring(ring) and get_base_ring(ring) is int:
        return int_poly_gcd(a, b)

    raise NotImplementedError


def int_poly_gcd(a, b):
    content_gcd = gcd(a.content(), b.content(), ring=int)
    primitive_gcd = gcd(
        a.primitive_part().cast(Fraction),
        b.primitive_part().cast(Fraction),
        ring=make_polynomial_ring(Fraction),
    )
    return content_gcd * primitive_gcd.cast(int)

def inv(n, p):
    coeff = extended_ea(n, p)[0]
    if coeff < 1:
        coeff += p
    return coeff


def is_primitive_root(x, p):
    # TODO: only check primes
    for i in range(2, p - 1):
        if pow(x, i, p) == 1:
            return False
    return True


def find_primitive_root(p):
    for i in range(2, p - 1):
        if is_primitive_root(i, p):
            return i


def fft(vec, w, p):
    k = len(vec)
    if k == 1:
        return vec

    even = fft(vec[::2], pow(w, 2, p), p)
    odd = fft(vec[1::2], pow(w, 2, p), p)

    bottom = [(even[i] + pow(w, i, p) * odd[i]) % p for i in range(k // 2)]
    top = [(even[i] + pow(w, i + k // 2, p) * odd[i]) % p for i in range(k // 2)]

    return bottom + top


def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors
