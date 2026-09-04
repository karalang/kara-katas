# 314. Binary Tree Vertical Order Traversal

Give the root column `0`, every left child its parent's column minus one, every
right child plus one. Return the node values **column by column, leftmost column
first**; within a column **top to bottom**; and where two nodes share a row and
a column, **left to right**.

```
        3            column -1 : [9]
       / \           column  0 : [3, 15]
      9   20         column +1 : [20]
         /  \        column +2 : [7]
        15   7       ->  [[9], [3, 15], [20], [7]]
```

## Approaches

| file | walk | how the columns are ordered |
|---|---|---|
| `vertical_order.kara` ★ | BFS, one column tag per node | a `SortedMap[i64, Vec[i64]]` keeps them in key order |
| `vertical_order_offset.kara` | BFS level frontier | an extent pass finds the range; columns are a plain `Vec` indexed by `column - leftmost` |
| `vertical_order_dfs.kara` | DFS tagging `(column, row, position)` | one sort over those three keys |
| `vertical_order_hashed.kara` | BFS into a hash `Map` | the keys sorted for the read-out |
| `differential.kara` | four arms, eight properties | — |
| `bench/vertical.kara` | 8 trees × 50,000 nodes × 240 passes | — |

## The one idea: BFS order **is** the required within-column order

"Top to bottom, then left to right" is precisely the order a breadth-first walk
visits nodes in. So a BFS that tags each node with its column and appends to that
column's list produces every column already in the required order — no sorting,
no per-row bookkeeping, one pass. Three of the four arms are that walk, differing
only in how they get the *columns themselves* into left-to-right order:

- **★** pays for an ordered map (`SortedMap`), so the read-out is one pass over
  the keys.
- **`_offset`** pays for a second walk (`extent`) to learn the leftmost and
  rightmost column first, then indexes a flat `Vec` — no map at all. It is the
  arm the benchmark mirrors, because it is the same algorithm in every language.
- **`_hashed`** pays for a sort of the hash-map keys at the end.

**A depth-first walk does not get the order for free**, and `_dfs` is here to
show what it costs. DFS can reach a deep node in the left subtree before a
shallow node in the right subtree that shares its column, so a column can come
out with a deeper value above a shallower one. The smallest case is

```
        1              column 1 holds 3 (row 1, right subtree)
       / \             and 6 (row 3, left subtree). Preorder reaches
      2   3            6 first, so a naive DFS prints [6, 3].
       \   \           The answer is [3, 6].
        4   5
         \
          6
```

`_dfs` repairs it by recording `(column, row, preorder-position)` per node and
sorting by that triple. The third key is what makes the left-to-right tie hold:
for two nodes at the same depth, the left-subtree one is visited first by
preorder, so preorder position *is* left-to-right order within a row.

## The differential: a spec oracle where values are distinct, the arms alone where they are not

The four arms are checked against each other (P1) and against eight properties.
Most of the properties are a **restatement of the specification** that no arm
computes, so agreement is evidence rather than coincidence.

**When every value is distinct**, one depth-first pass records each value's
`(column, row, preorder-position)` in a table, and the specification becomes five
pairwise checks over any candidate answer:

- **P2** — the answer is a permutation of the tree's values.
- **P3** — the columns are exactly the contiguous range `[leftmost, rightmost]`,
  none empty. (Every child is one column from its parent, so the occupied
  columns have no holes.)
- **P4** — every value sits in the column the table assigns it.
- **P5** — within a column, rows never decrease.
- **P6** — within a column, equal rows appear in increasing preorder position.

Together these pin the answer completely — an output passing all five *is* the
vertical order — without sorting anything, so they do not share `_dfs`'s
mechanism. P3–P6 are applied to **every arm's** output, so a wrong arm is named
by the property it breaks, not merely by P1's disagreement.

**When values repeat** — legal input that changes nothing about the answer's
structure — a value can no longer name a node, so the table cannot be built and
P3–P6 cannot run. In that band the checks are P1, P2, and a weakened P7, and the
count of such cases is reported, because it is where the arms stand on their own:

