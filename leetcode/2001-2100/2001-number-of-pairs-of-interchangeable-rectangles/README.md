# 2001. Number of Pairs of Interchangeable Rectangles

You are given `n` rectangles as a 0-indexed 2D array `rectangles`, where
`rectangles[i] = [width_i, height_i]`. Two rectangles `i` and `j` (`i < j`)
are interchangeable if they have the same width-to-height ratio, that is
`width_i / height_i == width_j / height_j` (decimal division, not integer
division). Return the number of pairs of interchangeable rectangles.

```
rectangles = [[4,8],[3,6],[10,20],[15,30]]  ->  6   (every pair: each ratio is 1/2)
rectangles = [[4,5],[7,8]]                  ->  0   (4/5 and 7/8 differ)
```

**Constraints:** `1 <= n <= 10^5`; `1 <= width_i, height_i <= 10^5`.

All `n` rectangles can share one ratio, so the answer reaches
`n (n - 1) / 2`, about `5 * 10^9`: past an `i32`, in an `i64`.

## Approaches

Reducing `w / h` by `gcd(w, h)` gives a pair of integers that names the
ratio exactly, with no floating point. Rectangles with equal reduced pairs
are interchangeable, and a group of `c` of them holds `c (c - 1) / 2` pairs.

| file | mechanism |
|---|---|
| `rectangles.kara` ★ | each reduced pair looked up in a `Map[(i64, i64), i64]`; the rectangle pairs with every one already counted under it. O(n log V) |
| `rectangles_sorted.kara` | the reduced pairs sorted, each run of `c` equal ones counted as `c (c - 1) / 2`. O(n log n) |
| `rectangles_cross.kara` | no gcd: sorted with `sort_by` comparing `w1 * h2` against `w2 * h1`, and equal ratios, side by side, counted as runs. O(n log n) |
| `rectangles_iter.kara` | the reduced pairs from `iter().map(..)` counted through `entry(..).or_insert(0)`, then `values().map(\|c\| c * (c - 1) / 2).sum()`. O(n log V) |
| `rectangles_packed.kara` | Stein's binary gcd (shifts and subtraction), the reduced pair packed into one integer `w * 100001 + h`, counted in a `SortedMap`. O(n log n) |
| `rectangles_solution.kara` | LeetCode's Rust template (`impl Solution`, `Vec<Vec<i32>>`, a `HashMap` with `entry`, a nested `fn gcd`), carried to Kāra by `karac fix`. O(n log V) |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's two examples
and six more; the sum and a checksum of the answers for 3000 sets of 1 to
20 rectangles with sides up to 6, and for 3000 sets of 1 to 40 rectangles
drawn as multiples of 1 to 5 base ratios; the same for 6 sets of 20000
rectangles, free or from pools of 3 to 80 ratios; and 100000 rectangles of
one ratio, whose answer `4999950000` needs 64 bits. `rectangles.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every pair `i < j` tested with `w_i * h_j == w_j * h_i`. It
checks 3000 problems of 1 to 40 rectangles, each either free with sides up
to 8 or drawn as multiples (up to 12) of 1 to 5 base ratios with sides up
to 7. Every random choice of a problem (the rectangles, a scale factor for
each, a split point, an index to copy) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | each rectangle scaled by its own factor (1 to 5) leaves the answer |
| P3 | every rectangle turned, `(w, h)` to `(h, w)`, leaves the answer |
| P4 | a copy of rectangle `j` appended adds as many pairs as rectangles already share `j`'s ratio |
| P5 | split in two, the answer is each half's plus the pairs across, counted literally |
| P6 | each arm agrees with at least three of the other five |

The differential prints `3000 problems: checksum 185911946, 108000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. Fifteen are kept, two or three to
each arm. All thirty are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the ratio not reduced | P1 2712, P2 2360, P4 2391, P5 2282, P6 2712 |
| M2 | ★: each rectangle paired with itself too | P1 3000, P4 3000, P6 3000 |
| M3 | sorted: the last run left out | P1 2454, P3 925, P4 1368, P5 2005, P6 2454 |
| M4 | sorted: the keys not sorted | P1 2128, P4 2215, P5 1836, P6 2128 |
| M5 | sorted: the run's start never moved | P1 2309, P3 436, P4 2309, P5 1986, P6 2309 |
| M6 | cross: equal ratio read as equal width | P1 2735, P2 1973, P3 595, P4 2503, P5 2336, P6 2735 |
| M7 | cross: the run never reset | P1 2156, P3 2032, P4 2238, P5 1901, P6 2156 |
| M8 | cross: both cross products halved | P1 312, P2 305, P3 161, P4 138, P5 224, P6 312 |
| M9 | iter: a count folded as `c * c / 2` | P1 2834, P4 1609, P5 1271, P6 2834 |
| M10 | iter: the height divided by `gcd(w, 1)` | P1 2695, P2 2400, P3 964, P4 2449, P5 2304, P6 2695 |
| M11 | packed: the key packed with base 7 | P1 32, P3 38, P4 4, P5 13, P6 32 |
| M12 | packed: the swap dropped from the gcd | P1 954, P3 1340, P4 527, P5 740, P6 954 |
| M13 | solution: the height read as the width | P1 1554, P3 1705, P4 1146, P5 1281, P6 1554 |
| M14 | solution: the count never grows | P1 2834, P4 3000, P5 2403, P6 2834 |
| M15 | solution: the sides cut to their low byte | P2 1302 |

