"""
A module that implements bitstring-based sets
"""
from typing import *


class BitSet:
    """
    A set using bitstring representation and bitwise operations

    Attributes:
        max_value: the largest integer this set stores (one less than the number of bits this set represents)
        value: the bitstring representation of this set as an int
    """
    def __init__(self, max_value: int, base_set: Optional[Union[Set[int], int]] = None):
        """
        Initializes a BitSet with the given base set

        :param base_set: a set of ints to add to this set, the value (int) of this set,
            or None to initialize the empty set.
        """
        self._nbits = max_value + 1
        self._value = 0
        if base_set is not None:
            if isinstance(base_set, int):
                self._value = base_set
            else:
                for i in base_set:
                    self.add(i)

    @property
    def value(self) -> int:
        return self._value

    @property
    def max_value(self) -> int:
        return self._nbits - 1

    @property
    def full_set_value(self) -> int:
        """
        :return: the value of `full_set` = (2 ** (max_value+1) - 1)
        """
        return (1 << self._nbits) - 1

    def full_set(self) -> 'BitSet':
        """
        :return: a BitSet of the same size with all elements
        """
        res = BitSet(self.max_value)
        res._value = self.full_set_value
        return res

    def complement(self) -> 'BitSet':
        """
        :return: a BitSet that is the complement of this set
        """
        return BitSet(self.max_value, self.complement_value())

    def complement_update(self):
        """
        Makes this set into its complement
        """
        self._value = self.complement_value()

    def complement_value(self) -> int:
        """
        :return: an int giving the value of this set's complement
        """
        return self.value ^ self.full_set_value

    def add(self, i: int):
        """
        Adds an element to this set

        :param i: an int, the element to add
        """
        self._value = self._value | (1 << i)

    def remove(self, i: int):
        """
        Remove an element from this set if it exists, or throws an error if it does not

        :param i: the element to remove
        :raise: KeyError if i is not in this set
        """
        if (self._value >> i) & 1 == 0:
            raise KeyError(str(i))
        self._value = self._value ^ (1 << i)

    def discard(self, i: int):
        """
        Remove an element from this set (if the element is not in the set, does nothing)

        :param i: the element to remove
        """
        self._value = self._value & (self.full_set_value ^ (1 << i))

    def clear(self):
        """
        Removes all elements from this set
        """
        self._value = 0

    def copy(self) -> 'BitSet':
        """
        :return: a copy of this BitSet
        """
        return BitSet(self.max_value, self.value)

    def union(self, *others: 'BitSet') -> 'BitSet':
        """
        Calculates the union between two or more BitSets

        :param others: the BitSets to perform the union with
        :return: a BitSet giving the union between all the sets (with the largest max_value)
        """
        value = self.value
        max_val = self.max_value
        for other in others:
            value = value | int(other)
            if isinstance(other, BitSet) and max_val < other.max_value:
                max_val = other.max_value
        return BitSet(max_val, value)

    def update(self, *others: 'BitSet'):
        """
        Adds the elements from one or more other sets to this set, and updates the max_value to be the largest
            between the sets.

        :param others: the BitSets containing the values to add
        """
        for other in others:
            self._value = self.value | int(other)
            if isinstance(other, BitSet) and self.max_value < other.max_value:
                self._nbits = other.max_value + 1

    def intersection(self, *others: 'BitSet') -> 'BitSet':
        """
        Calculates the intersection between two or more sets

        :param others: the BitSets to calculate the intersection with
        :return: a BitSet giving the intersection over all the sets
        """
        value = self.value
        max_val = self.max_value
        for other in others:
            value = value & int(other)
            if isinstance(other, BitSet) and max_val < other.max_value:
                max_val = other.max_value
        return BitSet(max_val, value)

    def intersection_update(self, *others: 'BitSet'):
        """
        Removes elements from this set that are not in all of the given sets

        Sets this set to the intersection between itself and all the sets in others

        :param others: the BitSets containing the values to keep
        """
        for other in others:
            self._value = self.value & int(other)
            if isinstance(other, BitSet) and self.max_value < other.max_value:
                self._nbits = other.max_value + 1

    def difference(self, *others: 'BitSet') -> 'BitSet':
        """
        Calculates the difference between two or more sets

        :param others: the list of BitSets containing elements to remove
        :return: a BitSet representing the difference of this set with the sets in others
        """
        value = self.value
        for other in others:
            value = value & other.complement_value()
        return BitSet(self.max_value, value)

    def difference_update(self, *others: 'BitSet'):
        """
        Removes all elements in any of the given sets

        :param others: the BitSets containing the values to remove
        """
        for other in others:
            self._value = self.value & other.complement_value()

    def symmetric_difference(self, other: 'BitSet') -> 'BitSet':
        """
        Calculates the symmetric difference between two sets

        The symmetric difference is the set of all elements that are in exactly one of the sets

        :param others: the BitSet to take the symmetric difference with
        :return: the symmetric difference of `self` and `other`
        """
        return BitSet(max(self.max_value, other.max_value), self.value ^ other.value)

    def symmetric_difference_update(self, other: 'BitSet'):
        """
        Sets this set to be the symmetric difference between itself and another set

        The symmetric difference is the set of all elements that are in exactly one of the sets

        :param others: the BitSet to take the symmetric difference with
        """
        self._nbits = max(self.max_value, other.max_value) + 1
        self._value = self.value ^ other.value

    def isempty(self) -> bool:
        """
        :return: True if this set contains no elements, else False
        """
        return self.value == 0

    def isdisjoint(self, other: 'BitSet') -> bool:
        """
        Calculates if this set and another contain any of the same elements

        :param other: the BitSet to compare to
        :return: True if the sets do not share elements, or False if they do
        """
        return self.value & other.value == 0

    def issubset(self, other: 'BitSet') -> bool:
        """
        Calculates whether this set is a subset of another

        :param other: the BitSet to check
        :return: True if this set contains only elements in `other`, else False
        """
        return self.difference(other).isempty()

    def issuperset(self, other: 'BitSet') -> bool:
        """
        Calculates whether this set is a superset of another

        :param other: the BitSet to check
        :return: True if `other` contains only elements in this set, else False
        """
        return other.difference(self).isempty()

    def __invert__(self):
        return self.complement()

    def __contains__(self, i: int):
        """
        Check if `i` is in this set

        :param i: the value to check membership of
        :return: True if i is in this set, else False
        """
        return (self.value >> i) & 1 == 1

    def __iter__(self) -> Generator[int, None, None]:
        """
        :return: an iterable over the elements in this set
        """
        for i in range(self.max_value):
            if i in self:
                yield i

    def __len__(self) -> int:
        """
        :return: the number of elements in this set
        """
        return bin(self.value).count('1')

    def __int__(self) -> int:
        """
        :return: self.value
        """
        return self._value

    def __str__(self) -> str:
        """
        :return: a string representation of this BitSet
        """
        return '{' + ', '.join(str(i) for i in iter(self)) + '}'
