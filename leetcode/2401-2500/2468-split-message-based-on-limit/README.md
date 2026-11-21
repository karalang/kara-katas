# 2468. Split Message Based on Limit

You are given a string, `message`, and a positive integer, `limit`.

You must **split** `message` into one or more **parts** based on
`limit`. Each resulting part should have the suffix `"<a/b>"`, where
`"b"` is to be **replaced** with the total number of parts and `"a"` is
to be **replaced** with the index of the part, starting from `1` and
going up to `b`. Additionally, the length of each of the resulting
parts (including its suffix) should be **equal** to `limit`, except for
the last part whose length can be **at most** `limit`.

The resulting parts should be formed such that when their suffixes are
removed and they are all concatenated **in order**, they should be
equal to `message`. Also, the result should contain as few parts as
possible.

Return *the parts* `message` *would be split into as an array of
strings*. If it is impossible to split `message` as required, return
*an empty array*.

```
message = "this is really a very awesome message", limit = 9
  ->  ["thi<1/14>","s i<2/14>","s r<3/14>","eal<4/14>","ly <5/14>",
       "a v<6/14>","ery<7/14>"," aw<8/14>","eso<9/14>","me<10/14>",
       " m<11/14>","es<12/14>","sa<13/14>","ge<14/14>"]
message = "short message", limit = 15  ->  ["short mess<1/2>","age<2/2>"]
```

**Constraints:** `1 <= message.length <= 10^4`; `message` consists only
of lowercase English letters and `' '`; `1 <= limit <= 10^4`.

With `b` parts, part `a` holds `limit - 3 - digits(a) - digits(b)`
letters, so `b` parts hold `b * (limit - 3 - digits(b))` letters less
the digits of 1 to `b`. The least `b` that holds the message is the
answer, and cutting greedily leaves the last part never empty. Once the
suffix of a `b`-digit count alone fills the limit, `3 + 2 * digits(b) >=
limit`, no larger count can do.

## Approaches

| file | mechanism |
|---|---|
| `split.kara` ★ | the count first: `b = 1, 2, ...` with a running sum of the counts' digits until `b` parts hold the message or a suffix alone fills the limit, then the parts cut in order. O(n) |
| `split_bands.kara` | band by band in closed form: within the counts of `d` digits, `b` parts hold `b * (limit - 3 - 2d)` letters less a constant of the band, so the least `b` of the band that holds the message is one division away. O(1) per band, O(n) to cut |
| `split_search.kara` | binary search band by band: within a band the letters held grow with `b`, so the least count that holds the message is found by halving, each count's room from the digits of 1 to `b` counted band by band. O(log n) per band, O(n) to cut |
| `split_retry.kara` | guess the count's width and retry: for `w = 1, 2, ...` the message is cut greedily with `w`-digit counts, letter by letter into each part, and the first guess whose part count has `w` digits answers. O(n) per width |
| `split_iter.kara` | iterators: the counts by `take_while` while a part has room, the running digit sum by `scan`, the least count by `find`, then each part's span by a second `scan` over the rooms and the parts by `map`. O(n) |
| `split_solution.kara` | LeetCode's Rust template: the ★ arm's running count over `i32`, the digits by a closure over `to_string`, each part cut from `message.as_bytes()` and turned back by `String::from_utf8`, and `format!` for the suffix; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 15 lines: LeetCode's two examples; then seven
more, a message that fits one part, a limit too small for any suffix,
one too small for two-digit counts, a last part of one letter, one
letter a part with a letter more than nine parts hold, two letters a
part, and a message that needs exactly 10 parts; then one message of `10^4` letters, the constraints'
longest, split with limits 6 and 11, both too small, 12, which takes
8893 parts, 100 and `10^4`, each as a part count and a checksum; and
3000 random messages of 1 to 300 letters with limits from 1 to 40, as a
checksum. `split.py` mirrors the ★ arm and its output is
byte-identical, and the mirror was checked on 3225 random messages of
1 to 129 letters with limits from 1 to 25 against every count tried in
turn, its parts filled to exactly `limit` and checked to join to the
message.

`check` first reports 4 errors on the template, and `karac fix`
carries it in one call, reporting 12 edits: the brackets of
`Vec<String>`, two edits; `Vec::with_capacity` and `String::from_utf8`
written with `.`; `format!` written as an f-string; `struct Solution
{}` added; `as_bytes` written `bytes`; the two `as usize` casts written
`as i64`, and the one inside `with_capacity` then dropped; the `usize`
of `0usize` dropped; and `vec![]` written `Vec.new()`. The closure
`|x: i32|`, `to_string()`, `1..=b`, the slice `bytes[i..end]` with
`to_vec()`, and `String.from_utf8(..).unwrap()` stand as Kāra.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: for `b = 1, 2, ...` every suffix `<a/b>` is written out as
text, every part but the last filled to exactly `limit` and the last
given the rest, and the first `b` for which the rest fits answers. No
digit count or formula stands in for a suffix's length. It checks 300
random messages of 1 to 60 letters with limits from 1 to 20, then 60
of up to 400 letters with limits from 6 to 15, which need two- and
three-digit counts. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the parts are the literal reading's |
| P2 | every part but the last is `limit` long, the last no longer, each ends in `<a/b>` for its place, and without them the parts join to the message |
| P3 | a letter added to the message: no fewer parts, and none if there were none |
| P4 | the limit one more: no more parts, and some if there were some |
| P5 | one part fewer cannot hold the message |
| P6 | each arm agrees with at least three of the other five |

