# 270. Closest Binary Search Tree Value

Given a BST and a floating-point `target`, return the node value closest to it.
**If two values are equally close, return the smaller one.**

```
[4,2,5,1,3]  target 3.714286  ->  4
[4,2,5,1,3]  target 2.5       ->  2     tied with 3 — the smaller wins
[4,2,5,1,3]  target 3.4       ->  3     the descent's last node, luckily
[4,2,5,1,3]  target 3.6       ->  4     the answer is an ANCESTOR
```

**Constraints:** `1 ≤ n ≤ 10⁴`; `0 ≤ Node.val ≤ 10⁹`; `-10⁹ ≤ target ≤ 10⁹`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `closest_bst_value.kara` ★ | descend toward the target, tracking the best seen | O(h) |
| `closest_bst_value_scan.kara` | visit every node, no search-tree property used | O(n) |
| `closest_bst_value_bounds.kara` | find the floor and the ceiling, then decide between two | O(h) |
| `differential.kara` | 4,000 randomized trees, three solvers cross-checked | — |

The tree is parallel arrays — `val`, `left`, `right`, `-1` for a missing child —
so every mirror is identical and the algorithm is the descent, not the
representation.

## The descent cannot just run to a leaf

The closest value is very often an **ancestor** of where the search ends.
Descending toward `target` narrows the interval containing it, and the best
candidate is whichever bound was tightest on the way down — so the answer has to
be tracked at every step, not read off the final node. A solver that returns the
last node visited is right on the easy cases and wrong whenever the target falls
in a gap. Injected, that mistake costs **1,289 mismatches** out of 4,000.

## The tie rule is where a correct-looking comparison goes wrong

With `target = 2.5` and values 2 and 3 the distances are exactly equal, and the
answer is 2. Written the obvious way:

```kara
if d < best_diff { best = v; best_diff = d; }     // strict — keeps the first seen
```

the winner depends on **visit order**, which differs between a descent and a full
scan. So the comparison has to break the tie on *value*:

```kara
if d < best_diff or (d == best_diff and v < best) { … }
```

Exact `==` on `f64` is not a smell here: a tie arises when the target sits at the
midpoint of two integers, and both distances are then the same representable
value, computed by the same subtraction.

## Why the third solver is the one that matters

Drop the tie-break from the ★ descent alone and the harness reports 376
mismatches. Drop it from the descent **and** the full scan — the two solvers that
both work by tracking a running best — and the count is unchanged at 376. But
where the detection comes from changes completely:

| tie-break dropped from | descent vs scan | descent vs bounds |
|---|---|---|
| the descent only | (differs) | 376 |
| **descent and scan both** | **0** | **376** |

**The two same-shaped solvers agree perfectly while both being wrong.** Only the
floor/ceiling form catches it, because it decides the tie *structurally* — floor
≤ target ≤ ceiling, so the floor is the smaller value and `<=` selects it without
comparing values at all. It cannot inherit a value-comparison bug because it
contains no value comparison.

That is the whole argument for a third mechanism rather than a third
implementation.

## Generator design

**Random float targets never tie.** Two values are equidistant only when the
target sits exactly at their midpoint, which a uniform draw hits with probability
zero — so a naive harness exercises the tie rule zero times and the strict-`<`
comparison passes forever.

So the midpoints are **constructed**: one family targets exactly between two
adjacent tree values (always a tie, and always between the two closest values),
and another offsets that midpoint by a hair each way so the boundary is probed
from both sides rather than only landed on. Two more families sit exactly on a
value and outside the range entirely, the latter exercising the floor/ceiling
form's open side.

Over 4,000 cases: **30,334 nodes built**, **747 targets that genuinely tie two
values** (19%), and **1,254 outside the value range**.

### What constructing the midpoints buys

The tie bug was also run against a control generator drawing **every** target
uniformly — same seeds, same trees, only the target family changed:

| generator | ties produced | mismatches for the tie bug |
|---|---|---|
| constructed midpoints | **747** | **376** |
| uniform targets only | **5** | **1** |

