# 1647. Minimum Deletions to Make Character Frequencies Unique

A string `s` is called **good** if there are no two different characters
in `s` that have the same **frequency**.

Given a string `s`, return *the **minimum** number of characters you need
to delete to make* `s` ***good**.*

The **frequency** of a character in a string is the number of times it
appears in the string. For example, in the string `"aab"`, the
**frequency** of `'a'` is `2`, while the **frequency** of `'b'` is `1`.

```
s = "aab"       ->  0
s = "aaabbbcc"  ->  2
s = "ceabaacb"  ->  2
```

**Constraints:** `1 <= s.length <= 10^5`; `s` contains only lowercase
English letters.

## Approaches

| file | mechanism |
|---|---|
| `deletions.kara` ★ | the letters' counts sorted from largest down: the largest keeps its count, and each after it at most one less than the one before it kept, never below 0. O(n + 26 log 26) |
| `deletions_set.kara` | the counts in a `Map` by letter, each stepped down past the counts a `Set` has taken, to 0 at the lowest, which any number of letters may share. O(n + 26^2) |
| `deletions_buckets.kara` | how many letters have each count, from the largest count down: of the letters sharing a count all but one move down a count, a deletion each. O(n) |
| `deletions_solution.kara` | LeetCode's Rust template: the counts in a `[0; 26]`, each stepped down past a `HashSet` of counts seen. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples, one letter
(0), every letter once (25), and four letters four times each (6); then
the deletions summed and a checksum for 3000 random strings of up to 10
letters from 4, 1000 of up to 1000 from 26, and 20 of up to `10^5` from
26. `deletions.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way of keeping between none and all of each letter is
tried, and the fewest deletions among those whose letters still present
all have different counts is the answer. It checks 3000 random strings
of 1 to 8 letters from the first 1 to 4 of the alphabet. Every string is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the letters relabelled from the far end of the alphabet give the same answer |
| P3 | one more letter, new to the string, adds 0 or 1 to the answer |
| P4 | the string reversed gives the same answer |
| P5 | each arm agrees with at least two of the other three |

P3 holds because the new letter either keeps its count of 1 where 1 is
free or is deleted, and taking it away from any good answer for the
longer string leaves a good answer for the shorter.

The differential prints `3000 problems: checksum 437873780, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the ★ arm
capping each count at `cap + 1` rather than `cap` no longer type-checks:
with `min(c, cap + 1)` the checker reads `c - keep` as an `i64`, which
`deletions: i32` cannot take without a cast.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cap allowed below 0 | P1 3000, P3 1223, P5 3000 |
| M2 | ★: the counts left smallest first | P1 3000, P5 3000 |
| M3 | ★: the next cap one below the count, not below what was kept | P1 180, P5 180 |
| M4 | set: a count stepped down past 0 when 0 is taken | P1 136, P3 664, P5 136 |
| M5 | set: no count ever taken | P1 935, P5 935 |
| M6 | buckets: the letters moved down a count lost | P1 180, P5 180 |
| M7 | buckets: the counts walked smallest first | P1 180, P5 180 |
| M8 | template: a step down not counted | P1 935, P5 935 |
| M9 | template: a count of 1 never stepped down | P1 664, P5 664 |
| M10 | template: a count of 1 never taken | P1 664, P5 664 |

## Benchmarks

The bench draws 500 random strings of `10^5` letters, LeetCode's
longest, each from the first 1 to 26 of the alphabet, all of them first,
then answers each by the ★ arm in all five languages. Every
implementation prints `500 strings of 100000 letters: deletions sum to
224, checksum 397660514`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.159 s |
| Kāra (`karac build`) | 0.182 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.185 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.190 s |
| Rust (`rustc -O`) | 0.191 s |
| Go | 0.386 s |
| Python | 15 s |

The sequential Kāra build is level with Rust and level with Rust with
overflow checks on, the equal-safety comparison (BENCHMARKS.md). C is
the fastest here at 0.159 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.152 s and
0.176 s on one run).

## Verification

All four arms print the same output as `deletions.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `21cdf88b69`.

## Writing it

The ★ and buckets arms indexed their counts with `(b - b'a') as i64`,
and the `lossless_cast` lint dropped the cast. The ★ arm returned its
`deletions` as the `i32` the signature asks for, and `karac fix` declared
it `deletions: i32`. The set arm checked clean as first written.

LeetCode's Rust template takes one `karac fix` of 8 edits: the `use
std::collections::HashSet;` line dropped, `struct Solution;` to `struct
Solution {}`, `c as u8` to `c as u32 as u8`, `HashSet::new()` to
`Set.new()`, `for &f in` to `for f in`, `&&` to `and` and `&f` to `f`.
The arm then checks and agrees with no hand edit.