P2 is the statement's own shape. P3 holds because any split of the
longer message, its last letter dropped, splits the shorter into as
many parts or, when the last part held only that letter, one fewer
whose new last part is still no longer than the limit. P4 holds because
a split under one limit, refilled greedily, fits the next. P5 is the
statement's fewest parts, checked by filling one part fewer, every
suffix written out, the way the literal reading does.

The first run's P5, every letter mirrored with the parts mirrored,
killed no mutant, since no edit looks at a letter, and was replaced.

The differential prints `360 cases: checksum 169173598, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every count in turn. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: every count one digit in the sum | P1 52, P2 52, P6 52 |
| M3 | ★: a count that just holds the message passed over | P1 48, P5 46, P6 48 |
| M6 | ★: each part a letter short | P1 204, P2 204, P6 204 |
| M7 | bands: one digit of the suffix dropped | P1 147, P2 147, P6 147 |
| M8 | bands: the count rounded down | P1 156, P2 156, P6 156 |
| M10 | bands: the earlier digits one apiece | P1 3, P2 3, P6 3 |
| M12 | search: each band one count short | P1 65, P2 65, P6 65 |
| M13 | search: a count that just holds passed over | P1 44, P5 44, P6 44 |
| M16 | search: the last count left out of the digits | P1 60, P2 60, P6 60 |
| M17 | retry: each index counted from 0 | P1 48, P2 48, P6 48 |
| M18 | retry: the first guess kept | P1 67, P2 67, P6 67 |
| M21 | retry: a one-digit count never guessed | P1 190, P3 2, P4 9, P5 2, P6 190 |
| M24 | iter: a count one letter short accepted | P1 46, P2 46, P6 46 |
| M25 | iter: the last letter never taken | P1 238, P2 238, P6 238 |
| M26 | iter: a part for every letter never tried | P1 5, P3 2, P6 5 |
| M27 | solution: the digits of a tenth | P1 77, P2 77, P6 77 |
| M28 | solution: only the last count digits summed | P1 105, P2 105, P6 105 |

P1 and P6 kill all seventeen, P2 thirteen, P5 three, P3 two, and P4
one, the retry arm's one-digit count never guessed (M21), which answers
a message that nine parts hold with ten or more parts, or with none.

Fourteen are not kept. Five fail exactly as a kept one: the ★ arm's
each index as wide as the count (M4) as the retry arm's each index
counted from 0 (M17); the ★ arm's parts numbered from 0, the retry
arm's count one more and the template's last byte never taken (M5,
M20, M29) as the iter arm's last letter never taken (M25); and the iter
arm's digit sum a count behind (M23) as the search arm's last count left
out of the digits (M16). Four fail apart from every kept one: the bands
arm's band top refused and the search arm's band top never tried (M11,
M14), alike; the retry arm's each piece a letter over (M19); and the
template's one more letter of room (M31). The search arm's later bands
searched too (M15) runs without end: it settles on the lowest count of
each band above the answer, up to `10^7` parts for a limit of 20, and
cuts that many, so it was stopped.

Four survive, and each is equivalent. The ★ arm's part with no room
allowed (M1) lets the loop try a count whose suffix alone fills the
limit, and the template's brackets and slash not counted and the iter
arm's one count of the suffix allowed for (M30, M22) try still more:
such a count gives its own-width parts no room or less than none, so
the letters held only fall past the last band with room, and none
holds a message that no earlier count did. The bands arm's band floor
ignored (M9) answers below a band's first count only when the band's
formula holds the message with fewer counts than the band starts at,
and then the band before, whose parts have more room, held it first.

## Verification

Every arm prints the same output as `split.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.8 to 2.9 s and the differential 3.2 s; under `karac __mir-llvm-asan` the arms take 0.7 to 1.0 s and the differential 1.3 s, and under `karac run` the differential takes 0.8 s.

## Benchmarks

The bench builds 20 messages of `10^4` lowercase letters and spaces
once from its own generator, then makes 2600 passes; each chooses every
message's limit, from 12 to 211, from the checksum so far, so no answer
carries over, then splits it, folding the part count, the last part's
length and the pass into the checksum. The bench uses the ★ arm in all
five languages, each count's digits by the language's own number to
text, an f-string in Kāra, `to_string` in Rust, `snprintf` in C,
`strconv` in Go and `str` in Python, and every part built as a string.
Every implementation prints `2600 passes over 20 messages of 10^4:
checksum 392621113`.

BENCHTAB
