# 2053. Kth Distinct String in an Array

A distinct string is a string that is present only once in an array.
Given an array of strings `arr` and an integer `k`, return the `k`th
distinct string present in `arr`. If there are fewer than `k` distinct
strings, return an empty string `""`. The strings are considered in the
order in which they appear in the array.

```
arr = ["d","b","c","b","c","a"], k = 2  ->  "a"
arr = ["aaa","aa","a"], k = 1           ->  "aaa"
arr = ["a","b","a"], k = 3              ->  ""
```

**Constraints:** `1 <= k <= arr.length <= 1000`; `1 <= arr[i].length <=
5`; `arr[i]` consists of lowercase English letters.

Whether a string is distinct depends on the whole array, but which one is
the `k`th depends on the array's order. So every approach first learns how
often each string occurs, by counting, by comparing, or by sorting, and
then takes the distinct ones in the array's order. A hash map's or set's
own order never decides the answer: it is per-process random in Kāra, so
an arm that walked one would print a different string on each run.

## Approaches

| file | mechanism |
|---|---|
| `distinct.kara` ★ | every string counted into a `Map[String, i64]`, then the array walked in its own order, counting `k` down over the strings counted once |
| `distinct_brute.kara` | the statement read directly: each string's occurrences counted by a scan of the whole array, `filter` and `count`, and the `k`th that occurs once returned. A million comparisons at the constraints' limit |
| `distinct_sets.kara` | two `Set`s in one pass, `seen` and `repeated`, the second fed when `insert` into the first finds the string already there; then the strings not repeated, in the array's order, through `filter` and `nth` |
| `distinct_sorted.kara` | the indices sorted by their strings with `sort_by` and `cmp`, so equal strings sit together; a run of one is a distinct string, and those indices, sorted back into the array's order, give the `k`th |
| `distinct_places.kara` | a `SortedMap[String, (i64, i64)]` from each string to where it first and last occurs; a string is distinct when the two are the same, and those first places, sorted, give the `k`th |
| `distinct_solution.kara` | LeetCode's Rust template (`use std::collections::HashMap`, a `HashMap<&str, i32>` filled with `*cnt.entry(s.as_str()).or_insert(0) += 1` over `&arr`, then a count-down of `k` over the strings seen once), carried by `karac fix` in two rounds to a clean check |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four more,
each array, `k` and its answer; then how many answers were found and a
checksum of them for 2000 random arrays of 1 to 30 strings of up to 3
letters, from 2 to 5 letters of the alphabet so that strings repeat; then
the same for 200 arrays of 1000 strings of up to 5 letters, the
constraints' limit, from 2 to 26 letters of the alphabet. `distinct.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the distinct strings listed in the order they appear, each
compared with every other place in the array, and the `k`th of the list
taken. It checks 500 random arrays of 1 to 30 strings, drawn before any
arm answers, each asked for every `k` from 1 to its length.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is `""` or a string that occurs in the array exactly once |
| P3 | the answers for `k` and `k + 1` are both `""`, or the one for `k + 1` is `""`, or both are strings and the one for `k` comes first in the array |
| P4 | a new string put at the end leaves a string answer the same |
| P5 | the array twice over has no distinct string: the answer is `""` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `500 arrays: checksum 500318750, 286632 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the `k`th string seen at most twice | P1 2880, P2 1386, P3 620, P5 3811, P6 2880 |
| M2 | ★: the last string returned when there is no `k`th | P1 5707, P2 4694, P3 6060, P4 5707, P5 7962, P6 5707 |
| M3 | ★: every string counted down, not only the distinct | P1 2806, P3 1004, P6 2806 |
| M4 | brute: no answer written as a dash | P1 5707, P2 5707, P3 6099, P4 435, P5 7962, P6 5707 |
| M5 | brute: the `(k-1)`th distinct string | P1 2582, P3 392, P6 2582 |
| M6 | brute: strings compared by length | P1 2208, P6 2208 |
| M7 | sets: every string kept, not only those not repeated | P1 7506, P2 5707, P3 3127, P5 7962, P6 7506 |
| M8 | sets: the strings repeated taken instead | P1 6406, P2 5707, P3 2976, P5 7962, P6 6406 |
| M9 | sets: the first string when there is no `k`th | P1 5707, P2 4832, P3 6099, P4 435, P5 7962, P6 5707 |
| M10 | sorted: runs of two taken as distinct | P1 2187, P2 693, P5 2255, P6 2187 |
| M11 | sorted: a run ended by its next string's length | P1 1917, P6 1917 |
| M12 | sorted: the indices never sorted by their strings | P1 5526, P2 3788, P3 1755, P5 7451, P6 5526 |
| M13 | places: a string distinct when it first and last occur apart | P1 2908, P2 1583, P5 3838, P6 2908 |
| M14 | places: the last place kept as the first | P1 2619, P2 1583, P3 931, P5 3838, P6 2619 |
| M15 | places: every string distinct | P1 3382, P2 1583, P5 3838, P6 3382 |
| M16 | solution: the adapter asking for the first | P1 5505, P3 5897, P6 5505 |
| M17 | solution: the count-down over every string | P1 1863, P6 1863 |

P1 and P6 kill all seventeen, P2, P3 and P5 eleven each, and P4 three.
P2 and P5 catch an arm that takes repeated strings for distinct ones (M1,
M7, M8, M10, M12 to M15); P5 asks for a string when none is distinct, so
it also catches an arm that answers something when there is no `k`th (M2,
M4, M9). P3 catches answers that are out of the array's order (M3, M14) or
that do not move on with `k` (M5, M16). P4 adds a new string at the end;
only the arms that answer a string where they should answer `""` (M2, M4,
M9) change, since the new string becomes what they find. Three kept edits
fail P1 and P6 alone: strings compared by length (M6), a run ended by its
next string's length (M11) and the count-down over every string (M17).

Of the thirty-four, seventeen were not kept. Two are equivalent: in the
sorted arm, each run's last index kept rather than its first, since a run
of one has the same first and last; and in the places arm, the first
place overwritten by each later one, since a string that occurs again
still has a first place different from its last. Every other edit fails as
another does. The `(k+1)`th string in five ways, from a count started one
higher to each string counted twice (★, sets, places, Rust twice), and
each string counted from 1 on first sight (★), all fail P1 and P6 on the
same 2255 questions, those where a later distinct string exists. A string
seen twice taken as distinct (brute, Rust) fails as M1; the brute arm's
first distinct string whatever `k` fails as M16; the ★ arm walked
backwards and the `k`th from the end (sets, sorted) fail the same way as
each other, as do the distinct places never sorted back (sorted) and
sorted by their strings (places).

## Verification

Every arm prints the same output as `distinct.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error. `karac
run` and a `karac build` binary print the same output for every arm and the
differential. `karac check --output=json` reports nothing on any of them.
Under `karac __mir-run` the arms take 1.4 s (Rust) to 2.8 s (sorted), and
the brute-force arm 188 s, its 200 million string comparisons about 1 µs
each; the differential takes 49 s; on kara 3dcd076373.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in two rounds of 11 and 2 edits to a clean check: the `use` line
dropped, `struct Solution;` to `struct Solution {}`, `HashMap<&str, i32>`
to `Map[Str, i32]`, `HashMap::new()` and `String::new()` to `Map.new()` and
`String.new()`, `Vec<String>` to `Vec[String]`, and `for s in &arr` to `for
s in ref arr`. `*cnt.entry(s.as_str()).or_insert(0) += 1` and
`cnt[s.as_str()]` stay as written. The adapter hands the harness's `i64`
`k` to it `as i32`.

