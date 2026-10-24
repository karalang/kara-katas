# 942. DI String Match

A permutation `perm` of `n + 1` integers of all the integers in the
range `[0, n]` can be represented as a string `s` of length `n` where:

- `s[i] == 'I'` if `perm[i] < perm[i + 1]`, and
- `s[i] == 'D'` if `perm[i] > perm[i + 1]`.

Given a string `s`, reconstruct the permutation `perm` and return it. If
there are multiple valid permutations `perm`, return **any of them**.

```
s = "IDID"  ->  [0,4,1,3,2]
s = "III"   ->  [0,1,2,3]
s = "DDI"   ->  [3,2,0,1]
```

**Constraints:** `1 <= s.length <= 10^5`; `s[i]` is either `'I'` or
`'D'`.

## Approaches

| file | mechanism |
|---|---|
| `di_string_match.kara` ★ | the smallest and largest numbers not used yet kept: at an I the smallest goes down, so whatever comes next is larger, and at a D the largest, so whatever comes next is smaller; the one number left goes last. O(n) |
| `di_string_match_runs.kara` | 0 to `n` in order, which fits a string of all I, and each run of D's from place `i` to place `j - 1` turned into a fall by reversing the numbers from place `i` to place `j`; the stretches of different runs do not overlap, and the steps into and out of each still rise. This gives the answer first in dictionary order. O(n) |
| `di_string_match_stack.kara` | the numbers handed out from 0 upward: each place pushed on a stack, and at an I, and at the end, the whole stack popped, each place popped getting the next number, so a run of D's comes off last place first and its numbers fall. O(n) |
| `di_string_match_spread.kara` | a start at the number of D's, then at each I one more than the largest so far and at each D one less than the smallest so far; every I adds a new top and every D a new bottom, so the numbers used are exactly 0 to `n`. O(n) |
| `di_string_match_topo.kara` | each letter an edge from the neighbouring place that must get the smaller number to the one that must get the larger, and the places numbered in a topological order of those edges, taken from a `VecDeque` of places with no edge left into them. O(n) |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms give different answers, all of them right, so every arm prints
the same 13 lines of verdicts rather than its answers, each answer
checked to hold each of 0 to `n` once and to rise at each I and fall at
each D: LeetCode's three examples and five more (one I, one D, `DIDI`,
`IIDD` and `DDDIII`); for 300 random strings of 1 to 100 letters, the
letters and how many answers fit; and four of LeetCode's longest,
100,000 letters: all I, all D, `ID` over and over, and random letters.
`di_string_match.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every permutation of 0 to `n`, kept when each letter is I
exactly where the permutation rises. It checks 3,200 random strings of
I and D with even odds: 3,000 of up to 5 letters, against the statement,
and 200 of up to 2,000 letters, against the other properties; 204,719
letters in all.

| | property |
|---|---|
| P1 | one of the statement's permutations, on the small strings |
| P2 | each of 0 to `n` once |
| P3 | a rise at each I and a fall at each D |
| P4 | the arm's answer for the letters swapped, I for D and D for I, fits them |
| P5 | the arm's answers for the letters reversed and for one more random letter at the end fit those |
| P6 | each arm agrees with at least two of the other four on whether its answer fits |

It prints `3200 strings of 204719 letters, checksum 80564459, 95000
checks over 5 arms: 0 failures` under `karac __mir-run` (30 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last number one past the largest left | P1 3000, P2 3200, P3 1593, P4 3200, P5 3200, P6 3200 |
| M2 | ★: the largest left starting one short | P1 2404, P2 2604, P3 1593, P4 2634, P5 2890, P6 2604 |
| M3 | ★: the largest left never lowered | P1 1350, P2 1550, P3 1234, P4 1570, P5 2089, P6 1550 |
| M4 | runs: the middle pair never swapped | P1 1788, P3 1988, P4 2049, P5 2587, P6 1988 |
| M5 | runs: each reversal one place too long | P1 1034, P3 1234, P4 1226, P5 2014, P6 1234 |
| M6 | runs: a run at the end never reversed | P1 1487, P3 1593, P4 1607, P5 2376, P6 1593 |
| M7 | stack: the bottom place left on the stack | P1 3000, P2 3200, P3 2528, P4 3200, P5 3200, P6 3200 |
| M8 | stack: emptied after an I instead of at one | P1 2434, P3 2634, P4 2604, P5 2909, P6 2634 |
| M9 | stack: a lone place kept on the stack at an I | P1 1880, P3 2080, P4 1980, P5 2416, P6 2080 |
| M10 | spread: the start at the number of I | P1 2498, P2 2691, P4 2691, P5 3200, P6 2691 |
| M11 | spread: each D two below the bottom | P1 2404, P2 2604, P4 2634, P5 2890, P6 2604 |
| M12 | spread: each I the old top | P1 2434, P2 2634, P3 1642, P4 2604, P5 2909, P6 2634 |
| M13 | topo: an I counted into the wrong place | P1 2434, P2 2634, P3 2349, P4 2604, P5 2909, P6 2634 |
| M14 | topo: the right neighbour queued with an edge left | P1 1027, P2 1226, P4 1235, P5 1886, P6 1226 |
| M15 | topo: only the first free place queued | P1 1364, P2 1564, P3 1564, P4 1553, P5 2324, P6 1564 |

P1, P4, P5 and P6 kill all fifteen, P3 twelve and P2 ten.

P2 misses the three runs mistakes and M8 and M9. Runs only swaps
numbers of 0 to `n`, so whatever it reverses wrongly is still a
permutation; and stack, which empties itself at the end whatever else it
does, still pops every place once, handing out 0 to `n` in order. All
five put the numbers in the wrong order, which P3 sees.

P3 misses M10, M11 and M14, which keep every rise and fall and get the
numbers wrong instead. Spread steps up at each I and down at each D
from wherever it starts and by however much it steps, so M10's start at
the number of I and M11's steps of 2 below only move its numbers out of
0 to `n`. M14 queues a place with one edge still into it, and queues it
again when that edge goes, so the place is numbered twice; the second
number, the one it keeps, comes after its other neighbour's, as it
should, and the number the first took is lost, so the numbers no longer
end at `n`.

Twenty-eight other edits were tried and set aside. Twenty failed exactly
the same checks as each other, in seven groups, so none of them was
kept: four that hand out 1 to `n + 1` or every other number (runs, stack
and topo starting at 1, and stack going up by 2); three that read the
letters the wrong way round (★, and stack and topo handing out the
numbers from the top); four that leave places numbered 0 (stack popping
one place at a time and pushing only places at an I or the end, and
topo freeing the left neighbour after an I and counting a D's edge
twice); three that always leave two places at 0 (stack never emptied
at the end, pushing each place after emptying, and wrapping the largest
number round to 0); runs leaving the place after each run out of its
reversal and stack read from the bottom, both of which rise at the last
D of every run, and so fail every string with a D; runs never reversing a
run at the start and stack emptied after the first place, both wrong
only when the string begins with a D; and stack skipping a number after
the first place and spread starting its top one above the start. Six
were sound but beyond three an arm (★ raising the smallest left by 2,
runs never reversing a run of one D and going on scanning inside each
run, spread starting one below the number of D, and topo never freeing
the first place and freeing the right neighbour at a D). One timed out:
runs cutting a run at the end one short, which then never moves past
it. One was judged equivalent and not run: topo taking places from the
back of its queue instead of the front, which gives another topological
order, and any topological order fits.

## Verification

Every arm prints the same output as `di_string_match.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 1.3 to 2.1 s each and the
differential 30 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Legacy refuses all five arms, the differential and the bench program at
the first `*` on an element of a `Vec`'s `.iter()` ("unary '*' requires
'ref T', ..."): on a `Vec[u8]` in ★, spread, the differential and the
bench program, and on a `Vec[i64]` in the harness's `fits` for runs,
stack and topo. That is legacy's older rule, under which the element is
a copy; under v2 it is a reference and the `*` is required. Legacy is
frozen, so none of this is filed.

