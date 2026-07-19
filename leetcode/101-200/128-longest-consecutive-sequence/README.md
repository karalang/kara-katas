# 128. Longest Consecutive Sequence

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Hash Table · Union Find &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-consecutive-sequence](https://leetcode.com/problems/longest-consecutive-sequence/)

Given an unsorted array of integers, return the length of the longest run of **consecutive** integers — in `O(n)`, so sorting (`O(n log n)`) is off the table.

```
[100, 4, 200, 1, 3, 2]              ->  4   (1,2,3,4)
[0,3,7,2,5,8,4,6,0,1]               ->  9   (0..8)
[]                                  ->  0
```

**Constraints:** `0 ≤ nums.length ≤ 10⁵`, `-10⁹ ≤ nums[i] ≤ 10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Hash-set run-start scan** ★ | O(n) time, O(n) space | [`longest_consecutive.kara`](longest_consecutive.kara) ✓ | [`longest_consecutive.py`](longest_consecutive.py) ✓ |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the Kāra solver agrees with the Python mirror. Answers are validated against the known LeetCode examples plus deterministic-LCG stress cases. Zero diagnostics, valgrind-clean.

## The mechanism

**Hash-set run-start scan** ([`longest_consecutive.kara`](longest_consecutive.kara), the ★). Put every value in a `Set[i64]`. A value `v` **starts** a run iff `v - 1` is absent from the set — so only from a genuine start do we walk `v+1, v+2, …` while present, counting the run. Because the inner walk only ever launches from starts and each value is stepped over at most once across all walks, the whole thing is `O(n)` despite the nested loop — the key insight that beats the sort.

## Kāra features exercised

- **`Set[i64]`** — `insert` / `contains` on a hash set of integers (the first corpus kata to lean on `Set` directly rather than `Map`-as-set); the run-start test `!s.contains(v - 1)` and the forward walk `s.contains(cur + 1)` are the whole hot path.
- **Amortized-`O(n)` nested loop** — the compiler sees a `while` inside a `while`; the linear bound is an algorithmic invariant, not a syntactic one.
- **Deterministic LCG generator** — `(x * 1103515245 + 12345) % 2³¹` builds the stress inputs; the multiply stays within i64 (kāra's default overflow check passes), matching the Python `& 0x7FFFFFFF` mask on non-negative values.

## Running

```bash
karac run   longest_consecutive.kara
karac build longest_consecutive.kara && ./longest_consecutive
python3 longest_consecutive.py
diff <(karac run longest_consecutive.kara) <(python3 longest_consecutive.py) && echo OK
```

## Notes

The hash-set scan is a legitimate build-once + punch shape (fill the set, then scan) and a candidate for a future cross-language benchmark; for now it is verified as a correctness dogfood (`Set[i64]` insert/contains) across all surfaces.
