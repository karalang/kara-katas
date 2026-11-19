# 1659. Maximize Grid Happiness

You are given four integers, `m`, `n`, `introvertsCount`, and
`extrovertsCount`. You have an `m x n` grid, and there are two types of
people: introverts and extroverts. There are `introvertsCount`
introverts and `extrovertsCount` extroverts.

You should decide how many people you want to live in the grid and
assign each of them one grid cell. Note that you **do not** have to have
all the people living in the grid.

The **happiness** of each person is calculated as follows:

- Introverts **start** with `120` happiness and **lose** `30` happiness
  for each neighbor (introvert or extrovert).
- Extroverts **start** with `40` happiness and **gain** `20` happiness
  for each neighbor (introvert or extrovert).

Neighbors live in the directly adjacent cells north, east, south, and
west of a person's cell.

The **grid happiness** is the **sum** of each person's happiness. Return
*the **maximum possible grid happiness**.*

```
m = 2, n = 3, introvertsCount = 1, extrovertsCount = 2  ->  240
m = 3, n = 1, introvertsCount = 2, extrovertsCount = 1  ->  260
m = 2, n = 2, introvertsCount = 4, extrovertsCount = 0  ->  240
```

**Constraints:** `1 <= m, n <= 5`;
`0 <= introvertsCount, extrovertsCount <= min(m * n, 6)`.

## Approaches

| file | mechanism |
|---|---|
| `happiness.kara` ★ | the cells in reading order, each left empty or given an introvert or an extrovert; the neighbours already decided are the cell above, n back, and the one to the left, so the last n choices, as a base-3 number, are all the state. Memoised in a flat `Vec` over (cell, introverts left, extroverts left, last n choices). O(mn I E 3^n) |
| `happiness_rows.kara` | every way of filling a row as a base-3 pattern, its people and the happiness inside it and between two rows worked out once, then a DP over rows keyed by the last row's pattern and the counts used. O(m 9^n I E) |
| `happiness_table.kara` | the ★ arm's state as a table filled from the last cell back, the last n choices kept as a `Vec` window and keyed in a `Map`. O(mn I E 3^n) |
| `happiness_solution.kara` | LeetCode's Rust template: the ★ arm's memoised search as nested `fn`s over `usize`s and a `Vec<i32>`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 8 lines: LeetCode's three examples, nobody to
place (0), one row of five (420), and the largest grid with six of each
(1240); then the happiness summed and a checksum for 300 random grids up
to 3 by 3 with up to 3 of each, and 200 up to 5 by 5 with up to 6 of
each. `happiness.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every way of leaving each cell empty or putting an introvert
or an extrovert in it, within the counts, each person's happiness
counted from its own neighbours, and the best total. It checks every
grid up to 3 by 3 with up to 3 introverts and up to 3 extroverts, 144
problems; the literal search is too slow for random draws in the
interpreter, and there are only 144 such problems to draw from.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the grid turned on its side gives the same answer |
| P3 | one more introvert or extrovert allowed never lowers the answer |
| P4 | one more row never lowers the answer |
| P5 | each arm agrees with at least two of the other three |

The differential prints `144 problems: checksum 82367867, 2880 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the
template's next mask written `(mask * 3) % p3 / 3 * 3` survived, and is
equivalent, since `mask * 3` is already a multiple of 3.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the cell to the left counted across a row's start | P1 39, P2 58, P5 39 |
| M2 | ★: the cell above never counted | P1 47, P2 60, P5 47 |
| M3 | ★: an introvert recorded as an extrovert in the state | P1 79, P5 79 |
| M4 | rows: an introvert starting at 100, not 120 | P1 108, P5 108 |
| M5 | rows: neighbours within a row never counted | P1 47, P2 60, P5 47 |
| M6 | rows: neighbours between rows never counted | P1 47, P2 60, P5 47 |
| M7 | table: the cell to the left counted across a row's start | P1 39, P2 58, P5 39 |
| M8 | table: every choice remembered as empty | P1 85, P5 85 |
| M9 | template: the cell above read from the left's digit | P1 53, P2 54, P5 53 |
| M10 | template: an introvert's left neighbour never counted | P1 41, P2 46, P5 41 |

## Benchmarks

The bench draws 2000 random problems on grids of 4 to 5 rows by 4 to 5
columns with up to 6 introverts and 6 extroverts, LeetCode's largest,
all of them first, then answers each by the ★ arm in all five
languages, each problem allocating its own memo table. Every
implementation prints `2000 grids of 4 to 5 by 4 to 5: happiness sums
to 1196460, checksum 64741373`. The C build also runs clean under gcc's
AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `ee08f070a` on LLVM 22:

| | median |
|---|---|
| Rust (`rustc -O`) | 0.409 s |
| C (`clang -O3`) | 0.438 s |
| Kāra (`karac build`) | 0.469 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.472 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.482 s |
| Go | 2.071 s |
| Python | 40 s |

The sequential Kāra build takes 1.15x Rust's time and 0.98x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md).

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes
nothing here: its user time is not above its real time (0.442 s and
0.443 s on one run).

## Verification

All four arms print the same output as `happiness.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `336218278`.

## Writing it

The ★ arm dropped two `as i64` casts on its counts, which widen
implicitly. The rows arm read a row as `let row = cells[p]`, which would
move a `Vec` out of an index, and `karac fix` borrowed it as
`ref cells[p]`. The table arm's two `vec![..]` became list literals.

LeetCode's Rust template takes one `karac fix` of 32 edits. The nested
`fn cost` and `fn dfs` move to the top level, which Kāra requires and
where they mean the same, since they capture nothing. `struct
Solution;` becomes `struct Solution {}`, every `usize` an `i64`
(`3usize.pow(n as u32)` to `3.pow(n as u32)`), `vec![-1i32; ..]` a
`Vec.filled`, `&mut Vec<i32>` a `mut ref Vec[i32]` with `&mut memo` and
`memo` at the calls written `mut memo`, and `||`, `&&` `or` and `and`.
The arm then checks and agrees with no hand edit.
