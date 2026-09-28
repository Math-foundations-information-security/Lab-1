import time

from lib.field import Field
from lib.polynomial import Polynomial
from lib.gcd import gcd, extended_gcd
from lib.mobius import mobius
from lib.euler import euler_phi
from lib.irreducibility import (
    build_table_polynomial,
    is_irreducible_by_table,
    is_irreducible_by_criterion,
    find_irreducible,
)

def demo_arithmetic(field):
    print("Конечное поле:", field, "\n")

    f = Polynomial([1, 1, 0, 1], field)
    g = Polynomial([1, 1, 1], field)

    print("f(x) =", f)
    print("g(x) =", g, "\n")

    print("f + g =", f + g)
    print("f - g =", f - g)
    print("f * g =", f * g)

    quotient, remainder = f.divmod(g)

    print("f / g:")
    print("  частное =", quotient)
    print("  остаток  =", remainder)
    print("f // g =", f // g)
    print("f % g  =", f % g, "\n")

    print("НОД(f, g) =", gcd(f, g), "\n")

    d, s, t = extended_gcd(f, g)

    print("Расширенный алгоритм Евклида:")
    print("gcd =", d)
    print("s   =", s)
    print("t   =", t)
    print("Проверка s*f + t*g =", s * f + t * g, "\n")


def demo_mobius():
    print("Функция Мёбиуса:")

    for n in range(1, 18):
        print(f"M({n}) = {mobius(n)}")

    print()

def demo_tables():
    print("Таблицы неприводимых многочленов T_{p,n}:")

    for p, n in [(2, 2), (2, 3), (2, 4), (3, 3)]:
        field = Field(p)
        table = build_table_polynomial(field, n)

        print(f"T_{p},{n}(x) =", table)

    print()


def demo_irreducibility():
    print("Проверка неприводимости (таблица и критерий Рабина):")

    tests = [
        (2, [1, 1, 1],        "x^2 + x + 1 над F2"),
        (2, [1, 0, 1],        "x^2 + 1 = (x+1)^2 над F2"),
        (2, [1, 1, 0, 1],     "x^3 + x + 1 над F2"),
        (2, [1, 0, 1, 0, 1],  "x^4 + x^2 + 1 над F2 (пример из п. 9)"),
        (2, [1, 1, 0, 0, 1],  "x^4 + x + 1 над F2"),
        (2, [1, 0, 0, 1, 1],  "x^4 + x^3 + 1 над F2"),
        (3, [2, 2, 0, 1],     "x^3 + 2x + 2 над F3 (теорема 12.1)"),
        (3, [1, 0, 1, 0, 1],  "x^4 + x^2 + 1 над F3 (задача с доски)"),
    ]

    for p, coefficients, title in tests:
        field = Field(p)
        f = Polynomial(coefficients, field)

        by_table = is_irreducible_by_table(f)
        by_criterion = is_irreducible_by_criterion(f)

        print(f"{title}: таблица = {by_table}, критерий = {by_criterion}")

    print()

    print("Все неприводимые степени 3 над F2:")

    for f in find_irreducible(Field(2), 3, count=8):
        print("  ", f)

    print()


def demo_inverse():
    print("Обратные по модулю неприводимых многочленов:")

    field3 = Field(3)

    modulus = Polynomial([2, 2, 0, 1], field3)
    a = Polynomial([1, 1, 1], field3)

    print("Поле F3, модуль m(x) =", modulus,
          "(неприводим:", is_irreducible_by_criterion(modulus), ")")
    print("a(x) =", a)

    inverse = a.inverse_mod(modulus)

    print("a^(-1) mod m =", inverse)
    print("Проверка a * a^(-1) mod m =", a * inverse % modulus, "\n")

    print("Поле F5, поиск неприводимого многочлена степени 10:")

    field5 = Field(5)
    start = time.perf_counter()

    found = find_irreducible(field5, 10, count=1)
    elapsed = time.perf_counter() - start

    modulus = found[0]

    print("m(x) =", modulus)
    print(f"Найден за {elapsed:.6f} сек.")

    a = Polynomial([2, 3, 0, 0, 1, 0, 0, 4, 0, 2], field5)

    print("a(x) =", a)

    inverse = a.inverse_mod(modulus)

    print("a^(-1) mod m =", inverse)
    print("Проверка a * a^(-1) mod m =", a * inverse % modulus, "\n")

def demo_euler():
    print("Функция Эйлера:")

    for n in range(1, 18):
        print(f"φ({n}) = {euler_phi(n)}")

    print()

def demo_polynomial_power():
    print("Возведение многочлена в степень:")

    field = Field(2)

    f = Polynomial([1, 1], field)

    print("f(x) =", f)

    for exponent in range(1, 6):
        print(
            f"f(x)^{exponent} =",
            f ** exponent
        )

    print()

    print("Возведение многочлена по модулю:")

    modulus = Polynomial(
        [1, 1, 0, 1],
        field
    )

    print("m(x) =", modulus)

    for exponent in [2, 3, 5, 10]:
        result = f.pow_mod(
            exponent,
            modulus
        )

        print(
            f"f(x)^{exponent} mod m(x) =",
            result
        )

    print()

def demo_order():
    print("Порядок многочлена:")

    field = Field(2)

    # x + 1
    f = Polynomial([1, 1], field)

    modulus = Polynomial(
        [1, 1, 0, 1],
        field
    )

    print("Поле:", field)
    print("f(x) =", f)
    print("m(x) =", modulus)

    order = f.order(modulus)

    print("Порядок f(x) =", order)

    print(
        "Проверка f(x)^order mod m(x) =",
        f.pow_mod(order, modulus)
    )

    print()

def demo_cyclotomic():
    print("Круговые многочлены:")

    field = Field(2)

    print("Поле:", field)
    print()

    for n in range(1, 11):
        polynomial = Polynomial.cyclotomic(
            n,
            field
        )

        print(
            f"Φ_{n}(x) =",
            polynomial
        )

    print()

def main():
    start_time = time.perf_counter()

    demo_arithmetic(Field(2))
    demo_mobius()
    demo_euler()
    demo_tables()
    demo_irreducibility()
    demo_inverse()
    demo_polynomial_power()
    demo_order()
    demo_cyclotomic()

    total_time = time.perf_counter() - start_time

    print(f"Общее время работы программы: {total_time:.6f} сек.")


if __name__ == "__main__":
    main()