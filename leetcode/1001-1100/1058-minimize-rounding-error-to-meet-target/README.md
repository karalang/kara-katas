# 1058. Minimize Rounding Error to Meet Target

Given an array of `prices` `[p1, p2, ..., pn]` and a `target`, round each
price `pi` to `Roundi(pi)` so that the rounded array sums to `target`. Each
`Roundi(pi)` is either `Floor(pi)` or `Ceil(pi)`.

Return the string `"-1"` if no rounding sums to `target`. Otherwise return
the smallest rounding error, `Σ |Roundi(pi) - pi|`, as a string with three
places after the decimal point.

```
prices = ["0.700","2.800","4.900"], target = 8  ->  "1.000"
prices = ["1.500","2.500","3.500"], target = 10 ->  "-1"
prices = ["1.500","2.500","3.500"], target = 9  ->  "1.500"
```

**Constraints:** `1 <= prices.length <= 500`; each price is a real number
in `[0.0, 1000.0]` written with exactly three decimals; `0 <= target <= 10^6`.

## Approaches

Read in thousandths, every price rounds down to its whole part. A price
with a fraction `f` that is rounded up instead adds 1 to the sum and
changes its error from `f` to `1000 - f`. So the target is reachable
exactly when `target - floor` lies between 0 and the count of prices with
a fraction, and rounding up the `target - floor` prices with the largest
fractions gives the least error: each one swapped for a smaller fraction
costs `2 (f - f')` more.

| file | mechanism |
|---|---|
| `rounding.kara` ★ | each price read digit by digit into thousandths; the fractions sorted from the largest, the first `target - floor` rounded up. O(n log n) |
| `rounding_float.kara` | each price parsed as an `f64`; the fractional parts sorted with `partial_cmp`, the error printed with `{:.3}`. O(n log n) |
| `rounding_count.kara` | the prices with a fraction counted by their 999 possible fractions, walked from 999 down. O(n + 1000) |
| `rounding_dp.kara` | `best[j]`, the least error with `j` of the fractions seen so far rounded up, which does not assume the largest fractions go up. O(k u) for k fractions and u rounded up |
| `rounding_heap.kara` | the fractions in a `PriorityQueue.max_first()`, the first `target - floor` popped rounded up. O(n + u log n) |
| `rounding_iter.kara` | `split_once` and `parse` into whole and fraction, `sum`, `filter`, a descending `sort_by`, then `take` and `skip`. O(n log n) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's three
examples and five more; how many targets were reached, the total error and
a checksum of every answer for 3000 random problems of 1 to 8 prices below
10 in quarters, and for 300 of 1 to 500 prices below 1000; and, for one
list of 500 prices, a checksum over every target from one below the least
sum to one above the greatest, the least and greatest error, and the two
answers one past each end. `rounding.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every way of rounding each price down or up, the ways whose sum
is the target, and the least error among them. It checks 3000 random
problems: 2000 of 1 to 9 prices below 10 whose fractions are quarters, so
that fractions tie often, and 1000 of 1 to 9 or 1 to 60 prices below 1000
with any fraction, each with a target from two below the least sum to two
above the greatest. Every tenth problem also asks each arm for every
target it can reach.

| | property |
|---|---|
| P1 | the answer is the statement read literally (for 9 prices or fewer, 512 ways) |
| P2 | the answer is `"-1"` exactly when the target is below every price rounded down or above every price rounded up |
| P3 | the prices reversed, or turned round by one, leave the answer |
| P4 | a whole price `7.000` added, with the target raised by 7, leaves the answer |
| P5 | over every reachable target the error falls and rises at most once: each further price rounded up costs at least as much as the one before |
| P6 | each arm agrees with at least three of the other five |

P5 holds because the k-th price rounded up adds `1000 - 2 f_k`, and the
fractions are taken from the largest down, so each addition is at least
the one before. A malformed answer on a reachable target counts as a P5
failure.

The differential prints `3000 problems: checksum 855372734, 110688 checks
over 6 arms: 0 failures` under `karac __mir-run` (17 s), `karac
__mir-llvm-run` and `karac __mir-llvm-asan` with no error, and the same
line under `karac run` and from a `karac build` binary. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one price more rounded up | P1 931, P5 232, P6 1205 |
| M2 | ★: a whole price kept as a fraction of 0, and 0.001 as whole | P1 344, P2 432, P4 274, P6 438 |
| M3 | ★: the thousandths unpadded | P1 192, P5 140, P6 220 |
| M4 | float: the error printed to two decimals | P1 1193, P5 84, P6 1477 |
| M5 | float: the floor taken as the nearest whole | P1 1442, P2 1097, P5 240, P6 1827 |
| M6 | count: fraction 999 never walked | P6 8 |
| M7 | count: at most one price of each fraction rounded up | P1 386, P5 128, P6 438 |
| M8 | count: too high a target let through | P1 862, P2 975, P6 975 |
| M9 | dp: the largest error kept | P1 1175, P3 685, P5 545, P6 1459 |
| M10 | dp: the table walked upward, a price rounded up twice | P1 896, P6 1169 |
| M11 | heap: the heap pops the smallest first | P1 650, P5 588, P6 914 |
| M12 | heap: one price fewer rounded up | P1 908, P5 220, P6 1180 |
| M13 | heap: only one price rounded down counted | P1 658, P5 326, P6 920 |
| M14 | iter: the first price rounded down not counted | P1 931, P6 1206 |
| M15 | iter: the floor the largest whole part | P1 1150, P2 1415, P4 159, P5 268, P6 1434 |

P6 kills all fifteen, P1 fourteen, P5 ten, P2 four, P4 two and P3 one.
M6 fails only P6, eight times: a fraction of exactly 999 is rare among
the random prices. P2 sees the edits that move the floor or the
count of fractions, and P4 the two that change how a whole price is read
(M2, M15). P3 sees only M9: keeping the largest error makes the answer
depend on the order the table meets the fractions. P5 misses M2, M6, M8, M10
and M14.

The other fifteen fail as kept ones do or in groups of their own. Four
fail exactly as M11, rounding up the smallest fractions (★, float, count,
iter), and the float arm's floor taken as the nearest whole fails as the
heap counting a fraction of a half in the floor. Three keep a whole price
as a fraction of 0 (★ counting every price, float, heap). Five get the
error of a price rounded up wrong, as `1 + d` (float), as `1000 - f` plus
`f` again (count), as `f` (dp) or as `999 - f` (iter), or start the dp
table at the target, and all five fail the same checks. Two count fraction
0.001 as whole (dp, iter), which only seven checks catch, since that
fraction is as rare as 0.999.

## Verification

Every arm prints the same output as `rounding.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. The runs used a release build of kara `1502aac7f4`. Under `karac
__mir-run` the arms take 2.7 s (float) to 32.4 s (dp).

