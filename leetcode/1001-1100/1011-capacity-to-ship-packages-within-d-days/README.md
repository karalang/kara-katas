# 1011. Capacity To Ship Packages Within D Days

A conveyor belt has packages that must be shipped from one port to
another within `days` days.

The `i`th package on the conveyor belt has a weight of `weights[i]`.
Each day, we load the ship with packages on the conveyor belt (in the
order given by `weights`). We may not load more weight than the maximum
weight capacity of the ship.

Return the least weight capacity of the ship that will result in all
the packages on the conveyor belt being shipped within `days` days.

```
weights = [1,2,3,4,5,6,7,8,9,10], days = 5  ->  15
weights = [3,2,2,4,1,4], days = 3            ->  6
weights = [1,2,3,1,1], days = 4              ->  3
```

**Constraints:** `1 <= days <= weights.length <= 5 * 10^4`;
`1 <= weights[i] <= 500`.

## Approaches

With a fixed capacity, loading each day with as many packages as fit
uses the fewest days, and more capacity never needs more days. So the
answer is the least capacity whose greedy loading fits in `days`; the
arms differ in how they search for it and how they count.

| file | mechanism |
|---|---|
| `ship_within_days.kara` ★ | bisection on the capacity between the heaviest package and the total, each step loading greedily. O(n log(sum)) |
| `ship_within_days_prefix.kara` | bisection with prefix sums: each check jumps a whole day at a time, binary-searching the last prefix within reach. O(n + log(sum) * days * log n) |
| `ship_within_days_next.kara` | raising the capacity to the next break: start at the lower bound; while the loading needs too many days, every capacity below the smallest "day's load plus the package that did not fit" loads the same way, so jump to it |
| `ship_within_days_backward.kara` | bisection with the greedy loading run from the last package backward, which splits the row as well as loading from the front. O(n log(sum)) |
| `ship_within_days_gallop.kara` | galloping search: capacities 1, 2, 4, 8, ... above the heaviest package until one fits, then bisection of the last gap. O(n log(answer - heaviest)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples and six
more (one package; four packages over four days and over one; and
three rows whose answer sits between the bounds); five rows of
LeetCode's longest, 50,000 packages: all 500 over 1 day, over 50,000
and over 7, and weights cycling from 1 to 500 over 100 days and over
49,999; and totals over random rows, each with weights from 1 to a
random top and days from 1 to the row's length: 2,000 of up to 10
packages, 200 of up to 1,000 and 5 of up to 50,000.
`ship_within_days.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: every way to cut the row into at most `days` runs of
consecutive packages, one run a day, and the least capacity any of
them needs, its heaviest day. It checks 2,800 random rows drawn as
above: 2,500 of 1 to 8 packages against the statement, and 300 of up to
1,500 against the other properties.

| | property |
|---|---|
| P1 | the statement's capacity, on the first 2,500 rows |
| P2 | at least the heaviest package and the total spread over the days, and at most the total |
| P3 | greedy loading at the capacity fits in `days`, and at one less does not |
| P4 | the packages in reverse order need the same capacity |
| P5 | every package three times as heavy needs three times the capacity |
| P6 | each arm agrees with at least two of the other four |

P3 is the answer's own certificate: it fits, and nothing smaller does,
since the greedy count only grows as the capacity shrinks. P2 tests
the total first, so a wildly wrong answer cannot overflow the product
it tests next.

It prints `2800 rows of 219251 packages: checksum 588048879, 82500
checks over 5 arms: 0 failures` under `karac __mir-run` (63 s, most of
it the statement's 128 ways to cut each eight-package row and the
other arms' long rows) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the search starting at 0 | P1 734, P2 826, P3 826, P4 770, P6 826 |
| M2 | ★: the first day not counted | P1 1287, P2 1020, P3 1441, P6 1441 |
| M3 | ★: a full day closed early | P1 984, P3 1190, P4 357, P5 1190, P6 1190 |
| M4 | prefix: one day fewer | P1 1343, P3 1487, P6 1487 |
| M5 | prefix: a day filled exactly refused | P1 1718, P3 2016, P5 2016, P6 2016 |
| M6 | prefix: the search ending below the total | P1 495, P2 496, P3 496, P5 496, P6 496 |
| M7 | next: the jump one past the break | P1 769, P3 897, P4 62, P5 992, P6 897 |
| M8 | next: the start below the heaviest package | P1 732, P2 824, P3 824, P4 597, P5 285, P6 824 |
| M9 | next: each new day counted twice | P1 1627, P3 1925, P6 1925 |
| M10 | backward: the first package never loaded | P1 1169, P2 859, P3 1235, P4 912, P6 1235 |
| M11 | backward: a full day closed early | P1 983, P3 1189, P4 357, P5 1189, P6 1189 |
| M12 | backward: the last package never loaded | P1 1175, P2 858, P3 1226, P4 912, P6 1226 |
| M13 | gallop: the heaviest package plus one | P1 1212, P2 288, P3 1306, P5 1306, P6 1306 |
| M14 | gallop: the bisection stopping a step early | P1 652, P2 250, P3 746, P5 746, P6 746 |
| M15 | gallop: one day fewer demanded in the bisection | P1 1203, P2 478, P3 1344, P5 1265, P6 1344 |

P1, P3 and P6 kill all fifteen, P2 and P5 nine each, and P4 seven. The
checks draw no random number that depends on an answer, so every
mutant sees the same rows and their counts can be compared. P3 alone
kills every edit, because an answer that is too large fails its
"one less does not fit" half and one too small fails its "fits" half.
P5 sees the edits that are off by a constant, a one or a single
package, which tripling the weights does not triple. P4 sees the edits
that treat the two ends of the row differently, such as leaving the
first or the last package behind, and those whose answer depends on
where the breaks fall.

Twelve other edits were tried and set aside. Four change no answer: the
★ arm's midpoint taken as `(lo + hi) / 2`, the prefix arm's search
starting at 0 (a capacity below the heaviest package never fits there,
so the search climbs past it), the next arm's spread rounded down, and
the galloping arm's midpoint taken from the top. Five failed exactly
the same checks as a kept one: the ★ arm and the backward arm each
demanding one day fewer, as M4; the prefix arm leaving the last package
behind, as M12; the backward arm counting each new day twice, as M9;
and the galloping arm not counting its first day, as M2. Two never
finished within 300 s under either backend, both in the next arm:
demanding one day fewer, and closing a full day early, each leave it
raising the capacity to the same value forever on a row shipped in one
day, which the edited test can never accept. One stopped with an
integer overflow: the next arm jumping to the largest break returns
`i64.MAX`, and P5 overflows tripling it.

## Verification

Every arm prints the same output as `ship_within_days.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer)
with no error; the differential prints its line under all three.
`karac check` passes all five arms, the differential and the bench
program. `karac run` and a `karac build` binary print the same output
for every arm and the differential. The release build is at kara
`8b6e8a9088`, with the runtime archives rebuilt there. Under `karac
__mir-run` the arms take 3.2 s (backward) to 17.8 s (next).

