# 2055. Plates Between Candles

There is a long table with a line of plates and candles arranged on top of
it. You are given a string `s` of the characters `'*'` and `'|'` only,
where a `'*'` is a plate and a `'|'` is a candle, and a 2D integer array
`queries` where `queries[i] = [left, right]` names the substring
`s[left..=right]`. For each query, find the number of plates between
candles in that substring: a plate counts when there is at least one
candle to its left and at least one to its right within the substring.
Return the answers in the order of the queries.

```
s = "**|**|***|", queries = [[2,5],[5,9]]  ->  [2,3]
s = "***|**|*****|**||**|*",
queries = [[1,17],[4,5],[14,17],[5,11],[15,16]]  ->  [9,0,0,0,0]
```

**Constraints:** `3 <= s.length <= 10^5`; `s` holds only `'*'` and
`'|'`; `1 <= queries.length <= 10^5`; `0 <= left <= right < s.length`.

The plates a query counts are exactly those between its first candle and
its last: every one of them has a candle on each side, and none outside
them does. So every approach finds those two candles and counts the
plates between them, by walking, by searching, or by reading off counts
made once for the whole string.

## Approaches

| file | mechanism |
|---|---|
| `plates.kara` ★ | one pass from the left counts the plates before each place and finds the nearest candle at or before it, one from the right the nearest at or after it; a query's answer is the difference of the counts at its first and last candle |
| `plates_brute.kara` | the statement read directly: each query's places walked, plates counted once a candle has been passed, and the count kept at each candle so the plates after the last are left out |
| `plates_search.kara` | the candles' places listed with `chars().enumerate()` and `filter`, and each query's first and last candle found with `partition_point`; the places between them less the candles among them |
| `plates_sorted.kara` | a `SortedMap` from each candle's place to how many candles come before it; a query asks `ceiling` for its first candle and `floor` for its last |
| `plates_text.kara` | each query read off the text: its slice `s[left..right + 1]`, the first candle with `find`, the last with `rfind`, and the plates between them counted with `filter` |
| `plates_solution.kara` | LeetCode's Rust template (`as_bytes()` against `b'*'` and `b'|'`, a `vec![0; n + 1]` of plate counts and two `vec!`s of nearest candles as `i32` indexed back with `as usize`, the answers a `map` over the queries `collect`ed), carried by `karac fix` in three rounds and one edit by hand |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples and four more,
each string, its queries and their answers; then the sum and a checksum
of the answers for 2000 random strings of 3 to 40 places, candles from
every place to one in five, with 1 to 20 queries each; then the same for
10 strings of 2000 places with 2000 queries each, candles from every
place to one in thirty. The brute-force and text arms walk each query, so
the larger strings are 2000 places, not the constraints' 100000; the bench
takes the ★ arm to the limit. `plates.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each plate in a query's range counted when a candle stands in
the range on each side of it. It checks 500 random strings of 3 to 40
places with 1 to 20 queries each, drawn as the harness draws its small
ones, before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | each answer is at least 0, at most the plates in the range, and at most the range's length less two |
| P3 | the string reversed, each query mirrored, has the same answers |
| P4 | a query split at a candle inside it answers the sum of its two parts; with none inside, it answers the places between its ends when both are candles, and 0 otherwise |
| P5 | the string with a candle put at each end, asked for its whole length, answers every plate in the string |
| P6 | each arm agrees with at least three of the other five |

The differential prints `500 strings: checksum 61569831, 18000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-five edits to the differential, five to seven to each of its arms,
each run under `karac __mir-run` and `karac __mir-llvm-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the candles counted as plates | P1 439, P2 356, P4 147, P5 500, P6 439 |
| M2 | ★: the first candle at or before the left end | P1 354, P2 296, P3 374, P4 172, P6 354 |
| M3 | ★: the last candle one place early | P1 291, P3 217, P4 251, P5 267, P6 291 |
| M4 | brute: the query's last place left out | P1 237, P3 276, P4 281, P5 267, P6 237 |
| M5 | brute: the count kept only at the first candle | P1 319, P4 56, P5 399, P6 319 |
| M6 | brute: the query's first place left out | P1 228, P3 276, P4 267, P5 270, P6 228 |
| M7 | search: the candles between counted as plates | P1 390, P2 317, P4 384, P5 487, P6 390 |
| M8 | search: the first candle in the whole string | P1 388, P2 370, P3 409, P4 387, P6 388 |
| M9 | search: the places listed, not the candles | P1 353, P2 55, P4 349, P5 388, P6 353 |
| M10 | sorted: the first candle the floor of the left end | P1 307, P2 250, P3 338, P4 133, P6 307 |
| M11 | sorted: the last candle the ceiling of the right end | P1 306, P2 231, P3 338, P4 114, P6 306 |
| M12 | sorted: the plates beside every candle | P1 439, P2 296, P4 396, P5 500, P6 439 |
| M13 | text: the plates after the last candle counted | P1 358, P2 162, P3 373, P4 162, P6 358 |
| M14 | text: the whole string searched, not the slice | P1 352, P2 349, P4 353, P6 352 |
| M15 | text: the plates before the first candle counted | P1 354, P2 172, P3 373, P4 172, P6 354 |
| M16 | solution: the candles counted as plates | P1 425, P2 214, P4 131, P5 472, P6 425 |
| M17 | solution: the adapter widening each query by one | P1 234, P2 69, P3 296, P4 69, P6 234 |

P1, P4 and P6 kill all seventeen, P2 thirteen, P3 ten and P5 nine. P4's
split at a candle catches nearly every wrong count: the two halves share
the candle, so an arm that miscounts at a candle or past the last one
gets the halves and the whole out of step. P3 reverses the string, which
swaps the roles of the first and last candle: an arm that treats the two
ends alike (M1, M5, M7, M9, M12, M14, M16) passes it, and one that looks
the wrong way at one end fails. P5 asks a walled string for its whole
length, so it catches the arms that miscount the plates between candles
themselves (M1, M3 to M7, M9, M12, M16), and passes those that look for
the wrong candle from a query's ends (M2, M8, M10, M11, M13 to M15,
M17), since both ends of its query are candles.

Of the thirty-five, eighteen were not kept. Six are equivalent, all ways
of letting a query with fewer than two candles answer: in the ★ arm,
such a query answering the plates after its one candle, the plates
counted through the last candle (a candle adds none), and "no candle
after" written as the last place rather than past the end; one candle enough in the search arm; one candle counted as
a pair in the sorted arm; and `l <= r` in the Rust arm. Each answers 0
there, as it should. Two crash, both in the Rust arm, indexing past the
end: the nearest candles looked up on the wrong sides, and no candle
after the last place written as `-1`. Nine fail as a kept one does: the
brute arm's plates counted before any candle and its count taken at the
end fail as M15 and M13; the search arm's candle at either end left out
fails as M6 and M4; the sorted arm's ranks left out fails as M7; each candle ranked by its place
(sorted) and the first candle taken as the last (text) fail as M5; the
text arm's slice one short fails as M4, and its candles counted as
plates as M1. The Rust arm's adapter asking every query from the start
fails on checks of its own, and was left out because that arm keeps two.

## Verification

Every arm prints the same output as `plates.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.
Under `karac __mir-run` the arms take 0.5 s (★) to 1.0 s (search), the
brute-force arm 3.2 s, and the text arm 27 s, a closure call for every
character of every query's slice; the differential takes 2.6 s.

