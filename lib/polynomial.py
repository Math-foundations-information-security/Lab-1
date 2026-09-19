from .mobius import prime_divisors
from .gcd import gcd, extended_gcd

class Polynomial:
    def __init__(self, coefficients, field):
        self.field = field

        if not coefficients:
            coefficients = [0]

        coefficients = [
            self.field.normalize(c)
            for c in coefficients
        ]

        while len(coefficients) > 1 and coefficients[-1] == 0:
            coefficients.pop()

        self.coefficients = coefficients

    @property
    def degree(self):
        if self.is_zero():
            return -1

        return len(self.coefficients) - 1

    def is_zero(self):
        return len(self.coefficients) == 1 and self.coefficients[0] == 0

    def is_one(self):
        return (
            len(self.coefficients) == 1
            and self.coefficients[0] == 1
        )

    def copy(self):
        return Polynomial(
            self.coefficients.copy(),
            self.field
        )

    def field_zero(self):
        return Polynomial([0], self.field)

    def field_one(self):
        return Polynomial([1], self.field)

    def _check_field(self, other):
        if self.field != other.field:
            raise ValueError(
                "Многочлены должны принадлежать одному полю"
            )

    def __add__(self, other):
        self._check_field(other)

        max_len = max(
            len(self.coefficients),
            len(other.coefficients)
        )

        result = []

        for i in range(max_len):
            a = (
                self.coefficients[i]
                if i < len(self.coefficients)
                else 0
            )

            b = (
                other.coefficients[i]
                if i < len(other.coefficients)
                else 0
            )

            result.append(
                self.field.add(a, b)
            )

        return Polynomial(result, self.field)

    def __sub__(self, other):
        self._check_field(other)

        max_len = max(
            len(self.coefficients),
            len(other.coefficients)
        )

        result = []

        for i in range(max_len):
            a = (
                self.coefficients[i]
                if i < len(self.coefficients)
                else 0
            )

            b = (
                other.coefficients[i]
                if i < len(other.coefficients)
                else 0
            )

            result.append(
                self.field.sub(a, b)
            )

        return Polynomial(result, self.field)

    def __mul__(self, other):
        self._check_field(other)

        if self.is_zero() or other.is_zero():
            return Polynomial([0], self.field)

        result = [
            0
            for _ in range(
                len(self.coefficients)
                + len(other.coefficients)
                - 1
            )
        ]

        for i, a in enumerate(self.coefficients):
            for j, b in enumerate(other.coefficients):

                result[i + j] = self.field.add(
                    result[i + j],
                    self.field.mul(a, b)
                )

        return Polynomial(result, self.field)

    def scalar_mul(self, scalar):
        scalar = self.field.normalize(scalar)

        result = [
            self.field.mul(c, scalar)
            for c in self.coefficients
        ]

        return Polynomial(result, self.field)

    def divmod(self, divisor):
        self._check_field(divisor)

        if divisor.is_zero():
            raise ZeroDivisionError(
                "Деление на нулевой многочлен"
            )

        remainder = self.copy()

        quotient = Polynomial([0], self.field)

        divisor_degree = divisor.degree
        divisor_lead = divisor.coefficients[-1]

        inverse_lead = self.field.inverse(
            divisor_lead
        )

        while (not remainder.is_zero() and remainder.degree >= divisor_degree):
            degree_difference = remainder.degree - divisor_degree

            coefficient = self.field.mul(
                remainder.coefficients[-1],
                inverse_lead
            )

            term_coefficients = (
                [0] * degree_difference
                + [coefficient]
            )

            term = Polynomial(
                term_coefficients,
                self.field
            )

            quotient = quotient + term

            remainder = (
                remainder - term * divisor
            )

        return quotient, remainder

    def __floordiv__(self, divisor):
        quotient, _ = self.divmod(divisor)
        return quotient

    def __mod__(self, divisor):
        _, remainder = self.divmod(divisor)
        return remainder

    def __eq__(self, other):
        if not isinstance(other, Polynomial):
            return False

        if self.field != other.field:
            return False

        return self.coefficients == other.coefficients

    def __pow__(self, exponent):
        if exponent < 0:
            raise ValueError(
                "Отрицательная степень не поддерживается"
            )

        result = Polynomial([1], self.field)
        base = self.copy()

        while exponent > 0:
            if exponent % 2 == 1:
                result = result * base

            base = base * base
            exponent //= 2

        return result

    def pow_mod(self, exponent, modulus):
        self._check_field(modulus)

        if modulus.is_zero():
            raise ZeroDivisionError(
                "Модуль не может быть нулевым"
            )

        result = Polynomial([1], self.field)
        base = self % modulus

        while exponent > 0:
            if exponent % 2 == 1:
                result = (result * base) % modulus

            base = (base * base) % modulus
            exponent //= 2

        return result

    def inverse_mod(self, modulus):
        self._check_field(modulus)

        if modulus.is_zero():
            raise ZeroDivisionError(
                "Модуль не может быть нулевым"
            )
        
        g, s, _ = extended_gcd(
            self,
            modulus
        )

        if not g.is_one():
            raise ValueError(
                "Обратного многочлена не существует: "
                "НОД не равен 1"
            )

        return s % modulus

    def __str__(self):
        if self.is_zero():
            return "0"

        terms = []

        for degree in range(len(self.coefficients) - 1, -1, -1):
            coefficient = self.coefficients[degree]

            if coefficient == 0:
                continue

            if degree == 0:
                term = str(coefficient)

            elif degree == 1:
                if coefficient == 1:
                    term = "x"
                else:
                    term = f"{coefficient}x"

            else:
                if coefficient == 1:
                    term = f"x^{degree}"
                else:
                    term = (
                        f"{coefficient}x^{degree}"
                    )

            terms.append(term)

        return " + ".join(terms)

    def __repr__(self):
        return (
            f"Polynomial("
            f"{self.coefficients}, "
            f"F_{self.field.p})"
        )