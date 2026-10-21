# 821. Shortest Distance to a Character

Given a string `s` and a character `c` that occurs in `s`, return an
array `answer` of the same length as `s`, where `answer[i]` is the
distance from index `i` to the closest occurrence of `c` in `s`. The
distance between indices `i` and `j` is `abs(i - j)`.

```
s = "loveleetcode", c = "e"  ->  [3,2,1,0,1,0,0,1,2,2,1,0]
s = "aaab", c = "b"          ->  [3,2,1,0]
```

**Constraints:** `1 <= s.length <= 10^4`, `s` and `c` are lower-case
English letters, and `c` occurs at least once in `s`.

## Approaches

The nearest `c` to an index is the last one at or before it or the first
one at or after it, so no approach has to look further than those two.

| file | mechanism |
|---|---|
| `shortest_to_char.kara` ★ | a sweep from the left keeping the last `c` seen, then a sweep from the right keeping the first, each index keeping the nearer. O(n) |
| `shortest_to_char_positions.kara` | the indices of `c` listed in order, then one walk over `s` with a pointer into the list that stays on the last index at or before the current one; the answer is that index or the next. O(n) |
| `shortest_to_char_bfs.kara` | a breadth-first search from every `c` at once, at distance 0, stepping to the two neighbours of each index reached through a `VecDeque`; the search reaches each index first from its nearest `c`. O(n) |
| `shortest_to_char_iter.kara` | the indices of `c` picked out of an `enumerate` by a `filter`, and each index's answer the `min` over a `map` of its distances to them. O(n k) for k occurrences of `c` |
| `differential.kara` | the four arms against the statement played out index by index, four properties |

Every arm prints the same 12 lines: LeetCode's two examples; six small
cases (one character; `c` first; `c` at both ends; `c` in the middle;
every character `c`; and three `c`s with six letters and then two
between them); three strings of LeetCode's largest length, 10,000, of
random letters looking for `q`, with one `z` at the end and with one `z`
in the middle, each with the sum of its answer and the farthest
distance; and 300 random strings of up to 41 characters of three
letters, with a total and a checksum. `shortest_to_char.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out: for each index, the distance to every index holding `c`, and
the smallest of them. It keeps no sweep, no list of indices and no
queue. Its 1,600 cases come in four kinds of 400: up to 40 characters of
three letters; up to 200 of all 26; a run of up to 300 `a`s with one
`b`; and up to 60 characters about half of which are `c`. Each case has
one `c` put in at a random index, so that `c` occurs at least once. The
farthest index from its `c` in any case is 294 away.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the string reversed gives the answer reversed |
| P3 | 0 at exactly the indices of `c`, and neighbouring answers differ by at most 1 |
| P4 | every letter other than `c` replaced by one other letter gives the same answer |

It prints `1600 cases (the farthest place 294 from its c), 25600 checks
over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the right sweep keeps the farther | P1 1567, P2 1407, P3 1567 |
| M2 | ★: the left sweep starts as if a `c` stood at 0 | P1 1180, P2 1407, P3 1180 |
| M3 | ★: the left sweep one too far | P1 1512, P2 1567, P3 1512 |
| M4 | positions: the next index never tried | P1 995, P2 995, P3 995 |
| M5 | positions: indices counted from 1 | P1 1600, P2 1590, P3 1600 |
| M6 | positions: the distance back not made positive | P1 1555, P2 1567, P3 995 |
| M7 | search: steps right only | P1 1513, P2 1567, P3 995 |
| M8 | search: the queue taken from the back | P1 995, P2 995, P3 995 |
| M9 | search: the last index never reached | P1 1166, P2 1407, P3 967 |
| M10 | iter: the indices of the other letters | P1 1586, P3 1586 |
| M11 | iter: the farthest `c` kept | P1 1116, P3 1116 |
| M12 | iter: indices counted from 1 | P1 1600, P2 1590, P3 1600 |

P1 kills all twelve. P2 sees every edit that breaks the left-right
symmetry, and not M10 and M11, which are as wrong reversed as forwards.
P3 sees all twelve too, as each one either loses a 0 at a `c` or puts a
jump of more than one between neighbours. P4 sees none: no edit reads
the letters other than `c`, and P4 holds the arms to the statement's
claim that only the places of `c` matter. M5 and M12, the same mistake
in two arms, fail on the same numbers of cases.

## Verification

Every arm prints the same output as `shortest_to_char.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`385539fdac`, with the runtime archives built from that tree; the
release build that runs `check` and `__mir-run` is at `d5daf8420c`, two
compiler changes ahead of it (`b2ead3a82f`, `8dd3fa3bd1`).

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy compiler runs none of the arms to the end. Its
interpreter prints the first line of each and then finds no `as_str` on
a `String`, which the harness calls. Its JIT and `karac build` find no
`len` on the `Str` parameter for the ★ and search arms, the differential
and the bench program, and panic in codegen on the `for` loops of the
positions and iterator arms. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
strings once, each of 10,000 random letters, LeetCode's largest, with a
letter to look for. Each of 50,000 rounds answers the next string
afresh: the characters collected into an array, two sweeps over it and
an array of 10,000 answers, which the round adds up. Every
implementation prints `50000 rounds of 64 strings: total 6331640506,
checksum 859076650`, the Kāra program under `karac __mir-run` included,
in 1,668 s with the interpreter's step limit raised by
`KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, six runs of each compiled
program and nine of v2's, five of them interleaved, and one of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.94 to 1.05 s |
| Rust (`rustc -O`) | 1.22 to 1.36 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.40 to 1.67 s |
| Go | 3.39 to 3.51 s |
| Python | 79.7 s |
| Kāra (`karac build --mir`) | 2.91 to 3.04 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 3.00 s, against C's
0.96, Rust's 1.29 (1.47 under overflow checks) and Go's 3.48, so about
three times C's time and twice and a third Rust's. Under valgrind's
cachegrind v2 runs 33.7 billion instructions, about 67 for each
character it answers, against C's 9.3 billion (19) and Rust's 20.0
billion (40), and 10.0 billion branches against C's 1.1 billion and
Rust's 6.1 billion, almost none of them mispredicted. Callgrind cannot
say where, since v2 inlines the whole function into `main`; the one
other entry is `memset`, 12% of v2's instructions, which zeroes the new
answer array. Built for `x86-64-v3`, the target `karac build` uses, C
takes 0.94 to 1.03 s and Rust with overflow checks 1.39 to 1.65 s,
against v2's 2.90 to 3.08 s in the same five interleaved runs. Python
takes 80 s, about 80 times C's time. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
