# 967. Numbers With Same Consecutive Differences

Given two integers `n` and `k`, return an array of all the integers of
length `n` where the difference between every two consecutive digits is
`k`. You may return the answer in any order. Note that the integers
should not have leading zeros: integers such as `02` and `043` are not
allowed.

```
n = 3, k = 7  ->  [181,292,707,818,929]
n = 2, k = 1  ->  [10,12,21,23,32,34,43,45,54,56,65,67,76,78,87,89,98]
```

**Constraints:** `2 <= n <= 9`; `0 <= k <= 9`.

## Approaches

| file | mechanism |
|---|---|
| `nums_same_consec_diff.kara` ★ | level by level: the numbers of one digit are 1 to 9, and each number of the next length is one of these with a digit appended, its last digit plus or minus k where that is a digit (once when k is 0). The whole level grows n - 1 times. O(9 · 2^(n-1)) numbers at most |
| `nums_same_consec_diff_dfs.kara` | depth first: each number built digit by digit from its first, recursing on every digit 0 to 9 that lies k from the last one, and collected when it has n digits |
| `nums_same_consec_diff_stack.kara` | the depth-first search without recursion: a stack of numbers with how many digits each still needs. The next digits are gathered in a `Set`, so when k is 0 the one next digit is pushed once |
| `nums_same_consec_diff_signs.kara` | sign patterns: every such number is a first digit and a choice, at each of the n - 1 steps, of going up or down by k, so n - 1 bits. Every first digit is tried with every pattern, the walks that stay within 0 to 9 are kept, and when k is 0, where up and down are the same step, only the pattern of all ups. O(9 · 2^(n-1) · n) |
| `nums_same_consec_diff_back.kara` | from the last digit: start from every last digit 0 to 9 and put digits in front, each the front digit plus or minus k, the place value growing tenfold each time; a number is kept only when its first digit, put in last, is not 0 |
| `differential.kara` | the five arms against the statement read literally, six properties |

