# 2016. Maximum Difference Between Increasing Elements

Given an integer array `nums` of size `n`, return the largest
`nums[j] - nums[i]` with `0 <= i < j < n` and `nums[i] < nums[j]`, or `-1`
if there is no such pair.

```
nums = [7,1,5,4]   ->  4
nums = [9,4,3,2]   ->  -1
nums = [1,5,2,10]  ->  9
```

**Constraints:** `2 <= n <= 1000`; `1 <= nums[i] <= 10^9`.

## Approaches

| file | mechanism |
|---|---|
| `difference.kara` ★ | one pass keeps the smallest value so far; each later value above it is a candidate. O(n) |
| `difference_brute.kara` | every pair `i < j` compared. O(n^2) |
| `difference_suffix.kara` | a pass from the right fills the largest value after each index, and each index pairs with it. O(n) with O(n) extra |
| `difference_fold.kara` | the ★ arm's pass as a `fold` over the pair (smallest so far, best so far). O(n) |
| `difference_split.kara` | divide and conquer: a run's best is its halves' best or the right half's largest less the left half's smallest; each half reports (smallest, largest, best). O(n log n) |
| `difference_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<i32>`, `let mut ans = -1` raised by `ans.max(..)`, `for &x in nums.iter().skip(1)`, a `&Vec` wrapper), carried by `karac fix` in two rounds |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's three
examples and six more; then the sum and a checksum of the answers for 3000
arrays of 2 to 12 values up to 1 to 20, each value a small step down from
the last with odds of its own, and for 6 arrays of 1000 values up to 7 to
10^9. `difference.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the
statement read literally: every difference `nums[j] - nums[i]` with `i < j`
and `nums[i] < nums[j]` listed, the largest of them, or -1 for none. It
checks 2000 problems drawn as the harness's small arrays are. Every random
choice of a problem (the values, a lift, a value to append) is drawn before
any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every value raised by the same amount leaves the answer |
| P3 | the values reversed, each `v` turned into `21 - v`, leave the answer |
| P4 | every value doubled doubles the answer, -1 staying -1 |
| P5 | a value above all the others appended makes the answer that value less the smallest of the others |
| P6 | each arm agrees with at least three of the other five |

The differential prints `2000 problems: checksum 645619020, 72000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust arm. All thirty are killed, each fails
the same way under both backends, none by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal value counted | P1 612, P6 612 |
| M2 | ★: the smallest never updated | P1 810, P3 965, P5 1414, P6 810 |
| M3 | ★: the second value skipped | P1 277, P3 380, P5 158, P6 277 |
| M4 | brute: a pair compared both ways | P1 901, P6 901 |
| M5 | brute: the last value never paired | P1 267, P3 404, P5 2000, P6 267 |
| M6 | brute: the first pair that rises taken | P1 807, P3 830, P5 1756, P6 807 |
| M7 | suffix: the largest after never carried | P1 362, P5 886, P6 362 |
| M8 | suffix: the last pair never read | P1 104, P3 144, P5 368, P6 104 |
| M9 | suffix: the largest after starting at 20 | P1 1993, P2 1990, P3 1968, P4 1993, P6 1993 |
| M10 | fold: the best replaced, not raised | P1 649, P3 820, P6 649 |
| M11 | fold: the largest so far kept | P1 942, P3 968, P5 1756, P6 942 |
| M12 | fold: the fold starting at 0 | P1 742, P6 742 |
| M13 | split: the cross pair never counted | P1 1258, P5 2000, P6 1258 |
| M14 | split: the cross pair taken left to right | P1 985, P3 330, P5 2000, P6 985 |
| M15 | split: the right half's best dropped | P1 330, P3 518, P5 753, P6 330 |
| M16 | solution: the second value taken as the first smallest | P1 232, P3 404, P5 129, P6 232 |
| M17 | solution: each rise one short | P1 1258, P4 1258, P5 2000, P6 1258 |

P1 and P6 kill all seventeen, P5 twelve, P3 eleven, P4 two and P2 one.
P3 turns the array around and flips its order, which swaps the role of the
earlier, smaller value with the later, larger one, so it sees every edit
that treats the two ends of a pair or of the array unevenly: a smallest
that stops moving (M2, M11), a value or a pair skipped at one end (M3, M5,
M8, M16), the first rise taken (M6), a best replaced by the last rise (M10), and
the split arm's halves or cross pair handled unevenly (M14, M15). It
misses the edits that are their own mirror image: an equal pair counted
(M1), a pair compared both ways (M4), and -1 read as 0 (M12). P5 appends a
value above all the rest, whose answer is fixed by the smallest value, so
it sees the edits that do not pair the last value with the smallest before
it: the last value unpaired (M5), the cross pair never counted (M13), a
largest after that never carries (M7), a rise one short (M17), and the
rest of the uneven ones. P2 and P4 see the edit that reads a value's size
rather than its order, the largest after seeded with 20 (M9); P4 alone
also sees a rise one short (M17), since doubling every value doubles a
rise but not a rise less one.

The other thirteen fail as a kept one does, or with counts of their own.
An equal value counted fails alike in all six arms (M1); the smallest never
updated alike in the ★, fold and Rust arms (M2); -1 read as 0 alike in the
★ and fold arms (M12); only neighbours compared (brute) as M7; the Rust arm
keeping the last rise as the fold arm's best replaced (M10). The ★ arm
measuring each rise from the first value, the suffix arm keeping the
smallest after rather than the largest, and the split arm taking the run's
smallest from its left half alone fail with counts of their own. Two drafts
were replaced: the ★ arm updating the smallest before the check, and the
suffix arm counting the index itself among those after it, both never
fail, since a value is never above itself.

## Verification

Every arm prints the same output as `difference.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports nothing
on any of them. Under `karac __mir-run` the arms take 0.25 s (split) to
0.86 s (brute) and the differential 1.3 s.

The five arms were written in Kāra and checked clean, with no fix.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds. The first, of nine edits, takes the struct, the
`Vec<..>` types, the `&` pattern and the `|&x|` closure, the `&Vec`
parameter and the `::` path, and leaves two errors: `ans.max(x - mn)` is
`i64` against `i32`, and so is the `ans` returned. Rust types `let mut ans
= -1` as `i32` from the `max` call and the return; under the ruling in
design.md §8 a method's receiver does not fix a literal, so `ans` stays
`i64` by design. When this kata was written there was no machine fix for
it (B-2026-11-08-20); there is now, and the second round writes `let mut
ans: i32 = -1` at the binding in one edit (kara 7ae9bc82c0).

## Benchmarks

The bench builds 1000 arrays of 10000 values up to 10^9 once in all five
languages, each value a step down from the last with odds that grow with
the array, and runs the ★ arm on each for 10 rounds: 10000 calls, 10^8
values read. Every implementation prints `10000 calls: sum 9094192211280,
checksum 247372035`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.275 to 0.297 s | 0.284 s |
| Kāra (`karac build`) | 0.277 to 0.291 s | 0.285 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.267 to 0.302 s | 0.286 s |
| Rust (`rustc -O`) | 0.293 to 0.304 s | 0.297 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.287 to 0.324 s | 0.300 s |
| Go | 0.406 to 0.451 s | 0.419 s |
| Python | 13.8 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.252 s) is not above its real time (0.285 s).

The sequential Kāra program is 0.96x Rust under overflow checks and 1.01x
C.