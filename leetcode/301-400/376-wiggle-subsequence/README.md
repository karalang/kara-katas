# 376. Wiggle Subsequence

A wiggle sequence is one whose differences between neighbours strictly
alternate between positive and negative. A sequence of one value, or of
two different values, is a wiggle. Return the length of the longest
subsequence of `nums` that is a wiggle.

```
nums = [1, 7, 4, 9, 2, 5]                    -> 6
nums = [1, 17, 5, 10, 13, 15, 10, 5, 16, 8]  -> 7
nums = [1, 2, 3, 4, 5, 6, 7, 8, 9]           -> 2
```

**Constraints:** `1 <= nums.length <= 1000`; `0 <= nums[i] <= 1000`.

## Approaches

| file | mechanism | time |
|---|---|---|
| `wiggle.kara` ★ | two running lengths: `up` is the longest wiggle of the prefix that ends going up and `down` the longest that ends going down; a rise sets `up = down + 1`, a fall sets `down = up + 1`, an equal pair changes neither | O(n), O(1) space |
| `wiggle_turns.kara` | skip equal neighbours and count the first step and every change of direction after it, plus one for the first value | O(n), O(1) space |
| `wiggle_dp.kara` | the textbook quadratic DP: `up[i]` and `down[i]` are the longest wiggles ending at `i` with a rise or a fall into it, built from every earlier `j` | O(n²) |
| `wiggle_extrema.kara` | collapse runs of equal values, then keep both ends and every strict peak or valley | O(n), with an O(n) copy |
| `differential.kara` | the four arms against an oracle that tries every subsequence, 40,000 checks, five properties | — |

Every arm prints the same 11 lines: the three LeetCode examples, seven
edge cases (one value, two equal, two different, all equal, plateaus
between turns, strictly falling, values at both bounds), and a checksum
over 300 random arrays of up to 1,000 values, a third of them drawn
from 0 to 5 so that runs of equal values are common. `wiggle.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle tries
every subsequence of the array and keeps the longest that wiggles, so
the arrays have at most 10 values. It runs 2,000 random arrays, half of
them drawn from 0 to 3.

| | property |
|---|---|
| P1 | each arm gives the oracle's length |
| P2 | repeating every value in place changes nothing |
| P3 | reversing the array changes nothing |
| P4 | reflecting every value to `1000 - v` changes nothing |
| P5 | the length is between 1 and `n`, and at least 2 when two values differ |

It prints `2000 cases, 40000 checks, 0 failures` under
`karac __mir-run`, `karac __mir-llvm-run`, `karac run --interp`, LLJIT,
`karac build` and `KARAC_AUTO_PAR=1 karac build`.

## Mutation testing

Eight edits to the copies inside `differential.kara`, each run under
`karac __mir-run`. All eight are killed.

| # | mutation | how |
|---|---|---|
| M1 | running: a rise sets `up = up + 1` | P1, P3 and P4, 3127 failures |
| M2 | running: a fall sets `down = max(down, up) + 1` | P1, P3 and P4, 2440 failures |
| M3 | turns: an equal step counts as a turn | P1, P2 and P3, 2519 failures |
| M4 | turns: the last direction is never remembered | P1, 1040 failures |
| M5 | DP: only the previous value `j = i - 1` is tried | P1 and P2, 2203 failures |
| M6 | extrema: runs of equal values are not collapsed | P1 and P2, 1941 failures |
| M7 | extrema: valleys are not kept | P1 and P4, 2182 failures |
| M8 | oracle: an equal step counts as a wiggle | P1, 952 failures |

## Verification

All four arms print the same output as `wiggle.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run` (the
same MIR compiled to LLVM), `karac run --interp`, LLJIT, `karac build`
and `KARAC_AUTO_PAR=1 karac build`.

## Benchmarks

The bench program answers 20,000 random arrays of 1,000 values, the
problem's largest, with the ★ arm, and folds the answers into a
checksum. The Kāra build and the C, Rust, Go and Python mirrors all
print `checksum 191500899`, and so does `karac __mir-llvm-run`. Timings are not taken yet; they need a
quiet machine.

## Compiler findings

None.
