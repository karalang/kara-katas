# 1220. Count Vowels Permutation

Given an integer `n`, count how many strings of length `n` can be formed
under the following rules:

- Each character is a lower case vowel (`'a'`, `'e'`, `'i'`, `'o'`, `'u'`).
- Each vowel `'a'` may only be followed by an `'e'`.
- Each vowel `'e'` may only be followed by an `'a'` or an `'i'`.
- Each vowel `'i'` may not be followed by another `'i'`.
- Each vowel `'o'` may only be followed by an `'i'` or a `'u'`.
- Each vowel `'u'` may only be followed by an `'a'`.

Since the answer may be too large, return it modulo `10^9 + 7`.

```
n = 1    ->  5          "a", "e", "i", "o", "u"
n = 2    ->  10         "ae", "ea", "ei", "ia", "ie", "io", "iu", "oi", "ou", "ua"
n = 5    ->  68
n = 144  ->  18208803
```

**Constraints:** `1 <= n <= 2 * 10^4`.

The arms are `fn count_vowel_permutation(n: i64) -> i64`. The two Rust
arms keep the method LeetCode gives Rust users, on `i32`, inside `impl
Solution`, and a one-line `count_vowel_permutation` calls it.

## Approaches

| file | mechanism |
|---|---|
| `count_vowels_permutation.kara` ★ | five running counts, the strings of the length so far that end in each vowel; a vowel's next count is the sum over the vowels that may come before it, all five updated at once by one multiple assignment. O(n) time, O(1) space |
| `count_vowels_permutation_table.kara` | every length's counts kept: a table of n rows of five, filled forward through the list of the vowels each may be followed by. O(n) space |
| `count_vowels_permutation_matrix.kara` | the rule as a 5 by 5 matrix, a 1 where one vowel may follow another, raised to the power n − 1 by repeated squaring; the answer is the sum of its entries. O(log n) |
| `count_vowels_permutation_memo.kara` | top-down: the strings of a length that start with a vowel are the sum, over the vowels that may follow it, of those one shorter that start with that one, each answer kept in a `Map[(i64, char), i64]`; the rule is a `match` from a vowel to the string of its followers. Recurses n deep |
| `count_vowels_permutation_slices.kara` | a Rust solution as LeetCode's Rust users write it (the counts in a `[i64; 5]`, a fresh `[0; 5]` each step filled forward through a `const FOLLOWS: [&[usize]; 5]` table, the total by `iter().sum::<i64>()`), carried to Kāra by `karac fix` |
| `count_vowels_permutation_chars.kara` | another Rust solution (the rule as a `HashMap<char, &str>` from each vowel to those that may come before it, collected from a list of pairs, and the counts as a `HashMap<char, i64>` rebuilt each step by `"aeiou".chars().map(..).collect()`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, four more properties |

Every arm prints the same 7 lines: LeetCode's three examples and `n = 1`,
a checksum of the answers for every `n` from 1 to 200 (`415921598`), and
the answers at `n = 10^4` (`76428576`) and at the constraints' top, `2 *
10^4` (`759959057`). `count_vowels_permutation.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac run` and `karac build`, and under the AddressSanitizer build.

The Mend loop: the table, matrix and memo arms check clean as written.
The ★ arm was first written with Rust's `let (mut a, mut e, ..)` and
`(a, e, ..) = (..)`, and the diagnostics' fixes made them `let mut (a, e,
..)` and `a, e, .. = ..`, Kāra's multiple assignment. The chars arm takes
one round of 14 fixes (among them `HashMap<char, &str>` to `Map[char,
Str]`, `before[&c]` to `before[c]`, and `sum::<i64>()` to `sum()`) and
checks clean. The slices arm takes one round of 15 fixes (`[&[usize]; 5]`
to `Array[Slice[usize], 5]`, `&[1]` to `[1]`, `[1i64; 5]` to `[1; 5]`,
`for &w in` to `for w in`) and then stops at its table: its rows differ in
length, so no `Array` holds them and Kāra has no constant for it.
`karac check` says so and names the type to build it with,
`Array[Vec[usize], 5]`, in the function that uses it; that move is the one edit made
by hand, and one more fix (a cast the result no longer needs) leaves it
clean.

## Gaps

Three, all fixed in kara at 2e40b2fffa.

- B-2026-11-18-60: the chars arm's `[('a', "eiu"), ..].into_iter().collect()`
  into a `Map[char, Str]` was refused (`FromIterator[(char, String)]` is
  not satisfied) with no fix, though the same list written straight into
  a `Vec[(char, Str)]` checks: design.md has a string literal be a `Str`
  where a `Str` is expected. The literal of `[..].into_iter().collect()`
  is now checked against the collected items, its numbers too (`[('a',
  200)]` into a `Vec[(char, u8)]` was refused the same way).
- B-2026-11-18-61: with that fixed, the chars arm printed the right answers under
  `karac run` and garbage under `karac build`: `m[k]` on a map whose
  values are views, `Map[char, Str]`, lent a pointer to the slot where
  the view itself belonged. It was there before this kata, for any
  `Map[_, Str]` or `Map[_, Slice[_]]` indexed in a built program.
- B-2026-11-18-62: the slices arm's `const FOLLOWS: Array[Slice[usize], 5] =
  [[1], [0, 2], ..]` was refused six times, once per list literal, with a borrow
  error about a temporary "which this function owns", a constant having
  no function. It is one error at the type now, saying why the table has
  no constant form and what to build instead; rows of one length get an
  `Array` of `Array`s as a machine fix.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every string of `n` vowels, as the `n` digits of a number in
base 5, kept when each letter may follow the one before it as the
statement words the rules, for `n` from 1 to 7 (`5 10 19 35 68 129
249`). 2000 cases, a third with `n` from 1 to 7, a third from 8 to 40 and
a third from 41 to 2000.

| | property |
|---|---|
| P1 | the statement read literally (`n` up to 7) |
| P2 | `c(n) = 3 c(n − 2) + c(n − 3) + c(n − 5)` modulo `10^9 + 7` (`n` from 6) |
| P3 | from 0 to `10^9 + 6` |
| P4 | below the modulus, every string grows by one to four letters: `c(n) <= c(n + 1) <= 4 c(n)` (`n` up to 29) |
| P5 | the ★ arm's answer |

P2 is the rule's matrix's characteristic polynomial, `x^5 − 3x^3 − x^2 −
1`: by Cayley–Hamilton every count satisfies it, whatever the vowels
begin with, and it is independent of how any arm counts. P4 holds because
every vowel may be followed by one to four others; past `n = 29` the
counts pass the modulus.

All 60,000 checks pass on every arm: `2000 cases: checksum 910370069,
60000 checks over 6 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's counts for
the same cases give the same checksum.

## Mutation testing

Twelve edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All
twelve are caught.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: u never follows i | P1 562, P2 1534, P5 9475 |
| S2 | ★: the total left unreduced | P2 863, P3 863, P5 4315 |
| T1 | table: i may follow i | P1 562, P2 1534, P4 83, P5 1895 |
| T2 | table: the answer read off the first row | P1 562, P2 1534, P5 1895 |
| M1 | matrix: the power one step short | P1 562, P2 95, P5 1895 |
| M2 | matrix: o may follow u | P1 562, P2 1534, P4 61, P5 1895 |
| D1 | memo: a remembered answer one too many | P1 456, P2 1534, P4 24, P5 1789 |
| D2 | memo: e followed by a only | P1 562, P2 1534, P5 1895 |
| L1 | slices: a count written over rather than added | P1 562, P2 1534, P5 1895 |
| L2 | slices: no string starts with u | P1 667, P5 2000 |
| C1 | chars: u never comes before a | P1 562, P2 1534, P5 1895 |
| C2 | chars: every one-letter count two | P1 667, P4 24, P5 2000 |

A mutation of the ★ arm fails P5 on all six arms, the ★ arm against the
other five. P1 catches every mutation but S2, whose total passes the
modulus only past `n = 7`; P3 catches S2 alone, and P2 with it, at the
863 cases where the unreduced total leaves the range. P2 catches every
mutation that changes the rule or the steps (S1, T1, M2, D2, C1, and T2,
L1, D1). It catches M1, whose answer is the count one length short, only
at `n = 6`, where it reads that arm's `n = 1`: elsewhere a count one
step behind satisfies the same recurrence. It misses L2 and C2, which
change only the one-letter counts, as it should, since the recurrence
holds whatever the counts begin with. P4 catches T1, M2, D1 and C2,
whose counts grow faster than the rule's. T1 gives `i` five followers.
The counts of T1, M2 and C2 pass the modulus at `n = 24`, 27 and 30,
against the rule's 31, inside the lengths P4 compares, and wrap; D1 adds
one at every length it remembers.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, five running counts, the strings of the length so far that end in
each vowel, for every n from 1 to 8000; checksum of the answers. Every
program prints `every n from 1 to 8000: checksum 304995047`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.187 to 0.203 s | 0.191 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.184 to 0.204 s | 0.189 s |
| Rust (`rustc -O`) | 0.184 to 0.195 s | 0.186 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.184 to 0.207 s | 0.190 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.184 to 0.196 s | 0.189 s |
| C (`clang -O3`) | 0.187 to 0.209 s | 0.198 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.185 to 0.201 s | 0.190 s |
| Go | 0.171 to 0.206 s | 0.177 s |
| Python | 7.023 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.190 s
against 0.189 s), and the two ranges overlap. C runs level with Kāra
(0.198 s against 0.189 s); Go is about 6% ahead of Kāra (0.177 s against
0.189 s). Python takes about 37x Kāra's time. No profile was taken.