> `duplicate-value cases beyond the spec oracle 600`

- **P7, the mirror relation.** Reflecting a tree negates every column, keeps
  every row, and reverses left-to-right within a row. So the mirror's vertical
  order is the original's column list reversed, with each equal-row run inside a
  column reversed too. It relates two runs over two different trees — the axis
  P2–P6 never vary. In the distinct band it is checked exactly; in the duplicate
  band, column-wise on sizes and multisets.

  **What P7 cannot see:** an arm that swapped left and right *consistently*
  computes `vertical(mirror(t))` for every `t`, and the mirror is an involution,
  so P7 holds for it perfectly. **P4 catches that arm at once** — every column is
  negated — which is why P4 exists even though P7 looks like it covers mirroring.

- **P8, closed forms.** A left spine of `n` nodes is `n` singleton columns; a
  right spine is `n` singletons the other way; a zigzag path occupies exactly two
  columns, alternating; a perfect tree of depth `d` has `2d - 1` columns whose
  sizes are sums of binomials. External answers reached by counting, not walking.

Bands are sized by the tree-walk interpreter, the slowest surface. The run
reports `cases 2282`.

## Mutation-tested, and the one survivor is a compiler finding

A differential that cannot fail is decoration, so each arm's mechanism was
mutated and the harness checked that the right property fires (harness:
`bench/`-independent, content-anchored to named function bodies, run against
`karac run`). Two semantics-preserving controls (a local rename, a `while`
spelling of a `for`) must stay silent, and do.

| mutation | fires | killed |
|---|---|---|
| A: left child gets column `c+1` | P1, P4 (+P3, P7, P8) | ✓ |
| B: placement mirrored (`hi - c`) | P1, P4 | ✓ |
| B: right child enqueued before left | P1, P6 | ✓ |
| C: sort ignores the row key | P1, P5 | ✓ |
| C: ties broken by value, not position | P1, P6 | ✓ |
| A: children pushed to the FRONT (DFS-order) | P1, P5, P6, P7 | ✓ |
| **X6: ALL arms mirrored consistently** | **P4, P8** (not P7) | ✓ |

**X6 is the deliberate probe of P7's blind spot.** Mirroring every arm at once
leaves them agreeing with each other (P1 silent) and satisfies P7 (the mirror is
an involution) — and P4 still fires on 101,136 cases, because the spec table is
external to all four arms. That is the two-tier point: P7 localises a fault the
arms share, P4 detects it.

The **ties-broken-by-value** mutation (C) only kills because the value generator
was hardened: distinct values are a *scrambled* permutation of the preorder
numbering (`counter * 37 mod 97`), so value order carries no information about
position. With a monotone `counter * 7` numbering that mutation was an equivalent
one — a real hole the harness surfaced and the fixture closed.

**One mutation survives `karac build` and `karac run` — and it is a compiler
bug, not a dead guard.** Removing arm D's `keys.sort()` (`_hashed`'s explicit
key sort) leaves the differential green under both compiled backends, at every
`KARAC_HASH_SEED`. Under `--interp` the same mutant is **killed** (P1 fires):
arm D's hash-map keys iterate in random order there, disagree with the sorted
arms, and the sort is revealed as load-bearing. The survival under codegen is the
finding below — a `Map` that should iterate randomly is iterating sorted.

## Benchmarks

`build-once + punch` ([BENCHMARKS.md](../../../BENCHMARKS.md)): grow 8 random
trees of 50,000 nodes **once**, then punch 240 vertical-order traversals through
them, each on the tree the running checksum selects so none can be hoisted,
folding every column's length and every value into the checksum. All five
languages print `checksum 414883072`. The `_offset` arm is mirrored — the one
arm that is the same algorithm in C, Rust, Go and Python (the ★ arm's `SortedMap`
has no C equivalent).

