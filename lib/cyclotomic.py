from .polynomial import Polynomial


def integer_divisors(n):
    if n < 1:
        raise ValueError(
            "Число должно быть положительным"
        )

    divisors = []
    divisor = 1

    while divisor * divisor <= n:
        if n % divisor == 0:
            divisors.append(divisor)

            if divisor != n // divisor:
                divisors.append(n // divisor)

        divisor += 1

    return sorted(divisors)

def x_power_minus_one(n, field):
    coefficients = [0] * (n + 1)

    coefficients[0] = -1
    coefficients[n] = 1

    return Polynomial(coefficients, field)

def _cyclotomic_recursive(n, field, cache):
    if n in cache:
        return cache[n]

    result = x_power_minus_one(n, field)

    divisors = integer_divisors(n)

    proper_divisors = [
        divisor
        for divisor in divisors
        if divisor < n
    ]

    for divisor in proper_divisors:
        factor = _cyclotomic_recursive(
            divisor,
            field,
            cache
        )

        quotient, remainder = result.divmod(factor)

        if not remainder.is_zero():
            raise ArithmeticError(
                "При построении кругового многочлена получен ненулевой остаток"
            )

        result = quotient

    cache[n] = result

    return result

def build_cyclotomic(n, field):
    if n < 1:
        raise ValueError(
            "Номер кругового многочлена должен быть положительным"
        )

    cache = {}

    return _cyclotomic_recursive(
        n,
        field,
        cache
    )