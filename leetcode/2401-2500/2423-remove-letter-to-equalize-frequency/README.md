# 2423. Remove Letter To Equalize Frequency

You are given a **0-indexed** string `word`, consisting of lowercase
English letters. You need to select **one** index and **remove** the
letter at that index from `word` so that the **frequency** of every
letter present in `word` is equal.

Return *`true` if it is possible to remove one letter so that the
frequency of all letters in `word` are equal, and `false` otherwise*.

**Note:**

- The **frequency** of a letter `x` is the number of times it occurs in
  the string.
- You **must** remove exactly one letter and cannot choose to do
  nothing.

```
word = "abcc"  ->  true
word = "aazz"  ->  false
```

**Constraints:** `2 <= word.length <= 100`; `word` consists of lowercase
English letters only.

Only the letters' counts matter, and removing a letter lowers one count
by one. There are at most 26 counts, so trying each held letter in turn
and comparing what is left costs a few hundred steps, whatever the word.

## Approaches

| file | mechanism |
|---|---|
| `equalize.kara` ★ | the 26 letter counts in an `Array[i64, 26]`; each held letter taken away once in turn, and the counts left that are not zero compared with the first of them. O(n + 26^2) |
| `equalize_naive.kara` | the statement tried directly: each index removed in turn, the word left counted afresh into a `Map[u8, i64]`, and its counts compared. O(n^2) |
| `equalize_cases.kara` | the cases, read off the held counts sorted: one letter; every letter held once; one letter held once and the rest all equally; or one letter held once more than the rest, all equal. O(n + 26 log 26) |
| `equalize_map.kara` | maps: a `Map[char, i64]` of the counts and a `Map[i64, i64]` of how many letters hold each count; taking a letter away moves it to the next lower count, and the word is good when one count is left, zero aside. O(n + 26) |
| `equalize_iter.kara` | iterators: the counts by `fold`, then `any` held letter whose count, one less, leaves every held count equal, by `map`, `filter` and `all`. O(n + 26^2) |
| `equalize_solution.kara` | LeetCode's Rust template: a `[0; 26]` count array indexed by `(c as u8 - b'a') as usize`, and the counts left after each removal gathered into a `HashSet` through `filter(\|&&x\| x > 0)`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's two examples; two
letters; one letter twice; one letter held once more than the rest; one
letter held once and the rest twice; one letter held twice more than the
rest; every letter once; then 3000 random words of 2 to 100 letters from
the first 1 to 6, each letter a copy of the one before with probability
1 in 1 to 3; and 3000 built one letter from equal, a few letters each
held the same number of times, then one letter added or taken away,
shuffled. Each set of 3000 prints how many were true and a checksum of
the answers in order. `equalize.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 20000 random words of up
to 10 letters against every removal counted by Python's `Counter`.

`check` first reports 4 errors on the template, and `karac fix` carries
it in one call, reporting 7 edits: the `use std::collections::HashSet;`
line deleted, with `HashSet` written `Set`; the brackets of
`HashSet<i32>`; the `&&` of the pattern `|&&x|` dropped; `struct
Solution;` given its braces; and `c as u8` written `c as u32 as u8`,
since Kāra refuses to cast a `char` straight to `u8`, its range not
fitting in 8 bits, and asks for the truncation through `u32` to be
written out (`E_CHAR_AS_NARROW_INT`), which `check` reports once the
template parses.
`[0; 26]`, `as usize`, `iter().filter(..).cloned().collect()` and
`set.len() <= 1` stand as Kāra.

The harness's near words drop a letter at random, and the first version
could leave a word of one letter, below the constraints, when the
starting word was a single letter: the ★ arm, which takes the word with
nothing left as good, and the map arm, which does not, then disagreed.
The harness now pads such a word to two letters.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each index removed in turn, and for every letter of the word
left, its count found by a walk of that whole word; good when every
count matches the first. No count array is kept. It checks 300 random
words of 2 to 12 letters from the first 1 to 4; then 30 of up to 100
letters from all 26; then 30 built one letter from equal, as the
harness builds them. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the letters sorted: the same answer |
| P3 | every letter renamed to the next, `z` to `a`: the same answer |
| P4 | the word reversed: the same answer |
| P5 | a letter the word lacks added once, when one is: true whenever every letter of the word is held the same number of times |
| P6 | each arm agrees with at least three of the other five |

P2, P3 and P4 hold because the answer depends only on the letters'
counts, which sorting, renaming one-to-one and reversing all keep. P5
holds because removing the added letter leaves the word itself.

The differential prints `360 cases: checksum 503104899, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts every letter with `str.count`. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a letter not held taken away | P1 18, P6 18 |
| M3 | ★: only a larger count refused | P1 91, P3 3, P6 91 |
| M5 | ★: the letter taken away twice | P1 76, P6 76 |
| M7 | naive: the removed index kept | P1 94, P5 121, P6 94 |
| M9 | naive: the last index never removed | P1 5, P2 16, P4 12, P5 101, P6 5 |
| M11 | naive: every letter counted once | P1 163, P6 163 |
| M13 | cases: one letter alone not taken as good | P1 103, P6 103 |
| M14 | cases: the rest never checked beside a lone letter | P1 81, P6 81 |
| M15 | cases: only the second count checked below the top | P1 26, P6 26 |
| M17 | map: a count emptied kept | P1 179, P5 121, P6 179 |
| M18 | map: the letter moved up, not down | P1 22, P6 22 |
| M20 | map: each count held by one letter | P1 60, P5 18, P6 60 |
| M23 | iter: the count one more, not less | P1 57, P5 107, P6 57 |
| M24 | iter: zero counts compared | P1 197, P5 139, P6 197 |
| M25 | iter: only a smaller count refused | P1 116, P3 9, P6 116 |
| M27 | solution: the count never restored | P1 52, P6 52 |
| M29 | solution: two counts left taken as good | P1 132, P6 132 |