Five ties in four thousand cases, and the bug shows up once — indistinguishable
from a flake. This is the same lesson as [#265](../265-paint-house-ii/)'s narrow
cost range and [#266](../266-palindrome-permutation/)'s small alphabet, arriving
through floating point: **the separating condition has to be manufactured, or it
does not occur.**

**Four failure modes measured:**

| injected bug | mismatches / 4,000 |
|---|---|
| descent returns the last node visited | **1,289** |
| tie-break dropped (either one or both distance-trackers) | **376** |
| floor/ceiling defaults a missing side instead of tracking it | **387** |

## Benchmark

`bench/` builds one **30,000-node BST and 100,000 f64 targets** once, then punches
the ★ O(h) descent over every target **22 times** — 2.2M descents. Sink `280341251`, reproduced by
**eight** builds: Kāra seq and auto-par, C seq and pthreads, Rust seq and rayon,
Go seq and goroutines, plus Python.

**This is the corpus's float lane.** Every node visited costs an i64→f64
conversion, a subtract, an absolute value, two f64 compares and a data-dependent
branch choosing the next child. There is an integer-division lane
([#258](../258-add-digits/)), a variable-divisor division lane
([#263](../263-ugly-number/)) and a pointer-chase lane
([#261](../261-graph-valid-tree/)), but nothing whose inner step is floating
point — this is that.

Sized to stay cache-resident on #261's lesson: three 30,000-element arrays plus
100,000 targets is about 1.5 MB, an order of magnitude below the 13 MB that made
#261 unrankable. The tree is built by random insertion, so its depth is the
~2·log₂(n) of a BST nobody rebalanced rather than the ~15 of a perfect one.

### What the x86 corroboration run shows

Re-measured 2026-08-15 when the parallel lane was added; the sink changed with
it (see below), so these supersede the earlier figures rather than confirming
them.

#### Sequential lane — per-core, `KARAC_AUTO_PAR=0`

| lang | mean (ms) | σ |
|---|---|---|
| Go | 491.4 ± 7.6 | 1.5% |
| Rust (checked + `target-cpu=v3`) | 496.7 ± 11.7 | 2.4% |
| Rust (checked, equal-safety) | 498.9 ± 16.0 | 3.2% |
| Rust | 518.6 ± 12.1 | 2.3% |
| **Kāra** | **535.9 ± 9.1** | 1.7% |
| C (`-march=x86-64-v3`) | 576.9 ± 14.4 | 2.5% |
| C | 594.1 ± 13.0 | 2.2% |

#### Parallel lane — 4 cores

| lang | mean (ms) | σ | user (ms) |
|---|---|---|---|
| **Kāra (`#[par_order_free]`)** | **152.6 ± 4.0** | 2.7% | 522 |
| Rust (rayon `par_iter`) | 155.7 ± 5.6 | 3.6% | 572 |
| Go (goroutines) | 155.9 ± 8.9 | 5.7% | 565 |
| C (pthreads — metal floor) | 183.9 ± 8.7 | 4.8% | 678 |

**Kāra is first in the parallel lane**, with a seq→par ratio of 535.9 → 152.6 ms —
**3.51× on 4 cores**. Its user time, 522 ms against the sequential lane's 522, says
the auto-par lowering adds no measurable total work here; rayon's 572 and Go's 565
are their schedulers' overhead, and C's 678 is the same `cmov` deficit the
sequential lane shows, multiplied across four threads.

**C is last in both lanes, and that is the same finding in two places.** The
sequential ordering is unchanged from the earlier measurement and its cause is
established below: `clang -O3` if-converts the child selection into a `cmov`
inside the address chain. A parallel lane that reproduced a *different* ordering
would have been the thing to distrust.

The sink is now `280341251` rather than the earlier `687179070`: it had to become
order-invariant for the parallel lane to exist. Each query contributes
`(t * 1000003 + best)` and those are summed — order-of-execution-invariant, while
the `t` factor keeps it sensitive to which query produced which answer, as a plain
sum of `best` would not be across 2.2M queries where answers repeat.

This one ranks: σ 1.8–2.9%, both C builds within 1% of each other, all three Rust
builds within 1%. **Kāra is 1.06× behind plain Rust and within noise of the
equal-safety build** — and the three Rust variants being indistinguishable is
itself informative, since a float compare has no overflow check to pay for.

**C is last, 1.21× behind Kāra, and the cause is confirmed: the `cmov`.** clang
if-converts the child selection, putting the comparison inside the *address*
dependency chain, where Kāra emits a branch the processor can speculate past.
Forcing LLVM to convert that `cmov` back to a branch — changing only the codegen,
not the workload or the source — takes C from **566.7 to 434.5 ms**, from last
place to level with Rust, on the same sink:

| build | mean | `cmov` in `main` |
|---|---:|---:|
| `clang -O3` (the lane) | 566.7 ms | 1 |
| `clang -O3 -mllvm -x86-cmov-converter-force-all` | **434.5 ms** | 0 |

So the whole C deficit is one if-conversion decision. This is
[#259](../259-3sum-smaller/)'s finding in a second setting — there plain
`rustc -O` if-converted a two-pointer loop and paid 65%; here `clang -O3`
if-converts a BST child selection and pays 23%. Both are serial dependency
chains where `cmov` forces a wait on the comparison and a branch does not.
`rustc` chose the branch here, which is why Rust was already fast.

### The lane measured nothing for two builds running

Two earlier versions produced numbers that had nothing to do with the languages.

**First, hand-written `abs`.** All five mirrors defined
`if x < 0.0 { 0.0 - x }`, on the theory that a shared spelling was parity-safe.
Backwards: every one of these languages *has* an absolute value — Kāra included
(`f64.abs()`) — so hand-writing it is the unnatural spelling everywhere, and
clang compiled it into a six-op branchless select inside the dependency chain
where `fabs` is one `andpd`. Worth **23%** to C by itself.

**Second, and worse, the generator confined every value to a 32K window.**
`state / 65536` on a 31-bit LCG is the top 15 bits and maxes at 32,767, so the
intended `% 1000000` never fired. Tree values spanned 0–32,767 instead of
0–999,999, and targets came out in **[−50999, −17233]** — *below every value in
the tree*. Every descent ran the left spine and returned the minimum.

The tell was a probe that could not fail: two attempts at a "predictable
direction" variant produced a sink byte-identical to the original, from two
independent toolchains. The original was already doing what the probe meant to
induce.

| | C | Kāra | ratio |
|---|---:|---:|---:|
| hand-written `abs`, 32K window | 1090.2 ms | 465.6 ms | 2.34× |
| `fabs`, 32K window | 850.0 ms | 385.9 ms | 2.20× |
| **fixed (published)** | **568.2 ms** | **470.5 ms** | **1.21×** |

A "C is 2.3× slower than Kāra" headline was available at every stage and would
have been wrong at every stage. Method in
[`bench/probe/README.md`](bench/probe/README.md).

Kāra's binary is 332.9 KiB against C's 15.7 KiB, Go's 2.22 MB and Rust's 3.87 MB;
peak RSS is 4.0 MiB against C's 2.9 MiB.

Published numbers await the Apple-silicon host —
`bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts).

## Kāra features exercised

- **`f64` arithmetic and comparison** on every surface — the interpreter, the
  JIT and both AOT builds agree byte for byte, which is not free: the
  interpreter's int-to-float handling was being fixed earlier the same day.
- **No implicit int/float promotion** — `sorted[at] as f64` is required, and the
  diagnostic says so. Note the asymmetry with integer *widening*, which **is**
  implicit at a declared destination: two different rules, both deliberate.
- **Cast precedence** — `((seed / 65536i64) % 4800i64) as f64` needs its parens;
  `as` binds tighter than `%`.
- **Parallel-array trees** with `-1` sentinels, and an explicit `Vec` stack for
  the iterative full traversal.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found.

## Running

```bash
karac run closest_bst_value.kara
karac run closest_bst_value_scan.kara
karac run closest_bst_value_bounds.kara

diff <(karac run closest_bst_value.kara) <(python3 closest_bst_value.py) && echo OK
diff <(karac run closest_bst_value.kara) <(karac run closest_bst_value_scan.kara) && echo OK
diff <(karac run closest_bst_value.kara) <(karac run closest_bst_value_bounds.kara) && echo OK

# 4,000 randomized trees, three mechanisms cross-checked
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in closest_bst_value closest_bst_value_scan closest_bst_value_bounds differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

```bash
# cross-language benchmark (needs hyperfine, rustc, clang, go)
BENCH_OUT=results.container-x86.json bash bench/bench.sh
```
