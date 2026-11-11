# 2086. Minimum Number of Food Buckets to Feed the Hamsters

You are given a 0-indexed string `hamsters` where `hamsters[i]` is
either `'H'`, a hamster at index `i`, or `'.'`, an empty index.

You will add some number of food buckets at the empty indices in order
to feed the hamsters. A hamster can be fed if there is at least one food
bucket to its left or to its right: a hamster at index `i` can be fed if
you place a food bucket at index `i - 1` and/or at index `i + 1`.

Return the minimum number of food buckets you should place at empty
indices to feed all the hamsters, or `-1` if it is impossible to feed
all of them.

```
hamsters = "H..H"   ->  2
hamsters = ".H.H."  ->  1
hamsters = ".HHH."  ->  -1
```

**Constraints:** `1 <= hamsters.length <= 10^5`; `hamsters[i]` is either
`'H'` or `'.'`.

Left to right, a hamster not already fed by a bucket on its left should
get one on its right, where the next hamster may share it, and on its
left only when the right is taken; a hamster with neither side empty
cannot be fed. One walk, O(n). The approaches differ in how they keep
the buckets placed, or whether they place any.

## Approaches

| file | mechanism |
|---|---|
| `bucket.kara` ★ | the greedy over `bytes()`, the buckets placed kept in a `Vec[bool]`, `return -1` at a hamster with no empty side. O(n) |
| `bucket_pattern.kara` | by text: `-1` when the street is `"H"`, `starts_with("HH")`, `ends_with("HH")` or `contains("HHH")`; else the hamsters less the `H.H`s, counted without overlap by `matches("H.H").count()` |
| `bucket_dp.kara` | dynamic programming over the cells: the fewest buckets for each of four states of the last cell, a bucket there or not and a hamster there waiting for its right or not, in a `Vec` of four with a `const UNSERVED` |
| `bucket_fold.kara` | the greedy as one `fold` over `iter().enumerate()`, carrying `(buckets, place of the last bucket, possible)` as a tuple |
| `bucket_struct.kara` | a `struct Street` of the cells and the buckets, with `empty(i)`, `fed(i)`, `place(i)` and `serve()`, the greedy mirrored: from the right end, the bucket on the left first |
| `bucket_solution.kara` | LeetCode's Rust template (`hamsters.as_bytes()`, a `usize` walk with `i += 2` past a bucket on the right, `-> i32`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each street and its count; then the sum of the counts, how many
streets cannot be served, and a checksum, for 2000 random streets of 1
to 30 cells, a hamster in 1 to 5 cells of 10; then the counts for two
of the constraints' largest, `10^5` cells put together from pieces that
can each be served, and `H.` over and over. `bucket.py` mirrors the ★
arm and its output is byte-identical; the ★ arm was also checked against
every set of empty cells on 3000 random streets of up to 12 cells, in
Python.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of the empty cells, as the bits of a mask, kept
when every hamster has a bucket beside it, and the fewest buckets of
those kept, or `-1` when none is. It checks 300 random streets of 1 to
12 cells, a hamster in 2 to 7 cells of 10; then 20 streets with no
hamster, and 20 put together from pieces that can each be served. All
340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the count is the statement read literally |
| P2 | the street reversed gives the same count |
| P3 | the count is `-1` exactly when the street is one hamster, starts or ends with two, or holds three in a row |
| P4 | a street that can be served takes at least half its hamsters, rounded up, and at most all of them |
| P5 | a street that can be served, with its first hamster made an empty cell, takes no more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 streets: checksum 125133333, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal counts was checked against a Python reading of the same
streets. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-four edits to the differential, five to seven to each of its
arms, each run under `karac __mir-llvm-run` and `karac __mir-run`.
Seventeen are kept, three to each Kāra arm and two to the Rust-template
arm. Each kept one is killed, fails the same way under both backends and
not by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last place on the right never used | P1 19, P2 32, P3 19, P6 19 |
| M2 | ★: a hamster that cannot be fed passed over | P1 127, P3 127, P4 69, P5 31, P6 127 |
| M3 | ★: the left bucket marked on the hamster | P1 47, P2 38, P3 24, P6 47 |
| M4 | pattern: one hamster alone served | P1 13, P3 13, P6 13 |
| M5 | pattern: two hamsters at the start served | P1 18, P2 37, P3 18, P6 18 |
| M6 | pattern: only four in a row refused | P1 15, P3 15, P6 15 |
| M7 | dp: a bucket costing nothing | P1 154, P4 154, P6 154 |
| M8 | dp: the street ending on a waiting hamster served | P1 90, P2 107, P3 51, P4 39, P6 90 |
| M9 | dp: a hamster next to a waiting one allowed | P1 91, P2 93, P3 58, P4 41, P6 91 |
| M10 | fold: no bucket taken as just before the street | P1 61, P2 92, P3 31, P4 31, P6 61 |
| M11 | fold: a street that cannot be served counting 0 | P1 127, P3 127, P4 127, P5 47, P6 127 |
| M12 | fold: a left bucket not counted | P1 67, P2 67, P4 33, P6 67 |
| M13 | street: fed by a bucket on the left | P1 63, P6 63 |
| M14 | street: the left place never taken | P1 108, P2 52, P3 82, P6 108 |
| M15 | street: each bucket counted twice | P1 154, P4 134, P6 154 |
| M16 | solution: the adapter's street one empty cell longer | P1 32, P2 37, P3 32, P6 32 |
| M17 | solution: the adapter's first hamster gone | P1 185, P2 61, P3 60, P4 90, P6 185 |

