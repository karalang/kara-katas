# 955. Delete Columns to Make Sorted II

You are given an array of `n` strings `strs`, all of the same length. We
may choose any deletion indices, and we delete all the characters in
those indices for each string. Suppose we chose a set of deletion
indices `answer` such that after deletions, the final array has its
elements in lexicographic order (i.e., `strs[0] <= strs[1] <= strs[2] <=
... <= strs[n - 1]`). Return *the minimum possible value of*
`answer.length`.

```
strs = ["ca","bb","ac"]       ->  1
strs = ["xc","yb","za"]       ->  0
strs = ["zyx","wvu","tsr"]    ->  3
```

**Constraints:** `n == strs.length`; `1 <= n <= 100`;
`1 <= strs[i].length <= 100`; `strs[i]` consists of lowercase English
letters.

## Approaches

| file | mechanism |
|---|---|
| `min_deletion_size.kara` ★ | pairs settled: the columns taken left to right, each kept unless it puts a pair of neighbouring strings out of order. A pair is settled once a kept column has the upper letter smaller; until then the kept columns are equal on it, so a column that breaks an unsettled pair must go, and keeping every column that can stay only settles more pairs. O(n m) for n strings of length m |
| `min_deletion_size_kept.kara` | the strings of the kept columns built as they grow: a column is kept when the strings with it added are still in order, each at most the next, as whole strings. O(n m^2) |
| `min_deletion_size_groups.kara` | the strings as runs of neighbours whose kept columns are all equal: a column stays when its letters never fall within a run, and then splits each run wherever its letter rises. O(n m) |
| `min_deletion_size_pending.kara` | the places of the pairs not yet settled kept in a list: a column is deleted when one of them falls, and otherwise kept, the pairs it settles leaving the list with `retain`; once the list is empty nothing more can break. O(n m) |
| `min_deletion_size_ranks.kara` | each string ranked by its kept prefix, equal prefixes sharing a rank: a column stays when the pairs of rank and letter never fall, and the new ranks number those pairs in order. O(n m) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 17 lines: LeetCode's three examples and six
more (one string, a tie the next column puts out of order, two equal strings, a
column deleted in the middle, a tie broken only by the last column, and
an equal pair after a falling one); for 300 random cases of 1 to 8
strings of 1 to 6 letters from `a` to `c`, 1,319 strings in all, the
total of the answers and a checksum; and seven cases of LeetCode's
largest size, 100 strings of 100 letters: random (100), the same sorted
(0) and sorted backwards (100), random from `a` and `b` (100), the same
sorted by their first 9 letters only (11), 100 copies of one string (0),
and one string with its last letter falling down the list (1).
`min_deletion_size.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every set of columns to delete is tried, and the fewest that
leave every string at most every string after it is the answer. It
checks 3,200 random cases, every second one sorted by its strings' first
few letters, which leaves the later columns to decide: 3,000 of 1 to 6
strings of 1 to 6 letters from the first 1 to 3 letters against the
statement, and 200 of up to 100 strings of up to 50 letters from the
first 1 to 26 against the other properties, 20,314 strings in all.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the letters used renamed, in alphabetical order, to as many random letters gives the same answer, since every comparison of two letters comes out the same |
| P3 | a column of one letter put in anywhere never breaks a pair nor settles one, and gives the same answer |
| P4 | one string written twice in a row gives the same answer |
| P5 | every column written twice gives twice the answer: both copies go or both stay |
| P6 | each arm agrees with at least two of the other four |

Large cases have at most 50 letters so that P5 stays within LeetCode's
100.

It prints `3200 cases of 20314 strings: 4852 columns deleted, checksum
610402085, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
(35 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Thirty-five edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: settled pairs checked too | P1 573, P6 659 |
| M2 | ★: a deleted column settles pairs | P1 297, P6 382 |
| M3 | ★: equal letters settle a pair | P1 367, P3 484, P6 376 |
| M4 | kept: a tie counted as out of order | P1 1897, P3 2530, P4 769, P6 1989 |
| M5 | kept: a deleted column's letters kept anyway | P1 399, P3 749, P6 403 |
| M6 | kept: only the first pair compared | P1 738, P4 135, P6 839 |
| M7 | groups: falls checked across the runs' edges | P1 274, P4 160, P6 351 |
| M8 | groups: the last run of each split dropped | P1 294, P3 547, P5 97, P6 298 |
| M9 | groups: a run split one place late | P1 294, P4 142, P6 373 |
| M10 | pending: the list shrinks after a deleted column too | P1 535, P5 1099, P6 632 |
| M11 | pending: the last pair left out | P1 465, P4 141, P6 468 |
| M12 | pending: an empty list counts the remaining columns as deleted | P1 911, P3 857, P4 998, P5 632, P6 998 |
| M13 | ranks: the rank weighed by 16, not 256 | P2 158, P5 10, P6 33 |
| M14 | ranks: the rank alone, without the letter | P1 994, P6 1099 |
| M15 | ranks: the letter subtracted | P1 1235, P6 1327 |

P6 kills all fifteen and P1 fourteen; P4 six (M4, M6, M7, M9, M11,
M12), P3 five (M3, M4, M5, M8, M12), P5 four (M8, M10, M12, M13) and P2
one (M13).

M13 passes P1: the small cases use only `a` to `c`, whose codes differ
by less than 16, so a rank step still outweighs the letter. P2 renames
them across the alphabet, where it does not.

Nineteen other edits were tried and set aside. Fourteen failed exactly
the same checks as a kept one: eight as M1 (★ settling a pair when it
falls, kept putting each new letter first and never growing the kept
strings, groups never splitting a run, pending keeping the pairs that
rise and never shrinking the list, ranks never renumbering and ranking
by the letter alone), three as M4 (★, pending and ranks refusing a
tie), ranks giving every key a new rank, as M3, ranks renumbering after
a deleted column, as M10, and ★ never checking the last pair, as M11.
Five were sound but beyond three an arm: ★ never deleting the first
column and reading the settled flags one place off, kept comparing every
string with the first, groups splitting where the letters agree, and
ranks skipping the first pair.

One was equivalent: groups keeping a run of one string, which has no
pair to break or split.

## Verification

Every arm prints the same output as `min_deletion_size.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the
arms take 0.5 to 0.7 s each and the differential 35 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 200 sets of 100 strings of 100 letters once,
the strings of each set drawn from its first 2 to 4 letters and sorted
by their first 0 to 11 letters, so that the sets keep from none to
about half of their columns. In each of 120 rounds it runs the ★ arm on
every set, each round starting from a different one, and folds the
answers into a checksum. Every implementation prints `120 rounds over
200 sets of 100 strings of 100 letters: 1268280 columns deleted,
checksum 552594758`. Each call reads the letters in place: `bytes()` in
Kāra, `as_bytes()` in Rust, string indexing in Go and Python, and a
`char` pointer per string in C.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.52 to 0.60 s | 0.54 s |
| Rust (`rustc -O`) | 0.62 to 0.75 s | 0.65 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.62 to 0.68 s | 0.65 s |
| Go | 0.69 to 0.81 s | 0.74 s |
| Python | 11.4 s | |
| Kāra (`karac build --mir`) | 0.75 to 0.84 s | 0.80 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
C's.

v2 takes 1.22 times Rust's median time under overflow checks and 1.48
times C's. Under valgrind's cachegrind v2 runs 3.36 billion
instructions and 1.15 billion branches with 50.3 million mispredicted,
Rust with overflow checks 2.64 billion, 0.74 billion and 47.7 million,
and C 1.17 billion, 0.35 billion and 44.9 million. v2 runs the most
instructions and branches; where they come from was not looked into.
