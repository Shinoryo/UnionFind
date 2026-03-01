# Union Find Test Case Design Document

## Overview

All test cases verify both **correctness of operations** and **group integrity**. According to the Union Find (Disjoint Set Union) definition, the data structure must maintain:

- Each element belongs to exactly one group
- `union(x, y)` merges the groups containing `x` and `y`
- `find(x)` returns a consistent representative for all elements in the same group
- Group sizes and counts are accurately maintained after every operation

This property is validated throughout the test suite.

## Terminology

- **Representative**: The element returned by `find(x)` that identifies a group. All elements in the same group share the same representative.
- **Group**: A set of elements that have been connected through `union` operations. Initially, each element forms its own singleton group.
- **Merge/Union**: The operation of combining two groups into one. The `union(x, y)` operation merges the group containing `x` with the group containing `y`.
- **Group Count**: The total number of distinct groups in the Union Find structure. Starts at `n` (all elements independent) and decreases by 1 with each successful union.
- **Group Size**: The number of elements in a group. Initially 1 for each element, increases when groups are merged.

## Test Design Approach

### Layered Testing Strategy

The test suite follows a **Layered Testing Approach** with complete coverage of boundary and edge cases:

```text
Layer 1: Foundation (Constructor)
└─ __init__(n)
   │
   └─── Layer 2: Core Operations (Depend on constructor)
        ├─ union(x, y)
        ├─ find(x)
        ├─ same(x, y)
        ├─ size(x)
        └─ group_count()
   │
   └─── Layer 3: Integration & Performance (Depend on core operations)
        ├─ Complex graph patterns (star, chain, multiple trees, cycles)
        └─ Large scale performance tests (scalability validation)
```

#### Rationale

**Layer 1 (Foundation)**: The constructor `__init__(n)` is the foundation. It creates the initial state where all elements are independent. Tests verify both valid inputs (n=1, 2, 3, ...) and invalid inputs (n<1) with exception handling.

**Layer 2 (Core Operations)**: All other methods (`union`, `find`, `same`, `size`, `group_count`) depend on a valid Union Find instance. Tests use the constructor to set up fixtures and verify:

- Correct behavior for valid inputs (successful unions, consistent representatives, accurate sizes)
- Exception handling for invalid inputs (out-of-range indices)
- Edge cases (self-union, repeated unions, operations on already-merged groups)
- Boundary values (negative indices, indices >= n, singleton groups, multiple group scenarios)

**Layer 3 (Integration & Performance)**: Complex scenarios and scalability tests build on core operations to verify:

- **Integration Tests**: Real-world graph patterns (star, chain, tree merges, cycle detection) that combine multiple operations
- **Performance Tests**: Large-scale scenarios (n=500-1000) to validate efficiency and correctness with significant data volumes

## 1. `__init__(n: int)` (Constructor)

| No. | Test Aspect | Verification Content | Test Input | Expected Result |
| --- | --- | --- | --- | --- |
| 1-1 | Invalid: `n = -1` | Rejects negative values | `UnionFind(-1)` | Raises `ValueError` |
| 1-2 | Invalid: `n = 0` | Rejects zero | `UnionFind(0)` | Raises `ValueError` |
| 1-3 | Boundary: `n = 1` | Creates singleton Union Find | `UnionFind(1)` | Creates 1-element structure; `group_count() == 1`; `find(0) == 0`; `same(0, 0) == True`; `size(0) == 1` |
| 1-4 | Valid: `n = 2` | Creates 2 independent elements | `UnionFind(2)` | Creates 2-element structure; `group_count() == 2`; each element is its own representative; `same(0, 1) == False` |
| 1-5 | Valid: `n = 3` | Creates 3 independent elements | `UnionFind(3)` | Creates 3-element structure; `group_count() == 3`; each element is its own representative; no elements share groups |

## 2. `union(x: int, y: int) → bool`

