# 2712. Minimum Cost to Make All Characters Equal

You are given a **0-indexed** binary string `s` of length `n` on which
you can apply two types of operations:

- Choose an index `i` and invert all characters from index `0` to index
  `i` (both inclusive), with a cost of `i + 1`.
- Choose an index `i` and invert all characters from index `i` to index
  `n - 1` (both inclusive), with a cost of `n - i`.

Return *the **minimum cost** to make all characters of the string
**equal***.

```
s = "0011"    ->  2
s = "010101"  ->  9
```

**Constraints:** `1 <= s.length == n <= 10^5`; `s[i]` is either `'0'`
or `'1'`.

## Approaches

| file | mechanism |
|---|---|
| `equal.kara` ★ | every flip changes exactly one boundary between neighbours, the one at its end, so each boundary between two unequal bits must be crossed an odd number of times and every other boundary an even number. Once is enough, by the cheaper of the two flips across the boundary before index i: the prefix flip ending there, cost i, or the suffix flip starting there, cost n - i. O(n) |
| `equal_meet.kara` | the cost of making `s[0..=i]` all equal to `s[i]` by prefix flips alone grows by i at each change, and that of making `s[i..]` equal to it by suffix flips alone likewise from the right; the two kinds of flip meet at some index, so the answer is the smallest sum of the two at one index. O(n) |
| `equal_halves.kara` | a boundary in the left half is cheapest crossed by a prefix flip, one in the right half by a suffix flip, so two loops, one per half, each count the boundaries at their own price, with no `min` per boundary; the string's `chars` collected first. O(n) |
| `equal_iter.kara` | the bytes' `windows(2)` with their places from `enumerate`, the unequal pairs kept by `filter`, each priced by `map` at the cheaper flip across it, and `sum`. O(n) |
| `equal_solution.kara` | a Rust solution as LeetCode's Rust users write it, `as_bytes()`, an `i64` accumulator built from `usize` indices with `as i64`, and `std::cmp::min`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples; one bit; two
that differ; `10^5` zeros, LeetCode's longest; `10^5` alternating; one
change in the middle; then the costs summed and a checksum for 2000
random strings of up to 20 bits and 50 of up to `10^5`, each bit
changed from the one before 0 to 8 times in 8. `equal.py` mirrors the ★
arm and its output is byte-identical.

```
2
9
0
1
0
2500000000
50000
2000 strings up to 20: costs sum to 34460, checksum 734592594
50 strings up to 100000: costs sum to 17968402682, checksum 49262729
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string of n bits a node, each prefix and suffix flip an
edge at its price, and Dijkstra's search from the string given to the
nearer of the two strings with every character equal, with no
boundaries. It checks 1000 random strings of 1 to 8 bits and 10 of up to
`10^5`, each bit changed from the one before 0 to 8 times in 8. Every
case is drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 8 bits, the answer is the literal reading's |
| P2 | every bit flipped: the same answer |
| P3 | the string reversed: the same answer |
| P4 | the last bit written once more: the answer is no smaller |
| P5 | the answer is at least the number of changes between neighbours and at most that many times half the length |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1010 cases: checksum 223661802, 30300 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same 1000 small cases by Dijkstra's search gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. P2 kills none of them: every arm looks only at
whether neighbours differ, which flipping every bit keeps. M1, M4 and M6
are one fault in three arms, every boundary priced by its prefix flip,
and fail the same cases.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: every boundary priced by its prefix flip | P1 481, P3 344, P5 297, P6 489 |
| M2 | ★: the suffix flip priced one more | P1 481, P3 311, P5 88, P6 489 |
| M3 | meet: the left costs one more per change | P1 497, P3 311, P5 100, P6 505 |
| M4 | meet: the meeting point the last index only | P1 481, P3 344, P5 297, P6 489 |
| M5 | halves: the middle boundary priced from the right | P1 458, P3 114, P4 54, P5 218, P6 462 |
| M6 | halves: the right half priced as the left | P1 481, P3 344, P5 297, P6 489 |
| M7 | iter: each pair's place taken one early | P1 585, P3 311, P5 233, P6 593 |
| M8 | iter: equal pairs counted | P1 807, P5 709, P6 817 |
| M9 | solution: a change costs half the length | P1 469, P6 477 |
| M10 | solution: the first boundary never seen | P1 458, P3 218, P5 169, P6 463 |

## Benchmarks

The bench draws 100 strings of `10^5` bits, LeetCode's longest, each bit
changed from the one before 0 to 8 times in 8, all of them first, then
answers each 5 times by the ★ arm in all five languages. Every
implementation prints `100 strings of 100000 bits, 5 rounds: costs sum
to 682660504810, checksum 588270608`.

BENCHTAB

## Verification

All five arms print the same output as `equal.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★, meet and halves arms checked clean as first written. The
iterator arm took one `karac fix`: an `.into_iter()` inserted after
`windows(2)`, which answers a `Vec` of windows rather than an iterator.

LeetCode's Rust template took one `karac fix` of 5 edits: `struct
Solution {}` added, `as_bytes()` became `bytes()`, `std::cmp::min(i, n -
i) as i64` became `min(i, n - i)`, since the indices are already `i64`,
and the wrapper's `s.clone()` became `s`, since a parameter borrows by
itself.