The backward arm walks its row by index and runs four times as fast as
the ★ arm under `karac __mir-run`, though it does the same work. That
led to kara B-2026-10-29-11, now fixed: `for w in v.iter()` called the
library's `VecIter` `next` once an element, where `for w in v` reads `v`
by position, and ran 8.5 times slower in the interpreter.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages: 20 rows of 50,000
packages, LeetCode's longest, with weights from 1 to 500, drawn once,
and 20 rounds that ship every row, each call with its own number of
days, folding each capacity into a checksum. Every implementation
prints `20 rounds over 20 rows of 50000 packages: checksum 121194998`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `8b6e8a9088`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.940 to 1.013 s | 0.970 s |
| Rust (`rustc -O`) | 0.911 to 1.019 s | 0.954 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.975 to 1.105 s | 0.986 s |
| Go | 0.680 to 0.721 s | 0.702 s |
| Python | 26.7 s | |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.906 to 1.010 s | 0.950 s |
| Kāra (`karac build`) | 1.126 to 1.210 s | 1.167 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. Python's run is about 28 times Kāra's.

v2 took 0.96 times Rust's median time under overflow checks and 0.98
times C's. Under valgrind's cachegrind v2 ran 6,239 million
instructions with 73.5 million branches mispredicted, Rust with
overflow checks 5,669 million and 73.5 million, Rust without them 6,722
million and 70.6 million, and C 6,722 million and 70.6 million. Every
version mispredicts about once a package, on whether it fits the day.
Go ran 0.72 times C's time; we did not look into why.

A plain `karac build` finds nothing to run in parallel here, by
`karac query concurrency`, and its binary runs on one core, yet it
took 1.23 times the sequential build's time and ran 7,228 million
instructions with 80.9 million mispredicted. That is kara B-2026-10-29-12.
