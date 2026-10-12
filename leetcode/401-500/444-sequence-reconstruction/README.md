# 444. Sequence Reconstruction

You are given an integer array `nums` of length `n`, a permutation of
the integers `1` to `n`, and a list of integer arrays `sequences`, each
a subsequence of `nums`. Check whether `nums` is the shortest possible
supersequence of `sequences`, and the only one: return `true` if it is,
`false` otherwise.

```
nums = [1,2,3], sequences = [[1,2],[1,3]]                ->  false   ([1,3,2] also works)
nums = [1,2,3], sequences = [[1,2]]                      ->  false   ([1,2] is shorter)
nums = [1,2,3], sequences = [[1,2],[1,3],[2,3]]          ->  true
```

**Constraints:** `1 <= n <= 10^4`; `nums` is a permutation of `1` to
`n`; `1 <= sequences.length <= 10^4`; `1 <= sequences[i].length <= 10^4`;
the total length of all sequences is at most `10^5`; every
`sequences[i]` is a subsequence of `nums` and the arrays are unique.

## Approaches

Every arm is `fn sequence_reconstruction(nums: Vec[i64], sequences:
Vec[Vec[i64]]) -> bool`. Each neighbouring pair in a sequence says one
value comes before another, so the sequences describe a directed graph,
and `nums` is the answer exactly when it is that graph's only
topological order. The arms also answer `false` when a sequence is not
a subsequence of `nums`, which an older version of the problem allowed.

| file | mechanism |
|---|---|
| `sequence_reconstruction.kara` ★ | positions and neighbouring pairs: with each value's position in `nums`, check that every sequence keeps that order and mark the neighbours in `nums` that some sequence holds side by side; every pair must be marked. O(n + total length) time, O(n) extra space |
| `sequence_reconstruction_kahn.kara` | Kahn's topological sort, which must never have a choice: one value ready at every step, and it must be the next one in `nums` |
| `sequence_reconstruction_dfs.kara` | a depth-first topological order (reverse finishing order, three colours to find a cycle); the order is unique exactly when every two neighbours in it are joined by an edge, kept in a `Set[(i64, i64)]` |
| `sequence_reconstruction_longest.kara` | the longest path: walking the values in `nums`'s order, a predecessor not yet reached refuses `nums`, and otherwise the order is unique exactly when the longest path passes through all `n` values |
| `differential.kara` | the four arms on 1,500 random cases, five properties |

Every arm prints the same 9 lines: the three LeetCode examples, three
edge cases (`n = 1`, a six-value case with two overlapping sequences,
and a case with no pairs at all), two cases outside the constraint (a
sequence that forces another order, and sequences that form a cycle),
and for 300 random cases the number answered `true` and a checksum. The
random cases are a shuffle of 1 to `n` for `n` up to 60 and windows of
it of up to 12 values, each value after a window's first left out one
time in ten; 129 of the 300 are `true`. `sequence_reconstruction.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 random cases built like the arms' random cases, `n` up to 40.

| | property |
|---|---|
| P1 | the answer is whether the windows hold every two neighbours in `nums` side by side, as the generator recorded while building them |
| P2 | on a second, small case (`n` up to 5, sequences of distinct values in random order, half of them sorted into `nums`'s order), the answer is brute force's: `nums` is the only order of 1 to `n` that keeps every sequence |
| P3 | adding `nums` itself as a sequence makes the answer `true` |
| P4 | reversing `nums` and every sequence keeps the answer |
| P5 | relabelling every value by a random order of 1 to `n` keeps the answer |

694 of the main cases and 592 of the small ones are `true`. P2 is the
only property whose inputs break the constraint, so it is the one that
sees sequences out of `nums`'s order and cycles. It prints `1500 cases,
4 arms, 30000 checks, 0 failures` under `karac __mir-run`, and a count
for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | positions: a sequence out of `nums`'s order is not refused | P2 275 |
| M2 | positions: a pair two apart counts as neighbours | P1 57, P2 11, P4 17, P5 57 |
| M3 | kahn: a choice of two ready values is allowed | P1 145, P2 55, P4 31, P5 131 |
| M4 | kahn: values left unplaced by a cycle are ignored | P2 66 |
| M5 | dfs: a cycle is not detected | P2 85 |
| M6 | dfs: the last pair of the order is not checked for an edge | P1 2, P2 36, P4 32, P5 3 |
| M7 | longest: a path one short of every value is accepted | P1 295, P2 125, P4 93, P5 295 |
| M8 | longest: a predecessor later in `nums` is not refused | P2 275 |

P3 kills nothing: every mutant here answers `true` more often than it
should, and P3's answer is always `true`. M1, M4, M5 and M8 only go
wrong on a sequence out of `nums`'s order or a cycle, which only P2
makes; without the brute-force case they would all survive. M6 shows
the generator's lean: a window clipped at the end of `nums` covers its
last pair, so the pair left uncovered is far more often the first, and
P4 is what turns that first pair into the last one.

## Verification

All four arms print the same output as `sequence_reconstruction.py`
under `karac __mir-run` (the v2 MIR interpreter) and
`karac __mir-llvm-run`, and `karac check` passes on every file. The
differential prints `30000 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends cannot check any of these files. Its type
checker predates bare parameters borrowing (D5): it refuses passing a
`Vec` element to a bare `Vec` parameter (`E_INDEX_MOVE_NON_COPY`, in
the arms' harness and the bench program) and a `mut ref Vec` to one
(the differential's brute force). Legacy is frozen, so these are noted,
not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 50 random cases of
`n = 5,000` once, windows of a shuffle as in the arms, with every other
case also holding `nums` itself so that half the answers are `true`
(1,669,611 values in all), then answers all 50 cases 30 times over.
Every implementation prints `30 rounds on 50 cases of n = 5000 (1669611
values in sequences): 780 true, checksum 934338663`, the Kāra program
under `karac __mir-run` included (in 25 s).

The mirrors keep the ★ arm's structure; C stores each case's sequences
flat with an array of offsets. Spot timings on a shared 4-core
container, three runs each (two for Python; `bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.16 to 0.17 s |
| Rust (`rustc -O`) | 0.23 to 0.25 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.25 to 0.32 s |
| Go | 0.29 to 0.31 s |
| Python | 5.3 to 5.4 s |

The frozen legacy `karac build` cannot build the program (see
Verification), so there is no legacy time. The Kāra program prints the
same line under `karac __mir-llvm-run` in 1.1 s, compile included; that
JITs the MIR's IR without optimization passes, so it is not a
benchmark.

## Compiler findings

No new findings.