P1, P4 and P6 kill fourteen, P5 thirteen, P3 nine and P2 five. P2 is
the only property that sees M15: the differential's sides stay below 256
until P2 scales them, and only there does a side lose its high bits. P2
misses every edit that keeps the reduced ratio a function of the ratio
alone (a lost run, a wrong fold, a self pair), since scaling leaves the
reduced pairs exactly as they were. P3 sees the edits that treat width and
height unevenly (M3 and M5 among them, through the sort order turning
changes). M11 is the faintest: base 7 merges only ratios whose packed keys
collide, 32 problems in 3000.

The other fifteen fail as a kept one does, or with a signature of their
own that adds nothing. The ★, sorted and iterator arms keying on one side
(width alone, width twice) fail alike; the ★ arm's count never kept, the
sorted arm's run of `c` counted as `c - 1` and the cross arm pairing only
neighbours fail alike; the iterator arm starting each count at one and the
Rust arm adding the count after it grows fail as M2; the Rust arm's
unreduced ratio fails as M1. The ★ arm's gcd stopping a step early, the
cross arm sorted by width alone, the iterator arm's gcd of `a + 1`, the
packed arm's lost factor of two, its loop stopped once `y <= x` and its
`c (c + 1) / 2 - c + c / 3` each fail with their own counts. One more
edit, Stein's loop without first making `x` odd, survived every check and
was replaced: the shift loop leaves at most one side even, so the common
divisor is odd and halving the other side still keeps it. The edit is
equivalent, not missed.

## Verification

Every arm prints the same output as `rectangles.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. Under `karac __mir-run` the arms take 1.0 s (sorted) to 1.7 s (the
Rust template) and the differential 6.6 s, at kara `85169d33d5`.

The ★ arm and four others were written in Kāra; three checked clean, and
the sorted and cross arms each carried one `||` / `&&`, which `karac fix`
turned into `or` / `and`. The Rust arm was written as LeetCode's Rust
template and reaches a clean check through `karac fix` alone, in three
rounds: eleven errors first (the `use`, the unit struct, generics in
`< >`, `::` paths, `&Vec`, the `&` in `|&(w, h)|`, and the nested `fn
gcd`), then `HashMap` to `Map`, then two warnings (the `ref` parameter that
a bare parameter already is, and `vec![..]` to a list literal). The nested
`fn gcd` inside the method had no fix when this kata started: the parse
read `fn` as a misspelt identifier ("'fn' is a reserved keyword") and
cascaded into two more errors. Kata 1061 met the same gap the same hour,
and its fix landed first: one diagnostic whose fix moves the function,
dedented, above the enclosing `impl` (kara 39dbc078da,
`tests/kata_1061_check_gaps.rs`).

## Benchmarks

The bench builds 20 sets of 100000 rectangles once in all five languages,
each a multiple of one of 10, 100, 1000 or 10000 base ratios with sides up
to 100000, and counts each set 10 times: 200 calls, two million map
updates. Every implementation prints `200 calls: sum 28862486400, checksum
162314877`. The C version uses its own open-addressing table, Rust a
`HashMap` (SipHash-1-3, as Kāra's `Map`), Go its built-in map.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `85169d33d5` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.563 to 0.656 s | 0.602 s |
| Rust (`rustc -O`) | 0.719 to 0.853 s | 0.761 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.903 to 0.997 s | 0.922 s |
| Go | 1.087 to 1.518 s | 1.208 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.200 to 1.323 s | 1.244 s |
| Kāra (`karac build`) | 1.201 to 1.353 s | 1.251 s |
| Python | 5.1 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (1.234 s) is below its real time.

Kāra is 1.35x Rust under overflow checks, and the gap is in instructions:
callgrind counts 12.2 billion for Kāra and 8.0 billion for Rust over the
whole run. Rust inlines its whole table probe and SipHash into `main` (97%
of its count). Kāra's lookup is an out-of-line runtime call,
`karac_mir_map_lookup_hv` (18% of its count), and an unnamed function in
the binary takes 51%; that it is the key's hash, run once for `get` and
again for `insert`, is inferred from the call pattern, not measured.
Both programs make the same two map calls per rectangle.
