# 1182. Shortest Distance to Target Color

Given an array `colors` holding the colours `1`, `2` and `3`, and queries
`[i, c]`, return for each query the shortest distance from index `i` to an
index holding colour `c`, or `-1` when no index holds it.

```
colors = [1, 1, 2, 1, 3, 2, 2, 3, 3], queries = [[1, 3], [2, 2], [6, 1]]  ->  [3, 0, 3]
colors = [1, 2], queries = [[0, 3]]                                       ->  [-1]
```

**Constraints:** `1 <= colors.length <= 5 * 10^4`, `1 <= colors[i] <= 3`,
`1 <= queries.length <= 5 * 10^4`, `0 <= queries[i][0] < colors.length`,
`1 <= queries[i][1] <= 3`.

The arms are `fn shortest_distance_color(colors: Vec[i64], queries:
Vec[Vec[i64]]) -> Vec[i64]`. The two Rust arms keep the method LeetCode
gives Rust users, over `Vec<i32>` and `Vec<Vec<i32>>`, inside `impl
Solution`, and a one-line `shortest_distance_color` converts the values and
calls it.

## Approaches

| file | mechanism |
|---|---|
| `shortest_distance_color.kara` ★ | for each colour a table of the distance from every index to its nearest index of that colour, filled by a sweep from the left and then one from the right; each query one lookup. O(n + q) |
| `shortest_distance_color_search.kara` | the indices of each colour listed in order, and each query a binary search (`partition_point`) for where its index would go: the nearest is the index found there or the one before it. O(n + q log n) |
| `shortest_distance_color_expand.kara` | each query looks outward from its index, one step further each way at a time, until it meets the colour or runs off both ends. O(n) a query |
| `shortest_distance_color_solution.kara` | a Rust solution as LeetCode's Rust users write it (the indices gathered into a `Vec<Vec<usize>>`, each query a `binary_search` whose `Err` gives the insertion point), carried to Kāra by `karac fix` |
| `shortest_distance_color_chain.kara` | another Rust solution, in iterator chains (a `scan` from the left keeping the last index of each colour in a `[Option<usize>; 4]`, one from the right keeping the next, and a `match` on the two `Option`s), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; one index asked
for every colour (`small 1: [-1, 0, -1]`); a colour that only lies to the
left (`small 2: [3, 1, -1]`); a tie between the two sides (`small 3: [3,
3, 2, 2]`); 2000 random arrays of 1 to 15 colours drawn from the first 1
to 3, five queries each (`2000 random arrays: checksum 406721472`); and
50000 colours, the constraints' most, with 50000 queries (`50000 colours,
50000 queries: 40119257`). `shortest_distance_color.py` mirrors the ★ arm
and its output is byte-identical; it also checks every answer but the last
line's against the statement read literally. Every arm gives the same
output under `karac run` and `karac build`.

The Mend loop: the ★ and expand arms take no fixes. The search arm's
`let (i, spots) = (q[0], at[q[1] - 1]);` takes one, `ref at[q[1] - 1]`.
The solution arm takes one round of 34 (among them `Vec<usize>` to
`Vec[i64]`, its `as usize` casts to `as i64`, the `&` of `|&c|` and
`binary_search(&i)`, and the `match` on `binary_search`'s `Ok` and `Err`
rewritten through `partition_point`) and its output matches. The chain arm
takes one round of 41 (among them `Vec<[Option<usize>; 4]>` to
`Vec[Array[Option[i64], 4]]` and each `scan` closure rewritten to Kāra's
shape) and its output matches. Both took more before the seven fixes below.

## Gaps

The two Rust arms found seven gaps, all fixed in kara.

- **A tuple `let` of an element got a copy.** `let (i, spots) = (q[0],
  at[q[1] - 1]);` was refused with a `.clone()` fix, a copy of the whole
  list of indices on every query, where `let spots = at[q[1] - 1];` gets
  the `ref` borrow when `spots` is only read. A part of a tuple `let` now
  gets it too. kara B-2026-11-17-103.
- **`Vec<[Option<usize>; 4]>` broke the file.** The `;` of the array type
  ended the scan of Rust's angle brackets, so the `Vec[..]` fix was
  dropped, and the parser's recovery offered a fix that wrote `[i64; 4;]`.
  Now the brackets are rewritten and the array type gets its own fix to
  `Array[T, N]`. kara B-2026-11-17-104.
- **Rust's `scan` over an array state got no rewrite.** `|last, (i, c)| {
  last[c] = Some(i); Some(*last) }` writes the state through its index
  and hands a copy out through `*`; it got a "drop the `*`" error, not the
  rewrite to Kāra's `scan`, which takes the state by value and returns
  `Some((next_state, item))`. It now gets `|last, (i, c)| { let mut last =
  last; last[c] = Some(i); Some((last, last)) }`. kara B-2026-11-17-105.
- **A state seeded with `None` was never solved.** A generic call whose
  closure returns `(state, item)`, with the state seeded by `None`,
  `Vec.new()` or `[None; 4]` and the item decided only by the closure, was
  refused with "expected 'Option[(?T0, _)]', found 'Option[(Option[i64],
  i64)]'", and `[None; 4]` kept its enum's own `T`. kara B-2026-11-17-106.
- **A `usize` inside an array type got no fix.** `Vec[Array[Option[usize],
  4]]` meeting the `i64` indices `enumerate` gives was refused with no fix,
  where `Vec[Option[usize]]` gets one to `i64`. kara B-2026-11-17-107.
- **The `binary_search` rewrite was misindented.** `let k = match
  p.binary_search(i) { .. };` became a block whose later lines lined up
  with the `match`, not the `let`. kara B-2026-11-17-108.
- **A `Copy` scan state read as not `Copy`.** The chain arm's `scan`
  closures hand the state out as `Some((last, last))`. The `[None; 4]`
  state is a `Copy` array once its `Option[i64]` is solved, but the
  ownership pass read the unsolved `Option[T]` and refused the second use
  as a use after a move, so `karac fix` added a `.clone()`. Fixed at kara
  5ac5b1ffda, and the `.clone()` is gone. kara B-2026-11-17-109.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the least `|i - j|` over every index `j` holding the colour, or
`-1`. 300 random arrays of 1 to 15 colours drawn from the first 1 to 3,
every index asked for every colour; the first ten hold one colour and the
next ten one colour repeated.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | `-1` exactly when the colour is absent |
| P3 | the colour lies that far away, on one side or the other |
| P4 | the array reversed, asked from the mirrored index, has the same answer |
| P5 | the next index's answer is at most one further or nearer |
| P6 | the ★ arm's answer |

All 190,620 checks pass on every arm: `300 arrays: checksum 894851327,
190620 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac build`.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac run`, each failing the same way under both. All ten
are caught.

