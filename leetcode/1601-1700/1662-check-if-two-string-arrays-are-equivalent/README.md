# 1662. Check If Two String Arrays are Equivalent

Given two string arrays `word1` and `word2`, return `true` *if the two
arrays **represent** the same string, and* `false` *otherwise.*

A string is **represented** by an array if the array elements
concatenated **in order** forms the string.

```
word1 = ["ab", "c"], word2 = ["a", "bc"]             ->  true
word1 = ["a", "cb"], word2 = ["ab", "c"]             ->  false
word1 = ["abc", "d", "defg"], word2 = ["abcddefg"]   ->  true
```

**Constraints:** `1 <= word1.length, word2.length <= 10^3`;
`1 <= word1[i].length, word2[i].length <= 10^3`;
`1 <= sum(word1[i].length), sum(word2[i].length) <= 10^3`; `word1[i]`
and `word2[i]` consist of lowercase letters.

## Approaches

| file | mechanism |
|---|---|
| `equivalent.kara` ★ | two cursors, each a word and a place in it, stepped together a letter at a time; no text is built. O(n) time, O(1) space |
| `equivalent_concat.kara` | the statement as written: each array joined with `concat()`, the two texts compared. O(n) time and space |
| `equivalent_chars.kara` | each array's letters as one lazy stream, `flat_map` over the words' `chars()`, the two streams compared with `Iterator.eq`. O(n) time, O(1) space |
| `equivalent_solution.kara` | a Rust solution as LeetCode's Rust users write it (two `flat_map` iterators stepped by hand with `next()`, matched as a pair with a guard), carried by `karac fix`, which made 5 changes in one pass |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (a word against its letters, a second array one word longer, and
one letter apart in the last word), then the equal pairs and a checksum
for 3000 random pairs of up to 12 letters, 300 of up to 1000 and 10 of
up to `10^5`. A random pair is a text of letters from the first one to
three of the alphabet, cut into words at random; half the pairs spell
the same text twice, and half spell it and a copy with one letter
changed, dropped, or added at the end. `equivalent.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: each array's words concatenated in order, a letter at a time,
and the two strings compared. It checks 3000 random pairs of up to 12
letters, drawn as above, each with the second array's text cut again
into other words.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the arrays swapped give the same answer |
| P3 | the second array's text cut into other words gives the same answer |
| P4 | every letter moved one along the alphabet gives the same answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 832357784, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: equal once either array is used up | P1 801, P5 801 |
| M2 | ★: the second cursor's word ended by the first word's length | panics, index out of bounds |
| M3 | ★: a word's first letter never compared | P1 248, P2 146, P5 248 |
| M4 | concat: the two texts compared by length | P1 474, P5 474 |
| M5 | concat: the second text a prefix of the first | P1 253, P2 801, P5 253 |
| M6 | chars: the streams zipped, so the longer one's tail is never seen | P1 801, P5 801 |
| M7 | chars: the first array's words read backwards | P1 721, P2 190, P5 721 |
| M8 | template: equal once the first stream ends | P1 548, P2 801, P5 548 |
| M9 | template: any two letters taken as equal | P1 474, P5 474 |
| M10 | template: on a difference, equal if the first stream has ended | P1 947, P2 44, P5 947 |

## Benchmarks

The bench draws 20 pairs of word arrays spelling texts of `10^6` letters
`a` and `b`, a thousand times LeetCode's largest, cut into words of about
8 letters; half the pairs spell the same text, and half differ in the
very last letter, so every check walks the whole text. All are built
first, then each pair is checked 20 times by the ★ arm in all five
languages: Kāra's `Vec[String]`, Rust's `&[String]`, Go's `[]string`,
Python's list of `str`, and C's array of heap strings with their
lengths. Every implementation prints `20 pairs of 1000000 letters, 20
rounds: 200 equal, checksum 960240790`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 1.874 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.206 s |
| Rust (`rustc -O`) | 2.291 s |
| Kāra (`karac build`) | 2.406 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 2.412 s |
| Go | 3.045 s |
| Python | 75 s |

The sequential Kāra build takes 1.05x Rust's time and 1.09x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 1.874 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (2.296 s and
2.476 s on one run).

## Verification

All four arms print the same output as `equivalent.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm was first written with Rust's `let (mut w1, mut i1) = (0,
0);` and `.as_bytes()`, and `karac fix` made it `let mut (w1, i1) = (0,
0);` and `.bytes()`. The concat and chars arms checked clean as first
written.

The differential names its arms with `fn arm_name(k: i64) -> Str {
["the ★ arm", "concat", "chars", "solution"][k] }`, and the check refused
it: "expected 'Str', found 'String'". A list of string literals was a
`Vec[String]` however its element was used, and `karac fix` appended
`.as_str()`, which only traded the error for E0509, a view of a temporary
returned. That was B-2026-11-19-131, fixed in kara `67cd85419b`: where a `Str` is
wanted, the literals of an indexed list take `Str`, as each would alone,
and the element read is a view of static text.
