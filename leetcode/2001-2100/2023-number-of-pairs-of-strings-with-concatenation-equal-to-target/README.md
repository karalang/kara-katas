# 2023. Number of Pairs of Strings With Concatenation Equal to Target

You are given an array of digit strings `nums` and a digit string
`target`. Return the number of pairs of indices `(i, j)`, `i != j`, such
that `nums[i] + nums[j]`, the two strings joined, equals `target`.

```
nums = ["777","7","77","77"],  target = "7777"  ->  4
nums = ["123","4","12","34"],  target = "1234"  ->  2
nums = ["1","1","1"],          target = "11"    ->  6
```

**Constraints:** `2 <= nums.length <= 100`; `1 <= nums[i].length <= 100`;
`2 <= target.length <= 100`; `nums[i]` and `target` hold digits only and
have no leading zeros.

A pair is ordered: `(i, j)` and `(j, i)` are two pairs, and both count when
both joins are the target. A pair joins to the target exactly when it cuts
the target into a prefix and the rest, so the target's cuts, at most 99,
are what to count over.

## Approaches

| file | mechanism |
|---|---|
| `pairs.kara` ★ | each string counted in a `Map`; the target cut at every point into `target[0..k]` and `target[k..]`, a cut into two different strings giving `count(a) * count(b)` pairs and into one string twice `count(a) * (count(a) - 1)`. O(n L + L^2) |
| `pairs_brute.kara` | every ordered pair of two different places, the strings joined by an f-string and compared with the target. O(n^2 L) |
| `pairs_ends.kara` | no string built: a pair fits when its lengths add up to the target's and the target `starts_with` the first and `ends_with` the second; the pairs as indices `0..n * n` through `filter` and `count` |
| `pairs_seen.kara` | one pass with a `Map` of the strings seen so far: a new string pairs with each earlier one it starts the target before (`strip_prefix`) and with each it ends the target after (`ends_with`), so every ordered pair is counted when its later string arrives. O(n L) |
| `pairs_sorted.kara` | the counts in a `SortedMap`, walked by its distinct strings: each one the target starts with pairs with the rest |
| `pairs_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, a unit struct, `impl Solution`, `for s in &nums`, `target.split_at(i)`, `*count.get(a).unwrap_or(&0)`, a `&Vec` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the total and a checksum of the counts for
3000 problems of 2 to 10 strings of 1 to 4 digits from 1-2, the target
with even odds two of them joined, and for 5 problems of 100 strings of up
to 100 digits, among them runs of 7s against targets of 2 to 199 7s.
`pairs.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every ordered pair of two different places whose strings,
joined with `push_str`, are the target. It checks 1500 problems of 2 to 10
strings of 1 to 4 digits from 1 to 1-3, with a target that with even odds
is two of them joined (perhaps one with itself), else 2 to 8 digits. Every
random choice of a problem is drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the strings in reverse order leave the count |
| P3 | every string listed twice makes the count `4c + 2d`, where `d` counts the strings that joined with themselves are the target |
| P4 | every string and the target written backwards leave the count |
| P5 | the target itself added to the list leaves the count |
| P6 | each arm agrees with at least three of the other five |

P3 holds because a pair of places in the doubled list is a pair of the
list taken from either copy of each, four ways, or a string with its own
copy, both ways. P4 holds because `a + b` written backwards is `b`
backwards then `a` backwards, so the pair `(i, j)` becomes `(j, i)`. P5
holds because every string is at least one digit long, so the target can
only be joined with a string to make something longer than itself.