| No. | Test Aspect | Precondition | Test Input | Expected Result |
| --- | --- | --- | --- | --- |
| 2-1 | Exception: `x < 0` | UnionFind with n=3 | `union(-1, 0)` | Raises `IndexError` or `ValueError` |
| 2-2 | Exception: `x >= n` | UnionFind with n=3 | `union(3, 0)` | Raises `IndexError` or `ValueError` |
| 2-3 | Exception: `y < 0` | UnionFind with n=3 | `union(0, -1)` | Raises `IndexError` or `ValueError` |
| 2-4 | Exception: `y >= n` | UnionFind with n=3 | `union(0, 3)` | Raises `IndexError` or `ValueError` |
| 2-5 | Edge case: Self-union | UnionFind with n=3 | `union(1, 1)` | Returns `False`; group structure unchanged |
| 2-6 | Normal: Merge different groups | UnionFind with n=3, elements 0 and 1 in different groups | `union(0, 1)` | Returns `True`; `same(0, 1) == True`; group count decreases by 1 |
| 2-7 | Edge case: Already merged (same order) | UnionFind with n=3, after `union(0, 1)` | `union(0, 1)` | Returns `False`; group structure unchanged |
| 2-8 | Edge case: Already merged (reverse order) | UnionFind with n=3, after `union(0, 1)` | `union(1, 0)` | Returns `False`; group structure unchanged |

## 3. `find(x: int) → int`

| No. | Test Aspect | Precondition | Test Input | Expected Result |
| --- | --- | --- | --- | --- |
| 3-1 | Exception: `x < 0` | UnionFind with n=3 | `find(-1)` | Raises `IndexError` or `ValueError` |
| 3-2 | Exception: `x >= n` | UnionFind with n=3 | `find(3)` | Raises `IndexError` or `ValueError` |
| 3-3 | Normal: Element is representative | UnionFind with n=3, no unions performed | `find(2)` | Returns `2` (or any consistent value for independent element) |
| 3-4 | Normal: Element is not representative | UnionFind with n=3, after `union(0, 1)` | `find(0)` and `find(1)` | Both return the same value (the group representative); the representative is either 0 or 1 |
| 3-5 | Consistency: Multiple calls | UnionFind with n=5, after `union(0,1)`, `union(1,2)`, `union(2,3)` | Call `find(0)`, `find(1)`, `find(2)`, `find(3)` multiple times | All calls return the same representative; repeated calls return consistent values; independent element (4) returns itself consistently |

## 4. `same(x: int, y: int) → bool`

| No. | Test Aspect | Precondition | Test Input | Expected Result |
| --- | --- | --- | --- | --- |
| 4-1 | Exception: `x < 0` | UnionFind with n=3 | `same(-1, 0)` | Raises `IndexError` or `ValueError` |
| 4-2 | Exception: `x >= n` | UnionFind with n=3 | `same(3, 0)` | Raises `IndexError` or `ValueError` |
| 4-3 | Exception: `y < 0` | UnionFind with n=3 | `same(0, -1)` | Raises `IndexError` or `ValueError` |
| 4-4 | Exception: `y >= n` | UnionFind with n=3 | `same(0, 3)` | Raises `IndexError` or `ValueError` |
| 4-5 | Normal: Same group (direct union) | UnionFind with n=4, after `union(0, 1)` | `same(0, 1)` | Returns `True` |
| 4-6 | Normal: Same group (transitive) | UnionFind with n=4, after `union(0, 1)` and `union(1, 2)` | `same(0, 2)` | Returns `True` (transitivity verified) |
| 4-7 | Normal: Same group (symmetric) | UnionFind with n=4, after `union(0, 1)` and `union(1, 2)` | `same(2, 0)` | Returns `True` (symmetry verified) |
| 4-8 | Normal: Different groups | UnionFind with n=4, after `union(0, 1)` | `same(0, 2)` | Returns `False` |
| 4-9 | Normal: Different groups (other pair) | UnionFind with n=4, after `union(0, 1)` | `same(1, 3)` | Returns `False` |

## 5. `size(x: int) → int`

| No. | Test Aspect | Precondition | Test Input | Expected Result |
| --- | --- | --- | --- | --- |
| 5-1 | Exception: `x < 0` | UnionFind with n=3 | `size(-1)` | Raises `IndexError` or `ValueError` |
| 5-2 | Exception: `x >= n` | UnionFind with n=3 | `size(3)` | Raises `IndexError` or `ValueError` |
| 5-3 | Normal: Singleton group | UnionFind with n=3, no unions performed | `size(2)` | Returns `1` |
| 5-4 | Normal: Group of 2, query representative | UnionFind with n=3, after `union(0, 1)` | `size(find(0))` | Returns `2` |
| 5-5 | Normal: Group of 2, query non-representative | UnionFind with n=3, after `union(0, 1)` | `size(0)` and `size(1)` | Both return `2` (size is consistent regardless of which element is queried) |
| 5-6 | Normal: Multiple groups | UnionFind with n=7, after `union(0, 1)`, `union(1, 2)`, `union(4, 5)` | `size(0)`, `size(1)`, `size(2)`, `size(4)`, `size(5)`, `size(3)`, `size(6)` | Elements 0, 1, 2 return `3`; elements 4, 5 return `2`; elements 3, 6 return `1` |

