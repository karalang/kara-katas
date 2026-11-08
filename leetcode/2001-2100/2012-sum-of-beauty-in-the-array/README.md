# 2012. Sum of Beauty in the Array

You are given an integer array `nums`. For each `1 <= i <= nums.length - 2`
the beauty of `nums[i]` is:

- 2, if `nums[j] < nums[i] < nums[k]` for every `0 <= j < i` and every
  `i < k <= nums.length - 1`;
- 1, if `nums[i - 1] < nums[i] < nums[i + 1]` and the previous condition
  does not hold;
- 0, if neither holds.

Return the sum of the beauties.

```
nums = [1,2,3]    ->  2
nums = [2,4,6,4]  ->  1
nums = [3,2,1]    ->  0
```

**Constraints:** `3 <= nums.length <= 10^5`; `1 <= nums[i] <= 10^5`.

Every value before `nums[i]` is smaller exactly when the largest of them
is, and every value after is larger exactly when the smallest is, so a
running maximum from the left and a running minimum from the right decide
the 2s.

## Approaches

| file | mechanism |
|---|---|
| `beauty.kara` ★ | a pass from the right fills the smallest value after each index; a pass from the left keeps the largest before and scores each middle index. O(n) |
| `beauty_brute.kara` | each index checked against every value before and after it, stopping at the first that breaks the order; failing that, against its two neighbours. O(n^2) at worst |
| `beauty_scan.kara` | the largest value up to each index by `scan`, the smallest from each index on by `scan` over `rev()`, then the middle indices scored by `map` and `sum`. O(n) |
| `beauty_sorted.kara` | the values after the current index counted in a `SortedMap`, each taken out as the walk reaches it, so the smallest after is the first key. O(n log n) |
| `beauty_flags.kara` | a pass from the left marks each index above everything before it, a pass from the right each index below everything after it; marked by both is worth 2. O(n) |
| `beauty_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, `vec![0; n]` prefix and suffix vectors, `&&`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 3000
arrays of 3 to 12 values up to 1 to 20, each value a step up from the last
with odds of their own, and for 6 arrays of 3000 values up to 100 or
100000. `beauty.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the
statement read literally: for each middle index, every value before and
every value after compared with it, then its neighbours. It checks 2000
problems drawn as the harness's small arrays are. Every random choice of a
problem (the values, a shift) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values reversed, each `v` turned into `top + 1 - v`, leave the answer |
| P3 | every value raised by the same amount leaves the answer |
| P4 | every value doubled leaves the answer |
| P5 | a value above all the others appended adds what the old last value is now worth: 2 above everything before it, else 1 above its left neighbour |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 730509498, 72000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an index equal to the largest before worth 2 | P1 107, P2 443, P5 811, P6 107 |
| M2 | ★: a peak counted as 1 | P1 911, P2 793, P5 549, P6 911 |
| M3 | ★: the largest before starting at the first middle value | P1 438, P2 361, P5 73, P6 438 |
| M4 | brute: a value after equal allowed | P1 413, P2 443, P6 413 |
| M5 | brute: the values after never checked | P1 1341, P2 1347, P6 1341 |
| M6 | brute: the last value never checked | P1 249, P2 410, P5 249, P6 249 |
| M7 | scan: the prefix maximum starting at 10 | P1 342, P2 208, P3 311, P4 245, P5 134, P6 342 |
| M8 | scan: the suffix minima never reversed back | P1 347, P2 306, P5 314, P6 347 |
| M9 | scan: the suffix minimum's state never carried | P1 375, P2 588, P6 375 |
| M10 | sorted: the current value never taken out | P1 436, P5 284, P6 436 |
| M11 | sorted: the largest key read | P1 575, P2 764, P5 1260, P6 575 |
| M12 | sorted: a 1 needing only the right neighbour | P1 1257, P2 1028, P5 1167, P6 1257 |
| M13 | flags: the second value never marked above | P1 414, P2 311, P5 60, P6 414 |
| M14 | flags: the top never raised | P1 281, P2 288, P5 834, P6 281 |
| M15 | flags: the flags joined by `or` | P1 1632, P5 1716, P6 1632 |
| M16 | Rust: the first value left out of the prefix maximum | P1 220, P2 410, P5 73, P6 220 |
| M17 | Rust: a neighbour tie worth one | P1 275, P2 880, P5 690, P6 275 |

