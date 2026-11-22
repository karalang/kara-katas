# 2785. Sort Vowels in a String

Given a **0-indexed** string `s`, **permute** `s` to get a new string
`t` such that:

- All consonants remain in their original places. More formally, if
  there is an index `i` with `0 <= i < s.length` such that `s[i]` is a
  consonant, then `t[i] = s[i]`.
- The vowels must be sorted in the **nondecreasing** order of their
  **ASCII** values. More formally, for pairs of indices `i`, `j` with `0
  <= i < j < s.length` such that `s[i]` and `s[j]` are vowels, then
  `t[i]` must not have a higher ASCII value than `t[j]`.

Return *the resulting string*.

The vowels are `'a'`, `'e'`, `'i'`, `'o'`, and `'u'`, and they can
appear in lowercase or uppercase. Consonants comprise all letters that
are not vowels.

```
s = "lEetcOde"  ->  "lEOtcede"
s = "lYmpH"     ->  "lYmpH"
```

**Constraints:** `1 <= s.length <= 10^5`, `s` consists only of letters
of the English alphabet in uppercase and lowercase.

## Approaches

| file | mechanism |
|---|---|
| `vowels.kara` ★ | the vowels, told by a `match` on the ten letters, gathered by `filter`, sorted, and written back into the vowels' places in order. O(n log n) |
| `vowels_counts.kara` | no sort: the ten vowels in ASCII order, "AEIOUaeiou", each counted in a `Vec[i64]` by its `position` there, and the vowels' places filled from the least vowel with a count left. O(n) |
| `vowels_queue.kara` | the vowels pushed into a `PriorityQueue`, which pops the least first, and one popped at each vowel's place as the letters are mapped again. O(n log n) |
| `vowels_map.kara` | each vowel's count in a `SortedMap[char, i64]` through `entry`; the map's `first()` is the least vowel left, taken at each vowel's place and removed when its count runs out. O(n log v), v at most 10 |
| `vowels_solution.kara` | a Rust solution as LeetCode's Rust users write it, a closure by `"aeiouAEIOU".contains(c)`, the vowels sorted by `sort_unstable` and handed back by `it.next().unwrap()` from their `into_iter()`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; every vowel
in falling order; no vowel; one letter; 3000 random strings of 1 to 20
letters, half of them vowels, with the count of letters and a checksum
of the answers; and 3 of `10^5` letters, LeetCode's longest, from all
52, with a checksum. `vowels.py` mirrors the ★ arm and its output is
byte-identical.

```
lEOtcede
lYmpH
AEIOUaeiou
bcdfgXYZ
a
3000 small strings: 31938 letters, checksum 761762028
3 strings of 10^5: checksum 40326224
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the consonants kept in their places, and each vowel's place
in turn given the least vowel of the string not yet placed, found by
looking over them all; no sort, no table and no queue. It draws 2000
random strings of 1 to 20 letters, half of them vowels, then 50 of up to
2000 letters from all 52, or every other one of vowels only, all before
any arm answers; the literal reading is asked only of the first 2000.

| | property |
|---|---|
| P1 | up to 20 letters, the string is the literal reading's |
| P2 | the answer sorted again: the same string |
| P3 | the letters reversed: the same vowels in the same order |
| P4 | the same length, every consonant in its place |
| P5 | the vowels read in order never fall, and each of the ten is there as often as in the string |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases: checksum 937011109, 61500 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases by the same least-vowel picks gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: E taken for a consonant | P1 795, P3 894, P5 845, P6 845 |
| M2 | ★: the vowels written back falling | P1 1769, P5 1819, P6 1819 |
| M3 | counts: the lower case vowels put first | P1 1615, P5 1665, P6 1665 |
| M4 | counts: a vowel written never counted off | P1 1769, P5 1819, P6 1819 |
| M5 | queue: the greatest vowel popped first | P1 1769, P5 1819, P6 1819 |
| M6 | queue: u taken for a consonant | P1 761, P3 860, P5 810, P6 810 |
| M7 | map: a vowel's count never taken down | P1 1248, P5 1297, P6 1297 |
| M8 | map: a vowel run out kept at 0 | P1 1769, P5 1819, P6 1819 |
| M9 | solution: the vowels left in the string's order | P1 1633, P3 1801, P5 1683, P6 1683 |
| M10 | solution: only lower case vowels moved | P1 1538, P3 1694, P5 1588, P6 1588 |

## Benchmarks

The bench draws 20 strings of `10^5` letters, LeetCode's longest, from
all 52, all of them first, then answers each 10 times by the ★ arm in
all five languages, each answer a new string: the vowels sorted by
Kāra's `sort`, Rust's `sort`, Go's `slices.Sort`, Python's `sorted` and
C's `qsort`. Every implementation prints `20 strings of 10^5, 10
rounds: checksum 575596176`.

BENCHTAB

## Verification

All five arms print the same output as `vowels.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The ★ arm first told a vowel by Rust's `"aeiouAEIOU".contains(c)`, a
`char` pattern; Kāra's `contains` takes a `Str`, and `karac fix` wrote
`c.to_string()`, a new string for every letter. The ★ arm, which the
bench times, tells a vowel by a `match` on the ten letters instead; the
map arm keeps the `contains(c.to_string())` the fix wrote. The map arm
first took the least key by Rust's `first_key_value()`, and the fix made
it `first()`. In the differential, `let value = got[arm]` moved a
`String` out of a `Vec`; the fix made it `ref got[arm]`.

LeetCode's Rust template took 8 `karac fix` edits, the wrapper
included: `struct Solution {}` added; `contains(c)` became
`contains(c.to_string())`; `Vec<char>` became `Vec[char]`; the `|&c|`
pattern dropped its `&`; `sort_unstable` became `sort`; the wrapper's
`&str` became `Str`; and `Solution::` became `Solution.`.
