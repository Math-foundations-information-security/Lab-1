def prime_divisors(n):
    result = []
    d = 2

    while d * d <= n:
        if n % d == 0:
            result.append(d)

            while n % d == 0:
                n //= d

        d += 1

    if n > 1:
        result.append(n)

    return result

def mobius(n):
    if n == 1:
        return 1

    divisors = prime_divisors(n)

    product = 1

    for p in divisors:
        product *= p

    if product != n:
        return 0

    if len(divisors) % 2 == 0:
        return 1

    return -1