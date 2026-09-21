"""Tests for MinimumExcludingSet."""

import unittest

from minimum_excluding_set import MinimumExcludingSet


class TestMinimumExcludingSet(unittest.TestCase):
    def test_empty_set_has_mex_zero(self):
        s = MinimumExcludingSet()
        self.assertEqual(s.mex, 0)
        self.assertEqual(len(s), 0)

    def test_add_increases_mex_when_gaps_filled(self):
        s = MinimumExcludingSet()
        s.add(0)
        self.assertEqual(s.mex, 1)
        s.add(1)
        self.assertEqual(s.mex, 2)
        s.add(3)
        self.assertEqual(s.mex, 2)

    def test_add_duplicate_does_not_change_mex(self):
        s = MinimumExcludingSet([0, 1])
        self.assertEqual(s.mex, 2)
        s.add(1)
        self.assertEqual(s.mex, 2)

    def test_discard_smaller_value_lowers_mex(self):
        s = MinimumExcludingSet([0, 1, 2])
        self.assertEqual(s.mex, 3)
        s.discard(1)
        self.assertEqual(s.mex, 1)

    def test_discard_larger_value_does_not_lower_mex(self):
        s = MinimumExcludingSet([0, 1, 2])
        s.discard(5)
        self.assertEqual(s.mex, 3)

    def test_discard_absent_value_does_not_change_mex(self):
        s = MinimumExcludingSet([0, 1])
        s.discard(10)
        self.assertEqual(s.mex, 2)

    def test_remove_existing_element(self):
        s = MinimumExcludingSet([0, 1])
        s.remove(0)
        self.assertEqual(s.mex, 0)
        self.assertNotIn(0, s)

    def test_remove_missing_element_raises_key_error(self):
        s = MinimumExcludingSet([0])
        with self.assertRaises(KeyError):
            s.remove(10)

    def test_clear_resets_to_empty(self):
        s = MinimumExcludingSet([0, 1, 2, 5])
        s.clear()
        self.assertEqual(len(s), 0)
        self.assertEqual(s.mex, 0)

    def test_init_with_iterable(self):
        s = MinimumExcludingSet([1, 2, 4])
        self.assertEqual(s.mex, 0)
        s.add(0)
        self.assertEqual(s.mex, 3)

    def test_init_with_generator(self):
        s = MinimumExcludingSet(x for x in range(3))
        self.assertEqual(s.mex, 3)

    def test_contains(self):
        s = MinimumExcludingSet([2, 5])
        self.assertIn(2, s)
        self.assertNotIn(3, s)

    def test_len(self):
        s = MinimumExcludingSet()
        self.assertEqual(len(s), 0)
        s.add(7)
        s.add(7)
        self.assertEqual(len(s), 1)

    def test_iteration_matches_contents(self):
        values = [0, 2, 5]
        s = MinimumExcludingSet(values)
        self.assertEqual(set(iter(s)), set(values))

    def test_repr_contains_elements(self):
        s = MinimumExcludingSet([1, 2])
        r = repr(s)
        self.assertIn("1", r)
        self.assertIn("2", r)

    def test_add_negative_raises_value_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(ValueError):
            s.add(-1)

    def test_add_non_int_raises_type_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(TypeError):
            s.add(1.0)  # type: ignore[arg-type]

    def test_discard_negative_raises_value_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(ValueError):
            s.discard(-1)

    def test_remove_negative_raises_value_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(ValueError):
            s.remove(-1)

    def test_discard_non_int_raises_type_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(TypeError):
            s.discard("0")  # type: ignore[arg-type]

    def test_remove_non_int_raises_type_error(self):
        s = MinimumExcludingSet()
        with self.assertRaises(TypeError):
            s.remove(None)  # type: ignore[arg-type]


if __name__ == "__main__":
    unittest.main()
