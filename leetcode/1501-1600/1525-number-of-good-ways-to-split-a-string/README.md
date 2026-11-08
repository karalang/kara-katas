# 1525. Number of Good Ways to Split a String

You are given a string `s`. A split of `s` into two non-empty strings
`s_left` and `s_right` whose concatenation is `s` is good when the number
of distinct letters in `s_left` and in `s_right` is the same. Return the
number of good splits.

```
s = "aacaba"  ->  2   ("aac", "aba") and ("aaca", "ba")
s = "abcd"    ->  1   ("ab", "cd")
```

**Constraints:** `1 <= s.length <= 10^5`; `s` holds only lowercase English
letters.

## Approaches

| file | mechanism |
|---|---|
| `splits.kara` ★ | the count of distinct letters in every prefix, walking from the left, and in every suffix, walking from the right; a split is good where the prefix before it and the suffix after it agree. O(n) |
| `splits_counts.kara` | one walk with two count tables: every letter starts on the right; moving one left adds a distinct letter on the left the first time and removes one on the right the last time. O(n) |
| `splits_ends.kara` | each letter's first and last place: before split `k` the left holds every letter first seen before `k` and the right every letter last seen at `k` or after; two running sums over those places give both counts. O(n + 26) |
| `splits_iter.kara` | the ★ arm with iterator adapters: `scan` carries the letters seen as a bit set and yields its `count_ones`, once from each end; `zip`, `skip`, `filter` and `count` compare them |
| `splits_solution.kara` | LeetCode's Rust template (`as_bytes()`, `[0usize; 26]`, `for &c in &b[..b.len() - 1]`, `filter(\|&&x\| x > 0)`): the counting arm, carried by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples, two more
from the problem's set (`aaaaa`, `acbadbaada`) and a single letter, then
checksums of the answers for 3000 random strings of 1 to 12 letters over
4, 300 of 1 to 300 over 26, and 30 of 1 to 100000 over 26. `splits.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: at every split, both halves cut out and their letters
collected into a `Set` each. It checks 3000 strings of 1 to 10 letters
over 3, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the string reversed leaves the answer |
| P3 | the letters renamed (a to b, b to c, c to a) leave the answer |
| P4 | the answer is at least 0 and at most the number of splits |
| P5 | every letter doubled keeps every old split good, so the answer does not fall |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3000 problems: checksum 560469090, 90000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirteen edits to the differential, two to three to each arm, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Twelve are killed,
each the same way under both backends; one survives, and it is
equivalent.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the prefix compared ends at the split's own letter | P1 2148, P6 2148 |
| M2 | ★: the first split skipped | P1 457, P2 210, P6 457 |
| M3 | ★: the suffix walk starts with the prefix's letters seen | P1 2181, P6 2181 |
| M4 | counts: a letter leaves the right one move early | P1 1977, P2 1288, P5 431, P6 1977 |
| M6 | counts: a letter counted on the left twice | P1 1270, P2 990, P5 466, P6 1270 |
| M7 | ends: the left count takes the split's own letter | P1 1766, P2 1530, P6 1766 |
| M8 | ends: the right count drops the split's own letter | P1 1820, P2 408, P5 449, P6 1820 |
| M9 | ends: each letter's first place overwritten by later ones | P1 1943, P2 431, P6 1943 |
| M10 | iter: each prefix paired with the suffix that starts inside it | P1 2605, P4 457, P6 2605 |
| M11 | iter: the suffix counts left in walking order | P1 2246, P2 1716, P6 2246 |
| M12 | template: a letter counted on the left at its second sight | P1 1764, P2 1147, P5 345, P6 1764 |
| M13 | template: the right starts with only repeated letters | P1 1201, P2 1000, P5 288, P6 1201 |

The survivor is the counting arm walking every letter rather than all
but the last (M5): the extra step leaves the right empty and the left
not, so it never counts.

## Benchmarks

The bench builds 200 random strings of 1 to 100000 letters (each over
its own 1 to 26 letters) once and answers each 10 times by the ★ arm, in
all five languages. Each answer takes its own copy of the string, as the
signature does (`malloc` and `free` in C). Every implementation prints
`10 passes over 200 strings of up to 100000 letters: 93015820 good
splits, checksum 177403067`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `a90821c8d` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.161 s |
| Kāra (`karac build`) | 0.206 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.209 s |
| Rust (`rustc -O`) | 0.246 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.274 s |
| Go | 0.353 s |
| Python | 11.7 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time equals its real time (0.20 s and 0.20 s on two runs).

Kāra is 0.76x Rust under overflow checks by median. Not traced.

## Verification

All five arms print the same output as `splits.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them and the differential. `karac check` reports nothing on any of them,
and `karac fix` has nothing left to change.

## Writing it

The ★, counts and ends arms were written in Kāra and `karac fix` had
nothing to change. The iterator arm took one edit, a redundant `as i64`
after `count_ones()` dropped. The differential's doubling wrote
`flat_map(|c| [c, c])`, which is refused (`flat_map` takes an iterator,
not a collection) with a fix to `[c, c].into_iter()`, applied.

The Rust template took 4 edits and then 2 over two rounds: the `&` and
`&&` patterns and the `&` before the slice dropped, then `as_bytes()` to
`bytes()` and the closing `as i64` dropped. Its `[0usize; 26]` tables and
`as usize` casts stay as written. It checks and agrees with no hand edit.
