from collections.abc import Callable

import pytest
from union_find import UnionFind


def _assert_index_error_like(callable_obj: Callable[[], object]) -> None:
    """Assert that callable raises IndexError or ValueError.

    Helper function for testing out-of-range index exceptions.
    Accepts either IndexError or ValueError since the specification
    allows implementations to choose either exception type.

    Args:
        callable_obj: A callable that is expected to raise an exception.
    """
    with pytest.raises((IndexError, ValueError)):
        callable_obj()


# ==================== 1. __init__(n: int) (Constructor) ====================


@pytest.mark.parametrize("n", [-1, 0])
def test_constructor_raises_when_n_is_less_than_1(n: int) -> None:
    """Test 1-1, 1-2: Constructor rejects n < 1 (n=-1, n=0)."""
    with pytest.raises(ValueError):
        UnionFind(n)


def test_constructor_with_n_1_creates_singleton_union_find() -> None:
    """Test 1-3: Constructor with n=1 creates singleton Union Find."""
    uf = UnionFind(1)

    assert uf.group_count() == 1
    assert uf.find(0) == 0
    assert uf.same(0, 0)
    assert uf.size(0) == 1


@pytest.mark.parametrize("n", [2, 3])
def test_constructor_with_n_greater_than_1_creates_independent_groups(n: int) -> None:
    """Test 1-4, 1-5: Constructor with n=2 or n=3 creates independent groups."""
    uf = UnionFind(n)

    assert uf.group_count() == n
    for i in range(n):
        assert uf.find(i) == i
        assert uf.same(i, i)
        assert uf.size(i) == 1

    for i in range(n):
        for j in range(i + 1, n):
            assert not uf.same(i, j)


# ==================== 2. union(x: int, y: int) ====================


@pytest.mark.parametrize(
    ("x", "y"),
    [(-1, 0), (0, -1), (3, 0), (0, 3)],
)
def test_union_raises_for_out_of_range_arguments(x: int, y: int) -> None:
    """Test 2-1, 2-2, 2-3, 2-4: union raises for out-of-range x or y."""
    uf = UnionFind(3)

    _assert_index_error_like(lambda: uf.union(x, y))


def test_union_returns_false_when_x_and_y_are_same() -> None:
    """Test 2-5: union returns False for self-union."""
    uf = UnionFind(3)

    assert uf.union(1, 1) is False


def test_union_returns_true_when_two_different_groups_are_merged() -> None:
    """Test 2-6: union returns True when merging different groups."""
    uf = UnionFind(3)

    assert uf.union(0, 1) is True
    assert uf.same(0, 1)


def test_union_returns_false_when_already_in_same_group_same_order() -> None:
    """Test 2-7: union returns False when already in same group (same order)."""
    uf = UnionFind(3)
    uf.union(0, 1)

    assert uf.union(0, 1) is False


def test_union_returns_false_when_already_in_same_group_reverse_order() -> None:
    """Test 2-8: union returns False when already in same group (reverse order)."""
    uf = UnionFind(3)
    uf.union(0, 1)

    assert uf.union(1, 0) is False


# ==================== 3. find(x: int) ====================


@pytest.mark.parametrize("x", [-1, 3])
def test_find_raises_for_out_of_range_argument(x: int) -> None:
    """Test 3-1, 3-2: find raises for out-of-range x."""
    uf = UnionFind(3)

    _assert_index_error_like(lambda: uf.find(x))


def test_find_returns_x_when_x_is_a_representative() -> None:
    """Test 3-3: find returns x when x is its own representative."""
    uf = UnionFind(3)

    assert uf.find(2) == 2


def test_find_returns_group_representative_when_x_is_not_representative() -> None:
    """Test 3-4: find returns consistent representative for elements in same group."""
    uf = UnionFind(3)
    uf.union(0, 1)

    representative = uf.find(0)
    assert uf.find(1) == representative
    assert uf.find(1) in {0, 1}


