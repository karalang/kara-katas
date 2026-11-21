# 2483. Minimum Penalty for a Shop

You are given the customer visit log of a shop represented by a
**0-indexed** string `customers` consisting only of characters `'N'`
and `'Y'`:

- if the `i`th character is `'Y'`, it means that customers come at the
  `i`th hour
- whereas `'N'` indicates that no customers come at the `i`th hour.

If the shop closes at the `j`th hour (`0 <= j <= n`), the **penalty**
is calculated as follows:

- For every hour when the shop is open and no customers come, the
  penalty increases by `1`.
- For every hour when the shop is closed and customers come, the
  penalty increases by `1`.

Return *the **earliest** hour at which the shop must be closed to incur
a **minimum** penalty.*

**Note** that if a shop closes at the `j`th hour, it means the shop is
closed at the hour `j`.

```
customers = "YYNY"   ->  2
customers = "NNNNN"  ->  0
customers = "YYYY"   ->  4
```

**Constraints:** `1 <= customers.length <= 10^5`; `customers` consists
only of characters `'Y'` and `'N'`.

Closing an hour later than `j` changes the penalty only by hour `j`:
one less if customers come then, one more if none do. So the penalty
at `j` is the penalty at 0 less the customers before `j` plus the empty
hours before it, and the answer is the earliest hour after which the
customers so far most outnumber the empty hours, 0 when they never do.

## Approaches

| file | mechanism |
|---|---|
| `shop.kara` ★ | by a running balance: customers less empty hours, walked hour by hour, the earliest hour of a strictly larger balance kept. O(n) |
| `shop_penalty.kara` | the penalty itself, kept running: it starts at the count of `'Y'`, the cost of closing at 0, and each hour passed takes one off or adds one; the least met first is kept. O(n) |
| `shop_prefix.kara` | by prefix and suffix counts: the empty hours before each `j` and the hours with customers from `j` on, filled from either end, and the first least sum. O(n) time and room |
| `shop_back.kara` | walking back from the end over the log's bytes: the penalty of closing after the last hour, the empty hours, then each hour stepped back over, a penalty no larger than the best moving the answer earlier, so ties end at the earliest. O(n) |
| `shop_iter.kara` | iterators: each hour a step by `map`, the balances by `scan`, numbered by `enumerate`, and the earliest strictly larger balance by `fold`. O(n) |
| `shop_solution.kara` | LeetCode's Rust template: `String` in, `i32` out; the penalty at 0 by `bytes().filter(...).count()`, then a walk over `bytes().enumerate()` with a `match` on the byte; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 14 lines: LeetCode's three examples; then
five more, one hour of each kind, two hours either way round, the
second a tie between opening not at all and closing last, and a tie
between two inner hours; then the constraints' largest, `10^5` hours,
all with customers, all without, taking turns, and random with odds of
a customer of a half and of six in ten; and 3000 random logs of 1 to 40
hours with odds from 0 to 100 in 100, as a checksum. `shop.py` mirrors
the ★ arm and its output is byte-identical, and the mirror was checked
on 20000 random logs of 1 to 14 hours against the penalty of every
hour counted afresh. The two agreed on every log.