P1 and P6 kill all seventeen, P5 six, P3 two, and P2 and P4 one each.

Fourteen are not kept. Six fail exactly as a kept one: the ★ arm's
count never restored (M2) as the template's (M27); the ★ arm's zero
count compared and the template's zero counts in the set (M4, M28) as
the iter arm's zero counts compared (M24); the map arm's two counts
left taken as good (M21) as the template's (M29); the iter arm's every
letter tried, held or not (M22) as the ★ arm's letter not held taken
away (M1); and the iter arm's every letter counted as `a` (M26) as the
naive arm's every letter counted once (M11). Four fail apart from every
kept one and were left out because those arms keep their share
already: the cases arm's gap of two taken (M16), the map arm's letter
held once moved to zero (M19), and the template's `a` never tried and
each letter counted twice (M30, M31).

Two survive. The cases arm's every letter once not taken as good (M12)
is equivalent: a word of `k > 1` letters each held once is still taken
by the next test, one letter held once and the rest at the top, and a
word of one letter by `k == 1`. The ★ arm's `z` never tried is not
equivalent, `aabbz` tells it apart, but only the 30 words drawn from
all 26 letters can hold a `z`, and none of them is one letter from
equal. Two more fail differently from one run to the next, under
either backend: the naive arm's only the first two counts compared and
count of one let pass (M8, M10) read its counts in the order of a
`Map`, which is random per process.

## Verification

Every arm prints the same output as `equalize.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 to 1.6 s, but for the naive
arm, which takes 14 s there and 0.6 s under `karac run`: it builds a
`Map` of counts afresh for every index it removes, and the interpreter
pays for each hash and insert. The differential takes 4.0 s under
`karac __mir-run`, 1.3 s under `karac __mir-llvm-asan` and 0.9 s under
`karac run`.

## Benchmarks

The bench builds `10^4` words once from its own generator: each starts
as 1 to 20 letters held 1 to 5 times each, has one letter added or
taken away, and is shuffled. It then makes 200 passes, answering every word and folding
the answer and the pass into the checksum. The bench uses the ★ arm,
the 26 counts with each held letter taken away in turn, in all five
languages. Every implementation prints `200 passes over 10^4 words:
checksum 832881492`. The counts are a fixed array of 26 in every
language but Python, whose list is made afresh for every word, and the
words are bytes.

BENCHTAB
