# 484. Find Permutation

A permutation `perm` of `n` integers of all the integers in the range
`[1, n]` can be represented as a string `s` of length `n - 1` where:

- `s[i] == 'I'` if `perm[i] < perm[i + 1]`, and
- `s[i] == 'D'` if `perm[i] > perm[i + 1]`.

Given a string `s`, reconstruct the lexicographically smallest
permutation `perm` and return it.

```
s = "I"   ->  [1, 2]
s = "DI"  ->  [2, 1, 3]
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is either `'I'` or
`'D'`.

## Approaches

Every arm is `fn find_permutation(s: String) -> Vec[i64]`, and borrows
the pattern. The Is cut the positions into blocks with only Ds inside;
each block holds the next numbers in order, largest first.

| file | mechanism |
|---|---|
| `find_permutation.kara` ★ | 1, 2, ..., n, which fits every I, with each run of Ds reversed in place with `swap` (positions `a` to `b + 1` for Ds at `a` to `b`) |
| `find_permutation_stack.kara` | 1 to n pushed in order onto a `Vec` used as a stack, emptied with `while let Some(x) = held.pop()` at every I and at the end |
| `find_permutation_blocks.kara` | no moves at all: one pass from the right finds the end `r` of each position's block, one from the left its start `l`, and position `i` gets `l + r + 1 - i` |
| `find_permutation_pick.kara` | greedy from the left: with `d` Ds right after position `i`, it takes the `(d + 1)`-th smallest unused number, removed by index from a sorted `Vec`. O(n^2) for the removals |
| `differential.kara` | the four arms on 1,500 joined patterns, three properties |

Every arm prints the same 9 lines: the two LeetCode examples, `D`, four
Ds, four Is, alternating letters, two mixed patterns, and for 300 random
patterns (1 to 40 letters, D with odds of 1 in 4, 1 in 2 or 3 in 4 in
turn) the count of numbers and a checksum of them. `find_permutation.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and runs them on
1,500 patterns, each two random patterns `a` and `b` joined as `a + "I"
+ b`: `a` of 0 to 14 letters and `b` of 1 to 15, or up to 6 and 7 in
one case in two, with D at the same three odds. The empty `a`, one
number, is outside the problem's constraints and only ever an argument
to P3.

| | property |
|---|---|
| P1 | the answer is a permutation of 1 to `n` that fits the pattern |
| P2 | for up to 8 numbers, it is the first fitting permutation in lexicographic order, found by stepping through every permutation from 1, 2, ..., n |
| P3 | the answer for `a + "I" + b` is the answer for `a`, then the answer for `b` with every number moved up by `a`'s length plus one |

P3 holds because the I is a block boundary: nothing on its right may be
smaller than anything on its left in the smallest answer. It prints
`1500 cases, 4 arms, 13524 checks, 0 failures` under `karac __mir-run`,
in 6.5 s, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, two to each arm, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the reversal stops one short of the end of the run | P1 1425, P2 323 |
| M2 | ★: each D is reversed on its own, not the whole run | P1 1045, P2 182 |
| M3 | stack: the stack is emptied at a D, not an I | P1 1500, P2 381, P3 1500 |
| M4 | stack: the last number is never pushed | P1 1500, P2 381, P3 1500 |
| M5 | blocks: a D never carries the block's end back | P1 1045, P2 182 |
| M6 | blocks: an I does not start a new block | P1 1500, P2 381, P3 1500 |
| M7 | pick: only the first D after a position counts | P1 1045, P2 182 |
| M8 | pick: the pick is half as far into the unused numbers | P1 1425, P2 323 |

The counts fall into three groups, and each group is one set of
patterns. M2, M5 and M7 are each right on any pattern without two Ds
in a row and wrong on every pattern with one, 1,045 of the 1,500. M1
and M8 are wrong wherever there is any D. M3, M4 and M6 are wrong on
every pattern, since every joined pattern has an I. P3 sees only the
three that are wrong everywhere: for the others, the answers to `a`
and `b` are wrong in the same way as the answer to the join, so P3
holds even when the answer is wrong.

## Verification

All four arms print the same output as `find_permutation.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file, the bench program included. The
differential prints `13524 checks, 0 failures` on both. The four arms
and the differential also run clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak.

The frozen legacy backends agree on every arm: `karac run --interp`,
LLJIT, legacy `karac build` and a `KARAC_AUTO_PAR=1` build print the
same output. The differential does not run there: the legacy
interpreter stops at `b.as_str()` ("method 'as_str' not found on type
'String'", as on kata 482), and legacy `karac build` refuses it ("value
'p' moved here, used again here", in the brute force, which reads the
permutation after lending it to `fits`). Legacy is frozen, so this is
noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 20 patterns of 100,000
letters (the problem's most), with D at odds from 0 in 20 to 19 in 20,
once, then solves each 10 times. Every implementation prints `200
solves of 100000 letters: 20000200 numbers, checksum 732810773`, the
Kāra program under `karac __mir-run` included (in 28 s).

Every mirror copies the letters out (Rust `Vec<char>`, Go `[]rune`, a
Python list, a byte copy in C, as the Kāra arm collects its chars into
a `Vec`), fills 1 to n into a fresh array and reverses each run of Ds
with swaps. Spot timings on a shared 4-core container, three runs each
(two for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.08 to 0.10 s |
| Rust (`rustc -O`) | 0.10 to 0.11 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.10 to 0.13 s |
| Go | 0.20 to 0.22 s |
| Python | 2.8 to 3.1 s |
| Kāra (`karac build`) | 0.10 to 0.12 s |
| Kāra (`karac build --mir`) | 0.18 to 0.19 s |

The compiled rows are short enough that start-up and the pattern
building are a real share of them; `bench.sh` with hyperfine on a
quiet machine is the measurement to trust. The legacy `karac build`
builds and runs this program correctly, so `bench.sh` is the
`scripts/new-bench.sh` output unchanged and times that build. The
`--mir` row is the v2 compiled backend, timed for comparison; it is
slower than the legacy build here, by about 0.08 s (where that goes was
not profiled). Both Kāra rows are timed at kara `b0b1557b39`. Under
`karac __mir-llvm-run` the program prints the same line in 1.0 s,
compile included; that JITs the MIR's IR without optimization passes,
so it is not a benchmark.

## Compiler findings

None. Every arm, the differential and the bench program ran first time
on the v2 backends.
