# 1052. Grumpy Bookstore Owner

There is a bookstore owner that has a store open for `n` minutes. You are
given an integer array `customers` of length `n` where `customers[i]` is the
number of the customers that enter the store at the start of the `i`th
minute and all those customers leave after the end of that minute.

During certain minutes, the bookstore owner is grumpy. You are given a
binary array `grumpy` where `grumpy[i]` is `1` if the bookstore owner is
grumpy during the `i`th minute, and is `0` otherwise.

When the bookstore owner is grumpy, the customers entering during that
minute are not **satisfied**. Otherwise, they are satisfied.

The bookstore owner knows a secret technique to remain **not grumpy** for
`minutes` consecutive minutes, but this technique can only be used **once**.

Return the **maximum** number of customers that can be satisfied throughout
the day.

```
customers = [1,0,1,2,1,1,7,5], grumpy = [0,1,0,1,0,1,0,1], minutes = 3  ->  16
customers = [1], grumpy = [0], minutes = 1                              ->  1
```

**Constraints:** `1 <= minutes <= n <= 2 * 10^4`;
`0 <= customers[i] <= 1000`; `grumpy[i]` is `0` or `1`.

## Approaches

The customers of the calm minutes are satisfied whatever happens. The
technique adds the customers of the grumpy minutes inside its window, so
the answer is the calm total plus the most any window of `minutes` saves.

