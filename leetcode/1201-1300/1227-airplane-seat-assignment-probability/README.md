# 1227. Airplane Seat Assignment Probability

`n` passengers board an airplane with exactly `n` seats. The first
passenger has lost the ticket and picks a seat randomly. But after that,
the rest of the passengers will:

- Take their own seat if it is still available, and
- Pick other seats randomly when they find their seat occupied

Return the probability that the `n`th person gets their own seat.

```
n = 1  ->  1.00000     the first person can only get the first seat
n = 2  ->  0.50000     the second gets the second seat when the first takes the first
```

**Constraints:** `1 <= n <= 10^5`.

The arms are `fn nth_person_gets_nth_seat(n: i64) -> f64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `nth_person_gets_nth_seat` calls it. Every
harness prints the probability to five places, as LeetCode does.

## Approaches

| file | mechanism |
|---|---|
| `airplane_seat_assignment_probability.kara` ★ | the closed form: the first passenger's random seat starts a chain, each passenger whose seat is taken picking among the free seats, until someone takes seat 1 (everyone after sits in their own) or seat `n` (the last cannot). Until it ends seats 1 and `n` are both free and equally likely, so for `n >= 2` the answer is 1/2. O(1) |
| `airplane_seat_assignment_probability_sums.kara` | by the first passenger's choice: seat 1 and everyone sits in their own, seat `n` and the last cannot, seat `k` between and passenger `k` faces the same problem with `n − k + 1` seats. So `f(n) = (1 + f(2) + ... + f(n − 1)) / n`, kept with a running sum. O(n) |
| `airplane_seat_assignment_probability_chain.kara` | forward along the chain: the probability that each passenger is displaced, each displaced passenger `k` choosing among seat 1 and seats `k + 1` to `n`; the answer is 1 less every chance that seat `n` is picked. O(n) |
| `airplane_seat_assignment_probability_recur.kara` | a Rust solution as LeetCode's Rust users write it, the recurrence `f(n) = 1/n + (n − 2)/n · f(n − 1)` by `Self::` recursion on `i32` with `as f64` casts, carried to Kāra by `karac fix`. Recurses n deep |
| `airplane_seat_assignment_probability_table.kara` | another Rust solution (the running-sum recurrence in a `vec![0.0f64; n + 1]` over `usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's two examples, `n` = 3, 4
and the constraints' top, `10^5` (all `0.50000`), and the total of the
answers for 300 random `n` from 1 to 3000 (`150.00000`).
`airplane_seat_assignment_probability.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the ★, sums and chain arms check clean as written. The
recur arm takes one round of 2 fixes (`struct Solution;` to `struct
Solution {}`, and `Self::nth_person_gets_nth_seat(n - 1)` to
`Solution.nth_person_gets_nth_seat(n - 1)`) and the table arm one round
of 4 (among them `n as usize` to `n as i64` and `vec![0.0f64; n + 1]` to
`Vec.filled(n + 1, 0.0)`), and both check clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way the passengers can board, the first and anyone
whose seat is taken trying each free seat with an equal share of the
probability, counted exactly in whole numbers over `n!`, for `n` up to
8. 1500 cases, a third with `n` from 1 to 8, a third from 9 to 40 and a
third from 41 to 3000. Answers are compared to within `10^−9`.

| | property |
|---|---|
| P1 | the statement read literally (`n` up to 8) |
| P2 | at least `1/n`, the first passenger's chance of taking seat 1 |
| P3 | at most `1 − 1/n` for `n >= 2`, less the first's chance of taking seat `n` |
| P4 | `n f(n) = 1 + f(2) + ... + f(n − 1)`, each from the same arm (`n` up to 40) |
| P5 | the same answer for `n` and `n + 1`, for `n >= 2` |
| P6 | the ★ arm's answer |

All 45,000 checks pass on every arm: `1500 cases: total 783.00000, 45000
checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac run`,
`karac build` and the AddressSanitizer build. Python's exact fractions
for the same cases give the same total.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: one passenger half the time too | P1 66, P2 66, P6 264 |
| S2 | ★: the first passenger's chance of seat 1 | P1 366, P4 866, P5 1434, P6 5464 |
| U1 | sums: divided by one seat fewer | P1 434, P3 1434, P4 934, P6 1434 |
| U2 | sums: the running sum never kept | P1 366, P4 866, P5 1434, P6 1366 |
| H1 | chain: the free seats counted one short | P1 434, P2 1434, P4 934, P6 1434 |
| H2 | chain: the first passenger displaced half the time | P1 434, P3 134, P4 934, P6 1434 |
| R1 | recur: one seat too many handed on | P1 434, P3 1434, P4 934, P6 1434 |
| R2 | recur: one passenger half the time | P1 66, P2 66, P6 66 |
| T1 | table: one passenger never seated | P1 66, P2 66, P6 66 |
| T2 | table: the sum only the last term | P1 300, P4 800, P5 1366, P6 1300 |

All ten are caught, and P1 catches every one. A mutation of the ★ arm
fails P6 on the four other arms. S1, R2 and T1 change only one
passenger's answer, and fail on the 66 cases with `n = 1`, where P2 sees
an answer below 1. S2, U2 and T2 give an answer that moves with `n` and
is still right for the smallest `n` (`1/n` and `1/m` are 1/2 at 2, and
T2's sum of one term is right up to 3), so P1 fails them on fewer cases
than the others, and P5, the same answer for `n` and `n + 1`, catches
them. U1, H2 and R1 give the same wrong answer for every `n`, 1 or 3/4,
which P5 cannot see; P3 catches it as more than the first passenger
leaves the last, on every case for 1 and on the 134 cases with `n` up to
3 for 3/4. H1's answer falls below `1/n`, which P2 catches. P4, the
recurrence with each arm's own answers, holds for any constant answer
only when that answer is 1/2, and fails every mutation but those that
change `n = 1` alone.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the
running-sum arm (the ★ arm's closed form is O(1)), f(n) = (1 + f(2) +
... + f(n - 1)) / n, for 1000 random n up to 10^5; the total of the
answers. Every program prints `1000 random n up to 10^5: total
500.00000`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.314 to 0.331 s | 0.320 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.316 to 0.338 s | 0.321 s |
| Rust (`rustc -O`) | 0.312 to 0.348 s | 0.320 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.314 to 0.349 s | 0.320 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.314 to 0.344 s | 0.322 s |
| C (`clang -O3`) | 0.317 to 0.339 s | 0.323 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.316 to 0.338 s | 0.324 s |
| Go | 0.317 to 0.337 s | 0.323 s |
| Python | 3.094 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.320 s
against 0.321 s), and the two ranges overlap. C runs level with Kāra
(0.323 s against 0.321 s); Go runs level with Kāra (0.323 s against
0.321 s). Python takes about 10x Kāra's time. No profile was taken.
