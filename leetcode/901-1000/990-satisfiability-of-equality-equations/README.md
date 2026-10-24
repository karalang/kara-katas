# 990. Satisfiability of Equality Equations

You are given an array of strings `equations` that represent
relationships between variables where each string `equations[i]` is of
length `4` and takes one of two different forms: `"xi==yi"` or
`"xi!=yi"`. Here, `xi` and `yi` are lowercase letters (not necessarily
different) that represent one-letter variable names.

Return `true` *if it is possible to assign integers to variable names
so as to satisfy all the given equations, or* `false` *otherwise*.

```
equations = ["a==b","b!=a"]  ->  false
equations = ["b==a","a==b"]  ->  true
```

**Constraints:** `1 <= equations.length <= 500`;
`equations[i].length == 4`; `equations[i][0]` is a lowercase letter;
`equations[i][1]` is either `'='` or `'!'`; `equations[i][2]` is `'='`;
`equations[i][3]` is a lowercase letter.

## Approaches

The letters that must be equal fall into classes, the connected
components of the graph whose edges are the `==` equations; the
equations can all hold exactly when no `!=` names two letters of one
class. Every arm finds the classes first and reads the `!=` after,
because `a!=c` is only wrong once both `a==b` and `b==c` are in.

| file | mechanism |
|---|---|
| `equations_possible.kara` ★ | union-find: each `==` joins its two letters' sets in a union-find over the 26 letters, with path halving on every find; then each `!=` asks whether its letters share a root. O(n α(26)) |
| `equations_possible_bfs.kara` | breadth-first search: the `==` equations are kept as adjacency lists, and a breadth-first search from each letter not yet reached numbers its component. O(n + 26) |
| `equations_possible_dfs.kara` | colouring by depth-first search: the same graph as a 26 by 26 table, coloured by a recursive search that passes each new colour to every letter equal to the one it starts from. O(n + 26²) |
| `equations_possible_closure.kara` | transitive closure: a 26 by 26 table holds every letter equal to itself and each `==` both ways, and Warshall's algorithm closes it under transitivity. O(n + 26³) |
| `equations_possible_relabel.kara` | relabelling: every letter starts with its own label, and each `==` gives every letter carrying the left letter's label the right letter's. O(26 n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines. The first ten are LeetCode's two
examples and eight more: equality carried through a third letter, and
broken by a `!=` through one; letters equal to themselves; `a!=a`
alone, and `a==a` alone; a `!=` that two equalities bridge; three
letters pairwise unequal, which is fine, since `!=` does not carry over
like `==`; and a `!=` read before the equalities that break it. Then
two sets of LeetCode's largest size, 500 equations: a chain from `a`
to `z` closed by `a!=z`, and the even letters made equal with each
unequal to the next letter, which is satisfiable. Then totals over
random sets: 300 of up to 5 equations over 3 letters with a quarter of
them `!=`, 3,000 of up to 50 and 300 of up to 500 over 26 letters with
one in 16 `!=`, and three of 500 with none. `equations_possible.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: it tries every way to give each letter an integer and asks
whether one makes every equation true. With L letters at most L values
need telling apart, so the integers 0 to L - 1 are enough, L^L ways in
all. It checks 3,200 random sets: 3,000 of up to 8 equations over 4
letters, 5 in 16 of them `!=`, against the statement, and 200 of up to
100 over 26 letters, alternately 1 in 16 and 12 in 16 `!=`, against the
other properties.

| | property |
|---|---|
| P1 | the statement's answer, on the first 3,000 sets |
| P2 | the equations read last to first give the same answer |
| P3 | every equation's sides swapped, and the letters renamed by a random permutation of all 26, give the same answer |
| P4 | one of the equations written a second time gives the same answer |
| P5 | one more random equation cannot make an impossible set possible |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 sets of 23750 equations: 1427 satisfiable, checksum
268887751, 95000 checks over 5 arms: 0 failures` under `karac
__mir-run` (20.8 s) and `karac __mir-llvm-run`, and the same
under `karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-one edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run`; fifteen are kept, three to each
arm, all fifteen are killed, and each fails the same checks under both.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the `!=` pass reads parents, not roots | P1 132, P2 189, P3 253, P4 48, P5 21, P6 152 |
| M2 | ★: the left letter joined, not its root | P1 83, P2 101, P3 168, P4 21, P5 14, P6 105 |
| M3 | ★: every equation joins | P1 565, P6 592 |
| M4 | bfs: each edge one way | P1 333, P3 521, P5 3, P6 353 |
| M5 | bfs: a reached letter numbered by itself | P1 712, P6 791 |
| M6 | bfs: a reached letter never queued | P1 207, P3 187, P5 17, P6 260 |
| M7 | dfs: a colour passed only to later letters | P1 114, P3 160, P5 10, P6 146 |
| M8 | dfs: a colour passed to the first equal letter only | P1 121, P3 174, P5 10, P6 145 |
| M9 | dfs: a colour never passed to z | P3 61, P6 3 |
| M10 | closure: the middle letter in the middle loop | P1 7, P3 22, P6 10 |
| M11 | closure: no letter equal to itself | P1 160, P6 164 |
| M12 | closure: each `==` one way | P1 290, P6 309 |
| M13 | relabel: only the left letter relabelled | P1 176, P2 252, P3 293, P4 44, P5 30, P6 220 |
| M14 | relabel: the right letter's index as the label | P1 82, P2 169, P3 172, P4 4, P6 100 |
| M15 | relabel: only the first match relabelled | P1 166, P2 255, P3 377, P4 49, P5 37, P6 205 |

P6 kills all fifteen, P1 fourteen, P3 eleven, P5 eight, and P2 and P4
five each. The graph arms build the same graph whatever order the
equations come in and however often one repeats, so P2 and P4 see only
the mutants whose answer depends on the order of the joins: M1 and M2
in the union-find and M13 to M15 in the relabelling. M3, M5, M11 and
M12 compute a fixed rule of their own that renaming, swapping and
adding cannot shake: M3 fails every set with a `!=` in it, M5 only a
set with some `x!=x`, M11 an `x!=x` whose letter is in no `==`, and
M12, with each `==` one way, asks whether one letter can reach the
other, which swapping every equation's sides, `!=` included, leaves as
it was. M9 goes wrong only at `z`, which the 4-letter sets never use,
so P1 cannot see it; P3's renaming moves letters onto `z`, and kills
it. M10 is Warshall's algorithm with its loops in the wrong order, the
classic slip: it finds the chains it meets in the right order and
misses the rest, 7 of the 3,000 small sets.

Sixteen other edits were tried and set aside. Seven failed exactly the
same checks as a kept one, all in dfs: one colour for every letter and
the table filled from the `!=`, as M3; each `==` one way in the table,
as M4; the `!=` comparing the letters instead of their colours, every
letter starting a colour of its own whether painted or not, and a
colour passed only to earlier letters, as M5, since the search goes
through the letters in order and so passes it to none; a colour passed
one step, as M6. Seven were sound but beyond three an arm: ★'s find
giving back the letter's parent; bfs numbering every start 0 and
searching from `a` alone; closure never taking `z` as the middle letter
and skipping the closure altogether; relabel taking the left letter's
index for its label and never relabelling `z`. Two survived and are
equivalent: ★ joining a root to the right letter itself rather than to
that letter's root, which joins the same two sets, and dfs reading its
table by column, which is symmetric. None crashed.

## Verification

Every arm prints the same output as `equations_possible.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `395f71ae05`, the runtime
archives rebuilt at `d867340a02`, whose runtime sources are the same.
Under `karac __mir-run` the arms take 1.6 s (★) to 6.1 s (closure,
which runs Warshall's 26³ loop for every set), and the differential
20.8 s, most of it in the statement's search over assignments.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench runs the ★ arm in all five languages. The program draws 20
random sets of LeetCode's largest size, 500 equations over the 26
letters, once: ten with no `!=` and ten with one in 256, two of which
are satisfiable. In each of 6,000 rounds it runs the arm on every set,
each round starting from a different one, and folds every answer into a
checksum. Every implementation prints `6000 rounds over 20 sets of 500
equations: 72000 satisfiable, checksum 346298436`. A satisfiable set
costs two passes over its 500 equations; an unsatisfiable one stops at
its first broken `!=`. Kāra, Rust, Go and Python keep each equation as
a string; C keeps them as 4-character arrays.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `395f71ae05`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.271 to 0.334 s | 0.285 s |
| Rust (`rustc -O`) | 0.354 to 0.422 s | 0.384 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.360 to 0.392 s | 0.387 s |
| Go | 0.306 to 0.355 s | 0.324 s |
| Python | 15.5 s | |
| Kāra (`karac build --mir`) | 0.407 to 0.494 s | 0.438 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 35 times
Kāra's.

v2 took 1.13 times Rust's median time under overflow checks and 1.54
times C's. Under valgrind's cachegrind v2 ran 4,086 million
instructions and 1,228 million branches with 10.8 million
mispredicted, Rust with overflow checks 3,281 million, 949 million and
10.2 million, and C 2,533 million, 437 million and 10.2 million. The
three mispredict alike, which fits the misses being the data-dependent
ones: where each find stops, and which way each equation goes. The
branches C does not make are the bounds checks on every `parent` and
byte read, which Rust and Kāra both keep, and Kāra makes another 280
million beyond Rust's (inferred, not traced).
