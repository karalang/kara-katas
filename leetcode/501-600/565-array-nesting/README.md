# 565. Array Nesting

You are given an integer array `nums` of length `n` where `nums` is a
permutation of the numbers in the range `[0, n - 1]`. You should build a
set `s[k] = {nums[k], nums[nums[k]], nums[nums[nums[k]]], ... }`
subjected to the following rule: the first element in `s[k]` starts with
the selection of the element `nums[k]` of `index = k`; the next element
in `s[k]` should be `nums[nums[k]]`, and then `nums[nums[nums[k]]]`, and
so on; we stop adding right before a duplicate element occurs in `s[k]`.
Return the longest length of a set `s[k]`.

```
nums = [5,4,0,3,1,6,2]  ->  4    (s[0] = {5, 6, 2, 0})
nums = [0,1,2]          ->  1
```

**Constraints:** `1 <= nums.length <= 10^5`; `0 <= nums[i] <
nums.length`; all the values of `nums` are unique.

## Approaches

Every arm is `fn array_nesting(nums: Vec[i64]) -> i64`. Each `s[k]` is
the cycle of the permutation through `k`, so the answer is the length of
the longest cycle.

| file | mechanism |
|---|---|
| `array_nesting.kara` ★ | each cycle walked once from its first unvisited index, marking a `Vec[bool]` as it goes; the longest walk wins; O(n) |
| `array_nesting_inplace.kara` | the same walk with the marks written into a copy of `nums`: each visited entry overwritten with n, a value no index has, after the next index is read; O(n) |
| `array_nesting_union.kara` | union-find: every `i` joined to `nums[i]`, by size with path halving, and the largest set's size; O(n α(n)) |
| `array_nesting_set.kara` | the ★ arm's walk with the marks in a `Set[i64]`: a walk stops when `insert` reports its index was already there; O(n) expected |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 12 lines: seven permutations at the edges (the
two examples, one element, two swapped, reversed, one cycle through
every index, and three cycles of different lengths), a total and
checksum over 300 random permutations of 1 to 50 elements, and four of
100,000, the problem's most: one cycle, every index fixed, neighbours
swapped in pairs, and random. `array_nesting.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read literally: for every k, a list started at `nums[k]`
and extended by `nums` of its last element until the next would repeat
one already in the list, and the longest list's length. Each arm is held
to the properties below on 1,000 random permutations of 1 to
30 elements: random, made of cycles of 1 to 8 indices laid out in order,
or the identity with up to three swaps, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is at least 1 and at most n |
| P3 | the indices renamed by a random permutation give the same answer |
| P4 | the inverse permutation gives the same answer |
| P5 | a cycle of 1 to 40 new indices added after the others gives the larger of the answer and that cycle's length |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac
__mir-llvm-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: each cycle counted one too long | P1 1000, P2 112, P5 852 |
| M2 | ★: the last cycle's length kept, not the longest | P1 685, P3 265, P5 35 |
| M3 | inplace: a fixed point not counted | P1 150, P2 150, P5 3 |
| M4 | inplace: the walk never leaves its start | P1 850, P5 976 |
| M5 | union: a merged set grows by one, not by the other set's size | P1 252, P3 416 |
| M6 | union: the answer starts at 0, not 1 | P1 150, P2 150, P5 3 |
| M7 | set: the walk steps two at a time | P1 519, P5 439 |
| M8 | set: every index seen so far taken as the cycle's length | P1 888, P5 1000 |
| E1 | ★: the maximum taken the other way round | 0 |
| E2 | inplace: the mark tested with `< n`, not `!= n` | 0 |
| E3 | union: union by size dropped | 0 |
| E4 | set: no skip for a start already seen | 0 |

Renaming the indices keeps the cycles but changes the order they are met
in, so P3 sees the two mutants whose answer depends on that order:
M2 keeps whichever cycle is walked last, and how far M5 undercounts
depends on the order the sets are joined. The inverse keeps every cycle
and its smallest index, so M2 meets the cycles in the same order there,
and P4 sees no mutant. M3 and M6 fail on the same 150 cases, the ones
where every index is fixed: a fixed point not counted leaves the inplace
arm at 0, and the union arm only raises its answer when it joins two
sets. E2 is safe because an entry is an index below n or the mark n;
E3 because union by size only keeps the trees short; E4 because a walk
from an index already seen stops at once with length 0.

## Verification

Every arm prints the same output as `array_nesting.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak. `karac check`
passes on every arm, the differential and the bench program.

The frozen legacy backends agree too: every arm prints the same output
under `karac run --interp`, `karac run` and `karac build`, the last with
`KARAC_AUTO_PAR=1` as well, and the differential prints `20000 checks,
0 failures` under `karac run --interp` and `karac build`. Only the bench
program is refused (see Benchmarks).

## Benchmarks

The bench program uses the ★ arm. It makes 20 permutations of
100,000 once (the problem's most), in turn a random one by Fisher-Yates
and one made of cycles of 1 to 2,000 indices laid out in order. Then
100 times over every permutation is answered. Every implementation
prints `20 permutations of 100000, 100 rounds: total 65147700, checksum
355495009`, the Kāra program under `karac __mir-run` included (92 s).

Each implementation makes fresh marks for every answer: a `Vec[bool]` in
Kāra and Rust, a `[]bool` in Go, a `calloc`'d array in C and a list in
Python. Spot timings on a shared 4-core container, three runs each (two
for Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.68 to 2.11 s |
| Rust (`rustc -O`) | 1.47 to 1.63 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.48 to 1.53 s |
| Go | 1.97 to 2.13 s |
| Python | 20.5 to 21.6 s |
| Kāra (`karac build --mir`) | 2.08 to 2.33 s |

The legacy `karac build` refuses this program, since it moves
`perms[(round * 7 + g) % count]` out of the index where v2 borrows it.
So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`585af34765`. Under `karac __mir-llvm-run` the program prints the same
line in 3.2 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 1.4 times Rust's in these runs. Every
implementation's walk is a chain of dependent loads at scattered
addresses, so the compiled languages land close together and their
timings move with the machine's load: a second set of three runs gave
Rust 1.54 to 1.77 s and Kāra 1.76 to 2.51 s.

## Compiler findings

None new. Nothing was filed from this kata.