P1 and P6 kill all seventeen, P3 thirteen, P2 ten, P4 nine, and P5
two. P3, which knows the streets that cannot be served from their text
alone, sees every edit that serves one of them or refuses one that can
be served: a side never looked at (M1, M14), a refusal skipped (M2, M11)
or missed (M4, M5, M6), a hamster taken as fed or waiting when it is not
(M3, M8, M9, M10). P2 sees an edit that treats the two ends or the two
sides differently. P4 sees a count that leaves its bounds: buckets free
(M7) or counted twice (M15), a left bucket not counted (M12), a hamster
left unfed (M8, M9, M10), a street that cannot be served counted (M2,
M11), a street with a hamster gone (M17). P5 sees only the arms that count a street
that cannot be served (M2, M11), where a hamster made an empty cell
leaves the street servable at some cost. One edit is seen by P1 and P6
alone: a bucket on the left taken as feeding (M13), which places more
buckets than it needs but serves every street it should, within the
bounds.

Of the thirty-four, seventeen were not kept, and none survives. Eleven
fail as a kept one: the ★ arm's hamster fed on its left given another
bucket and its bucket on the right not kept, the pattern arm's shared
buckets halved, the fold arm's hamster fed by a bucket on its right and
its right bucket recorded at the hamster, the struct arm's bucket not
kept and its walk from the left end, and the Rust arm's next cell not
skipped, all as M13, since each places more buckets than it needs and
no fewer; the ★ arm's left bucket not counted as M12; the dp arm's
hamster beside a bucket still waiting as M14; the Rust arm's street that
cannot be served counting 0 as M11. Six are killed with checks of their
own but were left out because their arm keeps three, or the Rust arm
two: the pattern arm's `H.` taken as shared and the dp arm's waiting
hamster left unfed past an empty cell, which fail alike (P1 130, P2 68,
P4 107), the pattern arm's two hamsters at the end served (P1 19, P2
37, P3 19), the dp arm's empty street costing one (P1 213, P4 150), the
★ arm's first cell's right never used (P1 40, P2 68, P3 40), and the
Rust arm's first place never on the left (P1 17, P2 32, P3 17).

## Verification

Every arm prints the same output as `bucket.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.3 s to 0.9 s, but for the dp
arm's 1.8 s, which tries four states at every cell, and the
differential 0.6 s (timed while other work shared the machine).

The pattern arm met one compiler gap. It counted the shared buckets as
Rust does, `hamsters.matches("H.H").count()`, and was refused "no method
'matches' on type 'Str'", though `match_indices` is there. `matches` is
now in the library, `match_indices` without the offsets: every
non-overlapping match, left to right, each a view into the text. Fixed
in kara 81aca4606b, test `tests/kata_2086_str_matches.rs`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 5, 2 and 1 edits: Rust's spellings (`&&` to `and`,
`struct Solution;` to `struct Solution {}`, the adapter's `&str` to
`Str`, `Solution::` to `.`); then `as_bytes()` to `bytes()` and the
adapter's `as i64`, which the `i32` widens to anyway; then the walk's
`usize` to `i64`, which the bytes' length is. The fixed arm reads as the
template does.

## Benchmarks

The bench puts one street of `10^6` cells together from pieces that can
each be served, and serves 3000 windows of `10^5` cells at random places
in it with the ★ arm in all five languages, each window a view into the
street where the language has one (a `Str`, a `&str`, a Go substring, a
pointer and a length) and a copied slice in Python: up to `3 · 10^8`
cells walked, less where a window cannot be served. Every implementation
prints `3000 windows: sum 72700429, 384 impossible, checksum 943141540`.

BENCHTAB
