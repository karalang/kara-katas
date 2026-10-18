# 754. Reach a Number

You stand at 0 on a number line. Move k, for k = 1, 2, 3 and so on, goes
k steps left or right, your choice each time. Return the fewest moves
that end exactly on `target`.

```
target = 2  ->  3      (0 -> 1 -> -1 -> 2)
target = 3  ->  2      (0 -> 1 -> 3)
```

**Constraints:** -10^9 <= target <= 10^9; target is not 0.

## Approaches

The moves can be mirrored, so only t = |target| matters. All k moves to
the right sum to 1 + ... + k; turning move i round takes 2i off that,
and every even amount up to the sum is a sum of distinct moves. So k
moves can end on t exactly when that sum is at least t and exceeds it by
an even number, and the answer is the first such k. The arms differ in
how they find it.

| file | mechanism |
|---|---|
| `reach_number.kara` ★ | add moves one at a time until the sum reaches t with an even excess; O(sqrt(t)) |
| `reach_number_float.kara` | start from (sqrt(8t + 1) - 1) / 2 with an `f64` square root, correct it a step either way, then add moves until the excess is even; O(1) |
| `reach_number_newton.kara` | the same start from an integer square root by Newton's method, then the answer from a table: the sums' parity repeats odd, odd, even, even; O(log t) |
| `reach_number_bisect.kara` | binary search for the first k whose sum reaches t, then add moves until the excess is even; O(log t) |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 12 lines: the two LeetCode examples;
1, -1, 4, 5 and -6; both ends of the range; a target equal to a sum 1 +
... + 44720 and one past it; and 1,000 random targets, with the total of
their answers and a checksum. `reach_number.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which grows the set of positions reachable after k moves, one move at a
time with both signs, until the target is in it. Every target from
-400 to 400 but 0 is checked against it. 1,000 more targets lie within
3 of a sum 1 + ... + k, where the square-root arms' rounding is most
likely to slip, and 1,000 are random; each of those 2,000 is negated at
random. The ★ arm's answers add up to 44,709,591 moves.

| | property |
|---|---|
| P1 | the answer is the definition's (the 800 small targets) |
| P2 | the negated target takes as many moves |
| P3 | a walk of that many moves, turning moves round from the largest down while the half-excess allows, ends on the target |
| P4 | no walk of one, two or three fewer moves ends on it, and four fewer moves sum to less than the target |

It prints `2800 targets (44709591 moves in all), 4 arms, 36800 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed. Three more edits, E1 to
E3, change nothing that can be seen, and the differential rightly
reports no failure for them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the target's sign kept | P1 399, P2 2798, P3 1390 |
| M2 | ★: the excess required to be a multiple of 4 | P1 386, P4 1370 |
| M3 | ★: a sum equal to the target not enough | P1 54, P4 217 |
| M4 | square root: the target's sign kept | P1 399, P2 2798, P3 1390 |
| M5 | square root: two moves at a time to fix the parity | P1 204, P4 713 |
| M6 | square root: started two too high, no step back | P1 414, P4 1443 |
| M7 | Newton: each step divided by 3, not 2 | P1 772, P3 2772 |
| M8 | Newton: k's parity read the wrong way | P1 386, P3 644, P4 713 |
| M9 | Newton: a sum equal to the target not enough | P1 54, P4 217 |
| M10 | bisect: searched only to 40,000 moves | P3 186 |
| M11 | bisect: the first sum above the target, not at least it | P1 54, P4 217 |
| M12 | bisect: three moves at a time to fix the parity | P1 386, P4 1357 |
| E1 | square root: the step back never taken | 0 |
| E2 | Newton: the shortcut for m < 1 only | 0 |
| E3 | bisect: searched to 200,000 moves | 0 |

P1 kills eleven of the twelve on the 800 small targets. M10 caps the
search at 40,000 moves, which matters only for targets beyond
800,020,000, and P3 sees it there, since that many moves cannot reach
them. P2 sees the two edits that keep the target's sign, M1 and
M4. P3 sees the edits that answer too few moves for some target,
M1, M4, M7, M8 and M10, and P4 the ones that answer too many,
M2, M3, M5, M6, M8, M9, M11 and M12; M8, reading k's parity the wrong
way round, does both. E1 never takes the square-root arm's step back,
which is never needed, since the floor of the root never overshoots;
E2 sends only m = 0 to the shortcut, and m = 8t + 1 is at least
9; E3 searches to 200,000 moves instead of 100,000. Two first choices
survived and were replaced, both because they change nothing. Requiring
the square-root arm's sum to pass t strictly in its upward loop is
undone by its step back. Rounding Newton's step up sometimes ends one
above the floor of the root, which raises k by one only where that floor
is even; there the arm's own correction lands on the same k unless t is
a sum 1 + ... + k, and then 8t + 1 is a perfect square, on which the
rounded-up method is exact. A script compared the two arms' answers for
every t below 3 million and found no difference.

## Verification

Every arm prints the same output as `reach_number.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`b84c5d937f`, whose last compiler change is `56a4cad109`. The runtime
archives were built after the last runtime change, `b09cd37112`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept every program here: each arm prints
the same output under the legacy interpreter, `karac run`, `karac build`
and an auto-par build, and the differential prints its line under the
legacy interpreter and `karac build`.

## Benchmarks

The bench program uses the ★ arm in all five languages, on 30,000 random
targets up to 10^9 in size, either sign, adding up the answers and a
checksum. The ★ arm walks some 28,000 moves for a target of that size,
so this measures the loop. Every implementation prints `30000 targets:
849461596 moves in all, checksum 470244008`, the Kāra program under
`karac __mir-run` included (in 55 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.27 to 0.30 s |
| Rust (`rustc -O`) | 0.27 to 0.33 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.40 to 0.45 s |
| Go | 0.26 to 0.28 s |
| Python | 21.0 to 21.5 s |
| Kāra (`karac build --mir`) | 0.39 to 0.43 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.40 s,
against C's 0.29, Rust's 0.30 and Go's 0.26, and level with Rust under
overflow checks (0.43), the equal-safety comparison: the loop is two
additions and a test, and Kāra checks both additions for overflow. Under
valgrind's cachegrind v2 runs 5.9 billion instructions and 2.5 billion
branches against C's and Rust's 5.1 billion and 0.85 billion; the extra
branches are presumably those checks, and almost none are mispredicted
(inferred, not read from the code). The legacy build of the same program
ran 0.32 to 0.45 s, a median of 0.40 s in the interleaved runs, so v2 is
level with legacy, inside M2's limit of twice legacy; new katas' benches
are outside M2's frozen set in any case. The comparison with C and Rust
waits until after M4.

## Compiler findings

None new.
