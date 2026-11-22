# 2716. Minimize String Length

Given a **0-indexed** string `s`, repeatedly perform the following
operation **any** number of times:

- Choose an index `i` in the string, and let `c` be the character in
  position `i`. **Delete** the **closest occurrence** of `c` to the
  **left** of `i` (if any) and the **closest occurrence** of `c` to the
  **right** of `i` (if any).

Your task is to **minimize** the length of `s` by performing the above
operation any number of times.

Return *an integer denoting the length of the **minimized** string.*

```
s = "aaabc"   ->  3
s = "cbbd"    ->  3
s = "dddaaa"  ->  2
```

**Constraints:** `1 <= s.length <= 100`; `s` contains only lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `minimize.kara` ★ | an operation deletes copies of the letter at the chosen index, never the index itself, so every letter keeps at least one copy; and while a letter has two copies, choosing either deletes the other. The answer is the number of distinct letters, counted by a `Set[char]` of the string's `chars`. O(n) |
| `minimize_bits.kara` | a letter's place in the alphabet is a bit of a `u32` mask, set by `fold` over the string's bytes, and the answer is the mask's `count_ones`. O(n) |
| `minimize_table.kara` | an `Array[bool, 26]` marks each letter met, and a letter counts the first time it is marked. O(n) |
| `minimize_sorted.kara` | the letters sorted, so the copies of each stand together, and a letter counts where it differs from the one before it. O(n log n) |
| `minimize_solution.kara` | a Rust solution as LeetCode's Rust users write it, `s.chars().collect::<HashSet<char>>().len() as i32`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; one letter; the
alphabet; 100 a's, LeetCode's longest; the alphabet backwards four times
over, cut to 100; then the lengths summed and a checksum for 5000 random
strings of 1 to 100 letters from the first 1 to 26. `minimize.py`
mirrors the ★ arm and its output is byte-identical.

```
3
3
2
1
26
1
26
5000 strings: lengths sum to 56599, checksum 667333195
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: from the string given, every operation the statement allows
tried, an index chosen and the closest copy of its letter on each side
deleted, breadth first over every string reached, and the shortest kept,
with no counting of letters. It checks 1000 random strings of 1 to 8 letters from
the first 1 to 4, then 500 of 1 to 100 from the first 1 to 26. Every
case is drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 8 letters, the answer is the literal reading's |
| P2 | the string reversed: the same answer |
| P3 | every letter moved 1 to 25 places on round the alphabet: the same answer |
| P4 | the string written twice: the same answer |
| P5 | a letter the string lacks added: one more; and the answer is between 1 and the shorter of the length and 26 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `1500 cases: checksum 700839014, 45000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
breadth-first search over the same 1000 small cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2, the answer capped at 25, fails only the 8
checks of the two strings that hold the whole alphabet, and M9 only the
strings that hold a z: the large cases are what reach them.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first letter left out | P1 283, P2 217, P4 355, P5 124, P6 355 |
| M2 | ★: the answer capped at 25 | P5 6, P6 2 |
| M3 | bits: letters paired into one bit | P1 495, P3 304, P5 983, P6 955 |
| M4 | bits: a letter's bit flipped, not set | P1 577, P4 1258, P5 242, P6 1030 |
| M5 | table: a letter never marked as met | P1 809, P4 1500, P5 364, P6 1284 |
| M6 | table: the table half as long, letters folded on it | P5 203, P6 253 |
| M7 | sorted: the letters never sorted | P1 375, P4 1077, P5 333, P6 825 |
| M8 | sorted: a letter counts where it differs from the first | P1 436, P3 220, P4 1077, P5 443, P6 889 |
| M9 | solution: every z left out | P3 296, P5 1, P6 20 |
| M10 | solution: every other letter only | P1 322, P2 258, P4 279, P5 760, P6 649 |

## Benchmarks

The bench draws `10^5` strings of 100 letters, LeetCode's longest, from
the first 1 to 26 letters, all of them first, then answers each 10 times
by the ★ arm in all five languages. The set is each language's own hash
set of characters: Kāra's `Set[char]`, Rust's `HashSet<char>`, Go's
`map[rune]struct{}`, Python's `set`, and in C a 64-slot open addressing
table with a multiplicative hash, built afresh for each string. Every
implementation prints `100000 strings of 100 letters, 10 rounds: lengths
sum to 13426290, checksum 309953706`.

BENCHTAB

## Verification

All five arms print the same output as `minimize.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four arms of our own checked clean but for the harness, whose
`backwards.slice(0, 100)` is a `Str` passed where the function takes a
`String`; `karac fix` added the `.to_string()` it names.

LeetCode's Rust template took one `karac fix` of 7 edits, the wrapper
included: the `use std::collections::HashSet;` became `struct Solution
{}`, the turbofish `collect::<HashSet<char>>()` became
`Set[char].from_iter(s.chars())`, since Kāra names the collection
before the call rather than after it, `Solution::` became `Solution.`,
the wrapper's `s.clone()` became `s`, and its `as i64` on the `i32`
answer was dropped.

The differential's literal reading asked `s.contains(missing)` of a
`char`; `contains` takes a `Str` pattern, and `karac fix` wrote
`missing.to_string()`. It also turned `missing as u8` into `missing as
u32 as u8`, since a `char` does not fit a `u8` in general.