Container x86-64, [`bench/results.container-x86.json`](bench/results.container-x86.json),
30 runs each. **These numbers are noisy** — the shared container has σ of 4–6%
and this run put unchecked `rustc -O` (431 ms) *above* the overflow-checked build
(402 ms), which is impossible on the merits and marks the run as contended. Read
them as a coarse band, not a ranking; canonical Apple-silicon numbers await an
idle run. See [#313's methodology note](../313-super-ugly-number/#a-methodology-note-because-the-first-version-of-this-table-was-wrong)
for why one contended run is not self-validating.

| | mean | vs kara |
|---|---:|---:|
| c (`-O3`) | 375 ms ± 16 | 0.92× |
| c (`-O3 -march=x86-64-v3`) | 379 ms ± 21 | 0.93× |
| rust (`-O -C overflow-checks=on`, equal safety) | 402 ms ± 15 | 0.98× |
| rust (equal safety + matched ISA) | 409 ms ± 18 | 1.00× |
| **kara** (codegen, seq) | **409 ms ± 27** | **1.00×** |
| rust (`-O`) | 432 ms ± 20 | 1.06× |
| go | 925 ms ± 28 | 2.26× |

Within the container's noise, **Kāra ties equal-safety and matched-ISA Rust**,
tracks `clang -O3` to within ~9%, and beats Go by 2.3×. The workload is
pointer-chasing (the tree walk) plus `Vec` growth (the frontier and the result),
a shape with no allocation-free inner loop for any language to run away on —
which is why the compiled languages cluster and Go's GC is what separates it.

## Compiler findings

The arms are clean — zero `karac check` diagnostics across all six sources, all
byte-identical under `karac run`, `karac build`, the default auto-parallelising
build, and `--interp`.

### One defect: codegen's `Map.keys()` can iterate SORTED and seed-independent, diverging from the interpreter

Filed as kara `B-2026-09-04-15`. `Map` iteration order is specified to be
per-process random (SipHash under a random key, pinnable with `KARAC_HASH_SEED`).
It is, under `--interp`. Under **codegen (JIT and AOT alike) a
`Map[i64, Vec[i64]].keys()` can instead iterate in sorted key order, identical at
every seed** — but only when a **structurally identical function over a
`SortedMap`** is also present in the module. This kata's differential is exactly
that shape (arm D over `Map`, arm A over `SortedMap`, near-identical bodies), which
is why the sort-removal mutant survives codegen while the interpreter kills it.

Minimal reproduction (`repro/map_keys_sorts.kara` / `repro/map_keys_random.kara`):
two BFS functions differing only in `Map` vs `SortedMap`. With the `SortedMap`
twin present, the `Map` arm's keys print sorted and seed-independent under
`karac build`, random under `--interp` — a run-vs-build divergence. Delete the
twin and codegen returns to random order. The trigger needs the growing map to
cross a rehash boundary (a small literal tree does not fire it; the 25-node
generated tree does), which points at the rehash path rather than the `keys()`
lowering itself.

The divergence is usually benign — sorted iteration is often what a user
accidentally wants — but it violates the documented contract, defeats
`KARAC_HASH_SEED` reproducibility, and silently masks order-dependence bugs,
which is exactly what it did to the mutant here.

### Two deferrals hit while writing the arms

- **Chained indexed receiver** (`cols[i][j].to_string()`) is a documented v1.x
  codegen deferral (MR5, `src/codegen/calls.rs`), so the demo formatter binds the
  element first (`let v = cols[i][j]; v.to_string()`). This kata is the "real
  workload" the checklist entry said would justify closing it.
- **`let`-destructuring a `ref` tuple** (`let (n, c) = ref_tuple`) is rejected
  (`tuple pattern used but type is 'ref (…)'`), while `match ref_tuple { (n, c) => … }`
  works and a consuming `for (n, c) in vec` works. The arms use the consuming
  `for` form; the residual is the `let` half of kara `B-2026-08-11-11`, still
  open.
