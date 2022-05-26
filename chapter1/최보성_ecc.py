from unittest import TestCase

from typing_extensions import Self


class FieldElement:
    def __init__(self, num: int, prime: int):
        if not (0 <= num < prime):
            raise ValueError(f'{num} not in range [0, {prime})')
        self.num = num
        self.prime = prime

    def create_in_same_order(self, num: int) -> Self:
        return self.__class__(num % self.prime, self.prime)

    def check_same_order(self, other: 'FieldElement', op: str):
        if self.prime != other.prime:
            raise TypeError(f'Cannot {op} two numbers in different Fields')

    def __repr__(self):
        return f'FieldElement({self.num}, {self.prime})'

    def __eq__(self, other: object):
        if isinstance(other, FieldElement):
            return self.num == other.num and self.prime == other.prime
        return False

    def __add__(self, other: object) -> Self:
        if isinstance(other, FieldElement):
            self.check_same_order(other, 'add')
            return self.create_in_same_order(self.num + other.num)
        return NotImplemented

    def __sub__(self, other: object) -> Self:
        if isinstance(other, FieldElement):
            self.check_same_order(other, 'subtract')
            return self.create_in_same_order(self.num - other.num)
        return NotImplemented

    def __mul__(self, other: object) -> Self:
        if isinstance(other, FieldElement):
            self.check_same_order(other, 'multiply')
            return self.create_in_same_order(self.num * other.num)
        return NotImplemented

    def __pow__(self, exponent: object) -> Self:
        if isinstance(exponent, int):
            n = exponent % (self.prime - 1)
            return self.create_in_same_order(pow(self.num, n, self.prime))
        return NotImplemented

    def __truediv__(self, other: object) -> Self:
        if isinstance(other, FieldElement):
            self.check_same_order(other, 'divide')
            return self * other ** -1
        return NotImplemented


class FieldElementTest(TestCase):

    def test_ne(self):
        a = FieldElement(2, 31)
        b = FieldElement(2, 31)
        c = FieldElement(15, 31)
        self.assertEqual(a, b)
        self.assertTrue(a != c)
        self.assertFalse(a != b)

    def test_add(self):
        a = FieldElement(2, 31)
        b = FieldElement(15, 31)
        self.assertEqual(a + b, FieldElement(17, 31))
        a = FieldElement(17, 31)
        b = FieldElement(21, 31)
        self.assertEqual(a + b, FieldElement(7, 31))

    def test_sub(self):
        a = FieldElement(29, 31)
        b = FieldElement(4, 31)
        self.assertEqual(a - b, FieldElement(25, 31))
        a = FieldElement(15, 31)
        b = FieldElement(30, 31)
        self.assertEqual(a - b, FieldElement(16, 31))

    def test_mul(self):
        a = FieldElement(24, 31)
        b = FieldElement(19, 31)
        self.assertEqual(a * b, FieldElement(22, 31))

    def test_pow(self):
        a = FieldElement(17, 31)
        self.assertEqual(a**3, FieldElement(15, 31))
        a = FieldElement(5, 31)
        b = FieldElement(18, 31)
        self.assertEqual(a**5 * b, FieldElement(16, 31))

    def test_div(self):
        a = FieldElement(3, 31)
        b = FieldElement(24, 31)
        self.assertEqual(a / b, FieldElement(4, 31))
        a = FieldElement(17, 31)
        self.assertEqual(a**-3, FieldElement(29, 31))
        a = FieldElement(4, 31)
        b = FieldElement(11, 31)
        self.assertEqual(a**-4 * b, FieldElement(13, 31))
