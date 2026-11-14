# 1153. String Transforms Into Another String

Given two strings `str1` and `str2` of the same length, determine whether
you can transform `str1` into `str2` by doing **zero or more
conversions**.

In one conversion you can convert **all** occurrences of one character in
`str1` to **any** other lowercase English character.

Return `true` if and only if you can transform `str1` into `str2`.

```
str1 = "aabcc",    str2 = "ccdee"     ->  true
str1 = "leetcode", str2 = "codeleet"  ->  false
```

**Constraints:** `1 <= str1.length == str2.length <= 10^4`; `str1` and
`str2` contain only lowercase English letters.

The arms are `fn can_convert(str1: Str, str2: Str) -> bool`.

## Approaches

A conversion moves all of one letter at once and letters never split, so
each letter of `str1` must meet one letter of `str2` wherever it stands.
That is enough when `str2` leaves some letter unused: a letter can wait
on that free letter while a cycle of conversions (`a` to `b` and `b` to
`a`) turns. When `str2` uses all 26 letters, the first conversion of any
string that also uses all 26 merges two of them for good, so only `str1
== str2` is reachable.

| file | mechanism |
|---|---|
| `can_convert.kara` ★ | arrays: the letter each letter of `str1` first meets kept in a `Vec` of 26, a second, different one refusing, and the letters of `str2` counted as they first appear. O(n) |
| `can_convert_map.kara` | a `Map[char, char]` from each letter of `str1` to the letter it first meets, checked at every later meeting, and the letters of `str2` in a `Set[char]`. O(n) |
| `can_convert_sorted.kara` | sorted lists: the pairs of letters at each place, sorted and `dedup`ed, so a letter going two ways shows as two neighbouring pairs with one first letter; and the letters of `str2` sorted and `dedup`ed. O(n log n) |
| `can_convert_build.kara` | by doing it: the conversions carried out on the string itself. A letter is converted once its target no longer waits, two waiting letters with one target are merged, and when only cycles wait, one letter of a cycle is parked on a letter the string does not hold and `str2` never uses. The answer is whether the string comes out as `str2`. O(26 n) |
| `can_convert_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `str1: String`, a `HashMap<char, char>` filled by `entry(a).or_insert(b)` and compared at every place, and `str2`'s letters counted by collecting a `HashSet`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, nine properties |

Every arm prints the same 15 lines: LeetCode's two examples; a swap
(`ab` to `ba`, true); a letter split in two (`aa` to `ab`, false); a
string with itself, of three letters and of all 26 (true); the 26 letters
sent one letter on (false, every letter used); 25 letters sent one on
(true, `z` free); the 26 letters with `a` sent to `b` (true); and the 26
letters and an `a`, sent one on with that `a` to `b` (false). Then 2000
random pairs of 1 to 60 letters, the first over 1 to 26 letters, sent
through a random map onto 1 to 26, one place changed with chance 0 to 7
in 8, with how many convert and a checksum (`2000 random pairs: 1322
convertible, checksum 243053464`), and four pairs of 10,000 letters, the
most the constraints allow: the 26 letters in turn sent one on (false),
the same with `y` and `z` both sent to `a` (true), a random string over
26 letters sent through a random map onto 25 (true), and that pair with
one place changed (false). `can_convert.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: a breadth-first search over the strings `str1` can become, one
conversion at a time. A letter in neither the string nor `str2` is as
good as any other such letter, so the search converts each letter of the
string to the letters of the string and of `str2` and to the first letter
outside both. It checks 2000 problems in four kinds of 500: strings of 1
to 8 letters over 1 to 4 letters sent through a random map onto 1 to 6, a
place changed in half; the same sent through a permutation of their
letters, cycles and all, a place changed in a quarter; strings of 26 to
60 letters holding all 26, sent through the identity, a permutation, a
permutation with two letters sent to one, or one of these with a place
changed; and strings of 10 to 60 letters over 5 to 26 letters sent onto 5
to 26. The search runs on the first two kinds, where 783 of the 1000
pairs convert. In the third kind `str2` uses all 26 letters in 306 pairs,
96 of them `str1` itself. Every random choice the properties make is
drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one (the two short kinds) |
| P2 | the places of both strings reordered alike give the same answer |
| P3 | the letters of both strings renamed alike give the same answer |
| P4 | the letters of `str1` alone renamed give the same answer, when `str2` leaves a letter free |
| P5 | each string twice gives the same answer |
| P6 | the first place repeated at the end of both gives the same answer |
| P7 | when `str1` converts to `str2` and `str2` to a third string, made from it by a random map, `str1` converts to the third |
| P8 | when `str2` uses all 26 letters, the answer is whether the strings are equal (letters never split) |
| P9 | a true answer stays true when `str2` is sent through a map onto 25 letters or fewer |
| P10 | a `str2` made from `str1` by a map that leaves a letter free, no place changed, is reached (969 pairs, 87 of them with 25 letters) |

