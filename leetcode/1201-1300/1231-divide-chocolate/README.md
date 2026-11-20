# 1231. Divide Chocolate

You have one chocolate bar that consists of some chunks. Each chunk has
its own sweetness given by the array `sweetness`.

You want to share the chocolate with your `k` friends so you start
cutting the chocolate bar into `k + 1` pieces using `k` cuts, each piece
consists of some **consecutive** chunks.

Being generous, you will eat the piece with the **minimum total
sweetness** and give the other pieces to your friends.

Find the **maximum total sweetness** of the piece you can get by cutting
the chocolate bar optimally.

```
sweetness = [1,2,3,4,5,6,7,8,9], k = 5  ->  6    [1,2,3], [4,5], [6], [7], [8], [9]
sweetness = [5,6,7,8,9,1,2,3,4], k = 8  ->  1    every chunk its own piece
sweetness = [1,2,2,1,2,2,1,2,2], k = 2  ->  5    [1,2,2], [1,2,2], [1,2,2]
```

**Constraints:** `0 <= k < sweetness.length <= 10^4`; `1 <= sweetness[i]
<= 10^5`.

The arms are `fn maximize_sweetness(sweetness: Vec[i64], k: i64) ->
i64`. The two Rust arms keep the method LeetCode gives Rust users, on
`i32`, inside `impl Solution`, and a short `maximize_sweetness` converts
to and from it.

## Approaches

| file | mechanism |
|---|---|
| `divide_chocolate.kara` ★ | binary search on the answer: every piece can be at least `m` sweet when a walk that cuts as soon as the piece reaches `m` makes `k + 1` pieces (any sweetness left over joins the last). The answer is the largest `m` that works, from 1 to the bar's share of `k + 1`. O(n log S) |
| `divide_chocolate_jumps.kara` | the same search, each test jumping over the prefix sums: the next cut after a piece that starts at prefix `from` is the first prefix of at least `from + m`, by `partition_point`. O(k log n) a test |
| `divide_chocolate_gallop.kara` | the answer built bit by bit from the top: from the least chunk, which always works, add each power of two that still leaves every piece that sweet |
| `divide_chocolate_search.kara` | a Rust solution as LeetCode's Rust users write it (the bounds by `*sweetness.iter().min().unwrap()` and `.sum::<i32>()`, `let (mut cuts, mut cur)`, `for &s in &sweetness`), carried to Kāra by `karac fix` |
| `divide_chocolate_fold.kara` | another Rust solution (the test a closure that `fold`s `(count, piece)` pairs over `sweetness.iter()` with `\|(cnt, cur), &s\|`, the search up to `10^9 / (k + 1)`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples and a bar
with no cut (`[3, 1, 4]`, `8`), a checksum of the answers for 1000 random
bars of 1 to 40 chunks (`336165603`), and three answers at the
constraints' top, 10^4 chunks up to 10^5: no cut (`164420591`, the whole
bar), 99 cuts (`1633445`) and 9999 (`12`, the least chunk).
`divide_chocolate.py` mirrors the ★ arm, and its output is
byte-identical. Every arm gives the same output under `karac run` and
`karac build`, and under the AddressSanitizer build.

The Mend loop: the ★ and gallop arms check clean as written. The jumps
arm was first written with a closure `|m: i64| -> bool`, which the fix
makes `|m: i64|`, and with Rust's `match prefix.binary_search(from + m) {
Ok(i) => i, Err(i) => i }`, which the fix makes `prefix.partition_point(|y|
y < from + m)` since B-2026-11-19-28 (see below). The search arm takes one round of
13 fixes (among them `Vec<i32>` to `Vec[i32]`, `let (mut lo, mut hi)` to
`let mut (lo, hi)`, `.sum::<i32>()` to `.sum()`, `for &s in &sweetness`
to `for s in ref sweetness`) and the fold arm one round of 7 (among them
the closure's `-> bool` dropped, `|(cnt, cur), &s|` to `|(cnt, cur), s|`,
and `let mut lo = 1` to `let mut lo: i32 = 1`), and both check clean.

## Gaps

One.

- B-2026-11-19-28, fixed in kara at 4dbf2fe839: the fix for a Rust `match` over
  `binary_search` whose two arms are the same index, `Ok(i) => i, Err(i)
  => i`, wrote `{ let i = prefix.partition_point(|y| y < from + m); if i
  < prefix.len() and prefix[i] == from + m { i } else { i } }`, a test
  whose two branches are the same. It now writes the search alone,
  `prefix.partition_point(|y| y < from + m)`, as it already did for
  `.unwrap_or_else(|i| i)`; two sides alike but not the bare index keep
  one side and drop the test.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to make the `k` cuts, as the bits of a number over
the `n − 1` places between chunks, the least sweet piece of each, and
the sweetest of those, for up to 12 chunks. 2000 cases, a third with 1
to 12 chunks, a third with 13 to 200 and a third with 201 to 2000, the
chunks up to 3, 100, 1000 or 10^5 in turn, so that sweetness ties.

| | property |
|---|---|
| P1 | the statement read literally (up to 12 chunks) |
| P2 | from the least chunk to the bar's share of `k + 1` |
| P3 | the bar reversed gives the same answer |
| P4 | every piece can be that sweet, and not one sweeter |
| P5 | one more cut never makes it sweeter |
| P6 | the ★ arm's answer |

P2 holds because every piece holds at least one chunk, and the least
piece is at most the average. P4 asks the greedy walk, written again in
the differential: it makes `k + 1` pieces of the answer, and not of one
more.

All 60,000 checks pass on every arm: `2000 cases: checksum 579650099,
60000 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and the AddressSanitizer build. Python's brute force
for the same cases gives the same checksum.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both.

