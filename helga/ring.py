from numbers import Integral
from abc import ABC


class Ring(ABC):
    @classmethod
    def is_field(self):
        return NotImplemented

    @classmethod
    def ring_eq(self, rhs):
        return self.__name__ == rhs.__name__

    @classmethod
    def is_polynomial_ring(self):
        pass

    @classmethod
    def base_ring(self):
        pass


class Integer(Ring, int):
    @classmethod
    def is_field(self):
        return False
