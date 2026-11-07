# 399. Evaluate Division

You are given equations `a / b = v` between named variables, as pairs
of names and a list of values, and queries `c / d`. Answer each query
from the equations, or with -1.0 when it cannot be determined. No
equation contradicts another, and no value is zero.

```
equations = [["a","b"],["b","c"]], values = [2.0, 3.0]
queries   = [["a","c"],["b","a"],["a","e"],["a","a"],["x","x"]]
-> [6.0, 0.5, -1.0, 1.0, -1.0]
```

`a / a` is 1.0 only when an equation names `a`; `x / x` for a name no
equation has is -1.0.

**Constraints:** `1 <= equations.len() <= 20`; `0.0 < values[i] <=
20.0`; `1 <= queries.len() <= 20`; names are 1 to 5 lowercase letters
and digits.

## Approaches

| file | mechanism | time | space |
|---|---|---|---|
| `evaluate_division.kara` ★ | union-find with weights: each variable keeps its parent and the ratio to it, so the walk to the root multiplies out to `variable / root`; an equation joins two roots with the ratio that keeps it true, and a query answers when both names share a root | O((E + Q) α(V)) | O(V) |
| `evaluate_division_dfs.kara` | a graph with an edge `a -> b` of weight `v` and `b -> a` of `1 / v` per equation; a query walks depth-first from `a`, multiplying the weights, until it reaches `b` | O(Q (V + E)) | O(V + E) |
| `evaluate_division_bfs.kara` | the same graph searched breadth-first, with a queue of (variable, product so far) | O(Q (V + E)) | O(V + E) |
| `evaluate_division_floyd.kara` | a table of every ratio, filled as in Floyd-Warshall: each variable in turn joins the known ratios `i / k` and `k / j` into `i / j` | O(V^3 + Q) | O(V^2) |
| `differential.kara` | the four arms on 3,000 random systems whose answers are known by construction, five properties | — | — |

Every arm prints the same 7 lines: the three LeetCode examples, three
edge cases (two separate groups of variables, a cycle of consistent
equations, a chain of ten variables), and for 300 random systems over 2
to 12 variables how many queries have an answer, how many do not, and a
checksum. Answers print with five decimals. In the random systems every
variable holds a hidden power of two and each equation is the ratio of
two of them, so every answer is exactly `2^k` whatever order an arm
multiplies in, and the checksum folds in `k`. `evaluate_division.py`
mirrors the ★ arm and its output is byte-identical.

Three spellings in the arms work around `karac check` gaps found
writing this kata; each is a compiler bug, and the arms should go back
to the first form once it is fixed:

- The harness takes its test names as `Vec[String]`. It first took
  `Vec[Str]` and passed `vec!["a", "b", ...]`, which the spec allows: a
  string literal is a `Str` where one is expected. `karac check` and
  `karac __mir-run` refuse a literal at type `Str` in a `let`
  annotation, a `vec!`, a tuple or a function's result (kara
  `B-2026-10-12-13`). The depth-first arm's `walk` takes `at: String`
  for a related reason: as `at: Str`, using `at` twice is refused as a
  move, though `Str` is `Copy` (kara `B-2026-10-12-14`).
- The ★ arm looks up a query's two names with two nested `if let`s. It
  first matched `(index.get(a), index.get(b))` against
  `(Some(i), Some(j))` and read `*i`, the spec form, since `Map.get`
  gives `Option[ref V]`; `karac check` refuses the `*` through a tuple
  pattern (kara `B-2026-10-12-16`).
- The graph arms multiply by `*w` in
  `for (next, w) in graph[at].iter()`, as the items of `Vec.iter()` are
  references. Until the fixes that closed kara `B-2026-10-12-9`
  (extended by this kata), `karac __mir-run` refused the `*` as
  `found 'f64'` and the arms wrote `w`.

## Differential

`differential.kara` holds copies of the four arms. Each of 3,000 random
systems splits 2 to 12 variables into up to three groups, gives each
variable a hidden power of two, and joins each group with a random
spanning tree of equations plus up to three more inside groups, so
every answer is known exactly.

| | property |
|---|---|
| P1 | a query inside a group is `2^(hidden[a] - hidden[b])` exactly |
| P2 | a query across groups, or naming a variable no equation has, is -1 |
| P3 | `a / a` is 1 for every variable an equation has |
| P4 | answering `b / a` gives the reciprocal of `a / b`, or -1 for both |
| P5 | writing every equation the other way round (`b / a = 1 / v`) changes no answer |

It prints `3000 systems, 60000 checks, 0 failures` under
`karac __mir-run`, and a count for each property when anything fails.

## Mutation testing

Eight edits to `differential.kara`, each run under `karac __mir-run`.
All eight are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | union-find: path compression keeps the old weight | P5 2043 |
| M2 | union-find: a join gives the root the inverse ratio | P1 1606, P5 2046 |
| M3 | union-find: a query answers `b / a` | P1 2400 |
| M4 | dfs: the reverse edge carries `v`, not `1 / v` | P1 2006, P4 2397, P5 2404 |
| M5 | dfs: the walk gives up after its first neighbour | P1 1349, P4 1619 |
| M6 | bfs: products divide by each edge instead of multiplying | P1 2400 |
| M7 | floyd: the first variable never joins two ratios | P1 852, P5 1184 |
| M8 | floyd: a query reads `b / a` | P1 2400 |

