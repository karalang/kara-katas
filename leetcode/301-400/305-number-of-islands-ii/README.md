# 305. Number of Islands II

A grid that starts as all water. Each operation turns one cell into land; after
each one, report how many islands exist. Land connects 4-directionally.

```
m = 3, n = 3

(0,0)      (0,1)      (1,2)      (2,1)
1 0 0      1 1 0      1 1 0      1 1 0
0 0 0      0 0 0      0 0 1      0 0 1
0 0 0      0 0 0      0 0 0      0 1 0
  -> 1       -> 1       -> 2       -> 3
```

## Approaches

| file | mechanism | build | per operation |
|---|---|---|---|
| `number_of_islands_ii.kara` ★ | union-find, rank + path compression, count kept **incrementally** | O(mn) | O(α(mn)) |
| `number_of_islands_ii_recount.kara` | the same forest, count **recomputed** by counting roots | O(mn) | O(mn) |
| `number_of_islands_ii_sparse.kara` | union-find over a sparse `Map[i64, i64]`, union by **size** | O(1) | O(α) |
| `number_of_islands_ii_flood.kara` | flood-fill the whole grid, the definition verbatim | O(1) | O(mn) |
| `differential.kara` | 2,160 operation sequences, 26,460 steps, four arms, seven properties | — | — |
| `bench/islands2.kara` | 65,536-cell shuffle × 160 passes (10.5M union-find operations) | — | — |