def test_find_returns_consistent_representative_across_multiple_calls() -> None:
    """Test 3-5: find returns consistent representative across multiple calls."""
    uf = UnionFind(5)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(2, 3)

    # Get initial representatives
    rep_0 = uf.find(0)
    rep_1 = uf.find(1)
    rep_2 = uf.find(2)
    rep_3 = uf.find(3)

    # All should return the same representative
    assert rep_0 == rep_1 == rep_2 == rep_3

    # Multiple calls should return the same value
    for _ in range(10):
        assert uf.find(0) == rep_0
        assert uf.find(1) == rep_0
        assert uf.find(2) == rep_0
        assert uf.find(3) == rep_0

    # Element 4 should remain independent
    rep_4 = uf.find(4)
    assert rep_4 == 4
    for _ in range(10):
        assert uf.find(4) == rep_4


# ==================== 4. same(x: int, y: int) ====================


@pytest.mark.parametrize(
    ("x", "y"),
    [(-1, 0), (0, -1), (3, 0), (0, 3)],
)
def test_same_raises_for_out_of_range_arguments(x: int, y: int) -> None:
    """Test 4-1, 4-2, 4-3, 4-4: same raises for out-of-range x or y."""
    uf = UnionFind(3)

    _assert_index_error_like(lambda: uf.same(x, y))


def test_same_returns_true_for_direct_union() -> None:
    """Test 4-5: same returns True for direct union."""
    uf = UnionFind(4)
    uf.union(0, 1)

    assert uf.same(0, 1)


def test_same_returns_true_for_transitive_connection() -> None:
    """Test 4-6: same returns True for transitive connection."""
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(1, 2)

    assert uf.same(0, 2)


def test_same_returns_true_for_symmetric_connection() -> None:
    """Test 4-7: same returns True for symmetric connection."""
    uf = UnionFind(4)
    uf.union(0, 1)
    uf.union(1, 2)

    assert uf.same(2, 0)


def test_same_returns_false_for_different_groups_first_pair() -> None:
    """Test 4-8: same returns False for different groups (first pair)."""
    uf = UnionFind(4)
    uf.union(0, 1)

    assert not uf.same(0, 2)


def test_same_returns_false_for_different_groups_second_pair() -> None:
    """Test 4-9: same returns False for different groups (second pair)."""
    uf = UnionFind(4)
    uf.union(0, 1)

    assert not uf.same(1, 3)


# ==================== 5. size(x: int) ====================


@pytest.mark.parametrize("x", [-1, 3])
def test_size_raises_for_out_of_range_argument(x: int) -> None:
    """Test 5-1, 5-2: size raises for out-of-range x."""
    uf = UnionFind(3)

    _assert_index_error_like(lambda: uf.size(x))


def test_size_returns_1_for_singleton_group() -> None:
    """Test 5-3: size returns 1 for singleton group."""
    uf = UnionFind(3)

    assert uf.size(2) == 1


def test_size_returns_2_for_group_of_two_when_x_is_representative() -> None:
    """Test 5-4: size returns 2 for group of two, querying representative."""
    uf = UnionFind(3)
    uf.union(0, 1)

    representative = uf.find(0)
    assert uf.size(representative) == 2


def test_size_returns_2_for_group_of_two_when_x_is_not_representative() -> None:
    """Test 5-5: size returns 2 for group of two, querying non-representative."""
    uf = UnionFind(3)
    uf.union(0, 1)

    representative = uf.find(0)
    non_representative = 1 if representative == 0 else 0
    assert uf.size(non_representative) == 2


def test_size_returns_correct_values_for_multiple_groups() -> None:
    """Test 5-6: size returns correct values for multiple groups of varying sizes."""
    uf = UnionFind(7)
    uf.union(0, 1)
    uf.union(1, 2)
    uf.union(4, 5)

    assert uf.size(0) == 3
    assert uf.size(1) == 3
    assert uf.size(2) == 3

    assert uf.size(4) == 2
    assert uf.size(5) == 2

    assert uf.size(3) == 1
    assert uf.size(6) == 1


# ==================== 6. group_count() ====================


def test_group_count_when_no_union_has_been_done() -> None:
    """Test 6-1: group_count returns initial n when no unions performed."""
    uf = UnionFind(3)

    assert uf.group_count() == 3


