# 525. Contiguous Array

Given a binary array `nums`, return the maximum length of a
contiguous subarray with an equal number of `0` and `1`.

```
nums = [0,1]                ->  2
nums = [0,1,0]              ->  2
nums = [0,1,1,1,1,1,0,0,0]  ->  6
```

**Constraints:** `1 <= nums.length <= 10^5`; `nums[i]` is either `0`
or `1`.

## Approaches

Every arm is `fn find_max_length(nums: Vec[i64]) -> i64`. Count a 1 as
+1 and a 0 as -1: a run has as many 0s as 1s exactly when the running
balance is the same at both its ends, so every arm looks for the two
prefixes furthest apart with the same balance, the empty prefix
included.

| file | mechanism |
|---|---|
| `find_max_length.kara` ★ | a `Map` from each balance to the first index it was seen at (the empty prefix at -1); every later return to it is measured |
| `find_max_length_array.kara` | the same, in an array of `2n + 1` places offset by `n`, since a balance lies between `-n` and `n` |
| `find_max_length_sorted.kara` | every prefix's (balance, length) pair sorted; each group of equal balances spans from its first to its last |
| `find_max_length_last.kara` | one pass records the last prefix length for each balance in a `Map`; a second pass from the left meets each balance first at its earliest and measures to its last |
| `differential.kara` | the four arms against a brute force over every run, five properties |

Every arm prints the same 11 lines: the answer for nine arrays (the
three examples, a single 0, two 1s, `0011`, `101010`, `0001`, and one
whose longest run is in the middle), then for 3,000 random arrays of 1
to 40 bits, each a 1 with chance one in 1 to 4, a total and a checksum
over the answers, and last the largest case: 100,000 random bits, and
60,000 0s followed by 40,000 1s (answer 80,000). `find_max_length.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and a brute force
that counts the 0s and 1s of every run. Each arm is held to the
properties below on 2,000 cases of random bits, each a 1 with chance
one in 1 to 4: a short array of 1 to 16 bits for P1, and a longer one
of 1 to 80 for the rest.

| | property |
|---|---|
| P1 | the answer is the brute force's, on the short array |
| P2 | the array back to front gives the same answer |
| P3 | every bit flipped gives the same answer |
| P4 | the array followed by its flip, balanced as a whole, gives its whole length |
| P5 | the answer is even and at most twice the count of the rarer bit |

It prints `2000 cases, 4 arms, 40000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the empty prefix put at 0, not -1 | P1 357, P2 332, P4 2000, P5 217 |
| M2 | ★: each run measured one short | P1 1236, P4 2000, P5 1485 |
| M3 | array: every index stored, so first is last | P1 1236, P4 2000 |
| M4 | array: the unseen mark tested as -1, not -2 | P1 1861, P5 1942 |
| M5 | sorted: the empty prefix left out | P1 357, P2 351, P4 2000 |
| M6 | sorted: the balance counts only the 1s | P1 1332, P3 1856, P4 2000, P5 813 |
| M7 | last: the run from the empty prefix never measured | P1 357, P2 351, P4 2000 |
| M8 | last: the first length kept, not the last | P1 1236, P4 2000 |
| E1 | ★: the step written `2 * x - 1` | 0 |
| E2 | array: two spare places | 0 |
| E3 | sorted: sorted by an explicit comparison | 0 |
| E4 | last: the length taken off in two steps | 0 |

M3 and M8 fail the same checks because both always answer 0: each
keeps only one index per balance, so a balance is never measured
against an earlier one. M5 and M7 are another pair, a run that starts
at the front never seen. M1 is close to them but not the same: with
the empty prefix at 0 a run from the front is measured one short, an
odd length, which P5 catches. M6 answers the longest stretch of 0s
instead, and every property but P2 catches it.

## Verification

Every arm prints the same output as `find_max_length.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
runs clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. The differential
prints `40000 checks, 0 failures` on the first two and runs clean
under the third. `karac check` passes on every arm, the differential
and the bench program.

On the frozen legacy backends, the array, sorted and last arms print
the same output under `karac run --interp`, LLJIT and `karac build`,
and under a `KARAC_AUTO_PAR=1` build. The ★ arm, the differential and
the bench program are refused at type checking, "unary '*' requires
'ref T' ... found 'i64'": legacy types the payload of a `Map`'s `get`
by value, so it refuses `*j`. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20 arrays of 100,000 bits
(the problem's longest) once, each bit a 1 with chance one in 2, 3 or
4 by turns, then solves every array in each of 20 rounds. Every
implementation prints `20 arrays of 100000, 20 rounds: total 11906040,
checksum 735412899`, the Kāra program under `karac __mir-run` included
(in 50.7 s).

Each mirror makes a fresh map for every call, as the ★ arm's
`Map.new()` does: Rust's `HashMap` with its default hasher, Go's
built-in map, Python's dict. C has no map of its own, so its mirror is
an open-addressing table with linear probing that doubles at half
full. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.59 s |
| Rust (`rustc -O`) | 1.10 to 1.18 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.09 to 1.19 s |
| Go | 1.29 to 1.36 s |
| Python | 6.28 to 6.53 s |
| Kāra (`karac build --mir`) | 1.40 to 1.49 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`df61cbfff6`. Under `karac __mir-llvm-run` the program prints the same
line in 12.9 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them as
written.