P10 holds by the construction the build arm carries out: a letter whose
target no longer waits is converted, and one letter of each cycle is
first parked on the free letter. All 79,845 checks pass on every arm:
`2000 problems (783 of the 1000 short ones convertible): checksum
184370843, 79845 checks over 5 arms: 0 failures`. A Python reading of the
same problems, by the same search, with the properties asserted against
the ★ arm's mirror, gives the same line.

## Mutation testing

Thirty-five edits to the differential, seven to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Thirty-two are caught; three are
equivalent. The map arm letting a full `str2` through when `str1` leaves
a letter free changes nothing, since a letter of `str1` meets one letter
of `str2`, so a `str2` of 26 letters comes only from a `str1` of 26. The
build arm parking a letter on a letter `str2` uses but the string does
not hold, and leaving a letter it converts onto marked as absent, change
nothing either: the parked letter waits for its own target before any
letter is converted onto it, and a letter marked absent is only ever
offered as a parking place, which a letter `str2` uses is not when the
spare must be one `str2` never uses. Twenty-four are kept, no two failing
the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `str2` of all 26 letters let through | P8 110 |
| M2 | ★: equal strings not let through first | P8 96 |
| M3 | ★: a letter's first meeting kept as itself | P1 375, P2 31, P4 266, P5 259, P6 208, P7 7, P9 327, P10 629 |
| M4 | ★: the letters of `str1` counted, not `str2`'s | P9 96, P10 87 |
| M5 | ★: the first place never read | P1 66, P2 111, P5 114, P6 114, P8 43 |
| M6 | ★: two letters must be left free | P10 87 |
| M7 | ★: a letter may go two ways | P1 217 |
| M8 | map: the map read at `str2`'s letter | P1 292, P2 101, P4 389, P5 53, P6 42, P7 23, P9 140, P10 502 |
| M9 | map: the first place never read | P1 66, P2 76, P5 71, P6 71 |
| M10 | map: the pair stored backwards | P1 254, P2 116, P4 334, P5 100, P6 76, P7 45, P9 196, P10 456 |
| M11 | sorted: repeated pairs kept | P1 369, P4 191, P5 189, P6 189, P9 263, P10 651 |
| M12 | sorted: two letters going to one refused | P1 292, P3 341, P4 351, P7 66, P9 379, P10 306 |
| M13 | sorted: the pairs left unsorted | P1 45, P2 100, P5 17, P6 17 |
| M14 | sorted: the first two pairs never compared | P1 157, P3 92, P4 100 |
| M15 | sorted: the letters of `str2` counted with repeats | P5 97, P6 6, P9 96, P10 261 |
| M16 | sorted: `str2` read backwards | P1 222, P2 73, P4 47, P6 120, P9 129, P10 520 |
| M17 | build: no two letters merged | P4 34, P7 7, P9 43, P10 86 |
| M18 | build: the string never compared with `str2` | P1 217, P2 3, P3 3, P8 17 |
| M19 | build: a merge run the wrong way | P1 12, P3 4, P4 137, P7 54, P9 132, P10 180 |
| M20 | build: the parked letter forgets its target | P1 135, P3 51, P4 220, P7 17, P9 23, P10 221 |
| M21 | build: a letter converted while its target waits | P1 182, P3 88, P4 279, P7 31, P9 141, P10 456 |
| M22 | solution: the map keyed by `str2`'s letter | P1 282, P9 231, P10 408 |
| M23 | solution: a letter going two ways answers true | P1 217, P8 100 |
| M24 | solution: the last place never read | P1 66, P2 79, P5 74, P6 74 |

