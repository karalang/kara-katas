# 2044. Count Number of Maximum Bitwise-OR Subsets

Given an integer array `nums`, find the maximum possible bitwise OR of a
subset of `nums` and return the number of different non-empty subsets with
the maximum bitwise OR. An array `a` is a subset of an array `b` if `a` can
be obtained from `b` by deleting some (possibly zero) elements of `b`. Two
subsets are considered different if the indices of the elements chosen are
different. The bitwise OR of an array `a` is `a[0] OR a[1] OR ... OR
a[a.length - 1]` (0-indexed).

```
nums = [3,1]       ->  2     ([3] and [3,1])
nums = [2,2,2]     ->  7     (every non-empty subset)
nums = [3,2,1,5]   ->  6
```

**Constraints:** `1 <= nums.length <= 16`; `1 <= nums[i] <= 10^5`.

OR only adds bits, so no subset's OR is above the OR of every value, and
the whole array reaches it: that is the maximum. With at most 16 values
there are at most 65535 non-empty subsets, few enough to try them all.

## Approaches

| file | mechanism |
|---|---|
| `subsets.kara` ★ | the target as a `fold` of `\|`, then a recursive take-or-skip search over the values counting the full choices whose OR is the target. O(2^n) |
| `subsets_masks.kara` | every mask from 1 to `2^n - 1`, its OR built bit by bit from `mask >> i & 1`, the target by a `for` loop with `\|=`. O(n 2^n) |
| `subsets_table.kara` | subsets counted by OR value: `ways[v]` subsets of the values so far have OR `v`, and a new value `x` adds `old[v]` to `ways[v \| x]`; the table sized to the first power of two above the target. O(n V) |
| `subsets_lowbit.kara` | each mask's OR from the mask less its lowest set bit, `or_of[mask & (mask - 1)] \| nums[mask.trailing_zeros()]`, the greatest OR and its count kept as the masks go by. O(2^n) |
| `subsets_iter.kara` | iterators throughout: `(1..1 << n).filter(\|mask\| (0..n).filter(..).fold(0, ..) == target).count()`. O(n 2^n) |
| `subsets_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<i32>`, `fold(0, \|a, &x\| a \| x)`, a running OR in a variable named `or`), carried by `karac fix` in one round (six edits) to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the sum and a checksum of the answers for 2000
arrays of 1 to 12 values up to 1 to 64, and for 20 arrays of 16 values,
the most the constraints allow (values up to 100000, 1024, 16 and 2 in
turn). `subsets.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every non-empty subset listed as positions, its OR taken, the
greatest OR found among them (not assumed to be the OR of everything), and
the subsets that reach it counted. It checks 1500 arrays of 1 to 10 values
up to 1 to 60, each with a shuffle. Every random choice is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the values shuffled leave the answer |
| P3 | the OR of everything appended adds `2^n`: every old subset, the empty one too, joined with it reaches the greatest OR |
| P4 | every value doubled leaves the answer |
| P5 | a value with a bit above all the others (64) appended leaves the answer: only that value with old values that reach the old greatest OR reaches the new one |
| P6 | each arm agrees with at least three of the other five |

The differential prints `1500 arrays: checksum 760045558, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each Kāra arm and two to the Rust-template arm. All thirty are killed, each
fails the same way under both backends, none by a crash, and no two kept
ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the target taken as the largest value | P1 979, P3 979, P5 931, P6 979 |
| M2 | ★: the last value never chosen for | P1 1500, P2 797, P3 1500, P5 1068, P6 1500 |
| M3 | ★: a taken value replacing the OR | P1 1291, P2 109, P5 335, P6 1291 |
| M4 | masks: the full set left out | P1 1500, P6 1500 |
| M5 | masks: the target a sum (`+=` for `\|=`) | P1 1313, P3 1500, P6 1313 |
| M6 | masks: the last value never in a mask | P1 1317, P2 797, P3 1272, P5 1068, P6 1317 |
| M7 | table: the empty subset counted twice | P1 1500, P3 1500, P6 1500 |
| M8 | table: the table updated in place | P1 1500, P2 964, P3 1500, P5 1500, P6 1500 |
| M9 | table: a value XORed in | P1 1312, P3 1500, P6 1312 |
| M10 | lowbit: the smaller mask taken by a shift | P1 1177, P2 825, P3 1266, P5 1068, P6 1177 |
| M11 | lowbit: the value at the highest bit | P1 1196, P2 1068, P3 1165, P5 1500, P6 1196 |
| M12 | lowbit: the first value alone skipped | P1 234, P2 59, P5 234, P6 234 |
| M13 | iter: a mask's values summed | P1 1313, P3 1500, P5 334, P6 1313 |
| M14 | iter: the first value never in a mask | P1 1324, P2 789, P6 1324 |
| M15 | iter: the target seeded with bit 0 | P1 137, P3 137, P4 1363, P6 137 |
| M16 | solution: the second value never in a mask | P1 1179, P2 771, P3 149, P5 149, P6 1179 |
| M17 | solution: the target XORed | P1 1233, P3 1500, P5 75, P6 1233 |