## Benchmarks

The bench answers 5000 arrays of 1000 strings of 1 to 5 letters, the
constraints' limit, from 2 to 26 letters of the alphabet, with the ★ arm in
all five languages: five million strings counted. Building the arrays is
part of the work timed. Rust counts into std's `HashMap` (SipHash, like
Kāra's `Map`) with a clone of each string as its key, as the Kāra arm's
`counts[s.clone()]` does; Go's map shares the string; C, which has no hash
map, counts into an open-addressing table over FNV-1a with a copy of each
new key. Every implementation prints `5000 arrays: 2905 answers found,
checksum 230044583`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `3dcd076373` on LLVM 22:

| | time | median |
|---|---|---|
| Go | 0.533 to 0.586 s | 0.550 s |
| C (`clang -O3`) | 0.522 to 0.579 s | 0.559 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.760 to 0.814 s | 0.775 s |
| Rust (`rustc -O`) | 0.751 to 0.829 s | 0.781 s |
| Kāra (`karac build`) | 0.758 to 0.887 s | 0.774 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.766 to 0.899 s | 0.805 s |
| Python | 6.9 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.768 s) is not above its real time (0.774 s).

The sequential Kāra program is 1.04x Rust under overflow checks and 1.44x
C. Kāra and Rust both hash with SipHash and clone each key; Go's map and
C's FNV-1a table hash faster, and Go's shares the string rather than
copying it. Overflow checks cost Rust nothing here: the work is hashing
and allocation, not arithmetic.
