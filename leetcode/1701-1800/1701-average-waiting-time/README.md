# 1701. Average Waiting Time

There is a restaurant with a single chef. You are given an array
`customers`, where `customers[i] = [arrivali, timei]`:

- `arrivali` is the arrival time of the `ith` customer. The arrival
  times are sorted in **non-decreasing** order.
- `timei` is the time needed to prepare the order of the `ith` customer.

When a customer arrives, he gives the chef his order, and the chef
starts preparing it once he is idle. The customer waits till the chef
finishes preparing his order. The chef does not prepare food for more
than one customer at a time. The chef prepares food for customers **in
the order they were given in the input**.

Return *the **average** waiting time of all customers*. Solutions within
`10^-5` from the actual answer are considered accepted.

```
customers = [[1,2],[2,5],[4,3]]               ->  5.00000
customers = [[5,2],[5,4],[10,3],[20,1]]       ->  3.25000
```

**Constraints:** `1 <= customers.length <= 10^5`;
`1 <= arrivali, timei <= 10^4`; `arrivali <= arrivali+1`.

## Approaches

| file | mechanism |
|---|---|
| `waiting.kara` ★ | an order starts when its customer has arrived and the chef is free, so the chef finishes at the later of the two plus its time, and the customer waits from arrival to then; the waits summed as an `i64` and divided once. O(n) |
| `waiting_fold.kara` | one `fold` over the customers with the pair (finishing time, waits so far) as its state, destructured in the closure's parameter. O(n) |
| `waiting_starts.kara` | every order's start time worked out into a `Vec` first, each the later of its arrival and the previous order's end; then each wait is the start less the arrival plus the order's time. O(n) time and space |
| `waiting_solution.kara` | a Rust solution as LeetCode's Rust users write it, `for c in &customers`, the pair taken out as `(c[0] as i64, c[1] as i64)`, `time.max(a)` and `as f64` at the end, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

The answer is printed to 5 places, `{:.5}`. Every arm prints the same 7
lines: LeetCode's two examples, one customer, and three who arrive at
once; then the answers summed and a checksum of each in units of
`10^-5` for 3000 random lists of up to 12 customers, 300 of up to 1000
and 10 of up to `10^5`. `waiting.py` mirrors the ★ arm and its output
is byte-identical; it rounds with `floor(x + 0.5)`, as Kāra's `round()`
takes a half away from zero and Python's `round()` to even.

```
5.00000
3.25000
4.00000
2.00000
3000 lists of up to 12 customers: answers sum to 15853.93745, checksum 152792606
300 lists of up to 1000 customers: answers sum to 169152.24822, checksum 684800238
10 lists of up to 100000 customers: answers sum to 4316746.21163, checksum 707919495
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a clock moves one unit at a time; the chef, free, waits for
the next customer in order to arrive, then cooks for their time, and the
customer's wait runs from their arrival until the clock stops at the
end of their order. It checks 3000 random lists of 1 to 8 customers,
each arriving 0 to 4 after the one before and wanting 1 to 5. Every case
is drawn before any arm answers. The answers are compared exactly: the
waits are whole numbers, divided once.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | every arrival 10 later gives the same answer |
| P3 | every arrival and every time doubled doubles the answer |
| P4 | one more customer, arriving once the chef is free, adds their own time to the waits |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 481614749, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. None fails P3, since doubling every
number doubles the waits whichever way they are worked out. M5 and M6
never move the chef's free time on and fail the same checks, P1 and P5
alone.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the chef never idle, arrivals ignored | P1 3000, P2 3000, P4 3000, P5 3000 |
| M2 | ★: the cooking left out of each wait | P1 3000, P4 3000, P5 3000 |
| M3 | ★: the waits divided by one customer more | P1 3000, P4 1017, P5 3000 |
| M4 | fold: an order taking no time | P1 3000, P4 3000, P5 3000 |
| M5 | fold: the finishing time never carried on | P1 2387, P5 2387 |
| M6 | starts: the previous order's time not added to its start | P1 2387, P5 2387 |
| M7 | starts: the cooking left out of each wait | P1 3000, P4 3000, P5 3000 |
| M8 | solution: `min` for `max` | P1 3000, P2 3000, P4 3000, P5 3000 |
| M9 | solution: the finishing time summed, not the wait | P1 3000, P2 3000, P4 3000, P5 3000 |
| M10 | solution: arrival and time swapped | P1 2883, P2 3000, P4 2982, P5 2883 |

## Benchmarks

The bench draws 50 random lists of `10^5` customers, LeetCode's longest,
arrivals and times up to `10^4` (one arrival in ten a step after the one
before), all of them first, then answers each 60 times by the ★ arm in
all five languages. Every implementation prints `50 lists of 100000
customers, 60 rounds: answers sum to 704352883215.28430, checksum
315194621`. The C mirror rounds with `round()` from `<math.h>`, so
`bench.sh` links it with `-lm`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.357 s |
| Go | 0.524 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.765 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.799 s |
| Kāra (`karac build`) | 1.823 s |
| Rust (`rustc -O`) | 1.824 s |
| Python | 24 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.357 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.752 s and 1.887 s on one
run).

## Verification

All four arms print the same output as `waiting.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ and starts arms checked clean as first written. The fold arm's
first draft seeded its state `(0i64, 0i64)`; the `redundant_suffix`
lint saw that `i64` is a literal's default, and `karac fix` dropped both
suffixes.

LeetCode's Rust template took one `karac fix` of 7 edits:
`struct Solution {}` added, `Vec<Vec<i32>>` written `Vec[Vec[i32]]`,
`for c in &customers` written `for c in ref customers`, and the
`0i64` suffixes dropped. `let (a, t) = (c[0] as i64, c[1] as i64)`,
`time.max(a)` and `total as f64 / customers.len() as f64` carried over as
written.

`arm_name` in the differential indexes a list of string literals for a
`Str`, as #1662's does (B-2026-11-19-131).
