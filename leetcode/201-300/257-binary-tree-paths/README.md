# 257. Binary Tree Paths

Every root-to-leaf path, rendered as `"1->2->5"`.

```
[1,2,3,null,5]  ->  ["1->2->5", "1->3"]
[1,2]           ->  ["1->2"]        the root has ONE child, so it is not a leaf
[]              ->  []
```

**Constraints:** `0 ≤ n ≤ 100`; `-100 ≤ Node.val ≤ 100`.

## Approaches

| file | what the path is carried as | copying cost |
|---|---|---|
| `binary_tree_paths.kara` ★ | a `String` extended at every node | O(n · depth) bytes |
| `binary_tree_paths_join.kara` | a `Vec[i64]`, rendered once per leaf | O(leaves · depth) |
| `binary_tree_paths_iter.kara` | explicit `Vec[Frame]`, prefix per frame | O(n · depth) |
| `differential.kara` | 4,000 randomized trees, all three agree | — |

## The mechanism

**A node with exactly one child is not a leaf.** That is the only rule here that
is easy to get wrong, and `[1,2]` yields one path rather than two because of it.

**The ★ file's cost is where the interest is** — and the dominant term is
memory, not copying. It builds a fresh prefix at every node, and each recursion
frame keeps its own alive for the duration of the call below it. On a spine that
means **O(depth²) bytes live simultaneously**; the join file holds one
`Vec[i64]`, so O(depth). Measured on a pure spine at n = 12,000:

| | time | peak RSS |
|---|---|---|
| `binary_tree_paths.kara` ★ | 0.29 s | **355 MB** |
| `binary_tree_paths_join.kara` | 0.00 s | **4.7 MB** |

At n = 24,000 the ★ form needs ~1.4 GB and takes **67 s**, against the ~1.2 s an
n² extrapolation predicts — past a point it is thrashing, not computing.

**An earlier version of this README got that claim wrong**, and the measurement
is what caught it. It said the join form is O(leaves · depth) and therefore O(n)
"on a path-shaped tree" — true only for a tree with ONE leaf. The first probe
generator branched 4% of the time, yielding ~0.04n leaves, so `leaves · depth`
is quadratic and **both** walks measured n²:

```
n=3000   string 0.02s   join 0.01s
n=6000   string 0.08s   join 0.07s
n=12000  string 0.31s   join 0.27s
```

Four percent branching was enough to erase the entire distinction. The
measurement now lives in [`bench/probe/`](bench/probe/) on a pure spine, where
the two separate by ~75× on memory.

The join file pays for that with state: its `Vec[i64]` is shared across the whole
walk, so the `pop` on the way back up is **mandatory**. The ★ file needs no undo
because each recursion owns its own prefix. Cheaper bytes, more careful state.

## Ownership shaped two of these files

Both were `perf[rc-fallback]` diagnostics — not errors, and not silenced.

**★:** `prefix: String` was consumed by the left recursion and re-used by the
right. The fix was to say what was meant — `prefix: ref String`. The walker never
keeps a prefix, it only reads one to build the next; the single owned copy
happens at the **leaf**, which is exactly where a new string comes into being.

**Iterative:** `f.prefix` read twice moved the field out of the owned frame
twice. Binding it to a local did *not* help — `push_str` accepts an owned value
or a borrow, and an owned local passed to it counts as a **consume** even though
the callee only copies bytes. The intended spelling routes through a `ref`
parameter, so the extension became a helper:

```kara
fn extend(prefix: ref String, v: i64) -> String { … }
```

which removed the RC and the duplication together. The compiler's own
`is_str_like` exists to allow exactly this, and its comment cites kata #722,
where the same call was rejected under `build` while `run` only warned.

### That second one turned out to be a compiler issue — kara `B-2026-08-13-1` (fixed)

Investigating the diagnostic rather than silencing it (the help text offers
`#[allow(rc_fallback)]` first) showed the ownership checker is **inconsistent
across the three methods the compiler documents together as read-only**:

| call, on an owned argument | ownership |
|---|---|
| `a.push_str(s)` twice | **MOVED** |
| `s.starts_with(t)` twice | **MOVED** |
| `s.contains(t)` twice | clean |
| receiver reuse, `s.contains(lit)` twice | clean |
| argument via a `ref String` parameter | clean |

