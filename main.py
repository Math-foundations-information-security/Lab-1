import time

from lib.field import Field
from lib.polynomial import Polynomial
from lib.gcd import gcd, extended_gcd
from lib.mobius import mobius

def main():
    start_time = time.perf_counter()

    field = Field(2)

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

    print("Функция Мёбиуса:")

    for n in range(1, 18):
        print(f"M({n}) = {mobius(n)}")

    total_time = time.perf_counter() - start_time

    print(f"\nОбщее время работы программы: " f"{total_time:.6f} сек.")

if __name__ == "__main__":
    main()