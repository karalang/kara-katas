# 1370. Increasing Decreasing String

You are given a string `s`. Reorder the string using the following
algorithm:

1. Remove the smallest character from `s` and append it to the result.
2. Remove the smallest character from `s` that is greater than the last
   appended character, and append it to the result.
3. Repeat step 2 until no more characters can be removed.
4. Remove the largest character from `s` and append it to the result.
5. Remove the largest character from `s` that is smaller than the last
   appended character, and append it to the result.
6. Repeat step 5 until no more characters can be removed.
7. Repeat steps 1 through 6 until all characters from `s` have been
   removed.

If the smallest or largest character appears more than once, you may
choose any occurrence to append to the result.

Return the resulting string after reordering `s` using this algorithm.

```
s = "aaaabbbbcccc"  ->  "abccbaabccba"
s = "rat"           ->  "art"
```

**Constraints:** `1 <= s.length <= 500`, `s` consists of only
lowercase English letters.

Each arm is `fn sort_string(s: Str) -> String`; the Rust solution's
takes a `String`, as LeetCode's signature does.

## Approaches

| file | mechanism |
|---|---|
| `sort_string.kara` ★ | the letters counted, then sweeps up from a to z and down from z to a, each taking one of every letter still left, until none is. O(n + 26 r) for r rounds |
| `sort_string_sorted.kara` | the letters sorted, then walked forward and backward in turn, each walk taking the first unused copy of every letter it passes and marking it used. O(n log n + n r) |
| `sort_string_map.kara` | the letters counted in a `SortedMap`, its keys walked up and down in turn, each walk taking one of every letter and dropping the letters it uses up |
| `sort_string_bounce.kara` | the letters counted as bytes; one index runs up the 26 letters and back down, turning at each end on the same letter, taking a letter each time it lands on one that is left, and the result built as a `Vec[u8]` |
| `sort_string_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let mut cnt = [0; 26];`, `String::with_capacity(s.len())`, `while res.len() < s.len()` around an up loop and a `(0..26).rev()` loop), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's examples and one letter
seven times (`abccbaabccba art cdelotee ggggggg ops`); and 2000 random
strings of 1 to 500 letters from the first 1 to 26 letters of the
alphabet, folded into a checksum (`2000 random strings: 86 unchanged,
checksum 343854524`). `sort_string.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the four Kāra arms check clean as first written. The
Rust solution takes 3 fixes: `struct Solution;` becomes `struct
Solution {}`, and `String::with_capacity` and `Solution::sort_string`
take `.` for `::`. `[0; 26]`, the `as usize` index and `s: String`
stand as Rust wrote them. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the letters left in a list, and each of the statement's
steps a scan of the list for the letter it names, taken out with
`Vec.remove`. It checks the examples, 1500 random strings of 1 to 20
letters and 500 of 1 to 200, each from the first 1 to 26 letters of
the alphabet.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the answer is the same letters, each as often |
| P3 | the string reversed, the same answer |
| P4 | the answer begins with every distinct letter once, in order |
| P5 | every letter moved up the alphabet alike, as far as the largest allows, the answer moved alike |
| P6 | the ★ arm's answer |

All 60,150 checks pass on every arm: `2005 cases: checksum 119017776,
60150 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, following the statement's
steps with `min` and `max` over the letters left, gives the same
checksum.

The differential's own Mend loop turned up a gap: `let by = b'z' as
i64 - top;` with `top: i64` draws W0310, an unnecessary cast, and
`karac fix` deletes it in `c as u32 as i64 + by` but offers nothing
for the byte literal, though the deletion is just as safe there
(B-2026-11-25-21). The cast stays, as written.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks. Two first ★ edits, every sweep upward and the up
sweep skipping a, failed as the map arm's every walk upward and the
bounce arm's start at b did, but for P6, and were replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last letter never taken | P1 612, P2 612, P4 68, P6 2448 |
| M2 | ★: each up sweep's letter counted twice | P1 1220, P2 1220, P6 4880 |
| M3 | sorted: every unused copy taken on the way forward | P1 1567, P4 1567, P6 1567 |
| M4 | sorted: the backward walk not started afresh | P1 942, P6 942 |
| M5 | map: every walk upward | P1 1376, P6 1376 |
| M6 | map: the first walk downward | P1 1863, P4 1863, P6 1863 |
| M7 | bounce: an end letter not taken again on the turn | P1 569, P5 954, P6 569 |
| M8 | bounce: the first walk starts at b | P1 1261, P4 1261, P5 1246, P6 1261 |
| M9 | solution: the down sweep skips z | P1 13, P5 904, P6 13 |
| M10 | solution: the up sweep writes the next letter | P1 2005, P2 2005, P4 2005, P5 1985, P6 2005 |

P1 and P6 kill all ten, P4 five, P5 four, P2 three, and P3 none. Every
arm reads only how often each letter occurs, so none sees the order of
the input (P3), which stands for an arm that would. Keeping the letters
(P2) catches only the edits that lose letters or write wrong ones (M1,
M2, M10). The opening run of distinct letters (P4) catches the edits
that disturb the first sweep: copies taken twice on the way up (M3), a
first walk downward (M6), a first walk from b (M8), a wrong letter
written (M10), and a string of distinct letters losing its last one
(M1). Moving every letter up the alphabet (P5) catches the edits whose
mistakes depend on where the letters sit: the bounce arm's turn at z
(M7) and its start at b (M8), which letters moved to the top meet
differently, the solution's down sweep skipping z (M9), and a letter
written one past, which wraps at z (M10).

## Benchmarks

The bench builds 20 strings of 500 letters, the constraints' most, from
the first 2 to 26 letters of the alphabet, once; then makes 6 * 10^4
rounds, each changing one letter of one string, drawn from the checksum
so far, sorting that string with the ★ arm and folding every letter of
the answer into the checksum. Every implementation prints `60000 rounds
over 20 strings of 500 letters: checksum 13274945`. The work is
counting 500 letters, the sweeps over 26 counts, and folding 500
letters, the same in every language; Kāra, Rust and Go copy the changed
string into a new one each round, C changes it in place.

BENCHTAB