The ★ arm was written in Kāra and checked clean. The other five were
written the way Rust writes them, and every one reaches a clean check
through `karac fix` alone, after four gaps were fixed in kara `4975afc0a9`:

- `let x: f64 = p.parse().unwrap();` (float, dp, heap) and `(w.parse()
  .unwrap(), f.parse().unwrap())` collected into a `Vec<(i64, i64)>`
  (iter) were refused with "`.parse()` takes its target from an expected
  `Option[T]`", and no fix. Only a later use names the target: the `let`
  past the `unwrap`, or the `collect`. The error now waits for the end of
  the check, and its fix writes `f64.parse(p)`; a `collect` into a written
  collection now solves the types its items left open, as Rust's does.
- `need as usize > diffs.len()` (float) was refused for comparing `usize`
  with `i64`, with no fix. `len()` is already `i64` in Kāra, so the fix
  drops the cast.
- `let need = need as usize;` (dp, iter), whose `usize` then meets `i64`,
  drew only the errors where it met. The fix drops the cast, leaving `let
  need = need;` (kara B-2026-11-06-3's remainder).
- `fracs.sort_unstable_by_key(|&f| Reverse(f))` (iter) drew a message
  naming `sort_by(|a, b| b.cmp(a))` but no fix. A `Reverse` that is a sort
  key's whole body now becomes `sort_by(|a, b| b.cmp(a))`, with the key
  written for each side (`|p| Reverse(p.1 * 2)` becomes `|a, b| (b.1 *
  2).cmp(a.1 * 2)`). One inside a larger key, `(p.0, Reverse(p.1))`,
  still gets no fix.

Two more findings, both filed in kara. The differential turned its prices
round by one with `rotate_left(1)`, which Kāra's `Vec` did not have
(B-2026-11-06-35); `Vec.rotate_left` and `rotate_right` were added in
kara `2fee84b590`. And `c.to_digit(10)` cost half of the benchmark's time
(B-2026-11-06-33, below).

## Benchmarks

The bench builds 40 lists of 500 prices below 1000 once in all five
languages, then asks the ★ arm for every target of each list, from one
below the least sum to one above the greatest, 8 times over. Every
implementation prints `121144 calls: checksum 50256577`. Each call reads
500 prices digit by digit, sorts up to 500 fractions from the largest and
writes the answer.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `2fee84b590` on LLVM 22:

| | time | median |
|---|---|---|
| Rust (`rustc -O`) | 0.675 to 0.915 s | 0.722 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.754 to 1.127 s | 0.789 s |
| C (`clang -O3`) | 1.209 to 1.295 s | 1.258 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.375 to 1.470 s | 1.411 s |
| Kāra (`karac build`) | 1.383 to 1.488 s | 1.420 s |
| Go | 2.080 to 2.707 s | 2.160 s |
| Python | 25.9 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.410 s) is below its real time.

Before kara `2fee84b590`, the Kāra program took 3.0 to 3.2 s. Each
`c.to_digit(10)` was a call into the runtime, which matched the method's
name against twenty strings for every char: callgrind put half of all
instructions there (B-2026-11-06-33). `to_digit` and `is_digit` of a char
are now computed in line. With that gone, Kāra is 1.8x Rust under overflow
checks, and most of the gap is the descending `sort_by`: deleting the sort
leaves 0.73 to 0.84 s against Rust's 0.54 to 0.56 s, so Kāra's `sort_by`
costs about 0.7 s where Rust's costs about 0.28 s, while a plain `sort()`
costs Kāra about 0.3 s (B-2026-11-06-34, open).