| # | mutation | failures by property |
|---|---|---|
| S1 | ★: a piece cut only once it passes m | P1 628, P2 149, P4 1862, P6 7448 |
| S2 | ★: one piece more than k + 1 asked for | P1 609, P2 146, P4 1506, P6 6024 |
| J1 | jumps: the last piece never tested | P1 406, P4 1286, P6 1286 |
| J2 | jumps: a piece of exactly m taken one chunk further | P1 628, P2 149, P4 1862, P6 1862 |
| G1 | gallop: the first step from the number of chunks | P1 378, P4 953, P6 953 |
| G2 | gallop: k pieces enough | P1 632, P2 606, P4 1535, P6 1535 |
| R1 | search: the surplus carried into the next piece | P1 394, P3 415, P4 1617, P6 1617 |
| R2 | search: the search from the sweetest chunk | P1 338, P2 897, P4 1099, P6 1099 |
| F1 | fold: k pieces enough | P1 632, P2 606, P4 1535, P6 1535 |
| F2 | fold: the surplus carried into the next piece | P1 394, P3 415, P4 1617, P6 1617 |

All ten are caught, and P1, the statement read literally, catches every
one. A mutation of the ★ arm fails P6 on the four other arms. Three
pairs fail alike: a piece cut only once it passes `m` (S1) and a piece
of exactly `m` taken one chunk further (J2) are the same mistake in two
forms, and so are k pieces taken as enough (G2, F1) and the surplus
carried into the next piece (R1, F2). P4, the answer works and one more
does not, catches all ten, since every one of them answers a sweetness
that is either not reachable or not the largest. P2 catches those whose
answer leaves its bounds: an extra piece asked for (S2) or a cut only
past `m` (S1, J2) can fall below the least chunk, k pieces taken as
enough (G2, F1) can pass the bar's share of `k + 1`, and a search from
the sweetest chunk (R2) never answers less than it. J1, which never
tests the last piece, and G1, whose first step is too small, stay inside
the bounds. P3, the bar reversed, catches only the carried surplus (R1,
F2), the one mistake that depends on which end the walk starts from. P5,
one more cut never sweeter, catches none: every mutation still answers
less as the cuts grow.

## Benchmarks

`bench/` runs the same workload in Kāra, C, Rust, Go and Python: the ★
arm, binary search on the answer with a greedy walk for each test, over
100 random bars of 10^4 chunks up to 10^5, each with a random number of
cuts, drawn once and each solved 20 times. Every program prints `100
bars of 10^4 chunks, 20 passes: checksum 966003486`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `684b860a50`
on LLVM 22. A plain `karac build` targets x86-64-v2, so the C and
overflow-checked Rust programs are also built at x86-64-v3 for
comparison:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.853 to 1.017 s | 0.868 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.847 to 0.936 s | 0.879 s |
| Rust (`rustc -O`) | 0.559 to 0.775 s | 0.597 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.843 to 0.999 s | 0.880 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.871 to 0.961 s | 0.901 s |
| C (`clang -O3`) | 0.560 to 0.721 s | 0.627 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.544 to 0.780 s | 0.613 s |
| Go | 0.394 to 0.440 s | 0.403 s |
| Python | 16.57 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Rust with overflow checks on runs level with Kāra (0.880 s
against 0.879 s), and the two ranges overlap. C is about 29% ahead of
Kāra (0.627 s against 0.879 s); Kāra takes about 2.2x Go's time (0.879 s
against 0.403 s). Python takes about 19x Kāra's time. No profile was
taken.
