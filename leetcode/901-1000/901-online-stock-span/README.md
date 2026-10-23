# 901. Online Stock Span

Design an algorithm that collects daily price quotes for some stock and
returns the span of that stock's price for the current day.

The span of the stock's price in one day is the maximum number of
consecutive days (starting from that day and going backward) for which
the stock price was less than or equal to the price of that day.

Implement the `StockSpanner` class: `StockSpanner()` initializes the
object, and `next(price)` returns the span of the stock's price given
that today's price is `price`.

```
StockSpanner()
next(100) -> 1, next(80) -> 1, next(60) -> 1, next(70) -> 2,
next(60) -> 1, next(75) -> 4, next(85) -> 6
```

**Constraints:** `1 <= price <= 10^5`, and at most `10^4` calls are
made to `next`.

## Approaches

A day the new price is at or above is passed over by every later span
that reaches it, together with every day that day's own span passed
over, so the arms differ in how they skip such days and what they keep
of them.

| file | mechanism |
|---|---|
| `online_stock_span.kara` ★ | a stack of prices and their spans: the earlier prices not yet beaten, falling from the bottom up; a new price pops every price at or below it, takes over their spans, and is pushed with the sum. O(1) a call amortized |
| `online_stock_span_back.kara` | every day read back: every price kept, and the span found by reading back one day at a time while the price is at or below the new one. O(n) a call in the worst case |
| `online_stock_span_jump.kara` | jumping back by spans: every price and its span kept and nothing removed; a day at or below the new price is passed over together with its whole span. O(1) a call amortized |
| `online_stock_span_indices.kara` | a stack of days: the days whose prices are not yet beaten; after popping, the span reaches back to just after the day on top, or to the first day. O(1) a call amortized |
| `online_stock_span_tree.kara` | a segment tree of maxima over the days, doubled when the days outgrow it; the span ends at the last earlier day priced above the new one, found by going down the tree. O(log n) a call |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 11 lines: LeetCode's example and seven more
(one price, four equal prices, prices rising, prices falling, a dip and
a climb, a rising five, and the largest price around the smallest); for
300 random cases of up to 1,000 prices, a quarter each random from 1 to
10^5, random from 1 to 5, rising and falling by random steps, 155,812
calls whose spans sum to 13,180,956, with a checksum; and two of
LeetCode's largest, 10,000 random prices and 10,000 rising ones. The
back arm reads every earlier day on the rising prices, which is why it
takes 9.6 s under `karac __mir-run` where the others take 1.2 to 3.4 s.
`online_stock_span.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: for each day, every count of days back tried, each window
read through for a price above that day's, and the largest count with
none kept. It checks 3,200 random cases: 3,000 of up to 8 random prices
from 1 to 4 against the statement, and 200 of up to 400 prices of the
four kinds above against the other properties;
53,190 calls in all.

| | property |
|---|---|
| P1 | the statement's spans, on the small cases |
| P2 | each span from 1 to the number of days so far; the day just before the span priced above that day, and yesterday at or below it exactly when the span is more than 1 |
| P3 | the same spans with every price `p` written `3p + 7` |
| P4 | the spans of a prefix are its first spans, and a price above every earlier one then spans every day |
| P5 | a price above all the others put in front changes no span, and one at or below all of them adds a day to the spans that reach the first day |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 53190 calls,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal price not popped | P1 2026, P2 2169, P5 734, P6 2169 |
| M2 | ★: a popped price adding one day, not its span | P1 1745, P2 1942, P4 1905, P5 2179, P6 1942 |
| M3 | ★: every price pushed with a span of 1 | P1 1745, P2 1942, P4 1905, P5 2179, P6 1942 |
| M4 | back: the first day never read | P1 2263, P2 2425, P4 3200, P5 3200, P6 2425 |
| M5 | back: today not counted | P1 3000, P2 3200, P4 3200, P5 3200, P6 3200 |
| M6 | back: a price one above counted as at or below | P1 1635, P2 1521, P3 1778, P5 3200, P6 1778 |
| M7 | jump: one day more skipped after each span | P1 2327, P2 2303, P4 2835, P5 3200, P6 2525 |
| M8 | jump: the first day never passed over | P1 2263, P2 2425, P4 3200, P5 3200, P6 2425 |
| M9 | jump: one day too many answered | P1 3000, P2 3200, P4 3200, P5 3200, P6 3200 |
| M10 | indices: a day of an equal price kept | P1 2026, P2 2169, P5 734, P6 2169 |
| M11 | indices: the first day missed when no day is left | P1 3000, P2 3200, P4 3200, P5 3200, P6 3200 |
| M12 | indices: the day left on top counted in | P1 2219, P2 2415, P5 3200, P6 2415 |
| M13 | tree: an equal price taken as above | P1 2026, P2 2169, P5 734, P6 2169 |
| M14 | tree: the prices lost when the tree doubles | P1 1989, P2 2053, P5 3200, P6 2178 |
| M15 | tree: a range keeping only its left half | P1 359, P2 530, P5 1037, P6 549 |

P1, P2, P5 and P6 kill all fifteen. Three mutants in three arms fail
exactly the same cases (M1, M10, M13): each stops a span at an earlier
price equal to today's, so they differ only where prices repeat. M2 and
M3 fail the same cases: either way a popped price adds one day rather
than the days it had passed over. M4 and M8 fail the same cases, both
never reaching the first day, and M5, M9 and M11 fail every case, each
one day out on every span or on the first day's. P3 changes no order
between prices and so kills only M6, the one mutant that compares a
price with another plus one, which stretching the prices changes. P4's
price above every earlier one must span the whole prefix, which every
mutant that miscounts the days before a span's start or gets the first
day wrong fails (M2 to M5, M7 to M9, M11). P5 kills all fifteen too:
its price in front moves the first day, which every span that reaches
the start depends on, and on about half the cases the price at or below
all of them equals the lowest, which is where the three equal-price
mutants (M1, M10, M13) go wrong.

No mutant had to be replaced.

## Verification

Every arm prints the same output as `online_stock_span.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 1.2 to 9.6 s
each (the back arm, above, is the slow one) and the differential 10 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, refuses all five arms and the
differential: `*p` on an element of `.iter()` is rejected, because
legacy's iterator gives the value itself. The bench program reads no
iterator element and legacy's build of it prints the right output.
Legacy is frozen, so this is not filed.