def test_group_count_after_one_successful_union() -> None:
    """Test 6-2: group_count decreases by 1 after one successful union."""
    uf = UnionFind(3)
    uf.union(0, 1)

    assert uf.group_count() == 2


def test_group_count_after_one_successful_and_one_unsuccessful_union() -> None:
    """Test 6-3: group_count unchanged after unsuccessful union."""
    uf = UnionFind(3)
    uf.union(0, 1)
    uf.union(1, 0)

    assert uf.group_count() == 2


def test_group_count_after_two_successful_unions() -> None:
    """Test 6-4: group_count decreases correctly after two successful unions."""
    uf = UnionFind(3)
    uf.union(0, 1)
    uf.union(1, 2)

    assert uf.group_count() == 1


def test_group_count_complex_scenario() -> None:
    """Test 6-5: group_count handles complex scenario with multiple operations."""
    uf = UnionFind(6)

    assert uf.group_count() == 6

    assert uf.union(0, 1) is True
    assert uf.group_count() == 5

    assert uf.union(2, 3) is True
    assert uf.group_count() == 4

    assert uf.union(1, 3) is True
    assert uf.group_count() == 3

    assert uf.union(0, 2) is False
    assert uf.group_count() == 3

    assert uf.union(4, 4) is False
    assert uf.group_count() == 3


# ==================== 7. Integration Tests ====================


def test_integration_star_pattern() -> None:
    """Test 7-1: Star-shaped union pattern (all nodes connect to center)."""
    uf = UnionFind(6)

    # Create star pattern: 0 is the center, 1-5 connect to 0
    for i in range(1, 6):
        assert uf.union(0, i) is True

    # All elements should be in the same group
    assert uf.group_count() == 1
    for i in range(6):
        assert uf.same(0, i)
        assert uf.size(i) == 6

    # All should have the same representative
    rep = uf.find(0)
    for i in range(1, 6):
        assert uf.find(i) == rep


def test_integration_chain_pattern() -> None:
    """Test 7-2: Chain-shaped union pattern (linear connections)."""
    uf = UnionFind(5)

    # Create chain: 0-1-2-3-4
    for i in range(4):
        assert uf.union(i, i + 1) is True

    # All elements should be in the same group
    assert uf.group_count() == 1
    rep = uf.find(0)
    for i in range(5):
        assert uf.find(i) == rep
        assert uf.size(i) == 5

    # Test transitivity across the chain
    assert uf.same(0, 4)
    assert uf.same(1, 3)


def test_integration_multiple_trees_merge() -> None:
    """Test 7-3: Build multiple trees and merge them."""
    uf = UnionFind(12)

    # Build first tree: 0-1-2
    uf.union(0, 1)
    uf.union(1, 2)

    # Build second tree: 3-4-5-6
    uf.union(3, 4)
    uf.union(4, 5)
    uf.union(5, 6)

    # Build third tree: 7-8
    uf.union(7, 8)

    # Independent nodes: 9, 10, 11
    assert uf.group_count() == 6  # 3 trees + 3 independent nodes

    # Merge first and second tree
    assert uf.union(2, 3) is True
    assert uf.group_count() == 5
    assert uf.size(0) == 7  # Tree size: 0-1-2-3-4-5-6

    # Merge the large tree with third tree
    assert uf.union(6, 7) is True
    assert uf.group_count() == 4
    assert uf.size(0) == 9  # All merged: 0-8

    # Verify connectivity
    for i in range(9):
        assert uf.same(0, i)

    # Independent nodes remain independent
    assert not uf.same(0, 9)
    assert not uf.same(0, 10)
    assert not uf.same(0, 11)


def test_integration_cycle_detection() -> None:
    """Test 7-4: Detect when union would create a cycle (already connected)."""
    uf = UnionFind(5)

    # Create a path: 0-1-2-3-4
    assert uf.union(0, 1) is True
    assert uf.union(1, 2) is True
    assert uf.union(2, 3) is True
    assert uf.union(3, 4) is True

    # Try to create cycles (should return False)
    assert uf.union(0, 4) is False  # Already connected via chain
    assert uf.union(1, 3) is False  # Already connected
    assert uf.union(0, 2) is False  # Already connected

    # Group structure should remain unchanged
    assert uf.group_count() == 1
    assert uf.size(0) == 5