## Benchmarks

The bench program builds 20 strings of 100,000 letters once, LeetCode's
longest, each of random letters with a chance of an I from 1 in 16 to 15
in 16; in each of 50 rounds it runs the ★ arm on every string, each
round starting from a different one, and folds the first, middle and
last numbers of each answer into a checksum. Every implementation
prints `50 rounds over 20 strings of 100000 letters: checksum
196868268`. C writes each answer into an array of `n + 1` allocated at
once; Kāra, Rust, Go and Python grow theirs one push at a time, and Kāra
copies each string's bytes into a `Vec[u8]` on every call, both as the
★ arm does.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.071 to 0.107 s | 0.077 s |
| Rust (`rustc -O`) | 0.35 to 0.40 s | 0.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.36 to 0.39 s | 0.37 s |
| Go | 1.84 to 2.45 s | 2.18 s |
| Python | 4.97 s | |
| Kāra (`karac build --mir`) | 0.39 to 0.44 s | 0.42 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about 65 times C's.

v2 takes 1.13 times Rust's median time under overflow checks and 5.4
times C's. Under valgrind's cachegrind v2 runs 1.86 billion
instructions and 0.61 billion branches with 28.7 million mispredicted,
Rust with overflow checks 1.28 billion, 0.41 billion and 28.6 million,
and C 1.18 billion and 0.05 billion branches with 6,900 mispredicted.
The letters are random, so a branch on each one is mispredicted about
as often as not where the odds are near even; C's handful of
mispredictions say it chooses between the smallest and the largest
without a branch, and that this choice, with C's single allocation,
accounts for most of the gap is inferred, not profiled. Go's time,
nearly six times Rust's, is inferred to be its slice growing by
`append` and the garbage collector reclaiming 1,000 arrays of 800 KB,
not profiled.