## Benchmarks

The bench program uses the ★ arm over 1,000,000 prices built once, a
random walk between 1 and 10^5 taking steps of -50 to 50, so that spans
run from one day to many thousands. Each round gives every price to a
fresh spanner, folds the spans into a checksum and changes one price; 50
rounds. C grows its two stacks with `realloc`, the others use their
growable arrays. Every implementation prints `50 rounds over 1000000
prices: spans summing to 15096942510, checksum 729294983`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.52 to 0.60 s | 0.54 s |
| Rust (`rustc -O`) | 0.67 to 0.74 s | 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.66 to 0.76 s | 0.67 s |
| Go | 0.70 to 0.76 s | 0.73 s |
| Python | 19.3 s | |
| Kāra (`karac build --mir`) | 0.64 to 0.69 s | 0.66 s |
| Kāra (`karac build --legacy`) | 0.62 to 0.72 s | 0.65 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 900's does.

v2 takes 0.99 times Rust's median time under overflow checks, 1.24
times C's and 1.03 times legacy's. Under valgrind's cachegrind C runs
1.92 billion instructions and 303 million branches, Rust with overflow
checks 3.48 billion and 554 million, v2 2.87 billion and 604 million,
and legacy 2.77 billion and 552 million. All four mispredict 47 to 49
million branches, about one a call: whether a call pops anything turns
on the random walk's step. The comparison with C and Rust waits until
after M4.