P1 and P6 kill all seventeen, P2 fifteen, P5 fourteen, and P3 and P4 one
each. P2 turns the array around and flips its order, which swaps "before"
with "after" and "smaller" with "larger", so it sees every edit that treats
the two sides unevenly; it misses the two that are their own mirror image:
the current value counted among those after it, which leaves no index a 2
(M10), and the two flags joined by `or` (M15). P3 and P4 see only the
prefix maximum seeded with 10, the one edit that reads a value's size
rather than its order (M7); the Rust arm's prefix left at the `0` it was
filled with (M16) forgets the first value, a mistake of order, not size.
P5 appends a
value above all the rest; it misses the edits whose mistake sits on the
"after" side, where the new largest value changes nothing: a value after
allowed to equal (M4), the values after never checked (M5), and the suffix
minimum's state lost (M9).

The other thirteen fail as a kept one does, or with counts of their own.
An equal value before allowed fails alike in the ★, brute and flags arms
(M1's counts). Leaving no index a 2 fails alike five ways: the ★ arm's
smallest after taken from the index itself, the sorted arm's first value
counted as after, the flags arm's bottom starting at the first value, the
Rust arm's prefix read at the index itself, and M10. A maximum that stops
rising fails alike three ways: the ★ arm's never raised, the brute arm
checking only the first value before, and the sorted arm raising it only
at a 2, which M14 also fails as. The Rust arm's suffix minimum taking the
maximum fails as M11. The scan arm's 1 needing only its left neighbour and
its first middle index skipped, and the Rust arm's last middle index
skipped, fail with counts of their own. Three drafts were replaced: the
sorted arm taking out a value with copies left, twice, which indexes a key
no longer there and stops ("key not found"); the ★ arm counting a 2 as a 1
as well, which fails as M10; and the flags arm marking an index equal to
the bottom, which fails as M4.

## Verification

Every arm prints the same output as `beauty.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any of
them. Under `karac __mir-run` the arms take 0.23 s (brute) to
0.44 s (scan) and the differential 2.4 s.

The five arms were written in Kāra and checked clean, the scan arm in
Kāra's own `scan`, whose closure takes the state and returns the next state
with the item (`Some((m, m))`). Written first in Rust's shape, `*m =
m.max(x); Some(*m)` over a `&mut` state, it drew six "drop the `*`" fixes
that leave `m = m.max(x); Some(m)` and a type error, `expected
Option[(i64, OutV)]`, with no fix and no word on the shape `scan` wants
(B-2026-11-08-45).

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (10, 2, 2 and 1 edits).
The first two carry the struct, the `Vec<..>` types, the two `vec![0; n]`,
the `&&`s, the `&Vec` parameter and `|&x|`, and the `::` path. That leaves
`pre[i - 1].max(nums[i])` and `suf[i + 1].min(nums[i])`, `i64` against
`i32`: `Vec.filled(n, 0)` gave its `0` the default `i64` where it was
written, where Rust types it `i32` from the `nums[i]` stored into it
later. Under the ruling in design.md §8 that is by design, since the
element is first read as a method's receiver, which does not fix a
literal; the third round writes the fix the ruling names, the suffix
`Vec.filled(n, 0i32)`, in both (B-2026-11-08-20, B-2026-11-08-53). The
fourth drops the wrapper's `ref`.

## Benchmarks

The bench builds 1000 arrays of 2000 values up to 100000 once in all five
languages, each value a step up from the last with odds that grow with the
array, and runs the ★ arm on each for 5 rounds: 5000 calls, two passes over
2000 values each. Every implementation prints `5000 calls: sum 6469800,
checksum 734941934`. Every language allocates the suffix minima per call,
as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.066 to 0.093 s | 0.072 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.063 to 0.098 s | 0.072 s |
| C (`clang -O3`) | 0.061 to 0.088 s | 0.075 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.069 to 0.093 s | 0.075 s |
| Kāra (`karac build`) | 0.069 to 0.093 s | 0.075 s |
| Go | 0.128 to 0.146 s | 0.139 s |
| Python | 3.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.060 s) is not above its real time (0.075 s).

The sequential Kāra program is 1.03x Rust under overflow checks and 1.00x
C.