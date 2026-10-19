# 769. Max Chunks To Make Sorted

`arr` is a permutation of 0 to n - 1. Split it into consecutive chunks,
sort each chunk on its own, and put them back in order. Return the most
chunks a split can have and still leave the whole array sorted.

```
[4, 3, 2, 1, 0]  ->  1
[1, 0, 2, 3, 4]  ->  4
```

**Constraints:** n is from 1 to 10; `arr` holds each of 0 to n - 1 once.

## Approaches

The sorted array holds value i at place i, so a chunk may end after
place i exactly when places 0 to i hold the values 0 to i. The arms find
those places in four ways.

| file | mechanism |
|---|---|
| `max_chunks_to_sorted.kara` ★ | a cut wherever the largest value so far equals the place; one pass, O(1) space |
| `max_chunks_to_sorted_sums.kara` | a cut wherever the running sum equals 0 + 1 + ... + i, which no other set of distinct values from 0 up reaches |
| `max_chunks_to_sorted_cycles.kara` | the permutation's cycles, each spanning from its smallest place to its largest; a cut wherever no span crosses |
| `max_chunks_to_sorted_stack.kara` | LeetCode 768's stack of chunk maxima, which needs nothing from the permutation; a smaller value merges every chunk whose largest is greater |
| `differential.kara` | the four arms against the definition, four properties |

Every arm prints the same 8 lines: the two LeetCode examples; a single
value; a sorted array; a rotation of three before a fixed value; two
arrays of swapped neighbours and of rotated triples; then 300 random
permutations of up to 10, each sorted and given a few swaps of near
places, with their chunks' total and a checksum.
`max_chunks_to_sorted.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
which tries every way of cutting the array and keeps the most pieces
that, each sorted on its own, make 0 to n - 1. Of the 1,800 random
permutations a third are shuffled and the rest sorted with a few swaps
of near places; the first 1,500, of up to 10 places, are checked against
the definition, and the last 300, of up to 2,000, against the other
properties.

| | property |
|---|---|
| P1 | the answer is the definition's (the 1,500 short permutations) |
| P2 | the inverse permutation has the same answer |
| P3 | the array reversed, each value v made n - 1 - v, has the same answer |
| P4 | a second permutation of up to 10, its values raised by n, appended adds its own answer |

It prints `1800 permutations (83571 chunks), 4 arms, 27600 checks,
0 failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error; the total is the ★
arm's.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: no running maximum | P1 736 |
| M2 | ★: a cut where the largest is one more than the place | P1 1084, P2 617, P3 617 |
| M3 | ★: the first place never read | P1 1140, P2 182, P3 615, P4 1330 |
| M4 | sums: the triangle number taken as i * i / 2 | P1 1366, P3 527, P4 960 |
| M5 | sums: a cut wherever the sum reaches the triangle number | P1 1084 |
| M6 | sums: no running sum | P1 1078, P2 274, P3 765, P4 1260 |
| M7 | cycles: a cycle reaching the last place visited | P1 426, P2 931, P3 888 |
| M8 | cycles: no cycle's reach ever recorded | P1 1084 |
| M9 | cycles: no running maximum of the reaches | P1 895 |
| M10 | stack: a merged chunk keeping the last popped largest | P1 145, P2 444, P3 210 |
| M11 | stack: at most one chunk merged | P1 530, P2 814, P3 814 |
| M12 | stack: a merged chunk keeping the new value as its largest | P1 525, P2 814, P3 814 |

P1 kills all twelve. M1, M5, M8 and M9 are seen by P1 alone: M1 counts
the values in their own places, and M9 answers n less the number of
cycles longer than one; the inverse and the mirror keep both counts, and
a second permutation adds its own. M5 and M8 answer n whatever the
array. P4 sees the edits that depend on where in the array a place sits,
M3, M4 and M6, since the appended values sit at places n and on. P2 and
P3 see the rest, the edits whose answer changes when the permutation is
turned round or inverted.

## Verification

Every arm prints the same output as `max_chunks_to_sorted.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`4f079681eb`, whose last compiler change is `ecb1a0322e`. The runtime
archives were built after the last runtime change, `176f59738b`.

Since kara `3c8e763161` (B-2026-10-18-31) the sanitizer lane sees leaks
itself. The leak check also copied each arm's and the differential's
lane executable as it was linked and ran it with the preloaded shim from
kata 708, which refuses the lane's hand-made stack so that LeakSanitizer
sees `main`: all five print their output and report no leak.

The frozen legacy backends accept all four arms, the differential and,
through a copy, the bench. Each arm prints the same output under the
legacy interpreter, `karac run`, `karac build` and an auto-par build,
and the differential prints its line under the legacy interpreter and
`karac build`, each with a warning that a borrowed `arr` is used after a
move, since legacy predates borrowed parameters. Legacy refuses the
bench at `max_chunks_to_sorted(pool[round % 64])`, as a move out of an
index; its timing below is of a copy whose parameter is `ref Vec[i64]`.
Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. LeetCode stops
at 10 values, too few to time, so sixty-four permutations of 2,000 are
built once, each sorted and then given a random number of swaps of near
places, so that chunks form; each of 150,000 rounds counts the next
one's chunks. Every implementation prints `150000 permutations of
2000: 116648409 chunks in all, checksum 635828458`, the Kāra program
under `karac __mir-run` included (in 118 s).

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.26 to 0.31 s |
| Rust (`rustc -O`) | 0.28 to 0.35 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.79 to 0.91 s |
| Go | 0.30 to 0.36 s |
| Python | 14.1 to 14.8 s |
| Kāra (`karac build --mir`) | 0.76 to 0.90 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend, the one this kata measures now that legacy is
frozen. That edit is by hand, on top of the `scripts/new-bench.sh`
output. Under `karac __mir-llvm-run` the program prints the same line in
2.8 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark.

So at the medians of the interleaved runs the v2 build takes 0.82 s,
against C's 0.28, Rust's 0.31 and Go's 0.31; Rust under overflow checks
takes 0.86 s, about as long as v2, and Kāra checks overflow by default.
Under valgrind's cachegrind C runs 2.7 billion instructions and
150 million branches and Rust 3.0 billion and 151 million, with
0.1 percent mispredicted: they compute the running maximum and the
comparison without branching. v2 runs 3.2 billion instructions but
718 million branches, 8.6 percent of them mispredicted, which is where
its time goes. The legacy build of the copy ran 0.78 to 0.91 s, a median
of 0.80 s in the interleaved runs, so v2 and legacy take about the same
time, inside M2's limit of twice legacy; new katas' benches are outside
M2's frozen set in any case. The comparison with C and Rust waits until
after M4.

## Compiler findings

None new.