P1 and P6 kill all seventeen, P3 thirteen, P5 eleven, P2 nine and P4 one.
P2 sees the edits that depend on where a value sits: a value at one
position never chosen (M2, M6, M14, M16), the OR replaced by the last value
taken (M3), the table updated in place, where a value can meet its own
update (M8), and the lowbit arm's masks read by position (M10, M11, M12).
P3 appends the OR of everything, which every old subset joined with it
reaches; it misses only the edits that still count those `2^n`: the OR
taken as the last value (M3), the full set left out of the old and the new
array alike (M4), and the first value treated differently, which the
appended last one never is (M12, M14). P5 appends 64, which only the
subsets that already reach the greatest OR may join; it sees the edits that
lose the appended value (M2, M6, M16, the last on one-value arrays, where 64
is the second), that misread the new top bit (M10, M11, M12), or that take a
target other than the OR (M1, M3, M8, M13, M17). P4 doubles every value,
which clears bit 0 everywhere, so only the target seeded with bit 0 (M15)
fails it: no doubled subset reaches that target.

The other thirteen fail as a kept one does, or are left out because their
arm already keeps three. The ★ arm's taken value XORed in fails as M9; the
masks arm's complement read, the table arm's full set left out, the lowbit
arm's new best counted from zero and the iterator arm's full set skipped
fail as M4; the masks arm's OR as its last value and the Rust arm's fail as
M3; the Rust arm's last value's masks left out fails as M2. The ★ arm's
skipped value counted twice, the table arm's count overwritten by a value
and the lowbit arm's count reset on a tie fail alike, on P1, P3 and P6 at
1250 each, but none is kept, since each arm keeps three already; the
iterator arm's missing masks counted and the Rust adapter's bit 0 cleared
fail on patterns of their own and are left out for the same reason.

## Verification

Every arm prints the same output as `subsets.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 0.9 s (table) to 48 s (iter) and the
differential 43 s, on kara 991c45adcd.

The five Kāra arms met no compiler gap and checked as written. The table
arm was first sized at `2^17` for every array, which is right but slow:
2000 small arrays each swept a 131072-entry table per value, minutes under
the interpreter; it now sizes the table to the target.

The Rust arm was written as LeetCode's Rust template. Its running OR is a
variable named `or`, a keyword in Kāra, and `karac fix` escapes it as
`r#or`. The first `karac fix` escaped the declaration and the comparison
but not `or |= nums[i];`: the parser offered the `r#` fix only before `=`,
the arithmetic compound assignments and the binary operators, not before
`|=`, `&=`, `^=`, `<<=` or `>>=`, and reported the use twice with no edit,
so the fix loop stopped there. Those five now take the fix too (kara
991c45adcd, `tests/kata_2044_keyword_compound.rs`), and `karac fix` carries
the arm in one round of six edits: `Vec<i32>` to `Vec[i32]`, `|a, &x|` to
`|a, x|`, and every `or` to `r#or`.

## Benchmarks

The bench builds 2000 arrays of 16 values once in all five languages, the
most the constraints allow, and runs the ★ arm's take-or-skip search on
each: 2000 calls of `2^17 - 1` steps. Every implementation prints `2000
calls: sum 115231414, checksum 901834645`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `991c45adcd` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.303 to 0.358 s | 0.336 s |
| Rust (`rustc -O`) | 0.333 to 0.395 s | 0.366 s |
| Go | 0.469 to 0.522 s | 0.489 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.539 to 0.638 s | 0.576 s |
| Kāra (`karac build`) | 0.599 to 0.641 s | 0.610 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.627 to 0.701 s | 0.656 s |
| Python | 17.4 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.604 s) is not above its real time (0.610 s).

The sequential Kāra program is 1.14x Rust under overflow checks and 1.96x
C.
