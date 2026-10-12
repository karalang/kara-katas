# 458. Poor Pigs

There are `buckets` buckets of liquid, exactly one of them poisonous.
To find it, you feed some pigs and wait: a pig that drinks the poison
dies `minutes_to_die` minutes later. A pig may drink from any number of
buckets at once, and after feeding there is nothing to do but wait
`minutes_to_die` minutes before feeding again. Given `minutes_to_test`
minutes in all, return the least number of pigs that find the poisonous
bucket.

```
buckets = 4,    minutes_to_die = 15, minutes_to_test = 15  ->  2
buckets = 4,    minutes_to_die = 15, minutes_to_test = 30  ->  2
buckets = 1000, minutes_to_die = 15, minutes_to_test = 60  ->  5
```

**Constraints:** `1 <= buckets <= 1000`;
`1 <= minutes_to_die <= minutes_to_test <= 100`.

## Approaches

Every arm is
`fn poor_pigs(buckets: i64, minutes_to_die: i64, minutes_to_test: i64) -> i64`.
With `T = minutes_to_test / minutes_to_die` rounds of feeding, a pig
ends in one of `T + 1` states (dead after round 1, ..., dead after
round `T`, or alive), and the pigs are independent, so `p` pigs tell
apart `(T + 1)^p` buckets.

| file | mechanism |
|---|---|
| `poor_pigs.kara` ★ | multiply the number of outcomes by `T + 1`, one pig at a time, until it covers the buckets. O(log buckets) |
| `poor_pigs_digits.kara` | number the buckets from 0 and count the base-`(T + 1)` digits of `buckets - 1`: pig `i` drinks in round `d` from every bucket whose `i`-th digit is `d`, which is the strategy itself. O(log buckets) |
| `poor_pigs_outcomes.kara` | count the outcomes as `Σ C(p, k)·T^k`, for which `k` pigs die and in which rounds, and try `p = 0, 1, 2, ...`. O(log² buckets) |
| `poor_pigs_logs.kara` | `ceil(ln buckets / ln (T + 1))` in floating point, then step it up or down by exact integer powers until it is right. O(log buckets) |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 12 lines: the three LeetCode examples, one
bucket, two buckets, 1,000 buckets with one round, an exact power of
10 and one more, `minutes_to_die` equal to `minutes_to_test`, 101
states, 10^12 buckets, and for 300 random cases (1 to 10^12 buckets,
spread over every number of digits, and
`1 <= minutes_to_die <= minutes_to_test <= 100`) the total number of
pigs and a checksum. The kata goes past LeetCode's 1,000 buckets so
that the answers reach 40 pigs. `poor_pigs.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases.

| | property |
|---|---|
| P1 | on 1 to 200 buckets and 1 to 4 rounds, the answer is brute force's: for `p = 0, 1, 2, ...`, step an odometer over every tuple of `p` pig states, counting them, until the count reaches the buckets |
| P2 | on 1 to 10^12 buckets, one bucket more needs the same number of pigs or one more |
| P3 | scaling `minutes_to_die` and `minutes_to_test` by 1 to 5 keeps the answer |
| P4 | time for one round more never needs more pigs |
| P5 | `(T + 1)^p` buckets need `p` pigs, and one bucket more needs `p + 1` |

It prints `1500 cases, 4 arms, 30000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an exact power takes one pig more | P1 44, P5 1500 |
| M2 | ★: the rounds are counted with a minute too many | P1 216, P3 12, P5 53 |
| M3 | digits: the digits of `buckets`, not `buckets - 1` | P1 44, P5 1500 |
| M4 | digits: the leading digit is not counted | P1 1492, P5 1500 |
| M5 | outcomes: the case where every pig dies is left out | P1 339, P5 1500 |
| M6 | outcomes: surviving is counted as one more round | P1 974, P5 1469 |
| M7 | logs: an estimate that is too high is kept | P1 2, P5 145 |
| M8 | logs: stepping down checks one power too low | P1 1492, P5 1500 |

P1 and P5 see all eight. P2 and P4 see none: every mutant is still a
monotone function of the buckets and of the time, which is all those
two properties ask. P3 sees only M2, the one mutant that reads the
minutes rather than the rounds. M7 is the case the logs arm's
stepping-down loop exists for: on 145 of the 1,500 exact powers,
`ln buckets / ln (T + 1)` lands a hair above the whole number, and the
ceiling is one pig too many.

## Verification

All four arms print the same output as `poor_pigs.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints
`30000 checks, 0 failures` on both. The four arms and the differential
also run clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak.

The frozen legacy backends agree too: every arm matches under
`karac run --interp`, `karac run` (LLJIT) and `karac build`, and with
`KARAC_AUTO_PAR=1`; the differential prints `0 failures` under
`karac run --interp` and `karac build`.

## Benchmarks

The bench program uses the ★ arm. It builds 1,000,000 queries once,
drawn like the random cases above (1 to 10^12 buckets over every number
of digits), then runs 20 rounds; each round gives one query a new
number of buckets and answers every query, summing the pigs. Every
implementation prints `20 rounds on 1000000 queries: 321674453 pigs,
checksum 151131473`, the Kāra program under `karac __mir-run` included
(in 40 s).

The mirrors keep the ★ arm's loop. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.60 to 0.65 s |
| Rust (`rustc -O`) | 0.64 to 0.68 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.60 to 0.62 s |
| Go | 0.67 to 0.70 s |
| Python | 15.5 s |
| Kāra (legacy `karac build`) | 0.63 to 0.70 s |
| Kāra (`karac build --mir`) | 0.69 to 0.72 s |

Nearly all the time is the integer division for the number of rounds
and the short multiply loop, which every language compiles alike.
`bench.sh` uses the default `karac build`, which is legacy. Under
`karac __mir-llvm-run` the program prints the same line in 1.5 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

No new findings.
