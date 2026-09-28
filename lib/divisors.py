def divisors(n):
    if n < 1:
        raise ValueError(
            "Число должно быть положительным"
        )

    result = []

    d = 1
    while d * d <= n:
        if n % d == 0:
            result.append(d)

            if d != n // d:
                result.append(n // d)

        d += 1

    return sorted(result)