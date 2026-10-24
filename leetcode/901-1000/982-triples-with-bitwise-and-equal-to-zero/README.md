# 982. Triples with Bitwise AND Equal To Zero

Given an integer array `nums`, return the number of AND triples.

An AND triple is a triple of indices `(i, j, k)` such that:

- `0 <= i < nums.length`
- `0 <= j < nums.length`
- `0 <= k < nums.length`
- `nums[i] & nums[j] & nums[k] == 0`, where `&` represents the bitwise
  AND operator.

```
nums = [2,1,3]  ->  12
nums = [0,0,0]  ->  27
```

**Constraints:** `1 <= nums.length <= 1000`; `0 <= nums[i] < 2^16`.

## Approaches

Every arm sizes its tables to the bits the values use: the smallest
power of two above the OR of all the values, 2^w for w bits.

| file | mechanism |
|---|---|
| `count_triplets.kara` ★ | pair counts, then the free bits' submasks: every ordered pair is counted by the AND of its values, and a third value x closes a triple with a pair exactly when the pair's AND is a submask of x's complement, so each x adds the counts at every submask of its complement. O(n^2 + n * 2^(w - b)) for b bits set in x |
| `count_triplets_map.kara` | distinct pair ANDs in a map: the pairs are counted by their AND in a `Map`, which holds only the ANDs that occur, and every third value is tried against each. O(n^2 + n * d) for d distinct ANDs |
| `count_triplets_sos.kara` | inclusion and exclusion over superset counts: sup[m] counts the values that have every bit of m, summed for all masks a bit at a time; the triples whose AND has every bit of m number sup[m]^3, so the sum over m of (-1)^\|m\| sup[m]^3 leaves those whose AND has no bit. O(w * 2^w) |
| `count_triplets_complement.kara` | pair counts against submask counts: the pairs counted by their AND, as in ★, and sub[m], the values inside m, summed for all masks a bit at a time; each AND adds its pairs times sub of its complement. O(n^2 + w * 2^w) |
| `count_triplets_mobius.kara` | pair counts without a pair loop: the pairs whose AND has every bit of m number sup[m]^2, and undoing the superset sums a bit at a time leaves the pairs whose AND is exactly m; each value then adds them at the submasks of its complement, as in ★. O(w * 2^w + n * 2^(w - b)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines. The first ten are LeetCode's two
examples and eight more: [0] (1); [1] (0); [1, 2] (6, all but the two
triples of one value); [1, 2, 4] (24); [3, 5, 6], whose AND is 0 only
with all three (6); [65535, 0] (7, every triple holding the 0);
three copies of LeetCode's largest value, 65535 (0); and
[32768, 32767] (6). Then totals and checksums over random lists: 300
of up to 12 values below 8 (105,096 triples), 3,000 of up to 30
values below 256 (7,007,374), and two of LeetCode's largest, 1,000
values below 2^16 (259,880,814). `count_triplets.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every (i, j, k), each from 0 to n - 1, counted when the AND
of its three values is 0. It checks 3,200 lists: 3,000 of 1 to 20
values against the statement, their values using 1, 2, 3, 4, 6 or 8
bits by turns, so that the narrow ones hold many zeros and repeats, and
200 of 60 values using 8 to 11 bits against the other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 lists |
| P2 | the order does not matter: the list reversed and rotated by a random amount gives the same count |
| P3 | every value's bits rotated by the same random amount within the bits in use, which keeps each triple's AND zero or not, gives the same count |
| P4 | a 0 appended joins every triple that holds it, (n + 1)^3 - n^3 more |
| P5 | a value with every bit in use appended adds three times the ordered pairs whose AND is 0 (the triples holding it once) and three times the zeros (holding it twice); three copies of it never make a triple |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 lists of 43328 values: triples 15475610, checksum
671525141, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (32.1 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty submask never counted | P1 2554, P4 3200, P5 2754, P6 2754 |
| M2 | ★: each AND counted once, not once per pair | P1 2594, P4 3200, P5 2754, P6 2794 |
| M3 | ★: the submasks of x, not of its complement | P1 2829, P4 3162, P5 3164, P6 3029 |
| M4 | map: the pairs keyed by their OR | P1 2584, P4 3162, P5 2754, P6 2784 |
| M5 | map: a 0 never closes a triple | P1 1533, P4 3200, P5 1552, P6 1552 |
| M6 | map: the lowest bit ignored in the test | P1 2307, P3 2147, P5 2475, P6 2507 |
| M7 | sos: every sign positive | P1 2962, P5 3200, P6 3162 |
| M8 | sos: subset sums for superset sums | P1 2679, P3 84, P4 3162, P5 3200, P6 2879 |
| M9 | sos: the top bit never summed | P1 2693, P3 2169, P4 3162, P5 2896, P6 2893 |
| M10 | complement: the AND itself, not its complement | P1 2958, P4 3162, P5 3153, P6 3158 |
| M11 | complement: superset sums for subset sums | P1 2770, P3 83, P4 3162, P5 3200, P6 2970 |
| M12 | complement: each value counted twice | P1 2622, P4 3200, P5 2754, P6 2822 |
| M13 | mobius: the inversion adds | P1 2962, P4 3162, P5 3200, P6 3162 |
| M14 | mobius: cubed, not squared | P1 2596, P4 3200, P5 2822, P6 2796 |
| M15 | mobius: each distinct value once | P1 1951, P4 2337, P5 2126, P6 2131 |

P1, P5 and P6 kill all fifteen, P4 thirteen (all but M6 and M7), P3
four (M6, M8, M9, M11) and P2 none. Every arm reads the values only
through counts or loops over all of them, so no edit here can see
their order; P2 guards against an arm that counts only i < j < k or
otherwise leans on the order. P3's rotation keeps every AND but sees an
edit tied to a particular bit, as M6 and M9 are; it can also move the
highest bit in use down, shrinking the table, and M8 and M11, whose
wrong sums depend on the table's size, fail there. A 0 is counted only
at the empty mask, so M7's sum without signs grows by exactly
(n + 1)^3 - n^3 too, and a 0 passes M6's test, which ignores only the
lowest bit, as it passes the right one.

Sixteen other edits were tried and set aside. Eleven failed exactly the
same checks as a kept one: map counting each AND once and resetting an
AND's count at each pair, sos squaring for cubing, and mobius not
squaring the pairs, as M2; map testing the third value with an OR, as
M4; map counting every pair twice and starting a new AND at 1, as M12;
map testing whether the AND lies inside x, as M3; map closing a triple
with an AND equal to x, as M7; mobius's inversion doing nothing, as
M13; and mobius never counting the empty submask, as M1. Four were
sound but beyond three an arm: ★ stepping its walk by one rather than
to the next submask; sos leaving the empty mask out; complement never
reading the last AND; mobius never summing the lowest bit. One crashed
in both lanes: ★ with the top bit never free takes `size / 2 - 1` for
the full mask, which is -1 when every value is 0, and indexes the
table at -1.

## Verification

Every arm prints the same output as `count_triplets.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 1.1 s (★) to 20.8 s (map, which tries every
third value against every distinct pair AND), and the differential 32.1 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

The map arm was first written `for (and, count) in pairs`. `karac`
refused the name with a clear message, `'and' is a reserved keyword
and cannot be used as an identifier; write r#and to use it as an
ordinary identifier`, but followed it with three errors that were not
true, among them one saying the file mixed top-level statements with
an explicit `fn main()`. The arm names it `mask`; the cascade is kara's
`B-2026-10-24-31`.

## Benchmarks

The bench runs the ★ arm in all five languages. The program makes 20
lists of 1,000 random values below 2^16, LeetCode's largest, once. In
each of 15 rounds it runs the arm on every list, each round starting
from a different one, and folds every count into a checksum. Every
implementation prints `15 rounds over 20 lists of 1000 values: triples
40573041030, checksum 592272062`. Each call allocates a zeroed table
of 65,536 counts, makes the million pair ANDs and walks the submasks
of every value's complement.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.314 to 0.344 s | 0.317 s |
| Rust (`rustc -O`) | 0.337 to 0.386 s | 0.360 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.387 to 0.471 s | 0.404 s |
| Go | 0.354 to 0.431 s | 0.390 s |
| Python | 23.8 s | |
| Kāra (`karac build --mir`) | 0.372 to 0.429 s | 0.398 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 60 times
Kāra's.

v2 took 0.99 times Rust's median time under overflow checks and 1.26
times C's. Under valgrind's cachegrind v2 ran 5,600 million
instructions and 1,506 million branches with 0.61 million
mispredicted, Rust with overflow checks 4,437 million, 1,374 million
and 0.61 million, and C 2,091 million, 361 million and 0.61 million.
Nothing here is hard to predict. v2 and Rust check every index into the
table, whose size is known only at run time, and C checks none, which
fits its fewer branches (inferred, not traced); v2 runs 26% more
instructions than Rust and 10% more branches in about the same time.
