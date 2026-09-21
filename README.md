# minimum_excluding_set

Maintains a dynamic set of non-negative integers and reports the smallest missing value (mex) in constant time.

## Usage

```python
from minimum_excluding_set import MinimumExcludingSet

s = MinimumExcludingSet([0, 2, 3])
print(s.mex)  # 1

s.add(1)
print(s.mex)  # 4

s.discard(3)
print(s.mex)  # 3
```

## Why this exists

The mex of a set of integers is a fundamental value in combinatorial game theory and scheduling algorithms. Recomputing it from scratch after each update costs O(n) time. This class keeps the mex up to date by incrementing it lazily on insertions and resetting it to the removed value on deletions when that value is smaller than the current mex. The trade-off is that deletions of small values can be followed by an O(n) scan on the next insertion, but in the common case where updates are local, the amortized cost is much lower than a full recomputation.

## Edge cases

Only non-negative integers are accepted. Passing a negative value raises `ValueError`, and passing a non-integer raises `TypeError`. Duplicates are ignored, as with a regular Python set. The `remove` method raises `KeyError` for missing values while `discard` silently does nothing. After `clear()`, the mex is zero.
