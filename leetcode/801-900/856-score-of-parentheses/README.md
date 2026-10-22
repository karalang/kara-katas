# 856. Score of Parentheses

Given a balanced parentheses string `s`, return its score: `()` scores
1; `AB` scores `A + B`, for balanced strings `A` and `B`; and `(A)`
scores `2 * A`.

```
s = "()"        ->  1
s = "(())"      ->  2
s = "()()"      ->  2
s = "(()(()))"  ->  6
```

**Constraints:** `2 <= s.length <= 50`, `s` holds only `(` and `)`, and
`s` is balanced.

## Approaches

| file | mechanism |
|---|---|
| `score_of_parentheses.kara` ★ | a stack of the scores of the groups still open, the whole string at its bottom: a `(` opens a group with a score of 0, and a `)` closes the top group, worth 1 if nothing closed inside it and twice its sum otherwise, and adds that to the group around it. O(n) time and space |
| `score_of_parentheses_depth.kara` | each `()` is worth two to its depth: unfolding the rules, the doubling of every group around a `()` applies to it alone, so a `()` inside `d` groups is worth `2^d`. One pass keeps the depth and adds `1 << d` at every `)` that follows a `(`. O(n) time, O(1) space |
| `score_of_parentheses_split.kara` | the rules as a recursion on a range: walk it keeping the balance, and every time the balance comes back to 0 one top-level group `(A)` has ended, worth 1 if `A` is empty and twice the score of `A` otherwise. O(n^2) time in the worst case, a string nested all the way down |
| `score_of_parentheses_tree.kara` | a recursive-descent parser reads the string into a tree of `Group`s, each holding the groups directly inside it, and the tree is scored as the rules say. O(n) time and space |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's four examples; seven more
(two nestings of three pairs, a group beside a pair, a mixed string, 25
pairs nested all the way down, which scores 2^24, 25 pairs side by side,
and 24 nested pairs beside one more); every balanced string of 1 to 8
pairs, 2,055 of them, with the sum of their scores; and 300 random
strings of up to 25 pairs, with the sum of their scores and a checksum.
`score_of_parentheses.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally, as rewriting: `()` becomes a score of 1, `(A)` with a score
`A` becomes `2A`, and two scores side by side become their sum, the
first rule that applies at the leftmost place each time, until one score
is left. Its 1,600 random strings come in four kinds of 400: 1 to 12
pairs opening a group one time in two, three times in four (deep
strings), and one time in four (shallow ones), and 1 to 4 pairs. Their
scores sum to 53,114.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the string followed by another random string scores the sum of the two |
| P3 | the string in a pair of parentheses scores twice as much |
| P4 | the string read backwards with each parenthesis turned around scores the same |
| P5 | a string of `p` pairs scores at least `p` and at most `2^(p - 1)` |
| P6 | a `()` put in at a random place inside `d` groups adds `2^d`, or `2^(d - 1)` when it goes into an empty group, whose 1 it turns into a 2 |

It prints `1600 cases, scores sum to 53114, 38400 checks over 4 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

P6 first said that the `()` always adds `2^d`, and all four arms failed
it in 422 cases each: put into an empty group, the new `()` does not
stand beside anything, it turns the group's score of 1 into 2.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group worth its sum, not twice it | P1 1168, P3 1600, P5 1168, P6 959 |
| M2 | ★: an empty group worth 2 | P1 1600, P5 888, P6 1600 |
| M3 | ★: a closed group added to the bottom of the stack | P1 824, P3 1379, P6 725 |
| M4 | depth: a pair worth two to one more than its depth | P1 1600, P5 888, P6 1600 |
| M5 | depth: a pair found by a `)` before the `)` | P1 1600, P3 1600, P5 1140, P6 1178 |
| M6 | depth: a pair worth one more than its depth | P1 725, P3 1168, P6 476 |
| M7 | split: an empty group told by the start of the range | P1 888, P2 853, P4 664, P5 603, P6 1137 |
| M8 | split: a group's inside taken with its `(` | P1 1168, P3 1069, P5 1168, P6 959 |
| M9 | split: the next group started at the last one's `)` | P1 1138, P2 1600, P4 683, P5 1031, P6 1396 |
| M10 | tree: a group with nothing inside worth 2 | P1 1600, P5 888, P6 1600 |
| M11 | tree: the `)` that closes a group not stepped over | P1 1138, P2 1600, P4 683, P5 1031, P6 1396 |
| M12 | tree: only the first group inside a group scored | P1 559, P3 901, P4 336, P5 362, P6 598 |

