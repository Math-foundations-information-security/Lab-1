def _factorize(n):
    factors = {}
    divisor = 2

    while divisor * divisor <= n:
        while n % divisor == 0:
            factors[divisor] = factors.get(divisor, 0) + 1
            n //= divisor

        divisor += 1

    if n > 1:
        factors[n] = factors.get(n, 0) + 1

    return factors

def _multiplicative_group_order(modulus):
    p = modulus.field.p
    n = modulus.degree

    if n < 1:
        raise ValueError(
            "Модуль должен иметь положительную степень"
        )

    return p ** n - 1

def _validate_unit(polynomial, modulus):
    if polynomial.is_zero():
        raise ValueError(
            "Нулевой многочлен не имеет мультипликативного порядка"
        )

    if polynomial.field != modulus.field:
        raise ValueError(
            "Многочлены должны принадлежать одному полю"
        )

    if polynomial.degree >= modulus.degree:
        polynomial = polynomial % modulus

    if polynomial.is_zero():
        raise ValueError(
            "Многочлен сравним с нулём по заданному модулю"
        )

def polynomial_order(polynomial, modulus):
    _validate_unit(polynomial, modulus)

    group_order = _multiplicative_group_order(modulus)
    factors = _factorize(group_order)

    order = group_order
    reduced_polynomial = polynomial % modulus

    for prime in factors:
        while order % prime == 0:
            candidate = order // prime

            if reduced_polynomial.pow_mod(
                candidate,
                modulus
            ).is_one():
                order = candidate
            else:
                break

    return order