The arms return their numbers in different orders, so the harness sorts
them. Every arm prints the same 17 lines: LeetCode's two examples and six
more (n = 2 with k = 0, where each digit repeats, and with k = 9, where
only 90 is left; n = 3 with k = 0 and k = 5, where 505 starts from a 5
going down to 0; n = 4 with k = 8, which leaves 1919, 8080 and 9191; and
n = 2 with k = 5); then for every n from 2 to 9, how many numbers there
are for each k from 0 to 9 and a checksum of the sorted lists; and the
total, 6,109 numbers summing to 1,476,349,311,554. That covers every input
LeetCode allows. `nums_same_consec_diff.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every number of n digits, its digits tested in turn. LeetCode
allows only 80 inputs, so the 3,200 cases are random draws of them:
3,000 with n of 2 or 3 against the statement and 200 with n from 4 to 9
against the other properties, k from 0 to 9 throughout; 51,166 numbers
in all. Every arm's answer is sorted before it is compared.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | strictly increasing once sorted, so no number twice, and as many numbers as there are walks of n - 1 steps of k from a first digit 1 to 9, counted by the digit they end on |
| P3 | every number has n digits, each next one k from the last |
| P4 | the numbers of n digits are those of n - 1 digits, the arm asked for them, with a digit k from their last appended |
| P5 | replacing every digit d by 9 - d maps the numbers starting with 1 to 8 onto themselves, and reading the digits backwards maps the numbers not ending in 0 onto themselves |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 cases: 51166 numbers, checksum 659619055, 95000 checks
over 5 arms: 0 failures` under `karac __mir-run` (13 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Twenty-seven edits to the differential, each run under `karac
__mir-run` and `karac __mir-llvm-run` with the same results; fifteen are
kept, three to each arm, and all fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the same digit appended twice when k is 0 | P1 309, P2 334, P4 334, P6 334 |
| M2 | ★: 9 never reached going up | P1 2858, P2 3058, P4 2805, P5 2564, P6 3058 |
| M3 | ★: a leading 0 allowed | P1 3000, P2 3200, P3 3200, P5 689, P6 3200 |
| M4 | dfs: one digit short | P1 3000, P2 1898, P3 3200, P4 1510, P6 3200 |
| M5 | dfs: no number starting with 9 | P1 3000, P2 3200, P5 1938, P6 3200 |
| M6 | dfs: only steps up | P1 2691, P2 2866, P4 2588, P5 1844, P6 2866 |
| M7 | stack: 0 never a later digit | P1 2691, P2 2866, P4 2047, P5 2564, P6 2866 |
| M8 | stack: no number starting with 1 | P1 2714, P2 2898, P5 2898, P6 2898 |
| M9 | stack: steps up one too far | P1 2858, P2 3058, P3 2709, P4 3010, P5 2870, P6 3058 |
| M10 | signs: the last step never taken | P1 3000, P2 2866, P3 3200, P4 1510, P6 3200 |
| M11 | signs: a walk off the edge cut short and kept | P1 2691, P2 2866, P3 2866, P4 2866, P5 699, P6 2866 |
| M12 | signs: the first digit left out of the number | P1 3000, P2 1310, P3 3200, P4 1510, P5 699, P6 3200 |
| M13 | back: no number ending in 0 | P1 1953, P2 2091, P4 2866, P5 1938, P6 2091 |
| M14 | back: every digit a place too high | P1 3000, P3 3200, P4 3051, P5 1535, P6 3200 |
| M15 | back: the front digit never moved on | P1 2691, P2 699, P3 2866, P4 2866, P5 2564, P6 2866 |

P1 and P6 kill all fifteen, P2 fourteen (all but M14, which finds the
right number of numbers, each ten times too big), P4 twelve (all but M3,
M5 and M8) and P5 twelve (all but M1, M4 and M10), and P3 eight (M3, M4,
M9 to M12, M14, M15). P4 misses the edits that only change which first
digits an arm starts from, since the arm asked for n - 1 digits starts
from the same wrong ones; P5 misses the duplicates and the numbers one
digit short, which its maps carry over unchanged.

Twelve other edits were tried and set aside. Eight failed exactly the
same checks as a kept one: dfs never taking 0 as a later digit, as M7;
stack taking only steps up, as M6, and never reaching 9, as M2; signs
trying every pattern when k is 0, as M1, dropping a walk that reaches 9,
as M2, and stepping only up, as M6; and back keeping a leading 0, as M3,
and putting the same digit in front twice when k is 0, as M1. Two were
sound but beyond three an arm: ★ one digit short and never reaching 0
going down. Two crashed and were not counted: stack starting every
number one digit short, which P4 asks for a single digit, so every
number needs -1 more digits, never reaches 0 and grows until the
multiplication overflows; and signs with half the patterns, whose
`1 << (n - 2)` shifts by -1 when P4 asks for a single digit, an overflow
the checked shift reports.

## Verification

Every arm prints the same output as `nums_same_consec_diff.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `e04ae2b46b`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 0.16 s (★) to 0.26 s (back) and the differential 13 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program runs the ★ arm on all 80 inputs LeetCode allows, every
n from 2 to 9 with every k from 0 to 9, in each of 2,000 rounds, and
folds every number into a checksum in the order the arm returns them.
Every implementation prints `2000 rounds over n from 2 to 9 and k from
0 to 9: 12218000 numbers, checksum 492617125`. Every call grows its
levels anew: a `Vec` in Kāra and Rust, a slice in Go, a list in Python,
and two `malloc`ed arrays of the largest level's size in C.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python, with karac at `e04ae2b46b`:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.096 to 0.136 s | 0.102 s |
| Rust (`rustc -O`) | 0.16 to 0.21 s | 0.17 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.18 to 0.26 s | 0.19 s |
| Go | 0.36 to 0.44 s | 0.40 s |
| Python | 3.9 s | |
| Kāra (`karac build --mir`) | 0.143 to 0.167 s | 0.148 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 38 times
C's.

v2 took 0.78 times Rust's median time under overflow checks and 1.45
times C's. Under valgrind's cachegrind v2 ran 1.41 billion instructions
and 293 million branches with 8.9 million mispredicted, Rust with
overflow checks 1.86 billion, 356 million and 12.9 million, and C 742
million, 74 million and 5.0 million. C sizes each level once and never
grows it, where the others double their vectors as they fill.