| # | mutation | failures by property |
|---|---|---|
| A1 | ★: the right-hand sweep overwrites the left's distance | P1 271, P4 542, P5 191, P6 1084 |
| A2 | ★: an absent colour not mapped to `-1` | P1 2492, P2 2492, P3 2492, P6 9968 |
| S1 | search: the index before the insertion point used only past the last | P1 271, P4 542, P5 191, P6 271 |
| S2 | search: the index at the insertion point one too far | P1 2974, P3 1034, P4 1543, P6 2974 |
| E1 | expand: stops at the nearer end | P1 646, P2 646, P5 116, P6 646 |
| E2 | expand: looks to the left only | P1 806, P2 535, P4 1543, P5 191, P6 806 |
| X1 | solution: a match one index to the right | P1 652, P3 652, P4 818, P5 233, P6 652 |
| X2 | solution: the left neighbour taken over the right | P1 271, P4 542, P5 191, P6 271 |
| R1 | chain: the farther side taken | P1 542, P5 382, P6 542 |
| R2 | chain: the right-hand table left unreversed | P1 2024, P2 417, P3 1365, P4 3196, P5 931, P6 2024 |

A mutation of the ★ arm fails P6 on every arm. A1, S1 and X2 are one
fault in three arms, an index on the right lost to one on the left, and
fail the same checks; P4 catches each twice, once for each side it sees.
P2 catches the faults that answer for an absent colour (A2) or miss a
present one (E1, E2, R2). P3 catches the answers no index holds the colour
at. R1 passes P4, since taking the farther side is as wrong mirrored.

## Benchmarks

`bench/` times the ★ arm against the same algorithm in C, Rust, Go and
Python: 4 arrays of 50000 colours and 50000 queries each, the constraints'
most, built once (the third colour rare, one index in 997); then 40 rounds
answering every array's queries, each answer folded into a checksum. Every
program prints `40 rounds of 4 arrays of 50000 queries: checksum
715521255`. Each call builds its three tables and its answer and frees
them; the queries are a `Vec` of two-element `Vec`s in Kāra, Rust and Go,
and an array of two-element arrays in C.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and two of Python, with karac `71fca9a17a`
and this kata's six fixes, on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.153 to 0.235 s | 0.160 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.156 to 0.185 s | 0.162 s |
| Rust (`rustc -O`) | 0.205 to 0.282 s | 0.221 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.212 to 0.265 s | 0.225 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.215 to 0.272 s | 0.229 s |
| C (`clang -O3`) | 0.185 to 0.251 s | 0.194 s |
| C (`clang -O3 -march=x86-64-v3`) | 0.182 to 0.238 s | 0.198 s |
| Go | 0.243 to 0.331 s | 0.284 s |
| Python | 5.38 to 5.43 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane; user time is within 5% of wall time for both Kāra
rows, so both ran on one core. The user time of Kāra, Rust and C is close
(0.15 s for Kāra and Rust, 0.14 s for C); the gap in wall time is the
kernel's. Each call's tables are 400 KB, above glibc's threshold for
`mmap`, so Rust and C hand them back to the kernel on every free and
fault them in again on the next call: about 60,000 minor page faults and
0.06 to 0.07 s of system time a run, against 3,700 faults and 0.004 s for
Kāra, whose allocator keeps the memory. That reading comes from
`getrusage`, not a profile. Go's user time is above its wall time, its
collector running beside it. Python takes about 33x Kāra's time.
