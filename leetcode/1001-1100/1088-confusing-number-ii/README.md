# 1088. Confusing Number II

A **confusing number** is a number that when rotated 180 degrees becomes
a different number with **each digit valid**.

We can rotate digits of a number by 180 degrees to form new digits.

- When `0`, `1`, `6`, `8`, and `9` are rotated 180 degrees, they become
  `0`, `1`, `9`, `8`, and `6` respectively.
- When `2`, `3`, `4`, `5`, and `7` are rotated 180 degrees, they become
  **invalid**.

Note that after rotating a number, we can ignore leading zeros. For
example, after rotating `8000`, we have `0008` which is considered as
just `8`.

Given an integer `n`, return *the number of **confusing numbers** in the
inclusive range* `[1, n]`.

```
n = 20   ->  6    (6, 9, 10, 16, 18, 19)
n = 100  ->  19   (6, 9, 10, 16, 18, 19, 60, 61, 66, 68, 80, 81, 86, 89, 90, 91, 98, 99, 100)
```

**Constraints:** `1 <= n <= 10^9`.

The arms take `n` as an `i64` and return the count as an `i64`.

## Approaches

| file | mechanism |
|---|---|
| `confusing_number_ii.kara` ★ | a depth-first walk over the numbers made only of the digits that rotate, each carrying its rotation: appending d to a number of k digits puts d's rotation in front of the old rotation, at 10^k. A number is counted when it differs from its rotation, and a walk stops at the first digit that takes it past n. O(the numbers up to n made of those digits, about 2 million for n = 10^9) |
| `confusing_number_ii_stack.kara` | the same walk on an explicit stack of `struct`s (number, rotation, power of ten), the digits' rotations in a `Map[i64, i64]`; a digit not in the map does not rotate (`if let Some(r) = turn.get(d)`) |
| `confusing_number_ii_count.kara` | counted, not walked: the numbers up to n made of the rotating digits, counted from n's decimal digits (at each place, the rotating digits below n's digit there times `5.pow(..)` of the places after it), less those that read the same rotated, which are built from the middle out as `String`s (`f"{a}{inner}{b}"` over the five pairs) and compared with n. O(log n) and O(the 2500 same-reading strings of ten digits) |
| `confusing_number_ii_text.kara` | every number made of the rotating digits, in order, read off a counter in base 5 whose digits 0 to 4 stand for 0, 1, 6, 8, 9; each rotated as text, its characters turned in reverse order, and read back with `i64.parse`, which drops the leading zeros. O(those numbers, times their length) |
| `confusing_number_ii_layers.kara` | one layer per length, with iterator chains: each layer the last one's numbers within n (`into_iter().filter(..)`) followed by every rotating digit (`flat_map` over a nested `map`), each counted by `filter(..).count()` when its rotation, worked out with `%` and `/`, differs from it |
| `confusing_number_ii_solution.kara` | LeetCode's Rust template (`struct Solution;`, `n: i32`, a counter passed down as `&mut i32`, an associated `fn dfs` over an array of `(digit, rotation)` pairs walked with `for &(d, r) in pairs.iter()`, `Self::dfs(.., &mut count)`, `\|\|`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's two examples and ten more
up to `1000000 -> 15427`, the sum of the answers for every n from 1 to
1000 (`47412`), and a checksum over 200 random n of 1 to 6 digits
(`527520770`). `confusing_number_ii.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a number is confusing when each of its digits turns and the
digits turned, read from the last to the first with leading zeros
ignored, make another number; the answer counts them from 1 to n. It
checks 2000 problems: 1400 with n from 1 to 300 and 600 with n from 1
to 1200, each with a window of 1 to 200 numbers below n. Every random
choice is drawn before any arm answers, and the literal reading of every
number up to 1200 is worked out once.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer for n is the answer for n - 1, plus one exactly when n is confusing |
| P3 | the answer for n is the answer for the greatest number up to n whose digits all turn |
| P4 | the answer for n, less the answer for n - w, is the number of confusing numbers above n - w, counted one by one |
| P5 | the answer is the count of numbers up to n whose digits all turn, which is the greatest of them read in base 5 with 0, 1, 6, 8, 9 as its digits, less those of them that read the same turned |
| P6 | the answer for n is the answer for one less than the next number whose digits all turn |

All 72,000 checks pass on every arm: `2000 problems: checksum 381947380,
72000 checks over 6 arms: 0 failures`. A Python reading of the same
problems, counting every number by its text, gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All thirty are caught,
each the same way under both backends. Fifteen are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: 6 read as 6 upside down | P1 1529, P2 27, P4 935, P5 1529 |
| M2 | ★: n itself left out | P1 264, P2 298, P3 1477, P4 439, P5 264, P6 128 |
| M3 | ★: the turned digit put last, not first | P1 1947, P2 84, P4 1470, P5 1947 |
| M4 | ★: a number ending in 0 never counted | P1 1947, P2 56, P4 1532, P5 1947 |
| M5 | stack: only the last digit turned | P1 1942, P2 44, P4 1437, P5 1942 |
| M6 | stack: nothing past three digits | P1 101, P2 21, P4 99, P5 101 |
| M7 | count: a leading 0 counted | P1 2000, P2 16, P4 917, P5 2000 |
| M8 | count: n itself never counted among the rotating | P1 322, P2 333, P3 1678, P4 756, P5 322, P6 173 |
| M9 | count: n left out of the same-reading ones | P1 58, P2 121, P3 201, P4 537, P5 58, P6 45 |
| M10 | text: the counter's digits out of order | P1 547, P2 163, P4 788, P5 547 |
| M11 | text: the number read backwards | P1 1947, P2 249, P4 1589, P5 1947 |
| M12 | layers: no leading 9 | P1 1952, P2 39, P4 984, P5 1952 |
| M13 | layers: the same-reading ones counted | P1 1957, P2 322, P4 1614, P5 1957 |
| M14 | solution: the rotation shifted a place | P1 1621, P2 59, P4 1151, P5 1621 |
| M15 | solution: no walk past a number that reads the same | P1 1947, P2 193, P4 1531, P5 1947 |

P1, P2, P4 and P5 catch all fifteen; P3 and P6 three each. P3 and P6
compare the answer at n with the answer at another number that has the
same rotating numbers below it, so they see only the edits that treat n
itself apart from the numbers below it: M2, and the count arm's two
comparisons with n (M8, M9). Every other edit is wrong in the same way
at both ends. P1 and P5 fail on exactly the same problems for every
edit, as both compare one answer at n with a count that does not depend
on the arm. M9 is the hardest to see: it is wrong only when n itself
reads the same turned, 58 of the 2000 problems.

Of the fifteen not kept, six fail exactly as a kept edit and nine fail
in ways of their own but were not needed. n left out in the stack, text,
layers and solution arms (the last by answering for n - 1) fails as M2;
the text arm turning its digits without reversing them as M3; and the
layers arm summing the turned digits as M5. Not needed: 9 not turning in
the ★ and stack arms (which fail alike), 0 left out in the stack and
layers arms (alike), the count arm's five leading digits for a shorter
length and 6 and 9 taken as their own middles, the text arm reversing
without turning, and the solution arm reading 9 as 9 and stopping at the
leading 0.

## Verification

Every arm prints the same output as `confusing_number_ii.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file. Under `karac __mir-run` the differential takes 34 s.