def test_integration_complex_merge_sequence() -> None:
    """Test 7-5: Complex sequence of merges and queries."""
    uf = UnionFind(10)

    # Step 1: Create pairs
    uf.union(0, 1)
    uf.union(2, 3)
    uf.union(4, 5)
    uf.union(6, 7)
    uf.union(8, 9)
    assert uf.group_count() == 5

    # Step 2: Merge pairs into larger groups
    uf.union(1, 3)  # Merge (0,1) with (2,3)
    assert uf.group_count() == 4
    assert uf.size(0) == 4

    uf.union(5, 7)  # Merge (4,5) with (6,7)
    assert uf.group_count() == 3
    assert uf.size(4) == 4

    # Step 3: Merge the two large groups
    uf.union(2, 6)  # Merge (0,1,2,3) with (4,5,6,7)
    assert uf.group_count() == 2
    assert uf.size(0) == 8

    # Step 4: Final merge
    uf.union(0, 8)  # Merge all into one group
    assert uf.group_count() == 1
    assert uf.size(0) == 10

    # Verify all elements are connected
    for i in range(10):
        for j in range(i + 1, 10):
            assert uf.same(i, j)


# ==================== 8. Large Scale Performance Tests ====================


def test_large_scale_union_find_with_thousand_elements() -> None:
    """Test 8-1: Large scale test with 1000 elements."""
    n = 1000
    uf = UnionFind(n)

    # Initial state
    assert uf.group_count() == n

    # Create a long chain: 0-1-2-...-999
    for i in range(n - 1):
        assert uf.union(i, i + 1) is True

    # Verify final state
    assert uf.group_count() == 1
    assert uf.size(0) == n
    assert uf.size(n - 1) == n

    # Verify connectivity
    rep = uf.find(0)
    assert uf.find(n - 1) == rep
    assert uf.same(0, n - 1)
    assert uf.same(0, n // 2)


def test_large_scale_multiple_independent_chains() -> None:
    """Test 8-2: Large scale test with multiple independent chains."""
    n = 1000
    chain_length = 10
    num_chains = n // chain_length
    uf = UnionFind(n)

    # Create multiple independent chains
    for chain_id in range(num_chains):
        start = chain_id * chain_length
        for i in range(start, start + chain_length - 1):
            uf.union(i, i + 1)

    # Verify group count
    assert uf.group_count() == num_chains

    # Verify each chain
    for chain_id in range(num_chains):
        start = chain_id * chain_length
        end = start + chain_length - 1

        # Elements within chain should be connected
        assert uf.same(start, end)
        assert uf.size(start) == chain_length

        # Elements across different chains should not be connected
        if chain_id < num_chains - 1:
            next_chain_start = (chain_id + 1) * chain_length
            assert not uf.same(start, next_chain_start)


def test_large_scale_star_pattern() -> None:
    """Test 8-3: Large scale star pattern with many nodes."""
    n = 1000
    uf = UnionFind(n)

    # Create star pattern: 0 is center, all others connect to 0
    for i in range(1, n):
        assert uf.union(0, i) is True

    # Verify final state
    assert uf.group_count() == 1
    assert uf.size(0) == n

    # Verify all nodes are connected to center
    rep = uf.find(0)
    for i in range(1, n):
        assert uf.find(i) == rep
        assert uf.same(0, i)


def test_large_scale_worst_case_repeated_queries() -> None:
    """Test 8-4: Large scale with many repeated find queries."""
    n = 500
    uf = UnionFind(n)

    # Create a long chain
    for i in range(n - 1):
        uf.union(i, i + 1)

    # Perform many find operations (path compression should help)
    rep = uf.find(0)
    for _ in range(100):
        for i in range(0, n, 10):  # Sample every 10th element
            assert uf.find(i) == rep

    # Verify structure is still correct
    assert uf.group_count() == 1
    assert uf.size(0) == n