The five Kāra arms met no compiler gap and checked as written.

The Rust arm was written as LeetCode's Rust template, and met three gaps.
`karac fix` carries it in three rounds of 6, 5 and 1 edits: `struct
Solution;` to `struct Solution {}`, `Vec<..>` to `Vec[..]`,
`s.as_bytes()` to `s.bytes()`, each `vec![v; n]` to `Vec.filled(n, v)`,
and the adapter's `vec![l as i32, r as i32]` to a list literal; the last
round's edit is `Vec.filled(n + 1, 0i32)` for the plate counts.

- That last edit is new: the counts' literal took the default `i64`, the
  answers' `map(..).collect()` into the `Vec<i32>` the template returns
  was refused as "trait bound `C: FromIterator[i64]` is not satisfied",
  and nothing said why. kara `cd92d5f643` has that error name the filled
  literal and carry its suffix as the fix, as a narrowing return already
  did (tests in `tests/kata_2055_collect_literal_fix.rs`).
- `prefix[i + 1] = prefix[i] + if b[i] == b'*' { 1 } else { 0 };` is then
  refused as narrowing with no fix: an `if` whose values are all literals
  is typed `i64` at once, though design.md §8 says a literal is a type
  variable that later uses fix, and Rust types it `i32`. That is kara
  B-2026-11-10-6. The arm writes `{ 1i32 }`, the one edit by hand.
- A list whose first element is a literal took that literal's default,
  so `[0, r as i32]` was a `Vec[i64]` while `[r as i32, 0]` was a
  `Vec[i32]`. Found by a mutation of the adapter; kara `c4dea5c9d7` lets the
  leading literal take the later element's type.

## Benchmarks

The bench answers 50 strings of 100000 places, the constraints' limit,
with candles from every place to one in fifty, each asked 100000 queries,
with the ★ arm in all five languages: five million places and five
million queries. Building the strings and queries is part of the work
timed. The Kāra, Rust and Go programs collect the string's characters
first, as the ★ arm does; C reads its bytes in place. Every
implementation prints `50 strings: sum 151447145081, checksum 92849392`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `0142335972` and the fixes from
katas 2054 to 2057, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.107 to 0.120 s | 0.110 s |
| Kāra (`karac build`) | 0.108 to 0.134 s | 0.111 s |
| C (`clang -O3`) | 0.133 to 0.149 s | 0.139 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.154 to 0.179 s | 0.158 s |
| Rust (`rustc -O`) | 0.158 to 0.178 s | 0.173 s |
| Go | 0.291 to 0.329 s | 0.304 s |
| Python | 9.2 s |  |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.106 s) is not above its real time (0.111 s).

The sequential Kāra program is 0.70x Rust under overflow checks and 0.79x
C. All three walk the string twice and answer each query with two
lookups; why Kāra's loops come out ahead has not been measured.