`check` first reports 1 error on the template, the `&` in the closure
pattern `|&b|`, and `karac fix` carries it in one call, reporting 5
edits: that `&` goes; both `bytes()` become `bytes().iter()`, since
Kāra's `bytes()` is a list and its adaptors need an iterator; `struct
Solution {}` is added; and the wrapper's `as i64` on the `i32` answer
goes, since an `i32` widens by itself. The byte literals, the `match`
with its `_` arm, `count() as i32` and `i as i32 + 1` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for every closing hour from 0 to `n`, the penalty counted
afresh over every hour, and the earliest hour of least penalty taken.
No running count is used. It checks 300 random logs of 1 to 10 hours,
then 60 of up to 30, each with odds of a customer from 0 to 100 in 100;
68 of the 360 have a tie for the least penalty. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | the hour is the literal reading's |
| P2 | every hour flipped and the log reversed: `n` less the latest hour of least penalty in the original |
| P3 | an hour with customers put first: one hour later |
| P4 | an hour without customers put last: the same hour |
| P5 | the penalty of closing at the hour is the least penalty |
| P6 | each arm agrees with at least three of the other five |

P2 holds because closing the flipped and reversed log at `n - j` keeps
open, reversed and flipped, exactly the hours the original keeps closed
at `j`, so the two penalties are equal and the earliest best of the one
is the latest best of the other. P3 holds because the new first hour
costs one at hour 0 and nothing at any later hour, which keeps every
other penalty as it was. P4 holds because the new last hour costs
nothing at any hour but `n + 1`, where it costs one. P5 accepts any
hour of least penalty, so it fails only an answer that is not one.

The differential prints `360 cases: checksum 365582348, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal earliest and latest hours was checked against a Python
reading that builds the same cases and counts the same way. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the latest best hour kept | P1 68, P2 68, P6 68 |
| M2 | ★: the hour counted before the step | P1 201, P2 219, P3 360, P5 201, P6 201 |
| M4 | ★: the best balance never raised | P1 62, P2 67, P3 80, P4 122, P5 36, P6 62 |
| M7 | penalty: the least begun one below closing at 0 | P1 66, P2 60, P3 225, P5 66, P6 66 |
| M10 | penalty: the first hour skipped | P1 237, P2 248, P3 159, P5 237, P6 237 |
| M11 | penalty: closing after the first hour never taken | P1 54, P2 48, P3 213, P5 43, P6 54 |
| M12 | prefix: an empty hour counted at its own hour | P1 96, P2 102, P3 170, P4 105, P5 96, P6 96 |
| M13 | prefix: waiting counted from the next hour | P1 201, P2 219, P3 159, P5 201, P6 201 |
| M14 | prefix: closing at the end never tried | P1 112, P2 123, P4 112, P5 112, P6 112 |
| M19 | back: a step back over an empty hour costing more | P1 248, P2 237, P4 360, P5 219, P6 248 |
| M20 | back: the walk stopping short of hour 0 | P1 159, P2 141, P3 159, P5 123, P6 159 |
| M21 | back: the answer the hour after | P1 248, P2 237, P4 112, P5 248, P6 248 |
| M24 | iter: an empty hour a step of 0 | P1 140, P2 133, P5 89, P6 140 |
| M25 | iter: the balance not carried | P1 137, P2 157, P3 124, P5 127, P6 137 |
| M26 | iter: the start at a loss | P1 36, P2 29, P3 36, P6 36 |
| M27 | solution: no better hour leaving the end | P1 159, P2 141, P3 159, P4 159, P5 149, P6 159 |
| M30 | solution: the first hour passed over | P1 90, P2 77, P3 213, P5 54, P6 90 |

P1, P2 and P6 kill all seventeen, P5 fifteen, P3 twelve, and P4 six.

Fourteen are not kept, and every one fails exactly as a kept one. Five
keep the latest hour of least penalty, not the earliest: the penalty,
prefix and template arms' latest least kept, the back arm's earliest
tie passed over and the iter arm's latest best balance kept (M8, M15,
M17, M22, M28), as the ★ arm's (M1); P1, P2 and P6 alone see them, on
the 68 cases with a tie. Three answer the hour after the best: the ★
arm's best hour one late, the iter arm's hour numbered from 0 and the
template's answer the hour itself (M5, M23, M29), as the prefix arm's
waiting counted from the next hour (M13). The penalty arm's least never
lowered and the template's best never lowered (M9, M31) fail as the ★
arm's best balance never raised (M4); the prefix arm's empty hours read
as waiting (M16) as the ★ arm's hour counted before the step (M2); the
★ arm's empty hour not counted against (M3) as the iter arm's empty hour
a step of 0 (M24); the ★ arm's walk started at a loss (M6) as the iter
arm's start at a loss (M26); and the back arm's end's penalty taken one
too high (M18) as the prefix arm's closing at the end never tried
(M14). No edit crashes, and every edit is killed by some check.

Six edits were replaced before this table was drawn. Three survived
every check: the penalty and template arms' closing at 0 costing the
empty hours, and the back arm's start counting customers, each starting
the penalty at the wrong count, which moves every hour's penalty by
the same amount and so leaves the best hour where it was. Three failed
exactly as a kept one: the penalty arm's customer's hour costing more
and its hour counted after the test, and the template's customer's hour
costing more.

## Verification

Every arm prints the same output as `shop.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.1 to 2.9 s and the differential 0.7 s; under `karac __mir-llvm-asan` the arms take 0.5 to 1.0 s and the differential 0.7 s, and under `karac run` the differential takes 0.5 s.

## Benchmarks

The bench builds 20 random logs of `10^4` hours once from its own
generator, odds of a customer a half, then makes 600 passes; each flips
one hour of every log, chosen by the checksum so far, so no answer
repeats the last, and folds the answer plus the pass into the checksum.
The bench uses the ★ arm in all five languages, each log kept as a list
of characters and joined into a fresh string for every answer; C copies
it into one buffer. Every implementation prints `600 passes over 20
logs of 10^4 hours: checksum 550168865`.

BENCHTAB
