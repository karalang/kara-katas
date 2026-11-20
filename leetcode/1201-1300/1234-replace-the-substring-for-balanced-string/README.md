# 1234. Replace the Substring for Balanced String

You are given a string `s` of length `n` containing only four kinds of
characters: `'Q'`, `'W'`, `'E'`, and `'R'`.

A string is said to be **balanced** if each of its characters appears
`n / 4` times where `n` is the length of the string.

Return the minimum length of the substring that can be replaced with
**any** other string of the same length to make `s` **balanced**. If `s`
is already **balanced**, return `0`.

```
s = "QWER"  ->  0
s = "QQWE"  ->  1    "QQWE" with one "Q" made "R"
s = "QQQW"  ->  2    "QQQW" with "QQ" made "ER"
```

**Constraints:** `n == s.length`; `4 <= n <= 10^5`; `n` is a multiple of
`4`; `s` contains only `'Q'`, `'W'`, `'E'`, and `'R'`.

The arms are `fn balanced_string(s: String) -> i64`. The two Rust arms
keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `balanced_string` calls it.

## Approaches

| file | mechanism |
|---|---|
| `replace_the_substring_for_balanced_string.kara` ★ | a sliding window: a window can be replaced to balance the string exactly when no letter outside it appears more than `n / 4` times, since its filling can then supply each letter's shortfall. Grow the right end, and while the outside fits, record the length and shrink from the left. O(n) |
| `replace_the_substring_for_balanced_string_lengths.kara` | binary search on the length: a window that works stays working one letter wider, so the shortest is found by bisection, each length tested by sliding a window of that size, the counts outside it in an `Array[i64, 4]`. O(n log n) |
| `replace_the_substring_for_balanced_string_prefix.kara` | prefix counts of each letter in a `Vec[Array[i64, 4]]`; from each start, the first end at which the window holds every letter's surplus, by a binary search. O(n log n) |
| `replace_the_substring_for_balanced_string_counted.kara` | the sliding window with the counts outside it in a `Map[char, i64]`, tested by `values().all(..)` |
| `replace_the_substring_for_balanced_string_bytes.kara` | a Rust solution as LeetCode's Rust users write it (the string's bytes, the counts in a `[0usize; 128]` indexed by `c as usize`, a closure over `b"QWER"`, the window slid by two `usize` indices), carried to Kāra by `karac fix` |
| `replace_the_substring_for_balanced_string_hashmap.kara` | another Rust solution (the counts in a `HashMap<char, i32>` built through `*count.entry(c).or_insert(0) += 1`, changed through `*count.get_mut(&c).unwrap()`, read back by `unwrap_or(&0)`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples and
`"QQQQ"` (`3`), a checksum of the answers for 1000 random strings of 4 to
40 letters, some leaning toward `Q` (`260880139`), and three answers at
the constraints' top, 10^5 letters: drawn evenly (`284`), leaning toward
`Q` (`49556`), and `"QWER"` 25000 times (`0`).
`replace_the_substring_for_balanced_string.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the lengths, prefix and counted arms check clean as
written. The ★ arm was first written with Rust's `s.as_bytes()`, which
the fix makes `s.bytes()`. The bytes arm takes one round of 19 fixes
(among them `as_bytes()` to `bytes()`, `[0usize; 128]` to `[0; 128]`,
`cnt[c as usize]` to `cnt[c]`, `&[usize; 128]` to `ref Array[i64, 128]`,
`&&` to `and`) and the hashmap arm one round of 26 (among them
`HashMap<char, i32>` to `Map[char, i32]`, `for &c in &chars` to `for c in
ref chars`, `get(&c).unwrap_or(&0)` to `get(c).unwrap_or(0)`,
`get_mut(&chars[right])` to `get_mut(chars[right])`), and both check
clean.

## Gaps

None found.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every window, and every way to fill it, as how many of each
letter the filling holds (counts that sum to the window's length), kept
when the string is then balanced, the shortest such window, for up to 12
letters. 2000 cases, a third with 4 to 12 letters, a third with 16 to
100 and a third with 104 to 1000, `Q` drawn up to six times as often as
each other letter.

| | property |
|---|---|
| P1 | the statement read literally (up to 12 letters) |
| P2 | from 0 to `3n / 4` |
| P3 | the string reversed gives the same answer |
| P4 | the letters renamed (`Q` and `W` swapped, `E` and `R`) give the same answer |
| P5 | at least every letter's surplus over `n / 4`, summed |
| P6 | the ★ arm's answer |

P2's bound is a string of one letter, whose window must hold all but `n
/ 4` of it. P5 holds because every surplus letter must lie in the
window.

All 72,000 checks pass on every arm: `2000 cases: checksum 204549539,
72000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python gives the
same checksum, and replacing each window by every string of its length,
for up to 8 letters, the same answers.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a letter outside held below n / 4 | P1 649, P2 254, P6 9910 |
| S2 | ★: a balanced string not answered 0 | P1 18, P6 90 |
| L1 | lengths: the first window one short | P1 600, P2 56, P3 1015, P6 1503 |
| L2 | lengths: the wrong letter let out of the window | a runtime error, `index out of bounds` |
| X1 | prefix: at least one of each letter needed | P1 667, P2 472, P6 970 |
| X2 | prefix: the window one short | P1 649, P5 654, P6 1982 |
| C1 | counted: the right letter put back for the left | P1 380, P3 1751, P6 1629 |
| C2 | counted: shrunk at most once a step | P1 380, P3 1751, P6 1629 |
| B1 | bytes: R never tested | P1 98, P4 351, P5 199, P6 209 |
| B2 | bytes: the window from the second letter | P1 354, P3 926, P5 397, P6 1073 |
| H1 | hashmap: one letter over n / 4 allowed | P1 649, P5 813, P6 1982 |
| H2 | hashmap: the last length kept, not the least | P1 182, P3 1547, P6 1307 |

All twelve are caught. A mutation of the ★ arm fails P6 on the five
other arms, and P1, the statement read literally, catches every one but
L2, which never gets that far: letting the wrong letter out of the
window reads one letter past the end, and the differential stops with
"index out of bounds". S2, which answers 1 for a string already
balanced, fails only those 18 strings, all short enough for P1, since 1
is in bounds and above a surplus of 0. P2, the bound `3n / 4`,
catches the arms that ask too much of a window: every letter outside
below `n / 4` (S1), at least one of each letter in the window (X1). P5,
every surplus held, catches those that ask too little: a window one
short (X2), one letter over `n / 4` allowed (H1), R never tested (B1),
the first letter never in a window (B2). P3, the string reversed,
catches the arms whose answer depends on direction: the first window
one short (L1), the first letter left out (B2), the last length kept
rather than the least (H2), and C1 and C2, which answer alike on every
case, since putting back the right end's letter ends the shrinking after
one step just as shrinking once does. P4, the letters renamed, catches
B1 alone, the one mutation that treats one letter unlike the others.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, a sliding window shrunk while no letter outside it passes n / 4,
over 40 random strings of 10^5 letters, `Q` drawn up to four times as
often as the rest, drawn once and each solved 20 times. Every program
prints `40 strings of 10^5 letters, 20 passes: checksum 324505593`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.821 to 2.008 s | 1.908 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.811 to 1.984 s | 1.890 s |
| Rust (`rustc -O`) | 1.646 to 1.855 s | 1.693 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.675 to 1.793 s | 1.742 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 1.613 to 1.872 s | 1.707 s |
| C (`clang -O3`) | 1.588 to 1.732 s | 1.645 s |
| C (`clang -O3 -march=x86-64-v3`) | 1.973 to 2.172 s | 2.004 s |
| Go | 2.152 to 2.284 s | 2.198 s |
| Python | 52.30 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on is about 8% ahead of Kāra (1.742 s
against 1.890 s). C is about 13% ahead of Kāra (1.645 s against 1.890
s); Kāra is about 14% ahead of Go (1.890 s against 2.198 s). Python
takes about 28x Kāra's time. No profile was taken.
