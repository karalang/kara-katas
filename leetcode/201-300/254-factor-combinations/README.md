# 254. Factor Combinations

Every way to write `n` as a product of factors, each factor in `[2, n-1]` — so
the trivial `[n]` is excluded.

```
12 -> [[2,2,3],[2,6],[3,4]]
32 -> [[2,2,2,2,2],[2,2,2,4],[2,2,8],[2,4,4],[2,16],[4,8]]
37 -> []            (prime)
 1 -> []
```

**Constraints:** `1 ≤ n ≤ 2³¹ - 1`.

## Approaches

| file | how a combination is completed | emits `[2,6]` … |
|---|---|---|
| `factor_combinations.kara` ★ | split at each divisor: `path + [i, n/i]` | before `[2,2,3]` |
| `factor_combinations_close.kara` | recurse first, then close with the remainder | after `[2,2,3]` |
| `factor_combinations_iter.kara` | explicit stack of frames, LIFO | in a third order |
| `differential.kara` | exhaustive sweep 2..10,000, all three agree | — |

## The mechanism

**The non-decreasing rule is the whole algorithm.** Each level may only use
divisors at least as large as the one above it. Without it `[2,6]` and `[6,2]`
are both generated and must be de-duplicated afterwards, which costs far more
than never producing the duplicate.

**The `i * i <= remaining` bound is that same rule, not an optimisation.** Past
that point the cofactor `remaining / i` would be *smaller* than `i`, which the
ordering has already forbidden — so the loop condition and the rule are one
thing said twice.

**The three files differ in when a combination is finished.** The ★ file emits
the two-factor split the moment it finds a divisor, then recurses to split the
cofactor further. The close-the-tail file emits nothing at a divisor — it
recurses first and completes a combination by appending whatever is left, guarded
by `remaining >= start` (the ordering rule applied to the last element) and a
non-empty path (which is what excludes the trivial `[n]`). The worklist is the ★
recursion with the call stack made explicit.

**The worklist pays for its own iteration.** A recursion can push a divisor,
recurse, and pop on the way back because the undo point is known; a worklist has
none — the child frame is consumed long after the parent moved on — so each frame
gets its **own copy** of the path. `path.push(i)` / `path.pop()` in the ★ file
becomes a fresh `Vec[i64]` per frame here, which is the real cost of going
iterative and the kind of thing worth seeing in a language with explicit
ownership.

## What it found: two layered codegen gaps

The three solvers generate in three different orders, so their shared `render`
sorts the `Vec[Vec[i64]]` lexicographically before printing — comparing lengths
and elements, which is the natural way to canonicalise a list of lists. **That
comparator cannot be compiled.**

```
codegen: no handler for method 'len' on variable 'x'
(method dispatch fell through; this is a codegen bug — add a dispatcher arm
 in `compile_method_call` …)
```

The diagnostic names itself a codegen bug, so this is a dispatch fall-through
rather than a deliberate deferral. Boundary, probed:

| inside a `sort_by` comparator | build |
|---|---|
| `x.len()` on `Vec[Vec[i64]]` | ❌ |
| `x.len()` on `Vec[String]` | ❌ |
| `x[0]` index | ❌ |
| tuple field `x.0` | ✅ |
| element `.len()` **outside** any closure | ✅ |

So the comparator's parameters reach codegen with no element type attached:
field access needs no type lookup and works, while method dispatch and index
lowering both need one and fall through. It is a whole family — sorting a
`Vec[Vec[T]]` or a `Vec[String]` by *any* content-derived key cannot be built.

