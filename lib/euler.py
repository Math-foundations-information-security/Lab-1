from .mobius import prime_divisors

def euler_phi(n):
    if n < 1:
        raise ValueError("Аргумент должен быть положительным")

    if n == 1:
        return 1

    result = n

    for p in prime_divisors(n):
        result -= result // p

    return result