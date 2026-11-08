# 1502. Can Make Arithmetic Progression From Sequence

A sequence is an arithmetic progression if the difference between any two
consecutive elements is the same. Given an array `arr`, return `true` if
it can be rearranged to form an arithmetic progression, otherwise `false`.

```
arr = [3, 5, 1]   ->  true    ([1, 3, 5] or [5, 3, 1], step 2 or -2)
arr = [1, 2, 4]   ->  false
```

**Constraints:** `2 <= arr.length <= 1000`; `-10^6 <= arr[i] <= 10^6`.

## Approaches

| file | mechanism |
|---|---|
| `progression.kara` ★ | sorted, every gap equals the first. O(n log n) |
| `progression_seen.kara` | no sort: the smallest and largest fix the step `(max - min) / (n - 1)`, which must divide evenly; every number must sit on a step from the smallest, no two on the same one (a `Vec[bool]`). O(n) time and space |
| `progression_place.kara` | in place: each number swapped to its step's index `(x - min) / d` until the slot holds its owner; an equal number already there is a repeat. O(n) time, O(1) extra |
| `progression_iter.kara` | sorted, then `zip` with itself one on (`skip(1)`) and `all` gaps equal the first |
| `progression_solution.kara` | LeetCode's Rust template (`mut arr: Vec<i32>`, `sort`, `windows(2).all(..)`), carried by `karac fix` to one error: blocked by B-2026-11-08-11 |
| `differential.kara` | the four arms that check against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's two
examples and six more, then the count of `true` and a checksum of the
answers for 20000 arrays of 2 to 8 numbers, 2000 of 2 to 200, and 40 of 2
to 1000. A third of the arrays are progressions, a third are progressions
with one number moved by one, and a third are drawn from a small range;
each is shuffled. `progression.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms that check and the
statement read literally: every order of the numbers, tried until one has
every gap equal. It checks 3000 problems of 2 to 8 numbers. Every random
choice of a problem (the numbers, a shuffle, a map `a * x + b`) is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally (arrays of up to 6 numbers) |
| P2 | the numbers shuffled leave the answer |
| P3 | every number mapped to `a * x + b` (`a` in ±1..±3, `b` in -50..50) leaves the answer |
| P4 | a progression stays one with the next term appended |
| P5 | two numbers always make one, and a progression's span divides evenly into `n - 1` steps |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 214397592, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a fifth, once it checks.

## Mutation testing

Twenty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Twelve are kept, three to
each arm. Nineteen are killed, each the same way under both backends, two
of them by a crash; one survives and is equivalent. No two kept ones fail
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the second gap never compared | P1 308, P3 22, P4 214, P5 229, P6 312 |
| M2 | ★: no sort | P1 449, P2 95, P4 206, P6 709 |
| M3 | ★: the last gap never compared | P1 389, P3 200, P4 447, P5 367, P6 447 |
| M4 | seen: a repeat never noticed | P1 127, P3 69, P6 205 |
| M5 | seen: a number off the steps by one let through | P1 115, P3 197, P6 189 |
| M6 | seen: the smallest started at 0, not the first number | P1 376, P3 686, P5 159, P6 460 |
| M7 | place: a number that belongs at or before the cursor passed over | P1 36, P2 28, P3 93, P6 60 |
| M8 | place: a number off the steps answers `true` | P1 233, P2 4, P3 82, P6 379 |
| M9 | place: the cursor moved on after every swap | P1 102, P2 236, P3 103, P6 184 |
| M10 | iter: numbers paired two on, not one | P1 590, P3 59, P4 435, P5 60, P6 852 |
| M11 | iter: the step read from the second and third numbers | P1 369, P5 369, P6 369 |
| M12 | iter: gaps up to the step accepted | P1 383, P3 467, P5 361, P6 488 |

P1 and P6 kill all twelve, P3 ten, P5 six, P2 four and P4 four. P2 sees
the edits that depend on where a number starts: an unsorted read (M2) and
the in-place arm's cursor (M7 to M9).

The other eight: the ★ arm answering `true` at the first unequal gap and
the iterator arm's `any` for `all` fail alike (P1 1025, P5 998, P6 1589);
the iterator arm without its sort fails as M2. The seen and place arms
answering an all-equal array wrongly (`n == 2` and `false` for `true`)
fail with counts of their own but add no property. Two crash under both
backends with an index out of bounds: the seen arm skipping the
divisibility check, and the place arm testing it against `n` for `n - 1`;
both put a number past the last step. One survives: the ★ arm comparing
gaps by absolute value, which is equivalent, since a sorted array's gaps
and its first gap are never negative.

## Rust template

The Rust arm was written as LeetCode's Rust template plus a thin `i64`
wrapper. `karac fix` makes five edits (`Vec<i32>` to `Vec[i32]`,
`Solution::` to `Solution.`, and the like) and stops at the parameter
`mut arr: Vec<i32>`. The parser refuses it, rightly, with advice: write
`arr: mut ref T`, or `arr: own T` and `let mut arr = arr;`. It carries no
edit because it cannot know which was meant (src/parser/items.rs). But a
Rust `mut name: T` parameter always means the second, an owned copy the
function may change, and Rust templates are where this spelling comes
from, so in a program written as Rust the edit is safe. The same error is
also reported four times for the one parameter. With the parameter written
`arr: own Vec[i32]` and `let mut arr = arr;` by hand, the arm checks
after one more `karac fix` edit and prints the ★ arm's
output. B-2026-11-08-11 tracks both.

## Benchmarks

The bench builds 3000 arrays of 2 to 1000 numbers once (the same mix as
the arms) and answers each ten times by the ★ arm: a copy sorted, then the
gaps compared. Every implementation prints `30000 answers over 3000 arrays
of 2 to 1000 numbers: 10280 can, checksum 209330723`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `83c2a5580` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.145 to 0.171 s | 0.152 s |
| Kāra (`karac build`) | 0.144 to 0.196 s | 0.154 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.179 to 0.236 s | 0.202 s |
| Rust (`rustc -O`) | 0.194 to 0.270 s | 0.207 s |
| Go (`slices.Sort`) | 0.572 to 0.687 s | 0.597 s |
| C (`clang -O3`, `qsort`) | 0.805 to 0.907 s | 0.865 s |
| Python | 2.28 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.140 s) is below its real time (0.149 s).

Each language uses its own library sort, so this compares sorts more than
code generation. Kāra's stable sort is 0.75x Rust's stable `sort` under
overflow checks by median. C's `qsort` calls its comparator through a
function pointer for every comparison and is the slowest native program;
Go's `slices.Sort` is a pattern-defeating quicksort. The arrays are mostly
shuffled progressions, so no sort gets a presorted run.

## Verification

Every arm but the Rust template prints the same output as
`progression.py` under `karac __mir-run` (the v2 MIR interpreter),
`karac __mir-llvm-run`, and `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer) with no error. `karac run` and a `karac build` binary print
the same output for every arm and the differential. `karac check` reports
nothing on any of them. Under `karac __mir-run` the arms take 0.9 to 1.2 s
and the differential 1.3 s.

## Writing it

The four arms were written in Kāra and checked with no diagnostic, and
`karac fix` made one edit to the differential.
