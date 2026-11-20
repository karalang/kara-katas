# 1716. Calculate Money in Leetcode Bank

Hercy wants to save money for his first car. He puts money in the
Leetcode bank **every day**.

He starts by putting in `$1` on Monday, the first day. Every day from
Tuesday to Sunday, he will put in `$1` more than the day before. On every
subsequent Monday, he will put in `$1` more than the **previous Monday**.

Given `n`, return *the total amount of money he will have in the
Leetcode bank at the end of the* `nth` *day.*

```
n = 4    ->  10    (1 + 2 + 3 + 4)
n = 10   ->  37    ((1 + 2 + ... + 7) + (2 + 3 + 4))
n = 20   ->  96
```

**Constraints:** `1 <= n <= 1000`.

## Approaches

| file | mechanism |
|---|---|
| `money.kara` ★ | week k, from 0, puts in k + 1 to k + 7, which is 28 + 7k, so w whole weeks make 28w + 7w(w - 1)/2; the d days after them put in w + 1 to w + d, d(w + 1) + d(d - 1)/2. O(1) |
| `money_days.kara` | day by day: a Monday one more than the Monday before, every other day one more than the day before it. O(n) |
| `money_weeks.kara` | a week at a time, 7m + 21 from a Monday of m, while seven days remain, and the days of the last short week one by one. O(n / 7) |
| `money_solution.kara` | a Rust solution as LeetCode's Rust users write it, each day's deposit from its week and its day in the week, `(1..=n).map(\|i\| (i - 1) / 7 + (i - 1) % 7 + 1).sum()`, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's three examples, one day,
one week and the last day; then the answers summed and a checksum for
every n from 1 to 1000, all the constraints allow. `money.py` mirrors the
★ arm and its output is byte-identical.

```
10
37
96
1
28
74926
every n from 1 to 1000: answers sum to 25593568, checksum 764549939
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a calendar walked a day at a time from a Monday, the weekday
counted 0 to 6, the first Monday's dollar, each later Monday's one more
than the Monday before, and each other day's one more than the day
before. It checks 3000 random n from 1 to 1000. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the nth day's deposit, the answer less the one before it, is one more than the day before's, or on a Monday than the Monday before's |
| P3 | the answer for n + 7 is the answer for n, the first week's, and a dollar for each of the n days |
| P4 | every day puts something in: the answer rises with n |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 229426176, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, `i // 7 + 1 + i % 7` summed over the days,
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. Two first drafts were replaced: one
made the days arm's other days `monday + 1`, which left `today` an `i64`
whose return `karac check` refused as a narrowing, so it never ran; and
one stopped the weeks loop at more than seven days left, which is
equivalent, since a last whole week counted a day at a time comes to
the same. M1, M8 and M9 all add a dollar for every day after the first
week, and M2, M3 and M7 all miscount the short last week by its days;
each group fails the very same checks. P3 holds under most mutants: a
mistake that grows by the same amount each week passes it.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the whole weeks' sum one week too many | P1 2989, P2 450, P5 2989 |
| M2 | ★: the last short week starting from the last whole week's Monday | P1 2550, P2 450, P4 4, P5 2550 |
| M3 | ★: the last short week's days counted from 1, not 0 | P1 2550, P2 450, P5 2550 |
| M4 | days: a week of six days | P1 2951, P2 844, P3 3000, P5 2951 |
| M5 | days: every Monday back to 1 | P1 2988, P2 401, P3 3000, P5 2988 |
| M6 | days: each day two more than the day before | P1 2996, P2 2595, P5 2996 |
| M7 | weeks: the short week's days counted from 1 | P1 2550, P2 450, P5 2550 |
| M8 | weeks: a whole week 7m + 28 | P1 2989, P2 450, P5 2989 |
| M9 | solution: the week taken from i, not i - 1 | P1 2989, P2 450, P5 2989 |
| M10 | solution: a day in the week counted modulo 6 | P1 2989, P2 844, P3 2514, P5 2989 |

## Benchmarks

The bench draws 500000 random n from 1 to 1000, LeetCode's range, all of
them first, then answers each 20 times by the ★ arm in all five
languages. Every implementation prints `500000 values of n, 20 rounds:
answers sum to 253371784380, checksum 222973757`. The work is a handful
of `i32` operations an answer, so the bench mostly measures the loop and
the checksum around it. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.048 s |
| Rust (`rustc -O`) | 0.049 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.049 s |
| Kāra (`karac build`) | 0.051 s |
| Go | 0.052 s |
| C (`clang -O3`) | 0.052 s |
| Python | 2.4 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (0.046 s and 0.047 s on one
run).

## Verification

All four arms print the same output as `money.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ and days arms checked clean as first written. In the days arm the
`total`, `monday` and `today` literals all meet only assignments, `+=`
and the return, so they take `i32` from it.

The weeks arm's `total` and `monday` started as plain `0` and `1`, as in
Rust. The short week adds `monday + d`, `d` an `i32` from `0..left`; in
Kāra an operator does not fix a literal's type (design.md §8 Literals),
so `monday` stayed `i64`, the sum widened, and `total` became an `i64`
returned as the `i32` answer. `karac check` named the narrowing and said
to declare `total: i32`; `karac fix` declared both, `total: i32` and
`monday: i32`.

LeetCode's Rust template took one `karac fix`: `struct Solution {}`
added. `(1..=n).map(..).sum()` over an `i32` range carried over as
written, the sum taking the return type.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