The differential prints `1500 problems: checksum 252252886, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Sixteen are kept, two or
three to each arm. All thirty are killed, each fails the same way under
both backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a string allowed to pair with itself | P1 373, P3 373, P6 373 |
| M2 | ★: the same pair counted once, not in both orders | P1 169, P3 373, P6 169 |
| M3 | ★: the right part one digit short | P1 654, P3 395, P4 290, P6 654 |
| M4 | brute: the first string joined to itself | P1 977, P5 373, P6 977 |
| M5 | brute: the last string never the first of a pair | P1 361, P2 403, P3 405, P4 176, P5 361, P6 361 |
| M6 | brute: a pair that only starts the target accepted | P1 723, P3 616, P4 378, P6 723 |
| M7 | ends: the lengths never compared | P1 920, P3 733, P5 1390, P6 920 |
| M8 | ends: the second string found anywhere | P1 140, P3 141, P4 232, P6 140 |
| M9 | seen: the suffix half never tried | P1 662, P2 368, P3 740, P4 368, P6 662 |
| M10 | seen: the head one digit long | P1 727, P2 745, P3 908, P4 408, P5 907, P6 727 |
| M11 | seen: a string seen only the first time | P1 281, P2 219, P3 760, P6 281 |
| M12 | sorted: the walk stopped at the first prefix | P1 491, P3 194, P4 189, P6 491 |
| M13 | sorted: the rest taken from one place early | P1 824, P3 568, P5 1040, P6 824 |
| M14 | Rust: two halves of one length taken as equal | P1 98, P3 141, P4 34, P6 98 |
| M15 | Rust: the right count read at the left | P1 886, P4 552, P6 886 |
| M16 | Rust: the left count squared on a match | P1 240, P4 123, P6 240 |

P1 and P6 kill all sixteen, P3 thirteen, P4 ten, P5 five and P2 four. P3
lists every string twice; it misses only the edits whose error scales
with the list as the count does (M4, M15, M16), and sees every edit that
mishandles a string paired with its own copy (M1, M2) or a count that
should multiply (M11). P4 writes every string and the target backwards,
which turns a prefix into a suffix; it sees the edits that treat the two
halves unevenly: a right part cut short (M3), the last string never first
(M5), a pair that only starts the target (M6), a second string found
anywhere (M8), the suffix half never tried (M9), a one-digit head (M10),
the walk stopped at the first prefix (M12), and the Rust arm's halves
equal by length, its right count read at the left and its left count
squared (M14 to M16). P5 adds the target itself
to the list, which no correct arm pairs with anything; it sees the edits
that let a string as long as the target, or longer, into a pair: a string
joined to itself (M4), the last string skipped as a first (M5), the
lengths never compared (M7), a one-digit head (M10), a rest taken a place
early (M13). P2 reverses the list, which only the edits that read its
order see: the last string never first of a pair (M5), and the one-pass
seen arm's suffix half never tried, its one-digit head and a string seen
only the first time (M9 to M11).

The other fourteen fail as a kept one does, or with counts of their own.
The brute and ends arms letting a string pair with itself fail as M1; the
sorted arm counting a string paired with itself once and skipping a
prefix that is its own rest fail as M2; the Rust arm counting a repeated
string once and the ★ arm doing the same fail alike (P1 494, P3 994).
With counts of their own: the ★ arm's last cut never tried (P1 338), the brute arm's pairs
with `i` before `j` only (P1 631), the ends arm's second string tested as
a prefix (P1 392) and lengths compared with one to spare (P1 653), the
seen arm's string counted before its own pairs (P1 994) and prefix half
only for the first string (P1 256), the sorted arm's counts of the rest
ignored (P1 122), and the Rust arm's cut one digit early (P1 158).

Five drafts were replaced. Four survived, all equivalent: the brute arm
joining each pair the other way round (every ordered pair is tried, so
the swap counts the same pairs), the ends arm's indices one short (the
last index is the pair of the last string with itself, which never
counts), the Rust arm's cut starting at 0 (the empty first part is no
string's) and its two parts swapped (`ca * cb` is the same product). The
sorted arm reading the rest as the string itself when the halves are the
same length did not check: `if .. { a } else { target[..] }` joins a
`ref String` and a `Str`, which Kāra refuses as Rust does.

## Verification

Every arm prints the same output as `pairs.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 0.4 s to 0.8 s (ends) and the
differential 3.8 s.

Four of the five arms were written in Kāra and checked clean with no fix.
The ends arm read its two strings as `let a = nums[p / n]`, which moves out
of an index; `karac fix` borrows them, `let a = ref nums[p / n]`, since
they are only read.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in four rounds (15, 2, 2 and 2 edits),
with two compiler changes made for it. The first round carries the unit
struct, the `Vec<..>` and `HashMap<..>` types, the `::` paths, `&nums`,
the `&0` in `unwrap_or(&0)` and the `&Vec`/`&String` wrapper, and drops
the `use`; the second renames `HashMap` to `Map`; the third writes `ans:
i32`, since `let mut ans = 0` kept its default `i64` beside the `i32`
counts and the method's `i32` return then refused it, and drops the
wrapper's `as i64`, a widening Kāra does by itself; the fourth drops the
wrapper's `ref`s. `target.split_at(i)` had no Kāra method to call: `Str`
and `String` gained `split_at` for this kata (kara `2653d79ae4`), and
the `ans: i32` round is Thread C's fix for B-2026-11-08-20 (kara
7ae9bc82c0).

## Benchmarks

The bench builds 300 problems of 100 strings once in all five languages:
each string some copies of a block of 1 to 3 digits, up to 100 digits, and
the target 2 or more copies of the same block, up to 100 digits, so most
cuts find strings on both sides. It runs the ★ arm on each for 20 rounds:
6000 calls. Every implementation prints `6000 calls: 589160 pairs,
checksum 571465996`. Every language counts the strings in a hash map of
owned copies (C with an open addressing table and FNV-1a) and looks up
the target's two parts as slices, as the Kāra program does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.072 to 0.090 s | 0.079 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.089 to 0.112 s | 0.092 s |
| Kāra (`karac build`) | 0.089 to 0.132 s | 0.097 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.102 to 0.132 s | 0.109 s |
| Rust (`rustc -O`) | 0.105 to 0.153 s | 0.110 s |
| C (`clang -O3`) | 0.108 to 0.127 s | 0.111 s |
| Python | 0.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.094 s) is not above its real time (0.097 s).

The sequential Kāra program is 0.84x Rust under overflow checks and 0.83x
C.