`is_str_like`'s own comment names all three as methods where *"the callee only
copies/scans the bytes, so there is no ownership reason to demand a move"* — the
typechecker was widened to accept a borrow, but the ownership checker still
classifies the owned-argument case as a consume for two of the three.

It is **not** a correctness bug: the value really is still readable afterwards,
and the same program prints identically under `run` and `build`. The cost was a
spurious move report, an unnecessary RC in harder shapes, and — as here — a
helper function introduced purely to turn two owned reads into two borrows.

**Fixed in `1299fd3`.** The cause was a single table: `collect_method_param_modes`
seeds builtin methods that have no syntactic signature, and `String.contains` was
the only String method ever added to it. That is the entire asymmetry above —
`contains` was on the list and the other two were not.

The fix went **wider than this kata measured**. The row named three methods,
taken from `is_str_like`'s doc comment; probing the neighbouring surface found
the same false positive on four more — `ends_with`, `find`, `split` and
`replace` — all fixed alongside. A doc comment's examples were treated here as
the population, which they were not.

`extend(prefix: ref String, v: i64)` is **kept**, but on style grounds now rather
than necessity: the inline spelling that used to warn re-checks clean against the
fixed compiler, and both produce identical output. It survives because factoring
two near-identical four-line constructions into a named function is better code,
not because the compiler requires it.

## Order is part of the answer

The iterative file must push the **right** child before the left, because the
stack is LIFO. Getting it backwards produces the right *set* of paths in fully
reversed order — measured, not assumed:

```
correct        [1->2->4, 1->2->5, 1->3->6, 1->3->7]
pushes swapped [1->3->7, 1->3->6, 1->2->5, 1->2->4]
```

So `differential.kara` compares an **order-sensitive positional digest**, not a
set or a sorted list. A sorted-set comparison would call those two identical and
the bug would ship.

## Generator design

A uniformly random tree is bushy: every path is short, and the ★ file's
O(n · depth) copying never diverges from the join file's O(leaves · depth) — the
distinction the kata exists to show goes untested. So the generator draws a high
null rate per side and makes **one case in three a pure spine**, producing trees
of depth near n with one or two leaves.

Over 4,000 cases: **18,146 nodes, 5,200 paths, longest rendered path 57 chars.**

## Benchmark

`bench/` builds one **random bushy tree of 150,000 nodes once**, then enumerates
every root-to-leaf path **5 times** with the ★ string-extending DFS. Depth is
~2·log₂(n) ≈ 34, so prefixes stay short and the work is path enumeration rather
than the pathological memory profile a spine produces (that lives in
[`bench/probe/`](bench/probe/)). Sink `489173119`, reproduced by all four
mirrors.

The ★ form is benched rather than the join form because those two differ in an
**intra-language algorithmic** property; mirroring both in four languages would
measure the same algorithmic fact four more times.

### The mirrors had to be equalised first

The first run read as a language result — C 315.7 ms against Rust 468.8 — on a
workload that is mostly string building. It was not. Two hypotheses, both
measured:

| hypothesis | test | result |
|---|---|---|
| Rust's `format!` machinery | swap to `write!` | 463 → 455 ms, **inside noise** |
| allocation strategy | Rust `String::with_capacity` | 473 → **372 ms** |

C computes the exact length and `malloc`s once; Go's `a + b + c` allocates the
total in a single concatenation. Kāra and Rust started from empty and grew. That
one asymmetry accounted for roughly **70% of the apparent C-versus-Rust gap** —
the mirrors were not doing equal work, which is the cross-language parity rule
this corpus rests on.

`String.with_capacity` already exists in Kāra, so this was a mirror not using an
available facility, not a missing feature — worth checking, since the other
answer would have been a ledger row rather than a fix. All four now pre-size.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Go | 127.2 ± 4.7 ms | 0.76× |
| C `clang -O3` | 137.4 ± 1.1 ms | 0.82× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 149.5 ± 2.1 ms | 0.89× |
| Rust `-O` | 150.6 ± 3.1 ms | 0.89× |
| **Kāra (codegen)** | **168.4 ± 7.0 ms** | 1.00× |