P1 kills all twelve. M2, M4 and M10 are one mistake in three arms, every
`()` worth twice as much, and fail the same cases; P2, P3 and P4 cannot
see it, since a score doubled everywhere still adds up, doubles and
reads backwards the same, and P5 and P6 can. M9 and M11 both count only
the first top-level group, the split arm because its balance never comes
back to 0 once it starts a group at a `)`, the tree arm because its
parser stops at the `)` it did not step over; P2 sees them on every
case, since the string after the join is always a second top-level
group. The edit first made as M8, a group's inside taken with its `)`,
was equivalent: the extra `)` takes the balance below 0 only after every
group inside has closed, so it changes nothing, and it was replaced.

## Verification

Every arm prints the same output as `score_of_parentheses.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `8439d277a6`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.3 to 0.4 s
and the differential 1.8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the ★, depth and split arms through
`karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build with the same
output. `karac run --interp` prints every line of every arm the same but
the last, `300 random strings of up to 25 pairs: scores sum to 7187,
checksum 283942615` where the others print 44250 and 447685840: the
harness passes `mut seed` to `random_string` and calls `next_random(mut
seed)` for the number of pairs in the same argument list, which v2's
two-phase borrows evaluate in order, as Python does, and the legacy
interpreter evidently does not, as in katas 852 and 854 (not traced).
The tree arm's `karac run` and `karac build` executables stop with a
segmentation fault, most likely in its `Vec[Group]` inside `Group` (not
traced). `karac run --interp` runs the differential to `0 failures`, but
`karac build` stops at its `rev()` ("not yet supported under `karac
build`"). Legacy refuses the bench program as moving a string out of an
index, which v2's borrowing parameters do not do. Legacy is frozen, so
these are noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
strings once, each of LeetCode's longest, 25 pairs: string `g` opens a
group, while any are left, `1 + g % 3` times in 4, from shallow strings
to deep ones. Each of 4,000,000 rounds scores the next string. The stack
grows on the heap in every language, the C twin's with `malloc` and
`realloc`. Every implementation prints `4000000 rounds of 64 strings:
scores sum to 1098858312500, checksum 107296841`, the Kāra program under
`karac __mir-run` included, in 421 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.39 to 0.56 s |
| Rust (`rustc -O`) | 0.59 to 0.82 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.63 to 0.91 s |
| Go | 0.91 to 1.12 s |
| Python | 13.5 to 17.2 s |
| Kāra (`karac build --mir`) | 0.78 to 0.96 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 0.83 s, against Rust's
0.68 (0.66 under overflow checks), C's 0.40 and Go's 0.96: 1.26 times
Rust's time under overflow checks, 2.08 times C's and 0.86 times Go's.
Under valgrind's cachegrind Rust runs 7.75 billion instructions and 1.58
billion branches, with 107 million mispredicted; v2 runs 9.69 billion,
2.34 billion and 132 million, and C 4.35 billion, 0.78 billion and 91
million. C reads its string a byte at a time, where Rust and v2 decode
each `char` from UTF-8 and check the stack's bounds, which most likely
accounts for most of their extra branches (not traced). Built for
`x86-64-v3`, the target `karac build` uses, C takes 0.37 to 0.43 s and
Rust with overflow checks 0.63 to 0.79 s, against v2's 0.82 to 0.96 s in
the same five interleaved runs. Python takes 13.5 s, about 34 times C's
time. The comparison with C and Rust waits until after M4.
