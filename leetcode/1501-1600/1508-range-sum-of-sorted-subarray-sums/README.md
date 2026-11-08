# 1508. Range Sum of Sorted Subarray Sums

You are given the array `nums` of `n` positive integers. Compute the sum
of every non-empty contiguous subarray, sort those `n * (n + 1) / 2` sums
in non-decreasing order, and return the sum of the numbers from index
`left` to index `right` (indexed from 1), inclusive, modulo `10^9 + 7`.

```
nums = [1, 2, 3, 4], n = 4, left = 1, right = 5    ->  13
nums = [1, 2, 3, 4], n = 4, left = 3, right = 4    ->  6
nums = [1, 2, 3, 4], n = 4, left = 1, right = 10   ->  50
```

The sums of `[1, 2, 3, 4]` sorted are `1, 2, 3, 3, 4, 5, 6, 7, 9, 10`.

**Constraints:** `1 <= n <= 1000`; `1 <= nums[i] <= 100`;
`1 <= left <= right <= n * (n + 1) / 2`.

## Approaches

| file | mechanism |
|---|---|
| `sums.kara` ★ | the sum of the `k` smallest sums, twice: a binary search for the `k`-th smallest sum, and a two-pointer sweep that counts every sum at most a bound and adds them up, from the prefix sums and the prefix sums of those. Every number is positive, so a window's sum grows with its right end. O(n log(sum)) |
| `sums_heap.kara` | a `PriorityQueue` merges the `n` sorted runs of sums that start at each place: pop `right` times, add from `left` on, push the popped run's next sum. O(right log n) |
| `sums_sort.kara` | every sum in a `Vec`, sorted, the places added. O(n^2 log n) |
| `sums_iter.kara` | each start's running sums by `scan` over `nums[i..]`, flattened by `flat_map`, sorted, and the places taken by `skip` and `take` |
| `sums_solution.kara` | LeetCode's Rust template (`Vec<i32>`, `n as usize`, `Vec::with_capacity`, `sort_unstable`, a slice summed), the sort arm, carried by `karac fix` to one error: B-2026-11-08-16 |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (one number, three equal numbers, and all 500500 places of 1000
numbers), then a checksum of the answers for 3000 arrays of 1 to 8
numbers, 300 of 1 to 100, and 3 of 1 to 1000, each with a random range
of places. `sums.py` mirrors the ★ arm and its output is byte-identical;
its function was also checked against sorting every sum in Python on 2000
random arrays.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: each subarray summed on its own, the sums kept sorted by
insertion, and the places added. It checks 2000 arrays of 1 to 10
numbers. Every random choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the places split anywhere: `left` to `mid` plus `mid + 1` to `right` is `left` to `right` |
| P3 | the numbers reversed leave the answer |
| P4 | every number tripled triples the answer |
| P5 | all the places add to each number times the subarrays holding it, `nums[i] (i + 1) (n - i)` |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2000 problems: checksum 161595161, 60000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Twenty-three edits to the differential, four to six to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept.
Seventeen are killed by a property and three by a crash, each the same
way under both backends; three survive, all equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a sum equal to the bound not counted | P1 93, P4 93, P6 93 |
| M2 | ★: the prefix sums' prefix taken one place late | P1 1997, P3 1596, P5 2000, P6 1997 |
| M3 | ★: the search's low end moved two past the middle | P1 62, P4 85, P6 62 |
| M4 | ★: the search's high end started at half the total | P1 1347, P4 1363, P5 1994, P6 1347 |
| M5 | heap: the `left`-th sum not added | P1 2000, P2 1282, P5 2000, P6 2000 |
| M6 | heap: a run extended by its last number again | P1 1678, P3 1609, P5 1799, P6 1678 |
| M7 | sort: the sums sorted largest first | P1 1632, P6 1632 |
| M8 | sort: each number taken mod 50 | P1 1780, P4 1874, P5 1801, P6 1780 |
| M9 | iter: one place too many skipped | P1 1996, P5 2000, P6 1996 |
| M10 | iter: each start's running maximum, not its sum | P1 1649, P5 1808, P6 1649 |
| M11 | iter: equal sums kept once | P1 587, P5 625, P6 587 |
| M12 | Rust: each run started at a tenth of its first number | P1 1961, P3 1526, P4 1739, P5 1976, P6 1961 |

P1 and P6 kill all twelve, P5 nine, P4 five, P3 three, and P2 one: M5,
the off-by-one at `left`, which a split repeats at `mid + 1`. M7 is seen
only by P1: the sums largest first still split, reverse, triple and add
up to the same total.

The other eight killed: the ★ arm's final correction made with `lo - 1`
(as M1), the sort arm starting at `left` (as M5), the iterator arm taking
one place too few (as M5), the Rust arm's slice one place early (as M5),
and the Rust arm's smallest sum dropped and a zero put first (as M9).
Three crash: the heap arm never extending a run past its second number
pops an empty heap (`unwrap()` on `None`), and the sort and Rust arms
skipping the one-number subarrays index past the sums. Three survive and
are equivalent: the heap arm adding `0 * end`, the Rust arm adding 0 to
a sum, and the Rust arm's modulus written `1_000_000_009` (no answer for
ten numbers of at most 100 reaches either).

## Rust template: B-2026-11-08-16

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` makes 9 edits and then 2, and leaves one error:
`let n = n as usize;` makes `n * (n + 1) / 2` a `usize`, and
`Vec.with_capacity` takes an `i64`, so it is refused as an implicit
coercion that may change sign. The message says to write `as i64`, but
the diagnostic carries no fix. With
`Vec.with_capacity((n * (n + 1) / 2) as i64)` written by hand, the arm
checks and prints the ★ arm's output on every lane.

## Benchmarks

The bench builds 40 arrays of 1000 numbers once and asks 25 random ranges
of places of each by the ★ arm in all five languages. Every
implementation prints `1000 ranges over 40 arrays of 1000 numbers:
checksum 987121753`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `acb9d4c5b` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.209 s |
| Rust (`rustc -O`) | 0.210 s |
| Go | 0.247 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.270 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.283 s |
| Kāra (`karac build`) | 0.286 s |
| Python | 5.55 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is its real time (0.273 s and 0.277 s on one run).

Kāra is 1.05x Rust under overflow checks by median. The two-pointer
sweep's multiplications are checked in Kāra and in that Rust build; plain
`rustc -O` wraps.

## Verification

All five arms print the same output as `sums.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them
(the Rust arm with its hand edit). Under `karac __mir-run` the ★ arm
takes 0.6 s, the sort and Rust arms 1.5 to 1.9 s, the iterator arm 8.5 s
and the heap arm 10.6 s (it pops 500500 sums for the largest example);
the differential takes 4.9 s.

## Writing it

The ★, heap, sort and iterator arms were written in Kāra and `karac fix`
had nothing to change. The iterator arm's
`(0..n).flat_map(|i| nums[i..].iter().scan(0, ..))` checks and runs as
written.
