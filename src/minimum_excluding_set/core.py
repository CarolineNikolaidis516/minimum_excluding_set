"""Core implementation of MinimumExcludingSet.

The mex (minimum excluded) of a set of integers is the smallest non-negative
integer not present in the set. This class maintains the mex incrementally so
that it can be reported in O(1) time after any number of insertions or
deletions, while each update costs amortized O(number of changed values).

Internally the elements are stored in a regular Python set, and the mex value
is advanced lazily on insertions and retracted on deletions when the deleted
element is smaller than the current mex.
"""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import final


@final
class MinimumExcludingSet:
    """A dynamic set of non-negative integers that can report its mex.

    Only non-negative integers are supported. Negative values raise
    ``ValueError`` at insertion time. The mex is defined as the smallest
    non-negative integer not present in the set.
    """

    __slots__ = ("_values", "_mex")

    def __init__(self, iterable: Iterable[int] = ()) -> None:
        """Initialize with an optional iterable of non-negative integers."""
        self._values: set[int] = set()
        self._mex: int = 0
        for value in iterable:
            self.add(value)

    def __contains__(self, value: object) -> bool:
        """Return True if ``value`` is in the set."""
        return value in self._values

    def __iter__(self) -> Iterator[int]:
        """Iterate over the elements currently in the set."""
        return iter(self._values)

    def __len__(self) -> int:
        """Return the number of elements in the set."""
        return len(self._values)

    def __repr__(self) -> str:
        """Return a developer-friendly representation."""
        return f"MinimumExcludingSet({list(self._values)!r})"

    @property
    def mex(self) -> int:
        """The minimum excluded value of the set.

        This is always a non-negative integer. The property is read-only;
        mutating the set happens through :meth:`add`, :meth:`discard`,
        :meth:`remove`, and :meth:`clear`.
        """
        return self._mex

    def add(self, value: int) -> None:
        """Add a non-negative integer to the set.

        Raises:
            TypeError: if ``value`` is not an integer.
            ValueError: if ``value`` is negative.
        """
        self._validate(value)
        self._values.add(value)
        # Advance mex while the current mex is present. Because the mex is
        # monotonically non-decreasing on insertions, we never need to scan
        # backwards here.
        while self._mex in self._values:
            self._mex += 1

    def discard(self, value: int) -> None:
        """Remove ``value`` from the set if present.

        Raises:
            TypeError: if ``value`` is not an integer.
            ValueError: if ``value`` is negative.
        """
        self._validate(value)
        if value in self._values:
            self._values.remove(value)
            if value < self._mex:
                self._mex = value

    def remove(self, value: int) -> None:
        """Remove ``value`` from the set, raising KeyError if absent.

        Raises:
            TypeError: if ``value`` is not an integer.
            ValueError: if ``value`` is negative.
            KeyError: if ``value`` is not in the set.
        """
        self._validate(value)
        if value not in self._values:
            raise KeyError(value)
        self.discard(value)

    def clear(self) -> None:
        """Remove all elements and reset mex to zero."""
        self._values.clear()
        self._mex = 0

    @staticmethod
    def _validate(value: int) -> None:
        """Validate that ``value`` is a non-negative integer."""
        if not isinstance(value, int):
            raise TypeError(f"expected int, got {type(value).__name__}")
        if value < 0:
            raise ValueError("negative integers are not allowed")
