def extended_ea(a, b):
    assert a > 0
    assert b > 0

    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)

    while r != 0:
        q = old_r // r
        (old_r, r) = (r, old_r - q * r)
        (old_s, s) = (s, old_s - q * s)
        (old_t, t) = (t, old_t - q * t)

    return (old_s, old_t)


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
