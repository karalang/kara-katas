# 775. Global and Local Inversions

Given `nums`, a permutation of the integers `0` to `n - 1`, a global
inversion is a pair `i < j` with `nums[i] > nums[j]`, and a local
inversion is an index `i` with `nums[i] > nums[i + 1]`. Return whether
the number of global inversions equals the number of local ones.

```
nums = [1, 0, 2]  ->  true    (one global inversion, one local)
nums = [1, 2, 0]  ->  false   (two global inversions, one local)
```

**Constraints:** `n` is from 1 to 100,000, and `nums` holds every
integer from 0 to `n - 1` once.

## Approaches

Every local inversion is a global one, so the counts are equal exactly
when no inversion spans more than one place. Two arms test that
directly; the other two count both kinds and compare.

| file | mechanism |
|---|---|
| `global_and_local_inversions.kara` ★ | every value at most one place from its own index, which in a permutation of 0 to `n - 1` holds exactly when no inversion spans more than one place; O(n) |
| `global_and_local_inversions_suffix.kara` | from the right, the least value at least two places ahead; a value greater than it is an inversion spanning more than one place; O(n), and it never uses that the values are 0 to `n - 1` |
| `global_and_local_inversions_fenwick.kara` | both kinds counted: the global ones with a Fenwick tree over the values seen so far, the seen values greater than `nums[i]` being the inversions that end at `i`; O(n log n) |
| `global_and_local_inversions_merge.kara` | both kinds counted: the global ones by merge sort, each value taken from the right half first being inverted with every value left in the left half; O(n log n) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: LeetCode's two examples; one value;
one swapped pair; five small permutations, ideal and not; an ideal
permutation of 100,000 values, LeetCode's limit, and the same with two
values three places apart swapped near its end; then 300 random
permutations of 1 to 60 values, a third uniformly random, a third ideal
(adjacent pairs swapped at random, never two overlapping) and a third
ideal with two values up to three places apart swapped, with how many
are ideal and a checksum. `global_and_local_inversions.py` mirrors the ★
arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition:
every pair `i < j` compared to count the global inversions, every
neighbouring pair for the local ones, and the two counts compared. Its
1,600 random permutations, 1,500 of 1 to 60 values and 100 of 61 to
400, are drawn as in the harness, each with a second permutation of 1 to
30 values for P4.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the inverse permutation gives the same answer |
| P3 | the permutation turned end for end, each value `v` becoming `n - 1 - v`, gives the same answer |
| P4 | a second permutation joined on after it, its values raised by `n`, is ideal exactly when both are |

It prints `1600 permutations (705 ideal), 4 arms, 25600 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the count of ideal
ones is the definition's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value two places from home allowed | P1 189 |
| M2 | ★: only values above their index checked | P1 96, P2 187, P3 187 |
| M3 | ★: any value away from home refused | P1 659 |
| M4 | suffix: the least value one place ahead | P1 222, P3 338, P4 83 |
| M5 | suffix: each value joining the least at once | P1 634, P2 4, P3 24, P4 2 |
| M6 | suffix: the first value never checked | P1 22, P2 14, P3 49, P4 22 |
| M7 | fenwick: the smaller values before counted | P1 686, P2 1, P4 4 |
| M8 | fenwick: the first local inversion missed | P1 338, P3 338, P4 91 |
| M9 | fenwick: the tree updated one slot at a time | P1 650, P2 7, P3 9, P4 4 |
| M10 | merge: one inversion for each value taken from the right | P1 667, P4 3 |
| M11 | merge: the merged run not copied back | P1 100, P2 190, P3 145, P4 61 |
| M12 | merge: runs of two left unsorted | P1 658, P2 50, P3 107, P4 51 |

P1 kills all twelve. M1 and M3 move the ★ arm's limit, to two places or
to none, the same way for every value; both kinds of permutation the
other properties build keep each value's distance from home, so only P1
sees them. M2 checks values above their index and not below, and both
the inverse and the turned permutation put a value that far below its
index where one was that far above, so P2 and P3 see it on the same
187 permutations. M4 and M8 each miss, or add, an inversion at one end
of the permutation, which turning it end for end moves to the other
end, so P3 sees them. The rest break the arm for most permutations, and
the other properties see them only where the two answers they compare
come out differently. No first choice survived.

## Verification

Every arm prints the same output as `global_and_local_inversions.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and under `karac __mir-llvm-asan` (AddressSanitizer)
with no error; the differential prints its line under all three. `karac
check` passes all four arms, the differential and the bench program. The
debug build that runs `__mir-llvm-run`, `__mir-llvm-asan` and `build
--mir` and the release build that runs `check` and `__mir-run` are both
at kara `4f079681eb`, whose last compiler change is `ecb1a0322e`. The
runtime archives were built after the last runtime change,
`176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms and the differential.
Each arm prints the same output under the legacy interpreter (`karac
run --interp`), the legacy JIT (`karac run`), `karac build` and an
auto-par build, each build with a warning that a borrowed `nums` is used
after a move, since legacy predates borrowed parameters. The legacy JIT
and `karac build` print the differential's line as above; the legacy
interpreter prints `1600 permutations (690 ideal), 4 arms, 25600 checks,
0 failures`, a different set of permutations. In
`permutation(mut seed, m, next_random(mut seed) % 3)` it passes the
first argument as `seed` was before the third advanced it, the behaviour
kata 771 notes: with that call's third argument computed into a name
first, the legacy interpreter prints 705 as well. Legacy refuses the
bench at `is_ideal_permutation(perms[g])`, as a move out of an index;
its timing below is of a copy whose parameter is `ref Vec[i64]`. Legacy
is frozen, so all this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 permutations
of 100,000 values, LeetCode's limit, are built once: half ideal, a
quarter ideal with two values three places apart swapped within the last
thousand places, and a quarter with such a swap anywhere. Each of 12,000
rounds answers the next one. Every implementation prints `12000 rounds
of 100000 values: 6000 ideal, checksum 512801984`, the Kāra program
under `karac __mir-run` included (in 342 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.46 to 0.51 s |
| Rust (`rustc -O`) | 0.73 to 0.92 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.87 to 4.61 s |
| Go | 0.63 to 0.84 s |
| Python | 40.3 to 41.0 s |
| Kāra (`karac build --mir`) | 0.93 to 1.14 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, since the legacy `karac build` refuses it (see
Verification); that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 4.1 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 0.96 s,
against C's 0.47, Rust's 0.81 and Go's 0.65. Under valgrind's
cachegrind v2 runs 12.5 billion instructions, Rust 10.5 billion and C
5.4 billion; none of the three is vectorized, so each value costs a few
instructions and a branch or two in all of them, and Kāra's overflow
checks on the subtraction and the `abs` are among its extra ones.
Rust with overflow checks on takes 4.32 s at the median, five times its
own unchecked build and four times Kāra's checked one; that is not
profiled. The legacy build of the copy ran 1.08 to 1.24 s, a median of
1.12 s, so v2 takes 0.86 times legacy. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new.