| file | mechanism |
|---|---|
| `grumpy.kara` ★ | one pass: the calm total, and a window of `minutes` slid along the day, adding the minute that enters and taking off the one that leaves. O(n) |
| `grumpy_prefix.kara` | a `Vec` of prefix sums of the customers lost, each window's saving a difference of two entries. O(n) |
| `grumpy_every.kara` | every start tried, the grumpy customers inside the window added up afresh. O((n - m + 1) m) |
| `grumpy_iter.kara` | the lost customers as a `Vec` from `zip` and `map`, the calm total from `filter`, and the best of `lost.windows(minutes)` summed. O((n - m + 1) m) |
| `grumpy_total.kara` | the satisfied total itself slid: the window starts at minute 0, and each step takes off a grumpy minute that leaves and adds one that enters. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 15 lines: the answers for LeetCode's two
examples and eight more (an owner never grumpy, always grumpy, and a day
whose two best windows sit at either end, among them); the total and a
checksum of the answers for 3000 random days of 1 to 10 minutes with up to
5 customers a minute, and for 300 days of 1 to 1000 minutes with up to
1000; and one day of 20000 minutes, the limit, with techniques of 1, 100
and 20000 minutes. `grumpy.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each minute the technique can start at, every customer is
counted as satisfied when the owner is calm that minute or the technique
is on, and the best start is kept. It checks 3000 random days: 2000 of 1
to 8 minutes with up to 3 customers, the owner grumpy half the time, and
1000 of 1 to 30 minutes with up to 50, grumpy a third of the time.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is at least the calm minutes' customers and at most all the customers, and all of them when the technique lasts the day |
| P3 | the day reversed gives the same answer |
| P4 | a technique a minute longer satisfies no fewer |
| P5 | every minute's customers doubled doubles the answer, and a calm minute of 7 customers added at either end adds 7 |
| P6 | each arm agrees with at least two of the other four |

P4 holds because a window a minute longer covers every window a minute
shorter. P5's calm minute is satisfied whatever happens and moves no
window's saving, since the windows still cover the same grumpy minutes.

The differential prints `3000 days: checksum 336613315, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (3.9 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three to
each arm. All fifteen are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the window never shrinks | P1 1041, P6 1041 |
| M2 | ★: the last window, not the best | P1 1148, P3 1537, P5 1070, P6 1148 |
| M3 | ★: the window a minute longer | P1 566, P6 566 |
| M4 | prefix: the window a minute shorter | P1 1442, P2 316, P3 831, P5 426, P6 1442 |
| M5 | prefix: the calm total counts the grumpy minutes instead | P1 2781, P2 2163, P5 3000, P6 2781 |
| M6 | prefix: the sums not cumulative | P1 1779, P2 392, P3 1534, P4 600, P5 452, P6 1779 |
| M7 | every: the window a minute shorter | P1 1433, P2 320, P3 831, P5 405, P6 1433 |
| M8 | every: the first window only | P1 1123, P3 1537, P5 1045, P6 1123 |
| M9 | every: the worst window | P1 2505, P2 578, P6 2505 |
| M10 | iter: the worst window | P1 1734, P5 984, P6 1734 |
| M11 | iter: windows of one minute | P1 1386, P2 264, P6 1386 |
| M12 | iter: the larger of the calm total and the saving, not their sum | P1 2148, P2 375, P5 856, P6 2148 |
| M13 | total: the first window a minute longer | P1 716, P2 379, P3 1039, P4 448, P5 1470, P6 716 |
| M14 | total: the second start never tried | P1 845, P3 1216, P4 340, P5 1567, P6 845 |
| M15 | total: a calm minute entering added again | P1 1660, P2 852, P3 1873, P4 877, P5 2978, P6 1660 |

P1 and P6 kill all fifteen, P5 eleven, P2 nine, P3 eight and P4 four. M1
and M3 are seen only by P1 and P6: a window that never shrinks saves every
grumpy customer up to its end, and one a minute longer saves a minute
more, so both answer more than the literal reading, but within all the
customers, the same both ways along the day, and growing with the
technique as the true answer does. P4 sees the edits that can answer less
for a longer technique: sums that are not cumulative (M6) and the total
slid from a wrong start (M13, M14, M15). P3 sees the edits that favour one
end of the day.

Fifteen other edits were set aside. Six fail exactly as a kept one does:
the prefix arm taking everything lost up to a window's end, or starting
from all that is lost, as M1; the every and iter arms counting the grumpy
minutes in the calm total, as M5; the iter arm leaving each window's first
minute out, as M4; and the total arm keeping the last window, as M2. Six
fail in pairs with no kept twin: the ★ and total arms taking off a calm
minute that leaves; the prefix and every arms never trying the last
window; and the every and iter arms saving the calm minutes. Three fail in
ways of their own: the ★ arm counting a grumpy minute in the calm total
too, or skipping the first minute, and the total arm never keeping its
first window.

## Verification

Every arm prints the same output as `grumpy.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. The runs used a release build of kara `6c8a806480`. Under `karac
__mir-run` the arms take 0.7 s (★, prefix, total) to 15 s (iter, whose
windows are summed one by one).

Every arm reached a clean check through `karac fix` alone. Written the way
Rust writes them, they drew `&&` and `||` (to `and` and `or`), the
turbofish in `w.iter().sum::<i64>()` (removed, the type coming from the
`max` it feeds), `**g` on a `zip` pair (to `*g`), and `*minutes` on a
tuple binding the loop already copies (to `minutes`).

## Benchmarks

The bench builds 200 days of 20000 minutes, up to 1000 customers a minute
and the owner grumpy half the time, once in all five languages, then runs
the ★ arm on each day with ten random techniques of 1 to 20000 minutes,
adding up the answers and folding each into a checksum. Every
implementation prints `200 days of 20000 minutes, 10 techniques each:
total 14189846112, checksum 828288174`. The days are generated in the
same order of random draws everywhere, and the slide is one pass of
bounds-checked reads per minute where the language checks them.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `6c8a806480` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.172 to 0.197 s | 0.178 s |
| Rust (`rustc -O`) | 0.184 to 0.191 s | 0.189 s |
| Kāra (`karac build`) | 0.344 to 0.359 s | 0.349 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.343 to 0.418 s | 0.356 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.365 to 0.388 s | 0.374 s |
| Go | 0.400 to 0.434 s | 0.407 s |
| Python | 7.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.31 s) is below its real time.

Kāra took 0.95 times Rust's median time under overflow checks, and 2.0
times C's. Building the days takes most of every program's time: eight
million draws of the random generator, whose multiply Kāra and Rust with
overflow checks test on every draw. That check is the gap to C and to
Rust without it, which run the same program in half the time.