Every earlier `sort_by` in the corpus compares **tuple fields**
([#56](../../1-100/56-merge-intervals/), [#252](../252-meeting-rooms/),
[#253](../253-meeting-rooms-ii/)), which is why nothing has hit this before.

**Fixed upstream in `b90027e`** — and fixing it exposed a second one underneath.

### kara `B-2026-08-10-16` — `return` inside a comparator

Re-checking the fix against **this kata's own comparator** rather than the 8-line
repro that was filed showed the repro fixed and the kata still broken, now at a
different site:

```
Module verification failed: "Function return type does not match operand
type of return inst!  ret { i64 } %ord / i64"
```

Boundary, probed on `Vec[(i64,i64)]` so the element type is held fixed:

| comparator body | build |
|---|---|
| single expression `\|x,y\| x.0.cmp(y.0)` | ✅ |
| block, **implicit** tail | ✅ |
| if-expression tail (what [#253](../253-meeting-rooms-ii/) uses) | ✅ |
| block with explicit **`return`** | ❌ |

So it is the `return` *keyword* in comparator position, independent of element
type: the implicit-tail path unwraps the `Ordering` struct and the explicit-return
path does not.

**Not a regression from the first fix.** That commit touches no return-type
logic, its tests are all single-expression comparators, and #254 is the only
program in the corpus with a block-bodied comparator — so nothing else could have
exercised this path before or after. It is a pre-existing gap the first one was
masking: previously this kata failed *earlier*, at method dispatch, and never
reached module verification.

This kata's comparator needs an **early return from inside a while loop** —
compare element by element, exit at the first difference — which cannot be
written as an implicit tail without restructuring into a sentinel-and-flag shape.
**The natural spelling was kept** rather than contorted. Fixed in `568e6ff` —
which exposed a third gap directly underneath, `B-2026-08-10-17`: a `return`
nested inside an `if` or loop was typechecked against `()` rather than the
closure's return type. Fixed in `819af61`, and that terminated the chain. All
three solvers now build.

Worth noting how the third was framed: it is neither nesting-dependent nor
`sort_by`-specific — a plain `Fn(i64)->i64` argument reproduces it with no
comparator involved. What decides it is which closure arm typed the body.

## Verification status

| file | interp | JIT | build | auto-par | Python |
|---|---|---|---|---|---|
| `factor_combinations.kara` ★ | ✅ | ✅ | ✅ | ✅ | ✅ |
| `factor_combinations_close.kara` | ✅ | ✅ | ✅ | ✅ | — |
| `factor_combinations_iter.kara` | ✅ | ✅ | ✅ | ✅ | — |
| `differential.kara` | ✅ | ✅ | ✅ | ✅ | ✅ |

Every program is byte-identical across all four surfaces, and the two with
mirrors match Python. The corpus A/B run==build guarantee holds.

Three of these rows were blocked when the kata landed, through **three layered
gaps** — `-13` (element type), then `-16` (explicit `return`) underneath it,
then `-17` (nested `return` typechecked against `()`) underneath that. Each was
invisible until the one above it was fixed. The matrix was re-run unchanged after
the last landed: **no solver needed editing**, which is the outcome that
justifies having kept the natural spelling through all three.

## The differential compares without sorting

Because the three generate in different orders, the harness hashes each
combination and **sums** the hashes. Addition is commutative, so the digest
depends on the multiset of combinations and not on generation order — no sort,
and no risk of a sort quietly hiding a disagreement about content.

An exhaustive sweep beats random sampling here: the interesting inputs are highly
composite numbers, which are rare under a uniform draw and dense in a contiguous
range. Over `2..10,000` — **8,770 factorable, 129,813 combinations, worst case
661 combinations at n=8,640, deepest 13 factors.**

**The harness was tested against a known defect rather than trusted.** Breaking
the worklist's non-decreasing rule (child frames restarting from 2 instead of
`i`) makes it report **965 mismatches** over `2..2,000`; restored, `0`.

## Benchmark

`bench/` sweeps **n = 2 … 150,000**, fully factorising each by the ★
sqrt-bounded backtracking — **4,005,306 combinations**. An exhaustive sweep
rather than build-once + punch, because there is nothing to build once here: the
input is the range and the work is the recursion.

This is a **recursion-and-allocation** workload, which is what distinguishes it
from the sort-dominated lanes next door: every combination found allocates its
own `Vec[i64]`, and highly composite n produce hundreds. The sink is the same
order-independent summed hash the differential uses, so a mirror enumerating in
a different order still has to agree on the multiset. Sink `855631428`,
reproduced by the C, Rust and Go mirrors.

### What the x86 corroboration run shows

| lang | mean (ms) | vs Rust |
|---|---|---|
| C | 462.5 ± 24.2 | 0.66× |
| **Kāra** | **671.5 ± 24.9** | **0.96×** |
| Rust | 697.4 ± 33.6 | 1.00× |
| Go | 707.5 ± 33.6 | 1.01× |
| Rust (checked) | 797.0 ± 77.9 | 1.14× |

Kāra and Rust are **at parity** here — 671.5 against 697.4 with overlapping
error bars, so the apparent 4% lead is not a lead. Against equal-safety Rust
(`overflow-checks=on`, the comparison Kāra's default trapping actually matches)
Kāra is ahead, though that row's σ is 9.8% and deserves the same caution.

**This lane is evidence for where kara `B-2026-08-10-9` lives.** That row records
Kāra's `sort_by` running ~2× Rust's, isolated from two sort-dominated katas
([#252](../252-meeting-rooms/), [#253](../253-meeting-rooms-ii/)). Here — deep
recursion, millions of small allocations, no sort at all — Kāra is level. Two
lanes behind on sorting and one at parity without it is consistent with the gap
being the sort specifically rather than general codegen, which is what that row
claims but could not show on its own.

**The C mirror needed a parity fix worth naming.** Its first version hashed each
combination inline off the path without ever materialising it, while Kāra, Rust
and Go allocate a fresh array per combination. The sinks matched exactly, so it
passed every check — but per-combination allocation is precisely what this
workload measures, so that row would have been artificially fast. It now
materialises like the others.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Go | 127.0 ± 0.7 ms | 0.40× |
| C `clang -O3` | 193.8 ± 4.6 ms | 0.61× |
| **Kāra (codegen)** | **317.0 ± 8.5 ms** | 1.00× |
| Rust `-O` | 330.0 ± 6.9 ms | 1.04× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 334.4 ± 10.2 ms | 1.05× |

**Kāra and Rust remain at parity, and that is the load-bearing result** — 317.0
against 330.0 ms, with equal-safety Rust at 334.4. It held on the container and
it holds here, which is what makes this lane evidence rather than a data point.

**The Go row inverts, and the inversion is the textbook signal.** Go went from
fourth on the container (707.5 ms, 1.01×) to **first** here by a wide margin
(127.0 ms, 0.40×). This kata allocates a fresh `Vec[i64]` per combination across
4,005,306 combinations — a pure per-allocation workload — and per-allocation
katas are exactly the class that inverts when the allocator gets cheap relative
to compute (BENCHMARKS.md § Hosts). Go's bump allocator and concurrent collector
take the whole benefit; C's `malloc` takes most of the rest. Kāra's position
relative to *Rust* is unchanged because both pay a similar per-allocation cost.

**This lane is the control that isolates the sort residual, and the M5
strengthens it.** kara `B-2026-08-10-9` is fixed (`50a50e8`); its shuffled-input
residual `B-2026-08-11-28` is not, and on this host that residual reads **3.70×**
on [#252](../252-meeting-rooms/) and **2.04×** on
[#253](../253-meeting-rooms-ii/) — both wider than their pre-fix x86 numbers
(1.89× and 1.62×), which is why it is re-opened for disposition as
`B-2026-08-15-30`. Here, with deep recursion and millions of small allocations
but **no sort at all**, Kāra is level with Rust on both hosts (0.96× on the M5).
Two sort-dominated lanes diverging while this one stays pinned is a stronger
separation than the container alone could show.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts). Order there: `c < kara < rust < go < rust_ovf`.

## Kāra features exercised

- **`Vec[Vec[i64]]` built by backtracking** with push/pop path management.
- **A struct carrying a `Vec`** (`Frame { remaining, start, path }`) pushed onto
  a `Vec[Frame]` worklist — per-frame owned copies, no shared mutable path.
- **A multi-statement `sort_by` comparator** with a loop and early returns — the
  construct `B-2026-08-10-13` is about.
- **Overflow-safe `i * i <= remaining`** rather than `i <= remaining / i`; Kāra
  traps on overflow by default, so the multiplication form is a deliberate choice
  the LeetCode bound makes safe.

## Running

```bash
karac run --interp factor_combinations.kara
karac run --interp factor_combinations_close.kara
karac run --interp factor_combinations_iter.kara

diff <(karac run --interp factor_combinations.kara) <(python3 factor_combinations.py) && echo OK
diff <(karac run --interp factor_combinations.kara) <(karac run --interp factor_combinations_close.kara) && echo OK
diff <(karac run --interp factor_combinations.kara) <(karac run --interp factor_combinations_iter.kara) && echo OK

# exhaustive sweep 2..10,000, three generators cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# the one program that currently reaches every surface
karac build differential.kara && ./differential
```