**Kāra's parity with Rust does not survive this host.** On the container the two
were level (370.6 vs 386.9, overlapping error bars); here Kāra is **1.13× behind
equal-safety Rust** and the gap clears both σ. Against C it is 1.23×, essentially
the container's 1.22× — so C did not move relative to Kāra, Rust did.

That pattern points at allocation. This kata builds a fresh `String` per
root-to-leaf path and a fresh `Vec` per level, and the M5's cheaper allocator
rewards the lanes that allocate most aggressively — Go moves from third to first
(343.6 → 127.2 ms is a 2.70× improvement against Kāra's 2.20×). Kāra keeps its
distance from C, whose `malloc` shape it most resembles, and loses ground to the
two lanes with the more specialised allocators.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts).

| lang | mean (ms) | vs Rust |
|---|---|---|
| C | 303.9 ± 23.8 | 0.79× |
| Go | 343.6 ± 12.7 | 0.89× |
| **Kāra** | **370.6 ± 13.3** | **0.96×** |
| Rust (checked) | 379.7 ± 12.5 | 0.98× |
| Rust | 386.9 ± 27.0 | 1.00× |

**Kāra and Rust are at parity** — 370.6 against 386.9 with σ of 3.6% and 7.0%,
so the intervals overlap and the nominal 4% lead is not a lead. Against C the
1.22× gap does sit outside both error bars and is probably real.

Equalising moved every row on that host, and moved Kāra most: 482.7 → 370.6 ms,
a 23% improvement against Rust's 17%. The C gap narrowed from 1.53× to 1.22×.
That is the measure of how much the first run was reporting allocator strategy
rather than the algorithm.

## Kāra features exercised

- **`ref String` parameters** threaded through a recursion, and the contrast with
  an owned one — the subject of both rc-fallback diagnostics above.
- **A struct carrying a `String`** (`Frame { node, prefix }`) pushed onto a
  `Vec[Frame]` worklist, each frame owning its own prefix.
- **`Vec[i64]` push/pop backtracking** with a mandatory undo.
- **`String.bytes()`** for the positional digest, and `f"{…}"` rendering of
  negative values.
- **Index-pool tree from a level-order array**, shared with
  [#199](../../101-200/199-binary-tree-right-side-view/) and
  [#250](../250-count-univalue-subtrees/).

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python. All four are **rc-fallback clean**.

One compiler issue found: `B-2026-08-13-1` above, fixed in `1299fd3`. The ★
file's diagnostic was the checker working correctly on code that deserved
restructuring; the iterative file's was not, and only investigating it rather
than reaching for `#[allow(rc_fallback)]` told the two apart.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`489173119`). Workload: build one 150k-node random bushy tree once, then 5 rounds of full root-to-leaf path enumeration via the string-extending DFS; sink = positional digest over all rendered paths.

Runtime, sequential lane on Apple M5 Pro (6P+12E), 2026-08-17 (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| Go | 118.0 ms | 0.78× |
| C `clang -O3` | 127.3 ms | 0.85× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 137.4 ms | 0.91× |
| Rust `-O` | 138.2 ms | 0.92× |
| **Kāra (codegen)** | 150.3 ms | 1.00× |

Kāra checks integer overflow by default, so the honest Rust baseline is the `-C overflow-checks=on` row, not `rustc -O`. Single-machine snapshot (`bench/results.json`, karac 5c9268b1294e); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology and caveats. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
karac run binary_tree_paths.kara
karac run binary_tree_paths_join.kara
karac run binary_tree_paths_iter.kara

diff <(karac run binary_tree_paths.kara) <(python3 binary_tree_paths.py) && echo OK
diff <(karac run binary_tree_paths.kara) <(karac run binary_tree_paths_join.kara) && echo OK
diff <(karac run binary_tree_paths.kara) <(karac run binary_tree_paths_iter.kara) && echo OK

# 4,000 randomized trees, three builders cross-checked order-sensitively
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in binary_tree_paths binary_tree_paths_join binary_tree_paths_iter differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