P1 and P10 catch eighteen of the thirty-two each, P9 sixteen, P4 eleven,
P5, P6 and P8 nine or ten, P2 and P7 eight, and P3 six. Three families
are seen by one property alone. The edits that let a full `str2` through
or stop letting equal strings through, in three arms each, change
answers only when `str2` uses all 26 letters, which the short kinds
never reach, and P8 alone holds the answer there. The edits that need
two free letters change answers only when `str2` uses exactly 25: P10
was added for them after a first run in which both survived, and 87 of
the pairs it covers have a `str2` of 25 letters. And a letter allowed to
go two ways (M7) breaks no property that compares the arm with itself,
since every reordering, renaming and doubling keeps the clash or keeps
it away; P1 sees it on the short pairs. P3, renaming every letter alike,
catches only the edits that read the letters' order or their positions
in the alphabet: the sorted arm's neighbours and the build arm's choice
of which letter to convert.

Of the eight caught and not kept, each fails exactly as a kept one: the
map and solution arms letting a full `str2` through, as M1, and not
letting equal strings through first, as M2; the map, sorted and solution
arms counting the letters of `str1`, as M4; and the solution arm needing
two free letters, as M6.

## Verification

Every arm prints the same output as `can_convert.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any file, and `karac fix` has nothing to apply.

The ★, map, sorted and build arms were written as Kāra. `karac fix`
added `.to_vec()` where the sorted arm sorts the letters of `str2.bytes()`,
a read-only view, and where the harness changes a place of `b.bytes()`;
and dropped the build arm's `as i64` on a byte difference stored in an
`i64` slot. `karac fix` carried the solution arm in three rounds:
`HashMap<char, char>` to `HashMap[char, char]`, `HashMap::new()` to
`HashMap.new()`, `collect::<HashSet<char>>()` to
`Set[char].from_iter(str2.chars())`, the adapter's `&str` to `Str` and
`Solution::` to `Solution.`, and the `use std::collections` line
dropped; then `struct Solution {}` declared and `HashMap` renamed `Map`;
then the harness's `.to_vec()`.

The kata found one gap. The build arm binds `let mut s = str1.bytes();`
and passes it as `convert(mut s, x, y)` to a `mut ref Vec[u8]`
parameter. That was refused with only "expected 'mut ref Vec[u8]', found
'Slice[u8]'" and no fix: `let mut` does not make a view writable, and
`.to_vec()` at the argument would hand the callee a copy whose changes
are lost. `karac check` now says that `s` is a read-only view and offers
`.to_vec()` where `s` is bound, one edit for every such call
(B-2026-11-14-29, fixed).

## Benchmarks

`bench/` times the ★ arm against the same arrays in C, Rust, Go and
Python. 64 pairs of 10,000 letters, LeetCode's longest, are built once in
four kinds in turn: the first string random over 26 letters sent through
a random map onto 25 (true, read to the end); the same with one place
then changed (false, read to that place); sent through a random
permutation of the 26 (false, read to the end before the count of
letters refuses it); and the string with itself (true, at the first
comparison). Each of 100,000 rounds answers one pair, in turn. Every
program prints `100000 rounds over 64 pairs of 10000 letters: 50000
convertible, checksum 43304648`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `9bedd8500a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.392 to 0.473 s | 0.404 s |
| C (`clang -O3`) | 0.477 to 0.582 s | 0.495 s |
| Go | 0.553 to 0.643 s | 0.582 s |
| Rust (`rustc -O`) | 0.560 to 0.624 s | 0.592 s |
| Kāra (`karac build`) | 0.703 to 0.816 s | 0.734 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.708 to 0.813 s | 0.745 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.705 to 0.787 s | 0.746 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.717 to 0.802 s | 0.748 s |
| Python | 46.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; a plain `karac build` gives the same binary, byte
for byte. Kāra ties overflow-checked Rust, the equal-safety comparison.
Rust without the checks takes about 0.79x Kāra's time, Go about 0.78x
and C about 0.54x to 0.66x; Python takes about 62x. The loop does
little per letter: two subtractions of `b'a'`, which the checked builds
test for underflow, two array reads and writes, which every language
but C bounds-checks, and a count. That the checks account for the gap to
C and unchecked Rust is inferred, not measured.
