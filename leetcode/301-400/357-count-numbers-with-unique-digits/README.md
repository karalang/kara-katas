# 357. Count Numbers with Unique Digits

Given an integer `n`, return the count of all numbers with unique digits,
`x`, where `0 <= x < 10^n`.

```
n = 2  ->  91   (every number from 0 to 99 except 11, 22, 33, ..., 99)
n = 0  ->  1
```

**Constraints:** `0 <= n <= 8`.

## Approaches

Each arm also takes a `base`, and prints the answer for bases 2 to 7 at every
width from 0 to one past the base, where the count stops growing: no number
has more distinct digits than its base has digits.

| file | mechanism | cost |
|---|---|---|
| `unique_digits.kara` ★ | count by length: a k-digit number has `b - 1` choices for its leading digit and then `b - 1`, `b - 2`, ... for the rest; sum over k | `O(n)` |
| `unique_digits_dfs.kara` | build every such number a digit at a time with a used-digit bitmask, counting each prefix | one call per number |
| `unique_digits_dp.kara` | digit DP over the number padded to n digits, memoised in a `Map` keyed by (position, digits used, started) | `O(n · 2^b · b)` |
| `unique_digits_subsets.kara` | walk every set of at most n digits as a bitmask; a set of k digits has `k!` orders, less the `(k - 1)!` that start with 0 | `O(2^b)` |
| `differential.kara` | the four arms against a brute-force oracle that checks the digits of every number, 403 checks, five properties | — |

Every arm prints the same 15 lines: the answers for `n = 0` to `8` in base
10 and the table for bases 2 to 7. `unique_digits.py` mirrors the ★ arm and
its output is byte-identical.

The number 0 is the trap. Its spelling starts with the digit 0, so every
method that forbids a leading zero has to add it back by hand: the length
count starts its total at 1, the search counts the empty prefix, and the
subset count adds 1 before walking the sets.

## Differential

`differential.kara` holds copies of the four arms and an oracle that knows
nothing about counting: it walks every number below `base^n` and checks its
digits with a bitmask. It covers bases 2 to 7 at every width from 0 to
`base + 1` where `base^n <= 300,000`.

| | property |
|---|---|
| P1 | every arm returns the oracle's answer, and the arms agree where the oracle is too slow |
| P2 | the count never falls as n grows, and stops rising exactly at `n = base` |
| P3 | the step from `n - 1` to `n` is the count of n-digit numbers, `(b - 1) · (b - 1) · (b - 2) · ...` over n factors |
| P4 | one digit allows exactly `base` numbers |
| P5 | base 10 matches the known answers for n = 0 to 8 (the search is left out here; the arm's own run covers it) |

It prints `403 checks, 0 failures` under `karac run --interp`, LLJIT, and
both builds.

## Mutation testing

Eleven edits to the copies inside `differential.kara`, each built and run.
All eleven are killed. The properties listed are those among the first ten
failures the run prints.

| # | mutation | how |
|---|---|---|
| M1 | length count: the choices never shrink | P1 and P3, 99 failures |
| M2 | length count: forgets the number 0 | P1 and P4, 169 failures |
| M3 | search: allows a leading zero | P1, 64 failures |
| M4 | search: never marks a digit used | P1, 52 failures |
| M5 | search: counts only full-length numbers | P1, 64 failures |
| M6 | DP: the memo key ignores the position | P1, 44 failures |
| M7 | DP: a padding zero marks 0 as used | P1, 46 failures |
| M8 | subsets: no leading-zero subtraction | P1, 72 failures |
| M9 | subsets: sets of exactly n digits skipped | P1, 61 failures |
| M10 | subsets: the factorial is one factor short | P1, 59 failures |
| M11 | oracle: checks every other digit | P1, 100 failures |

Two candidate mutations were dropped as equivalent rather than run: removing
the length count's `k <= base` guard (the running product reaches 0 at
`k = base + 1` anyway) and dropping `started` from the DP's memo key (an
unstarted state always has an empty digit set, and a started one never does).

## Verification

All four arms and the differential are byte-identical under `karac run`
(LLJIT), `karac run --interp`, `karac build` with `KARAC_AUTO_PAR=0`, and the
default auto-parallelising `karac build`, and the four arms match
`unique_digits.py` byte for byte. Under valgrind at `KARAC_OPT_LEVEL=0`
every arm ends with `in use at exit: 0 bytes in 0 blocks` and
`ERROR SUMMARY: 0 errors`. The bench program prints
`bases 2 to 11: checksum 36315606` under LLJIT and both builds, as do its C,
Rust, Go and Python mirrors.

## Benchmarks

Not measured yet. The bench programs in `bench/` and their C, Rust, Go and
Python mirrors are written and agree on the printed checksum, but the timings
still have to be taken on a quiet machine. This section will carry the table
when they are.

## Compiler findings

Every arm type-checked and ran as first written. Probing other spellings
of the same counts (a `fold`, an iterator `product`, an `Array[bool, 16]`
passed `mut`, an explicit-stack search, a counting closure) found three
gaps. With them avoided, every spelling agrees on all four surfaces and is
clean under valgrind.

- **B-2026-10-06-126 (fixed in kara, parse): Rust's turbofish on a method
  call was reported as a missing semicolon.** `(1..k).map(|i| base - i)
  .product::[i64]()` failed with "Expected Semicolon, found ColonColon". It
  is now named as a turbofish, with a `karac fix` edit that deletes it; the
  type goes on the binding instead. Fixed in kara `63b3156d3`.
- **B-2026-10-06-127 (open, codegen):** a `fold` whose closure
  destructures a tuple accumulator, `|(s, p), k| (s + k, p * k)`, does not
  build; `|acc, k| (acc.0 + k, acc.1 * k)` does.
- **B-2026-10-06-128 (open, codegen):** `sum` or `fold` on a range held
  in a binding (`let r = 1..=n; r.sum()`) does not build; the same call on
  the range literal does.
