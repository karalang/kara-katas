# 412. Fizz Buzz

Given `n`, return a list of strings for `1` to `n`: `"FizzBuzz"` for
multiples of 3 and 5, `"Fizz"` for multiples of 3, `"Buzz"` for
multiples of 5, and the number itself otherwise.

```
n = 3   -> ["1","2","Fizz"]
n = 5   -> ["1","2","Fizz","4","Buzz"]
n = 15  -> ["1","2","Fizz","4","Buzz","Fizz","7","8","Fizz","Buzz","11","Fizz","13","14","FizzBuzz"]
```

**Constraints:** `1 <= n <= 10^4`.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `fizz_buzz.kara` ★ | test each case, the multiple of 15 first, since it is also a multiple of 3 and of 5 | O(n) | O(n) |
| `fizz_buzz_concat.kara` | build each entry from its parts: add `"Fizz"` when 3 divides, `"Buzz"` when 5 does, and the number if the entry is still empty | O(n) | O(n) |
| `fizz_buzz_counters.kara` | two counters that run to 3 and to 5 and start again, so no `%` at all | O(n) | O(n) |
| `fizz_buzz_match.kara` | `match (i % 3, i % 5)` with arms `(0, 0)`, `(0, _)`, `(_, 0)` and `_`, checked in order | O(n) | O(n) |
| `differential.kara` | the four arms on 1,000 random `n`, five properties | — | — |

Every arm prints the same 7 lines: the answers for 1, 3, 5, 15, 16 and
31, and for 100 random `n` from 1 to 10,000 the number of words and of
numbers and a checksum over every byte. `fizz_buzz.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms, run on 1,000 random
`n` from 1 to 300:

| | property |
|---|---|
| P1 | the answer has `n` entries |
| P2 | the words stand exactly at the multiples, marked by stepping through the multiples of 3 and of 5 with no division |
| P3 | every other entry is its number in decimal, read back digit by digit |
| P4 | the answer for `n` is the start of the answer for `n + k` |
| P5 | there are `n / 15` `"FizzBuzz"`, `n / 3 - n / 15` `"Fizz"` and `n / 5 - n / 15` `"Buzz"` |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | cases: `"FizzBuzz"` only at multiples of 30 | P2 946, P5 946 |
| M2 | cases: the loop stops before `n` | P1 1000, P2 1000, P3 1000, P5 447 |
| M3 | concat: an entry with a word gets its number too | P2 992, P5 992 |
| M4 | concat: each number is written one too large | P3 1000 |
| M5 | counters: the counter for 3 restarts at 1 | P2 984, P3 981, P5 984 |
| M6 | counters: the counter for 5 starts at 1 | P2 984, P3 985, P5 449 |
| M7 | match: `"FizzBuzz"` is `(0, 1)`, not `(0, 0)` | P2 983, P5 575 |
| M8 | match: a number is written modulo 100 | P3 660 |

No arm or mutant fails P4: each builds the entries in order from 1 with
no look at `n` but where to stop, so a shorter answer is always the
start of a longer one. It is kept to guard against an arm that one day
fills its list in another order. M2 fails P5 only when the missing last
entry is a word.

## Verification

All four arms print the same output as `fizz_buzz.py` on every backend:
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. `karac check` passes on every file. The differential prints
`20000 checks, 0 failures` under `karac __mir-run` and
`karac run --interp`.

Under `karac __mir-llvm-run` the differential stops at the missing
`String.as_str` native: its `read_number(entry: Str)` is passed a
`String`, as in katas 383 to 411. The frozen legacy codegen has no
`bytes()` on that `Str` parameter, which stops LLJIT, `karac build` and
`KARAC_AUTO_PAR=1 karac build` on it. Neither is filed.

## Benchmarks

The bench program calls the ★ arm 2,000 times with `n` from 9,000 to
10,000 (the problem's limit), each entry a fresh string as LeetCode's
`List<String>` asks, and folds the bytes of each answer into a total and
a checksum. Every implementation prints `2000 calls: 79770964 bytes,
checksum 936808904`; a 20-call cut of the Kāra program under
`karac __mir-run` prints the same as the C program cut the same way. The
C mirror copies every entry into its own allocation, as the Kāra, Rust
and Python ones do; Go's string literals are shared, so only its
numbers allocate. Spot timings on a shared 4-core container, three runs
each (`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| Kāra (legacy `karac build`) | 0.50 to 0.59 s |
| Go | 0.75 to 0.87 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.10 to 1.33 s |
| Rust (`rustc -O`) | 1.16 to 1.40 s |
| C (`clang -O3`) | 1.30 to 1.37 s |
| Python | 2.8 s |

The time is allocation and number formatting, not the tests. Why the
Kāra program is the fastest has not been looked into; how the legacy
backend stores a literal pushed as a `String` is the first thing to
check. The Kāra program also prints the same line under
`karac __mir-llvm-run` in 7.2 s, compile included; that JITs the MIR's
IR without optimization passes, so it is not a benchmark. The
`karac build` time is the frozen legacy backend.

## Compiler findings

No new findings.
