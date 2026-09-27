import itertools

from .mobius import mobius, prime_divisors
from .polynomial import Polynomial
from .gcd import gcd

def divisors(n):
    result = []

    d = 1
    while d * d <= n:
        if n % d == 0:
            result.append(d)

            if d != n // d:
                result.append(n // d)

        d += 1

    return sorted(result)

def _monic(f):
    lead = f.coefficients[-1]

    return f.scalar_mul(f.field.inverse(lead))

def _x(field):
    return Polynomial([0, 1], field)

def x_pk_minus_x_mod(field, k, modulus):
    p = field.p

    result = _x(field)

    for _ in range(k):
        result = result.pow_mod(p, modulus)

    return result - _x(field)

def build_table_polynomial(field, n, max_power=1 << 12):
    p = field.p

    if p ** n > max_power:
        raise ValueError(
            "Слишком большое p^n для явного построения таблицы"
        )

    def binomial(k):
        coefficients = [0] * (p ** k + 1)
        coefficients[1] = p - 1
        coefficients[-1] = 1

        return Polynomial(coefficients, field)

    numerator = Polynomial([1], field)
    denominator = Polynomial([1], field)

    for d in divisors(n):
        mu = mobius(d)

        if mu == 1:
            numerator = numerator * binomial(n // d)
        elif mu == -1:
            denominator = denominator * binomial(n // d)

    quotient, remainder = numerator.divmod(denominator)

    if not remainder.is_zero():
        raise ArithmeticError(
            "T_{p,n} построен неверно: деление нацело не получилось"
        )

    return quotient

def is_irreducible_by_table(f):
    if f.is_zero() or f.degree < 1:
        return False

    n = f.degree

    if n == 1:
        return True

    field = f.field
    f = _monic(f)

    numerator = Polynomial([1], field)
    denominator = Polynomial([1], field)

    for d in divisors(n):
        mu = mobius(d)

        if mu == 0:
            continue

        factor = x_pk_minus_x_mod(field, n // d, f)

        if mu == 1:
            numerator = (numerator * factor) % f
        else:
            denominator = (denominator * factor) % f

    try:
        inverse = denominator.inverse_mod(f)
    except ValueError:
        return False

    return ((numerator * inverse) % f).is_zero()

def is_irreducible_by_criterion(f):
    if f.is_zero() or f.degree < 1:
        return False

    n = f.degree

    if n == 1:
        return True

    field = f.field
    f = _monic(f)

    if not x_pk_minus_x_mod(field, n, f).is_zero():
        return False

    for q in prime_divisors(n):
        h = x_pk_minus_x_mod(field, n // q, f)

        if not gcd(f, h).is_one():
            return False

    return True

def find_irreducible(field, n, count=1):
    p = field.p
    found = []

    for constant in range(1, p):
        for tail in itertools.product(range(p), repeat=n - 1):
            candidate = Polynomial(
                [constant] + list(tail) + [1],
                field
            )

            if is_irreducible_by_criterion(candidate):
                found.append(candidate)

                if len(found) == count:
                    return found

    return found