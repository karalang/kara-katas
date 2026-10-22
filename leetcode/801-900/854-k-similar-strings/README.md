# 854. K-Similar Strings

Strings `s1` and `s2` are `k`-similar, for a nonnegative integer `k`, if
`s1` can be turned into `s2` by swapping the positions of two letters in
`s1` exactly `k` times. Given two anagrams `s1` and `s2`, return the
smallest `k` for which they are `k`-similar.

```
s1 = "ab",  s2 = "ba"   ->  1
s1 = "abc", s2 = "bca"  ->  2
```

**Constraints:** `1 <= s1.length <= 20`, `s2.length == s1.length`, both
strings hold only letters from `{'a', 'b', 'c', 'd', 'e', 'f'}`, and
`s2` is an anagram of `s1`.

## Approaches

| file | mechanism |
|---|---|
| `k_similarity.kara` ★ | breadth-first search over swaps that fix a letter: some shortest sequence of swaps fixes the first misplaced position first, with a swap that brings in the wanted letter from a position where it is itself misplaced, since swapping in a letter that was already right only moves the problem. So from each string only those swaps are tried, and a breadth-first search over the strings they reach, with a set of the strings seen, finds the fewest swaps |
| `k_similarity_bound.kara` | the same swaps explored depth first, each undone after its branch, keeping the best count found: a branch is given up once its swaps so far plus `(m + 1) / 2`, a lower bound for `m` misplaced positions since a swap fixes at most two, reach the best |
| `k_similarity_cycles.kara` | the most cycles in the misplacement graph: an edge from letter `x` to letter `y` for every position that holds `x` and wants `y`. Every letter has as many edges out as in, so the edges split into cycles, and a cycle of `k` edges takes `k - 1` swaps. The answer is the misplaced positions less the most cycles; with six letters the graph is tiny, so every simple cycle through the first edge is tried and the best split of each remaining set of edge counts is remembered in a map |
| `k_similarity_deepen.kara` | iterative deepening: can the strings be matched in 0 swaps, then 1, then 2, each time by a depth-first search over the ★ arm's swaps that never goes deeper than the limit and needs no record of the strings it has seen. A branch with `m` positions misplaced is cut when `(m + 1) / 2` swaps would overrun the limit |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples; nine more
(one letter, equal strings, a rotation of six letters, which takes five
swaps, two halves exchanged, an alternation, a pair whose four misplaced
letters are fixed by two swaps, a pair of 15 letters, and two pairs of
LeetCode's longest strings, 20 letters, that take 10 and 16 swaps); 12
random pairs of 20 letters from all six, with the sum of their swaps;
and 300 random pairs of up to 12 letters from up to six, with the sum of
their swaps and a checksum. `k_similarity.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: a breadth-first search over every swap of two positions from
every string reached, until `s2` is. Its 1,600 cases of 1 to 7 letters
come in four kinds of 400: from two letters, from three, from all six,
each with a random rearrangement as `s2`, and from all six with a few
random swaps, so that `s2` is close to `s1`. Their swaps sum to 1,554.
The statement's search is too slow for longer strings, so every fourth
case also draws a pair of 8 to 14 letters from all six, 400 in all, and
holds the arms there to each other.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | `s1` and `s2` exchanged give the same answer |
| P3 | every letter renamed by one permutation of `a..f` gives the same answer |
| P4 | both strings' positions moved by one permutation give the same answer |
| P5 | with `m` positions misplaced, the answer is at least `(m + 1) / 2` and at most `m - 1` (0 when `m` is 0) |
| P6 | on the long pair, at least two of the other three arms give the arm's answer |

It prints `1600 cases and 400 long pairs, swaps sum to 1554, 38400
checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

P6 was added after a first run of the mutants below against P1 to P5
left three alive: two in the cycles arm, which only go wrong on strings
longer than the statement's search can check, and one in the ★ arm,
which searched only the first eight strings of each level. That last one
hangs on a long pair that the cut search cannot finish, so it was
replaced by M3.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count starting at one | P1 1600, P5 1324, P6 1600 |
| M2 | ★: only the first new string from each string kept | P1 38, P2 64, P4 56, P6 191 |
| M3 | ★: the search aimed at the string it starts from | P1 988, P5 988, P6 900 |
| M4 | bound: the bound one too high for an even count | P1 38, P2 64, P4 56, P6 151 |
| M5 | bound: a swap not counted | P1 988, P5 988, P6 900 |
| M6 | bound: a swap not undone | P1 38, P2 64, P4 56, P6 191 |
| M7 | cycles: a cycle's edges not given back | P6 33 |
| M8 | cycles: the memo keyed on the first edge | P6 27 |
| M9 | cycles: the letter f never walked to | P1 43, P2 77, P3 87, P5 35, P6 161 |
| M10 | deepen: the limit starting at one | P1 612, P5 612, P6 700 |
| M11 | deepen: a branch cut when it has just enough swaps left | P1 988, P5 712, P6 900 |
| M12 | deepen: a swap counted twice | P1 411, P5 222, P6 397 |

P6 kills all twelve and is the only property that kills M7 and M8: up to
7 letters, the cycles arm's split never needs the edges a cycle gave
back, or a memo entry told apart by more than its first edge (most
likely, not traced). M3 and M5 both answer 0, and fail the 988 cases
whose answer is not 0. M2, M4 and M6 fail the same cases of P1 to P4,
most likely by one swap too many on the same strings (not traced). P3
kills only M9, the one edit that treats one letter differently from the
others.

## Verification

Every arm prints the same output as `k_similarity.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `8439d277a6`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.2 to 7.5 s
and the differential 4.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run all four arms through `karac run`, `karac
build` and a `KARAC_AUTO_PAR=1` build with the same output, and build
the differential, which prints `0 failures`. `karac run --interp` prints
every line the same but the last, `300 random pairs: swaps sum to 529,
checksum 402366122` where the others print 569 and 1370533: the harness
passes `mut seed` to `random_pair` and calls `next_random(mut seed)` for
the number of letters in the same argument list, which v2's two-phase
borrows evaluate in order, as Python does, and the legacy interpreter
evidently does not, as in kata 852 (not traced). It takes 93 s on the
iterative-deepening arm and does not finish the differential in 60 s.
Legacy refuses the bench program as moving a string out of an index,
which v2's borrowing parameters do not do. Legacy is frozen, so these
are noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
pairs once, each of LeetCode's longest strings, 20 letters: pair `g`
draws its first string from the first `2 + g % 5` letters of `a..f`, and
its second is a random rearrangement of the first. Each of 6,400 rounds
asks the next pair. The C twin keeps the strings seen in an
open-addressing hash set of its own, and Rust and Go use their standard
sets. Every implementation prints `6400 rounds of 64 pairs: swaps sum to
47500, checksum 448183552`, the Kāra program under `karac __mir-run`
included, in 118 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.78 to 0.89 s |
| Rust (`rustc -O`) | 1.47 to 1.69 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.37 to 1.58 s |
| Go | 1.59 to 2.15 s |
| Python | 7.1 to 7.5 s |
| Kāra (`karac build --mir`) | 1.54 to 2.02 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.73 s, against Rust's
1.59 (1.49 under overflow checks), C's 0.83 and Go's 1.74: 1.16 times
Rust's time under overflow checks, 2.08 times C's and 0.99 times Go's.
Under valgrind's cachegrind Rust runs 13.64 billion instructions and
1.91 billion branches, with 52 million mispredicted; v2 runs 14.41
billion, 2.35 billion and 62 million, and C 3.48 billion, 0.52 billion
and 35 million. C runs a quarter of Rust's instructions most likely
because its hash and its strings are its own, a short FNV hash over
bytes kept in one array, where Rust and v2 hash each string with SipHash
and allocate it (not traced). Built for `x86-64-v3`, the target `karac
build` uses, C takes 0.78 to 0.85 s and Rust with overflow checks 1.40
to 1.63 s, against v2's 1.66 to 1.72 s in the same five interleaved
runs. Python takes 7.4 s, about 9 times C's time. The comparison with C
and Rust waits until after M4.
