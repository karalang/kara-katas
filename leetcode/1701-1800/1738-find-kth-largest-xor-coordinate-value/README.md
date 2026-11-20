# 1738. Find Kth Largest XOR Coordinate Value

You are given a 2D `matrix` of size `m x n`, consisting of non-negative
integers. You are also given an integer `k`.

The **value** of coordinate `(a, b)` of the matrix is the XOR of all
`matrix[i][j]` where `0 <= i <= a < m` and `0 <= j <= b < n`
**(0-indexed)**.

Find the `k`th largest value **(1-indexed)** of all the coordinates of
`matrix`.

```
matrix = [[5,2],[1,6]], k = 1      ->  7
matrix = [[5,2],[1,6]], k = 2      ->  5
matrix = [[5,2],[1,6]], k = 3      ->  4
```

**Constraints:** `m == matrix.length`; `n == matrix[i].length`;
`1 <= m, n <= 1000`; `0 <= matrix[i][j] <= 10^6`; `1 <= k <= m * n`.

## Approaches

| file | mechanism |
|---|---|
| `kth.kara` ★ | the value of (a, b) is the value above XOR the value to the left XOR the value diagonally above-left, which both of those counted, XOR the cell itself. A table one row and one column wider than the matrix fills in one pass; the m n values are sorted, and the k-th from the top is the answer. O(m n log(m n)) |
| `kth_heap.kara` | each column keeps the XOR of its cells so far, and a row's running XOR of those gives each coordinate's value with no table; a smallest-first `PriorityQueue` keeps the k largest values seen, its top the answer. O(m n log k) |
| `kth_bits.kara` | every value is below `2^20`, so the answer is built a bit at a time from the top: the next bit is 1 exactly when at least k values are at least the answer so far with that bit set. The values come from two rows of running XORs. O(20 m n) |
| `kth_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `vec![vec![0; n + 1]; m + 1]` prefix table filled from `1..=m` and `1..=n`, the values pushed, `sort_unstable_by(\|a, b\| b.cmp(a))`, and `v[k as usize - 1]`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, then one
cell of 0, a 2 by 2 of the largest values, and a largest value in the
corner; then the answers summed and a checksum for 3000 random matrices
of up to 4 by 4 values below 8, 300 of up to 40 by 40 and 3 of up to
1000 by 1000 values up to `10^6`, LeetCode's limits, each with a random
k. `kth.py` mirrors the ★ arm and its output is byte-identical.

```
7
5
4
0
0
1000002
3000 matrices of up to 4 by 4 values below 8: answers sum to 10450, checksum 447115955
300 matrices of up to 40 by 40 values below 1000001: answers sum to 164028051, checksum 343704225
3 matrices of up to 1000 by 1000 values below 1000001: answers sum to 1811184, checksum 907236441
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each coordinate's value the XOR of every cell from (0, 0) to
it, worked out anew, and the k-th largest of them the one with fewer
than k values above it and at least k at or above it. It checks 3000
random matrices of 1 to 4 by 1 to 4 values below 8, each with a random
k. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the matrix transposed gives the same answer |
| P3 | the answer for k + 1 is at most the answer for k |
| P4 | a row and a column of zeros put in front give the same answer |
| P5 | each arm agrees with at least two of the other three |

P4 holds because the zeros add only coordinates of value 0, and no
value is below 0. The differential prints `3000 problems: checksum
906368787, 60000 checks over 4 arms: 0 failures` under every lane in
Verification, and a Python reading of the statement, the values XORed
anew and sorted largest first, gives the same checksum. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M5 keeps the heap at k - 1 values, and
`peek().unwrap()` panics on the first problem whose k is 1, which ends
the run with exit 101 and no count; the other nine fail checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the diagonal value not XORed out | P1 734, P5 734 |
| M2 | ★: the k-th smallest taken, not the k-th largest | P1 2376, P3 1418, P4 2645, P5 2376 |
| M3 | ★: the cell ORed in, not XORed | P1 1916, P5 1916 |
| M4 | heap: each column's running XOR replaced by the cell | P1 1321, P2 1771, P5 1321 |
| M5 | heap: the smallest popped once there are k, not more than k | panics: `unwrap()` on `None` |
| M6 | heap: each value the column's XOR alone, the row's running XOR dropped | P1 1306, P2 1771, P5 1306 |
| M7 | bits: the diagonal read straight above, not above-left | P1 770, P2 792, P4 1275, P5 770 |
| M8 | bits: the lowest bit never set | P1 1493, P5 1493 |
| M9 | solution: every value XORed with 1 more | P1 1198, P4 1402, P5 1198 |
| M10 | solution: the value at k / 2 taken, not k - 1 | P1 1245, P5 1245 |

## Benchmarks

The bench draws 4 random 1000 by 1000 matrices of values up to `10^6`,
LeetCode's largest, each with a random k, all of them first, then
answers each 5 times by the ★ arm in all five languages; each answer
builds its table and its list of `10^6` values anew and sorts it. Every
implementation prints `4 matrices of 1000 by 1000, 5 rounds: answers
sum to 15571865, checksum 984086200`. Kāra and Rust sort with their
`sort`, Go with `slices.Sort` and C with `qsort`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ad6400d909` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.392 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.397 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.497 s |
| Rust (`rustc -O`) | 0.505 s |
| Go | 1.670 s |
| C (`clang -O3`) | 2.342 s |
| Python | 11 s |

The sequential Kāra build is 21% faster than Rust and 20% faster than
Rust with overflow checks on, the equal-safety comparison
(BENCHMARKS.md). C trails here because `qsort` calls its comparator
through a pointer on every compare while sorting the million values,
where Rust and Kāra sort with the comparison inlined.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.365 s and 0.382 s on one
run).

## Verification

All four arms print the same output as `kth.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `ad6400d909`.

## Writing it

The ★ arm took one `karac fix`: `values.len() - k as i64` lost a cast
the `i32` k takes to `i64` by itself. The heap arm's running `value`, a
plain `0` that meets the `i32` cells only through `^=`, was declared
`: i32`. The bits arm checked clean as first written.

LeetCode's Rust template's prefix table, `vec![vec![0; n + 1]; m + 1]`,
became `Vec.filled(m + 1, Vec.filled(n + 1, 0))`, whose `0` keeps the
default `i64` since the table meets the `i32` cells only through `^`.
Its values were pushed into `v`, a `Vec.with_capacity(m * n)` with no
element type of its own, and `v[k as usize - 1]` returned as the `i32`
answer was refused as a narrowing with no fix: the walk from a read
back to its literal knew a fill's elements and bindings pushed into a
collection, not a fill's element pushed into one. Since kara `38ba199571`
(B-2026-11-20-69) it follows the push, and the template took one `karac fix`
of 9 edits: `struct Solution {}` added, `Vec<..>` written `Vec[..]`,
`vec!` written `Vec.filled` with the inner literal `0i32`,
`Vec::with_capacity` written `Vec.with_capacity`, and
`sort_unstable_by` written `sort_by`. `1..=m`, `b.cmp(a)` and `k as
usize - 1` carried over as written.

The differential took one `karac fix`: `k as i64 == m * n` lost a cast
the `i32` k takes by itself. `arm_name` in it indexes a list of string
literals for a `Str`, as #1662's does (B-2026-11-19-131).
