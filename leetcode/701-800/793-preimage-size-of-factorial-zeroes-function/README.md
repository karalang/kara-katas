# 793. Preimage Size of Factorial Zeroes Function

`f(x)` is the number of zeroes at the end of `x!`: `f(3) = 0` since `3!
= 6`, and `f(11) = 2` since `11! = 39916800`. Given `k`, count the
non-negative integers `x` with `f(x) = k`.

```
k = 0  ->  5     (0!, 1!, 2!, 3! and 4! end in no zeroes)
k = 5  ->  0     (no factorial ends in exactly five)
k = 3  ->  5
```

**Constraints:** `0 <= k <= 10^9`.

## Approaches

`f(x)` is `x/5 + x/25 + x/125 + ...`, and it never goes down as `x`
grows. It changes only at multiples of 5, so every count it reaches is
reached by exactly five `x` in a row, and at a multiple of 25 it jumps
by two or more, so the counts in between are never reached. The answer
is therefore 5 or 0.

| file | mechanism |
|---|---|
| `preimage_size_fzf.kara` ★ | binary search over `x` from 0 to `5k + 5` for the least `x` with `f(x)` at least `k`, and 5 when `f` of it is `k`, 0 when it is more; O(log² k) |
| `preimage_size_fzf_count.kara` | the least `x` with `f(x)` at least `k + 1` less the least with at least `k`, each by binary search, so the 5 or 0 comes out of the subtraction; O(log² k) |
| `preimage_size_fzf_digits.kara` | `f` gains 1, 6, 31, 156, ..., `(5^i - 1) / 4`, over each block of `5^i` numbers, so a count is reached when it is a sum of those block sizes with each used at most four times; going from the largest block size not above `k` down, 0 when one goes into what is left five times, else 5; O(log k) |
| `preimage_size_fzf_walk.kara` | `f(x)` lies between `x/4 - log₅ x - 1` and `x/4`, so the least `x` with at least `k` is a little above `4k`: start at the multiple of 5 at or below `4k` and step 5 until `f` reaches `k`; O(log² k) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 9 lines: LeetCode's three examples; `k = 6`,
reached at `x = 25`; 11, 29 and 30, which `f` jumps over at 50 and 125;
`k = 10^9`, LeetCode's largest; and 300 random `k` up to a billion, with
how many have five and a checksum. `preimage_size_fzf.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
walking `x` up from 0, adding to `f` the fives in each `x`, and counting
the `x` that have each count up to 3,000. It also checks its own
Legendre sum for `f`, used by P3 and P4, against a sum over `1..x` of
the fives in each number at ten `x`. Every arm is then held to the
definition at every `k` from 0 to 3,000, and to three properties at
1,600 random large cases, each a `k` up to a billion, an `x` up to about
four billion, and a `y` up to four billion with 5 in it two to five
times.

| | property |
|---|---|
| P1 | the count is the definition's, for every `k` up to 3,000 |
| P2 | the count for a random `k` is 0 or 5, and the same from every arm |
| P3 | the count for `f(x)` is 5 |
| P4 | the `j - 1` counts that `f` jumps over at `y`, which has 5 in it `j` times, have 0, and the counts on each side of them 5 |

It prints `k up to 3000 (2403 with five, 10 of 10 sums agreeing) and
1600 large cases, 4 arms, 31204 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: f counting only the multiples of 5 | P1 598, P2 954, P4 1600 |
| M2 | ★: the search for f above k, not at least k | P1 2403, P2 3846, P3 1600, P4 1600 |
| M3 | ★: five whenever f reaches k or more | P1 598, P2 954, P4 1600 |
| M4 | count: the search capped at 4k, below every answer | P1 3001, P2 1600, P3 1600, P4 1600 |
| M5 | count: the search for f at least k - 1 | P1 961, P2 515, P3 321, P4 1600 |
| M6 | count: f skipping the multiples of 25 | P1 653, P2 349, P3 71, P4 1590 |
| M7 | digits: a count jumped over when a block size goes in four times | P1 1718, P2 1213, P3 1515, P4 1600 |
| M8 | digits: a block size equal to k left out | P1 3 |
| M9 | digits: a block size taken off once, not as often as it goes in | P1 734, P2 399, P3 138, P4 1600 |
| M10 | walk: the walk started 5 too high | P1 1 |
| M11 | walk: steps of 10 | P1 1052, P2 637, P3 783, P4 1342 |
| M12 | walk: the walk going on while f is k | P1 2403, P2 1282, P3 1600, P4 1600 |

P1 kills all twelve, and P2 and P4 all but the two that are seen at only
a few `k`. Starting the walk 5 too high gives a wrong answer only at `k
= 0`, since for any larger `k` the least `x` is above `4k` and so at
least 5 past the start. Leaving out a block size equal to `k` errs only
at the block sizes from 31 up (at 6 it happens to find 5 anyway), of
which 31, 156 and 781 are in P1's range and none was among the random
`k`.

## Verification

Every arm prints the same output as `preimage_size_fzf.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`cfbbf3e8eb`, whose last compiler change is `b115567cf2`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and
the bench program unchanged, and print the same output under the legacy
interpreter (`karac run --interp`), the legacy JIT (`karac run`), `karac
build` and an auto-par build.

## Benchmarks

The bench program uses the ★ arm in all five languages. Each of
4,000,000 rounds draws a random `k` up to a billion, LeetCode's largest,
and asks how many `x` have `k` zeroes, by the ★ arm's binary search, so
about 32 steps each computing `f` with about 13 divisions by 5. Every
implementation prints `4000000 values of k: 3199888 with five, checksum
765365400`, the Kāra program under `karac __mir-run` included (in 233
s).

The bench measures integer division and the branch of a binary search.
Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 3.26 to 3.38 s |
| Rust (`rustc -O`) | 3.28 to 3.40 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.95 to 2.28 s |
| Go | 2.25 to 2.84 s |
| Python | 89.84 to 91.53 s |
| Kāra (`karac build --mir`) | 1.84 to 2.10 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 14.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.95 s,
against C's 3.34, Rust's 3.32 (2.12 under overflow checks) and Go's
2.39. Under valgrind's cachegrind C and Rust run the same 13.6 billion
instructions and 1.84 billion branches, and v2 12.2 billion instructions
but 3.86 billion branches, mispredicting 214 million to their 130
million. That C and plain Rust are the slow ones, and Rust under
overflow checks is not, is not profiled. One guess, not measured, is a
choice between a branch and a select in the search's step, which waits
on a chain of divisions. The legacy build ran 3.32 to 3.43 s, a median
of 3.41 s in the interleaved runs, so v2 takes 0.57 times legacy. The
comparison with C and Rust waits until after M4.

## Compiler findings

Nothing new in v2.
