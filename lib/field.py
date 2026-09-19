class Field:
    def __init__(self, p):
        self.p = p

    def normalize(self, a):
        return a % self.p

    def add(self, a, b):
        return (a + b) % self.p

    def sub(self, a, b):
        return (a - b) % self.p

    def mul(self, a, b):
        return (a * b) % self.p

    def inverse(self, a):
        a %= self.p

        if a == 0:
            raise ZeroDivisionError(
                "Нулевой элемент не имеет обратного"
            )

        old_r, r = a, self.p
        old_s, s = 1, 0

        while r != 0:
            q = old_r // r

            old_r, r = r, old_r - q * r
            old_s, s = s, old_s - q * s

        return old_s % self.p

    def __eq__(self, other):
        if not isinstance(other, Field):
            return False

        return self.p == other.p

    def __str__(self):
        return f"F_{self.p}"