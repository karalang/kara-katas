# 1515. Best Position for a Service Centre

A delivery company wants to build a new service centre in a new city. It
knows the positions of all its customers on a 2D map and wants the centre
placed so that the sum of the Euclidean distances to all customers is the
least. Given `positions[i] = [xi, yi]`, return that least sum. Answers
within `10^-5` of the actual value are accepted.

```
positions = [[0,1],[1,0],[1,2],[2,1]]  ->  4.00000
positions = [[1,1],[3,3]]              ->  2.82843
```

**Constraints:** `1 <= positions.length <= 50`; `positions[i].length == 2`;
`0 <= xi, yi <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `centre.kara` ★ | ternary search twice: the sum of distances is convex, so its least value along each line `x = c` is convex in `c` too. For each `x` tried, the best `y` is found by a ternary search over 0..100, and `x` by one over those. 60 rounds each shrink 100 to under `10^-8`. O(60 · 60 · 4 · n) |
| `centre_weisz.kara` | Weiszfeld's iteration: the next point is the customers' mean weighted by one over each one's distance, until it stops moving (a customer met exactly counts at distance `10^-12`). Since the iteration only creeps toward a best point that is a customer, each customer's own sum is tried too |
| `centre_step.kara` | a shrinking-step search: from the customers' mean try a step in each of eight directions, take the first that lowers the sum, and halve the step when none does, down to `10^-7` |
| `centre_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>`, a `cost` closure, `.powi(2)`, `sum::<f64>()`), the step search, carried by `karac fix` |
| `differential.kara` | the four arms against the statement read as a bound, six properties |

Every arm prints the same 6 lines: LeetCode's two examples, one customer,
and a triangle (0,0), (100,0), (50,87) to five places, then a checksum of
the answers in hundredths for 300 sets of 1 to 8 customers on 0..10 and
30 sets of 1 to 50 customers on 0..100. `centre.py` mirrors the ★ arm and
its output is byte-identical.

The arms reach the least sum by different paths, so they agree to about
`10^-7`, not to the bit; the checksum takes hundredths, which every arm
reaches on every set.

The step search first tried the four axis directions only, as most
published solutions do. On one of the 300 small sets it stopped at
13.48683 where the least sum is 13.48241: the sum there has a ridge
along a diagonal, and no axis step goes down from it while the step
shrinks. Eight directions find it. The first ★ arm was that search too;
it is now the ternary search, which has no such corner.

## Differential

The least sum has no closed form, so `differential.kara` reads the
statement as a bound: on a grid of step `h` every point lies within
`h / √2` of the best one, and moving a point that far moves each of the
`n` distances by at most that much. It checks 400 sets of 1 to 8
customers on 0..10, every random choice drawn before any arm answers.
Answers are compared within `10^-5` of their size.

| | property |
|---|---|
| P1 | the answer is at most the sum at every point of a grid of step 1/4 on 0..10, and at least the grid's least sum less `n h / √2` |
| P2 | the customers listed in another order leave the answer |
| P3 | every customer moved by `(t, t)`, `t` up to 49, leaves the answer |
| P4 | every coordinate doubled doubles the answer |
| P5 | every customer listed twice doubles the answer |
| P6 | each arm agrees within `10^-4` with at least two of the other three |

The differential prints `400 problems: checksum 482595010, 9600 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirteen edits to the differential, three or four to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run` on the first 100
problems (the interpreter takes 2.5 minutes over all 400). Eight are
killed, each the same way under both backends; five survive.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the inner search keeps the low side whichever is smaller | P1 100, P3 99, P4 100, P6 100 |
| M2 | ★: 10 rounds of the inner search, not 60 | P1 79, P3 91, P4 90, P6 89 |
| M3 | ★: the outer search keeps the larger side | P1 100, P3 99, P4 100, P6 100 |
| M4 | Weiszfeld: distances floored at 0.5, not `10^-12` | P1 2, P4 8, P6 10 |
| M5 | Weiszfeld: 20 iterations, not 20000 | P1 1, P6 5 |
| M6 | step: a move taken only when it gains 0.01 | P1 47, P4 34, P5 34, P6 73 |
| M7 | Rust: the y distance taken from each customer's x | P1 75, P6 83 |
| M8 | Rust: stop at a step of `10^-2` | P1 19, P4 9, P6 17 |

P1 and P6 kill all eight, P4 six, P3 two, P5 one. M5 is the faintest:
Weiszfeld from the mean is close after 20 steps on most sets, and only
one in 100 lands far enough off to cross the grid bound.

Five survive, also over all 400 problems compiled. Three are equivalent:
the ★ arm reading the line's sum at `lo` rather than the middle (after
60 rounds they differ by `10^-8`), the step arm shrinking by 1.5 rather
than 2, and the Rust arm starting `y` at the customers' mean `x`. Two
are not, and this differential does not see them: Weiszfeld without the
customers' own sums (its `10^-12` floor lets it reach a customer closely
enough on these sets) and the step search on axes alone (the one stall
above, in 300 sets, did not recur in these 400).

## Benchmarks

The bench solves 100 sets of 50 customers on 0..100 by the ★ arm in all
five languages, 7.2 million square roots per set. Every implementation
prints `100 sets of 50 customers on 0..100: checksum 667406241`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `d8a8878fe` on LLVM 22:

| | median |
|---|---|
| Go | 0.130 s |
| Kāra (`karac build`) | 0.130 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.130 s |
| Rust (`rustc -O`) | 0.129 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.130 s |
| C (`clang -O3`) | 0.131 s |
| Python | 5.4 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.128 s and 0.129 s on one run).

Kāra is 1.00x Rust under overflow checks by median: the loop is bound by
the latency of the dependent square-root and compare chain, which every
compiler emits the same way. C uses `__builtin_sqrt` so that its link
needs no `-lm`.

## Verification

All four arms print the same output as `centre.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them.
Under `karac __mir-run` the ★ arm takes 24 s, the others 1 to 2 s, and
the differential 2.5 minutes.

## Writing it

The Kāra arms were written in Kāra and `karac fix` had nothing to change.
The Rust arm took 14 and then 1 `karac fix` edits (among them
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `sum::<f64>()` to a typed sum,
`vec![..]` to a list, `Solution::` to `Solution.`, and `!moved` to
`not moved`) and checks. Its four axis directions became eight by hand
after the stall above, the one edit not made by `karac fix`.