## 6. `group_count() → int`

| No. | Test Aspect | Precondition | Test Procedure | Expected Result |
| --- | --- | --- | --- | --- |
| 6-1 | Initial state: No unions | UnionFind with n=3 | Call `group_count()` | Returns `3` |
| 6-2 | After 1 successful union | UnionFind with n=3, after `union(0, 1)` returns `True` | Call `group_count()` | Returns `2` |
| 6-3 | After 1 successful, 1 unsuccessful union | UnionFind with n=3, after `union(0, 1)` returns `True`, then `union(1, 0)` returns `False` | Call `group_count()` | Returns `2` (count unchanged after unsuccessful union) |
| 6-4 | After 2 successful unions | UnionFind with n=3, after `union(0, 1)` returns `True`, then `union(1, 2)` returns `True` | Call `group_count()` | Returns `1` |
| 6-5 | Complex scenario | UnionFind with n=6, after `union(0, 1)`, `union(2, 3)`, `union(1, 3)` (3 successful), `union(0, 2)` (unsuccessful), `union(4, 4)` (unsuccessful) | Call `group_count()` after each operation | After 1st: `5`; After 2nd: `4`; After 3rd: `3`; After 4th: `3`; After 5th: `3` |

## 7. Integration Tests (Complex Graph Patterns)

| No. | Test Aspect | Test Scenario | Expected Result |
| --- | --- | --- | --- |
| 7-1 | Star pattern | UnionFind with n=6; connect nodes 1-5 to center node 0 | All elements in same group; `group_count() == 1`; all share same representative; `size(i) == 6` for all i |
| 7-2 | Chain pattern | UnionFind with n=5; create chain 0-1-2-3-4 | All elements in same group; transitivity verified (0 and 4 are connected); `size(i) == 5` for all i |
| 7-3 | Multiple trees merge | UnionFind with n=12; build 3 trees (0-1-2, 3-4-5-6, 7-8) and 3 independent nodes; merge trees progressively | Group count decreases correctly; sizes increase properly; connectivity is maintained; independent nodes remain separate |
| 7-4 | Cycle detection | UnionFind with n=5; create chain 0-1-2-3-4; attempt to union already-connected elements | `union` returns `False` for already-connected elements; group structure remains unchanged |
| 7-5 | Complex merge sequence | UnionFind with n=10; create 5 pairs, merge pairs into groups, merge groups into one | Group count: 10→5→4→3→2→1; sizes grow correctly; all elements eventually connected |

## 8. Large Scale Performance Tests

| No. | Test Aspect | Scale | Test Scenario | Expected Result |
| --- | --- | --- | --- | --- |
| 8-1 | Long chain | n=1000 | Create chain 0-1-2-...-999 | All elements connected; `group_count() == 1`; `size(0) == 1000`; ends of chain are connected |
| 8-2 | Multiple independent chains | n=1000 | Create 100 chains of length 10 | `group_count() == 100`; elements within each chain connected; elements across chains not connected |
| 8-3 | Star pattern | n=1000 | Connect all nodes 1-999 to center node 0 | All elements connected to center; `group_count() == 1`; `size(0) == 1000` |
| 8-4 | Repeated queries | n=500 | Create long chain; perform 100 iterations of find queries on sampled elements | All queries return consistent representative; verifies path compression optimization |

## Implementation Notes

### Test Structure

Tests use `pytest.mark.parametrize` for boundary value testing to ensure:

- Concise test code
- Clear test parameter visibility
- Easy addition of new boundary cases

### Exception Testing Strategy

The helper function `_assert_index_error_like()` accepts both `IndexError` and `ValueError` because the specification allows implementations to choose either exception type for out-of-range errors.

### Lint Configuration

Test-specific lint rules are disabled via `per-file-ignores` in `pyproject.toml`:

- `PT011`: Allows broad `pytest.raises` for flexible exception testing
- `S101`: Allows `assert` statements (standard in pytest)
- `PLR2004`: Allows magic numbers (boundary values are clearer as literals)

These rules are disabled only for test files, maintaining strict checking for production code.