M1 is caught by P5 alone, which feeds the same equations written the
other way round; why the generator's own order hides it was not
traced. M3, M6 and M8 each answer the reciprocal, so they fail
the same 2,400 checks, and P4 cannot see any of them: an arm that
inverts every answer still gives reciprocal pairs. M7's first version
skipped the last variable instead of the first and survived: the last
variable to get an index is usually a leaf of its tree, so it is
rarely the only way between two others.

## Verification

All four arms print the same output as `evaluate_division.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and `karac check` passes on every file. The differential prints `60000
checks, 0 failures` under both. The Floyd arm also matches under
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`, and the two graph arms under `karac run --interp`. The rest
stop in the frozen legacy backends: its typechecker refuses the
`*i` of `if let Some(i) = index.get(name)`, and its codegen has no
`for` over `graph[at].iter()` when `graph` is a `Map`. Not filed.

## Benchmarks

The bench program uses the ★ arm on 100,000 systems, each of 20
equations and 20 queries (the problem's limits) over up to 40 variables
named `v0`, `v1`, ..., built from an LCG. As in the harness, every
variable holds a hidden power of two, so every answer is exact; the
program counts the answered queries and folds their exponents into a
checksum. Every implementation prints `100000 systems: 799127 answered,
checksum 609728220`; a 2,000-system cut of the Kāra program under
`karac __mir-run` prints the same as the C program cut the same way. C
has no map type, so its mirror carries an open-addressing table of
heap-allocated names; the others use their own hash maps.

### Apple M5 Pro, 2026-11-07

30 runs each, 5 warmups, on the Apple M5 Pro, karac `0.8.0-dev.14773+gdef97ac6a`
(gdef97ac6a, the v2/MIR backend), measured 2026-11-07, with the Kāra binary built
`KARAC_AUTO_PAR=0`. This is the kata's first M5 measurement; Python was not run.
The last column is Kāra's mean over that row's mean.

| implementation | mean | Kāra / this |
|---|---|---|
| **kāra `karac build`, seq** | **387.4 ms ± 5.3** | **—** |
| c `clang -O3` | 475.2 ms ± 4.7 | 0.82× |
| go `go build` | 515.4 ms ± 7.4 | 0.75× |
| rust `-O` | 543.1 ms ± 6.0 | 0.71× |
| rust `-O -C overflow-checks=on` (equal-safety) | 546.6 ms ± 6.8 | 0.71× |

Kāra is 0.71× `rustc -O`, 0.71× equal-safety Rust, 0.82× C and 0.75× Go.
The gaps were not investigated on this host. There is no legacy figure: legacy dd86e3955 cannot compile this kata.

Compile time (cold, 10 runs) and artefact size:

| | compile | binary | peak RSS |
|---|---|---|---|
| c | 61.9 ms ± 0.8 | 49.2 KiB | 1.0 MiB |
| rust | 133.0 ms ± 4.9 | 476.3 KiB | 1.3 MiB |
| kāra | 151.1 ms ± 3.1 | 67.2 KiB | 1.4 MiB |
| go | — | 2450.6 KiB | 10.6 MiB |

`karac build` is 2.4× clang's cold compile and 1.1× rustc's. Kāra's
68,784-byte binary is 1.4× clang's and 7.1× smaller than rustc's. Raw numbers are in
[`bench/results.json`](bench/results.json). The sink matches across the Kāra,
Rust, C and Go builds (`100000 systems: 799127 answered, checksum 609728220`).

### Container x86-64 history

Spot timings on a shared 4-core container (`bench.sh` timings need a
quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.99 s |
| Rust (`rustc -O`) | 1.45 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.61 s |
| Go | 2.4 s |
| Python | 7.2 s |

The Kāra program prints the same line under `karac __mir-llvm-run` in
15 s, compile included; that JITs the MIR's IR without optimization
passes, so it is not a benchmark. The legacy `karac build` refuses it,
as above.

## Compiler findings

- **A string literal is not a `Str` where one is expected** (kara
  `B-2026-10-12-13`), except as a call argument or inside `Some(...)`.
  `let x: Str = "abc";`, `let v: Vec[Str] = vec!["ab", "c"];`,
  `let t: (Str, i64) = ("ab", 1);` and `fn g() -> Str { "abc" }` are
  refused with `expected 'StringSlice', found 'String'`.
- **`karac check` treats `Str` as move-only** (kara `B-2026-10-12-14`).
  A `Str` parameter used twice is refused as a move, and so is `v[0]`
  read out of a `Vec[Str]`; the spec says `Str` is `Copy`, and
  `karac __mir-run` runs the same program.
- **`karac __mir-run` types a string range as `String`** (kara
  `B-2026-10-12-15`). `let x: Str = text[0..2];` passes `karac check`
  and is refused by the MIR builder.
- **A tuple pattern drops the `ref` from `Map.get`'s option in
  `karac check`** (kara `B-2026-10-12-16`); `if let` on one `get` keeps
  it.
- **Destructured `Vec` tuple items were values under `karac __mir-run`**
  (kara `B-2026-10-12-9`, extended): the row said the shape was specific
  to `Map`, and it was not. The row is closed and the arms use `*w`.