The arms found no compiler gap. The text arm first reached for Rust's
`trim_start_matches('0')` to drop the rotation's leading zeros; karac
names the Kāra alternatives, and the arm reads the rotation back with
`i64.parse`, which drops them anyway. The bench found a gap in the build:
a plain `karac build` that parallelized nothing still shipped the
lowering auto-par records its candidates with, and ran 15% slower than
the `KARAC_AUTO_PAR=0` build (below).

Every file went through `karac fix`. In the count arm it put `.iter()`
after `.bytes()`, wrote `s.parse()` as `i64.parse(s)`, and dropped the
`.to_string()` from the literals of a returned list of `String`s; in the
harness it wrote `n = n * 10` as `n *= 10`. The Rust arm reaches a
clean check in two rounds and gives the text the arm holds: first the
syntax (`struct Solution;` to `struct Solution {}`, `Self::` to
`Solution.`, `Solution::` to `Solution.`, `&mut i32` to `mut ref i32`,
`&mut count` to `mut count`, `for &(d, r)` to `for (d, r)`, and `||` to
`or`); then `: i32` on `count`, the `as i64` on `n` dropped, and `mut`
at the recursive call's `count`.

## Benchmarks

The bench draws 400 random n from 1 to 10^9, LeetCode's largest, once,
and answers each with the ★ arm, folding the answers into a total and a
checksum. Every implementation prints `400 n up to 10^9: 345592512
confusing numbers, checksum 529503063`. Each mirror walks the same
recursion over the same five digits, with the rotation of a digit from a
`match` (Rust), a `switch` (C and Go) or a dictionary (Python).

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `610ff4d444`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.837 to 0.953 s | 0.863 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.844 to 0.936 s | 0.880 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.015 to 1.184 s | 1.065 s |
| Kāra (`karac build`, before B-2026-11-09-57's fix) | 1.157 to 1.245 s | 1.223 s |
| Rust (`rustc -O`) | 1.354 to 1.555 s | 1.450 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.569 to 1.811 s | 1.649 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.611 to 1.858 s | 1.677 s |
| Go | 2.120 to 2.354 s | 2.190 s |
| Python | 82.3 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. The work is about 2 million calls of one short
recursion per n, all integer arithmetic. Kāra takes 65% of the time of
Rust with overflow checks at the same ISA and 73% of plain `rustc -O`'s,
and Go takes 2.1x Kāra's; C takes 81% of Kāra's time, Python 77x. Why
Rust trails here is not measured.

Every loop the auto-par gate looked at is refused (the walk is
recursive, the bench's `main` carries its seed and folds into its
checksum), and a plain `karac build` ran on one core (user 1.205 s of
1.223 s real), yet it was 15% slower than the sequential build and its
binary differed. With nothing to run as tasks, the build kept the
lowering that records the candidates, which ends a block between every
statement to delimit them. It now lowers the program in order, and the
plain build's binary is byte-identical to the `KARAC_AUTO_PAR=0` one
(kara B-2026-11-09-57, pinned by `tests/kata_1088_auto_par_in_order.rs`).