The static version of this problem is [kata #200](../../101-200/200-number-of-islands/),
which counts islands in a fixed grid. What the "II" adds is that the answer must
be maintained *between* operations, and that is a different problem: #200 can
scan, this one cannot afford to.

## The mechanism, and the one line that is the whole problem

The answer only ever moves in small, local steps. A new land cell is its own
island, so the count goes **up** by one; then it is merged with each already-land
neighbour, and every merge that genuinely joins two distinct islands brings the
count **down** by one. Four neighbours, so each operation moves the answer by at
most +1 and at least −3. Nothing rescans the grid.

The subtlety worth writing carefully:

```kara
fn r#union(mut ref self, a: i64, b: i64) {
    let ra = self.find(a);
    let rb = self.find(b);
    // Already the same island — merging again must NOT change the count.
    if ra == rb {
        return;
    }
    ...
    self.count -= 1;
}
```

`count -= 1` belongs **inside** the "the roots really were different" path, not
next to the call. Two neighbours of a new cell can already belong to the same
island — add the fourth cell of a 2×2 block and two of its neighbours are
already joined — and merging them again must decrement nothing. That single
misplaced line is this arm's characteristic bug, and it is why the differential
carries an arm that keeps no counter at all.

`parent[x] == -1` means "still water", so one array answers both the land/water
question and the forest, with no second grid to keep in step.

### `r#union`, and why the kata does not rename it

`union` is a Kāra keyword — the FFI untagged-union type (design.md § FFI
Unions) — so it cannot be a bare identifier. It is also the name this operation
has in every textbook and every other language's disjoint-set implementation.
Renaming it to `merge` would be routing around the collision rather than meeting
it, so the ★ arm uses the **`r#` raw-identifier escape** (design.md § Raw
Identifiers), which is the sanctioned spelling for exactly this and works at
both the definition and the call site:

```kara
fn r#union(mut ref self, a: i64, b: i64) { ... }
ds.r#union(idx, idx - n);
```

The `_recount` arm spells it `merge` instead, so the corpus carries one of each.
This is the second keyword collision in three katas — #303 hit `blocks`, one of
the eight effect verbs — and the diagnostic's silence about the escape is
recorded under **Compiler findings** below.

## Properties, not just agreement

| # | property | what it pins down |
|---|---|---|
| P1 | four arms, one answer, at every step | the algorithm, from four directions |
| P2 | count is never negative and never exceeds the cells added | the answer's range |
| P3 | one operation moves the count by at most +1, at least −3 | the answer's *shape* — weakly (see below) |
| P4 | repeating every operation changes nothing | idempotence of a duplicate add |
| P5 | the running answer matches an independent recount of the land set so far | ties the incremental state to a from-scratch count |
| P6 | a completely filled grid is exactly one island | the terminal case |
| P7 | the final count is independent of the **order** the same land set arrived in | **no arm computes this** |

```
sequences 2160
steps 26460
P1..P7 all 0
DIFFERENTIAL OK
```

**P7 is the one that could not be faked.** Every arm is inherently
order-sensitive — each processes operations one at a time and carries state
forward — so an order dependence is exactly the fault four-way agreement is
blind to, because all four arms would carry it. Feeding the same land set in
several permutations and demanding one answer tests a property of the *problem*
that no line of any arm is trying to satisfy. It earns its place in the mutation
table below: a wrong neighbour stride is caught by P7 and by nothing else that
P1 does not already cover.

## Mutation-tested, because a differential that cannot fail is decoration

Nine mutations, each verified to have applied and compiled. **Two of them are
controls that must NOT fire** — mutations that change performance without
changing the answer. A battery that flags those is flagging edits, not faults.

| # | mutation | caught by |
|---|---|---|
| M1 | `count -= 1` also runs on a **same-root** union — *the characteristic bug* | P1 P2 · P5 P6 |
| M2 | the same-root early return deleted entirely | P1 P2 · P5 P6 |
| M4 | the "up" neighbour uses the wrong stride | P1 · P5 P6 **P7** |
| M6 | `add()` forgets to increment the count | P1 P2 P3 P5 P6 |
| M7 | the right-neighbour bound is off by one | **bounds-check panic** |
| M8 | the sparse arm drops its decrement | P1 |
| M9 | the flood arm misses the "up" direction | P1 P5 |
| M3 | **control** — path compression deleted | *(correctly survives)* |
| M5 | **control** — the rank tie-break bumps the wrong root | *(correctly survives)* |

### P3 cannot catch the bug it looks like it was written for

M1 is the interesting row. The delta bound says one operation moves the count by
at most +1 and at least −3 — and the misplaced decrement turns a legitimate delta
of 0 into −3, which is **still inside the bound**. P3 stays silent (the `·` above)
on precisely the fault a reader would assume it exists to catch. It is kept
because it pins the shape of the answer sequence cheaply, not because it
discriminates; P1, P2, P5 and P6 are what actually catch M1.

M7 is worth reading too: an off-by-one on the right-hand bound is caught by
Kāra's bounds check panicking, not by any property. That is a real safety net
rather than a test, and the distinction matters — the same mutation in the C
mirror is silent memory corruption.

### The two controls

M3 removes path compression and M5 bumps the wrong root's rank on a tie. Both
make the forest *deeper* — asymptotically worse — and neither makes it *wrong*,
because correctness of union-find depends only on which root a cell reaches, not
on how fast it gets there. Both correctly survive the whole battery. They are in
the table to show the differential distinguishes "slower" from "broken".

## Benchmarks

Shuffle all 65,536 cells of a 256×256 grid once; then punch 160 passes, each
rebuilding the disjoint-set forest and replaying every operation — 10.5M
union-find operations, `build-once + punch`
([BENCHMARKS.md](../../../BENCHMARKS.md)). All five languages print
`checksum 852131712`.

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3 -march=x86-64-v3`, matched ISA) | 446.4 ms | 0.78× |
| c (`-O3`) | 480.7 ms | 0.84× |
| rust (`-O`) | 498.1 ms | 0.88× |
| go | 561.5 ms | 0.99× |
| **kara** (codegen, seq) | **569.0 ms** | **1.00×** |
| rust (equal safety + matched ISA) | 634.5 ms | 1.12× |
| rust (`-O -C overflow-checks=on`, equal safety) | 650.9 ms | 1.14× |
| python | 15.430 s | 27.1× |

Kāra is **1.18× behind `clang -O3`** — the *narrowest* compiled gap of the three
range/grid katas in this run (#303 was 1.52×, #304 1.74×) — ties Go, and is
faster than equal-safety Rust in both its forms.

The reason is what the loop body is made of. #304's hot loop was four indexed
loads and three subtractions: four bounds checks against seven real
instructions, which is as exposed as that overhead ever gets. This one is
dominated by **pointer chasing** — `while parent[root] != root { root =
parent[root]; }` is a dependent load chain whose latency the check rides along
inside. The same bounds check costs proportionally far less when the machine is
already waiting on memory. Python lands at only 27× for the same reason, its
closest showing in this run.

The per-pass forest rebuild (two 65,536-element arrays) is part of the workload
by necessity rather than oversight — union-find is destructive, so a replay
against a full grid would do nothing — and it is identical in all five
languages.

## Compiler findings

The kata itself is clean: zero `karac check` diagnostics on all six sources, and
all five kata sources are byte-identical under `karac run`, `karac build` and the
default auto-parallelising build, matching the Python oracle.

Probing the surface around it — the discipline this corpus adopted after #304,
where writing only in already-known-good idioms hid two real defects — turned up
two diagnostics gaps, both filed:

- **`B-2026-09-02-29`** (parser, medium) — **12 of the 18 future-reserved
  keywords leak an internal `Error(...)` Debug rendering into the user-visible
  diagnostic**, plus a cascading second error:

  ```
  error[parse]: t.kara:1:17: Expected pattern, found Error("'async' is reserved
                for future use and cannot be used as an identifier")
  ```

  The other six (`asm`, `comptime`, `dyn`, `global_asm`, `try`, `yield`) give a
  clean `E0003`. This is the exact shape `B-2026-07-08-13` was filed to fix; that
  row fixed the `E0003` path, and this is the unfixed remainder.

- **`B-2026-09-02-30`** (diagnostics, low) — **no reserved-keyword diagnostic
  mentions the `r#` escape**, though design.md § Keywords names it as *the*
  remedy and says "tooling can do the rewrite automatically". Six for six across
  the keywords tested, in every syntactic position. The sibling naming
  diagnostic does better — `` `DS` is Const-class ... consider renaming to `Ds` ``
  names its remedy in prose. This kata hit the collision on `union`, #303 hit it
  on `blocks`; both times the compiler knew the identifier, knew the escape, and
  offered neither.

Idioms probed and found clean, several of them more natural than what earlier
katas in this run used: associated-function constructors (`DisjointSet.new(n)`),
range-`for` over an `i64` bound, `+=` / `-=` on a struct field through
`mut ref self`, unary minus, `not`, `Map[i64, i64]` keyed mutation inside a
`mut ref self` method, and the `r#` escape at both definition and call site.

## Running it

```bash
karac run number_of_islands_ii.kara           # ★ union-find, incremental count
karac run number_of_islands_ii_recount.kara   # same forest, count recomputed
karac run number_of_islands_ii_sparse.kara    # sparse Map, union by size
karac run number_of_islands_ii_flood.kara     # flood fill, the definition
karac run differential.kara                   # 2,160 sequences, 26,460 steps

bash bench/bench.sh                           # cross-language lane
```
