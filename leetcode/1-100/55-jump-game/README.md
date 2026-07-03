# 55. Jump Game

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming · Greedy &nbsp;·&nbsp; **Source:** [leetcode.com/problems/jump-game](https://leetcode.com/problems/jump-game/)

From index 0, `nums[i]` is the maximum forward jump length from `i`. Return **whether** you can
reach the last index.

```
[2,3,1,1,4]  →  true    (0 → idx1 → last)
[3,2,1,0,4]  →  false   (index 3 holds a 0 nothing overshoots — stuck)
```

**Constraints:** `1 ≤ n ≤ 10⁴`, `0 ≤ nums[i] ≤ 10⁵`. This is the **decision** sibling of
[#45 Jump Game II](../45-jump-game-ii/), which counts the *fewest* hops on inputs guaranteed
reachable; here reachability is exactly the question, and a single scalar answers it. Every
index and reach stays far inside `i64`.

## Why this kata — reachability as a reach-closure, read three ways

Reachability is the transitive closure of the relation "index `i` reaches every `j` in
`(i, i+nums[i]]`". The last index is reachable iff it lies in that closure of `{0}`. The three
canonical solvers are three factorings of that one closure — grow it forward, shrink a goalpost
backward, or materialize it as a table:

| Lens | State | The idea in one line |
|---|---|---|
| **Greedy forward max-reach** ★ | one scalar | carry `farthest` = rightmost reachable index; if the cursor ever passes it, bail; else extend by `i + nums[i]` |
| **Backward last-good index** | one scalar | seed `good = n-1`; scanning right-to-left, any `i` with `i + nums[i] ≥ good` becomes the new `good`; reachable iff `good == 0` |
| **Bottom-up DP** | `Vec[bool]` | `reach[j]` = can `j` be stood on?; from each reachable `i` mark `(i, i+nums[i]]` — the literal closure |

**Greedy** grows the closure into a single running horizon: `farthest` is the closure's right
edge, and the only way to fail is for the cursor to walk off it (a `0`-cell with nothing
overshooting). **Backward** evaluates the same relation from the destination: it walks a
goalpost `good` leftward onto every index that can still reach it, and success is the goalpost
arriving at 0. **DP** discards the greedy shortcut entirely and writes the closure out cell by
cell, paying `O(n²)` for the honesty.

**The shared correctness pin — the "stuck" case.** All three must return `false` on
`[3,2,1,0,4]`: index 3 holds a `0`, and no earlier reach overshoots it, so the closure of `{0}`
stops at index 3 and never touches index 4. That single input is what each solver's core test
is really about:

- **Greedy** reaches index 3 with `farthest == 3`, then at `i == 4` finds `4 > farthest` and
  bails — the horizon stalled one short.
- **Backward** never lets `good` move left of 4 until some `i` clears it; index 3's reach
  `3 + 0 = 3 < 4` fails the test, and no index to its left reaches 4 either, so `good` never
  reaches 0.
- **DP** marks nothing beyond index 3, so `reach[4]` stays `false`.

Three encodings of one closure, one input that separates "reachable" from "stuck" — that
convergence is the kata. The dual trivial pin is `[0]` (`n == 1`): already standing on the last
index, so all three return `true` without a single jump.

## Approaches

| Approach | File | Time · Space | Answer via |
|---|---|---|---|
| **Greedy forward max-reach** ★ | [`jump_game.kara`](jump_game.kara) | `O(n)` · `O(1)` | running `farthest` horizon |
| **Backward last-good index** | [`jump_game_backward.kara`](jump_game_backward.kara) | `O(n)` · `O(1)` | goalpost `good` walked to 0 |
| **Bottom-up reachability DP** | [`jump_game_dp.kara`](jump_game_dp.kara) | `O(n²)` · `O(n)` | `reach[n-1]` table lookup |
| Oracle | [`jump_game.py`](jump_game.py) | — | mirrors all three + cross-checks them |

The greedy and backward forms are both allocation-free (a read-only `Slice[i64]` view + one
scalar) and `O(n)`; they differ only in which end of the closure they grow. The DP form
allocates one `Vec[bool]` and pays `O(n²)` — the literal-closure contrast, the same
table-vs-scan trade as [#45](../45-jump-game-ii/) and [#42](../42-trapping-rain-water/). All
three `.kara` files share a line-for-line-identical 12-case harness (mixed, leading/trailing
zeros, single-element, one-big-leap, and two distinct "stuck" arrays) and print one lowercase
boolean per case, diffing byte-for-byte against the Python oracle under `karac run`,
`karac build`, and the default auto-par build.

## What this kata surfaced

A **clean pass** — like [#45 Jump Game II](../45-jump-game-ii/), [#51 N-Queens](../51-n-queens/),
and [#53 Maximum Subarray](../53-maximum-subarray/), all three solvers typechecked, ran, and
built correctly on the first A/B run, agreeing with the oracle byte-for-byte across `karac run`,
`karac build` (`KARAC_AUTO_PAR=0`), and the default auto-par build. No compiler gap turned up.

The three shapes that could plausibly have snagged each behaved correctly on all surfaces:

- a **`Vec[bool]` DP table** grown with `push(false)` and written by computed index
  (`reach[j] = true`) — a heap boolean vector rather than the `Vec[i64]` sentinel table of
  [#45](../45-jump-game-ii/)'s DP solver, exercising bool as a first-class heap element;
- **early `return` out of a nested `while`** the moment the horizon covers the last index (the
  greedy solver returns from inside the scan, not by falling through);
- a **descending `i64` loop** (`i = n-2` down to `0`, guarded `i >= 0`) in the backward scan,
  the mirror of the forward katas' ascending counters.

The auto-par build was **byte-identical** to the sequential one for all three files, exactly as
expected: the greedy and backward scans carry a loop-borne dependency (`farthest` / `good`), and
the DP relaxation writes a shared `Vec`, so the reduction analyzer never engages any of them.

## Kāra features exercised

- **Read-only `Slice[i64]` view** — both the ★ greedy and the backward solver take the input as
  a bare `Slice[i64]` and walk it with a single `i64` scalar and no allocation, the
  in-place-scan footing of [#41](../41-first-missing-positive/) and [#45](../45-jump-game-ii/).
- **`Vec[bool]` reachability table** — the DP solver allocates one `Vec[bool]` of length n,
  seeds it with `push(true)` / `push(false)`, and relaxes it forward by computed index — bool as
  a heap element, the allocating contrast to the scalar scans.
- **Early `return` from a nested loop** returning `bool` — the greedy solver decides and exits
  mid-scan; the backward solver returns a `good == 0` comparison.
- **Descending `i64` loop** — the backward scan counts `i` down from `n-2` to `0`, the mirror of
  the ascending counters elsewhere in the corpus.
- **Three factorings of one reach-closure** — forward horizon, backward goalpost, and explicit
  DP table — all agreeing across the LeetCode examples under both `karac run` and `karac build`.

## Benchmarks

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh          # KARA_BENCH_INCLUDE_PY=1 to include the Python row
```

`bench/bench.sh` builds the Rust file with `rustc -O` (plus a `-C overflow-checks=on`
equal-safety variant), the C file with `clang -O3`, the Kāra file with `karac build`, and the Go
module with `go build` (all cached in `bench/target/`, gitignored), then times them with
`hyperfine` per the [BENCH.md protocol](../../../BENCH.md) and writes
[`bench/results.json`](bench/results.json).

| File | What it does |
|---|---|
| [`bench/jump_game.kara`](bench/jump_game.kara) | **Greedy forward max-reach kernel** over a length-1000 array, one `i64` checksum sink |
| [`bench/jump_game.rs`](bench/jump_game.rs) | mirror; `rustc -O` (+ `overflow-checks=on`) |
| [`bench/jump_game.c`](bench/jump_game.c) | mirror; `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | mirror; `go build` |
| [`bench/jump_game.py`](bench/jump_game.py) | mirror; CPython |

**Workload.** A reachable length-`N=1000` array `nums` (entries `1 + i%4`, so every index can
always step at least one forward and the last index is always reachable) is built **once**, then
**`TOTAL = 200000`** times a single slot is punched (`nums[k%n] = 1 + k%9`, a wider reach). Each
iteration runs the greedy scan, which returns the **index at which it decided** — here always the
early-exit point where `farthest` first covers the last index — and folds that index into a
rolling checksum (sink `989962259`). The punch is **not reverted**, so the array evolves, the
decision index varies with the loop index (no hoisting), and the checksum carries a loop-borne
dependency — a single-lane (seq) bench by construction. The hot loop **allocates nothing**;
every value stays well inside `i64` under Kāra's default overflow checking, so all six mirrors
fold to one **bit-exact, cross-language-diffable** value.

### Seq lane — runtime (single-threaded greedy forward max-reach)

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 5 --runs 30`, means:

| Implementation | Wall time | vs Kāra |
|---|---|---|
| `go   jump_game` (go build) | **81.6 ms ± 3.4 ms** | 1.35× faster |
| `rust jump_game` (`-C overflow-checks=on`) | 106.3 ms ± 2.6 ms | 1.04× faster (= safety) |
| `rust jump_game` (rustc -O) | 108.7 ms ± 1.6 ms | 1.02× faster |
| **`kara jump_game`** (codegen, seq) | **110.4 ms ± 2.8 ms** | — |
| `c    jump_game` (clang -O3) | 110.9 ms ± 2.3 ms | 1.00× (tie) |
| `py   jump_game` (CPython) | 7182 ms | 65× slower |

**Kāra ties the C/Rust cluster and Go pulls ahead.** The C-family — `rustc` (108.7), its
equal-safety variant (106.3), C (110.9), and Kāra (110.4) — all land inside a ~4.6 ms band, well
under a single run's noise (σ ≈ 2–3 ms). Kāra is **dead-even with `clang -O3`** (110.4 vs
110.9 ms, a 0.5 ms tie) and within noise of both Rust variants, including the
overflow-checks-on comparator that matches Kāra's checked-by-default integer semantics
([design.md § Arithmetic Overflow](../../../../kara/docs/design.md)) — so there is **no safety
tax to isolate** on this branch-predictable scalar scan.

The one real spread is **Go, ~1.35× ahead at 81.6 ms.** Unlike [#45](../45-jump-game-ii/), where
every native mirror (Go included) tied within ~4%, `gc` lowers *this* particular kernel — a
bounds-checked linear scan with an early-exit `return` and a running max — into a tighter inner
loop than the LLVM/`gc` back ends produce for the C-family here. It is a codegen difference on
the scan shape, not an algorithmic one: all six run the identical greedy solve and fold the
identical checksum. Kāra's default-safe output sits squarely with C and Rust; the honest finding
is a C-class tie with Go the outlier, rather than [#45](../45-jump-game-ii/)'s six-way dead heat.
Python runs the identical algorithm interpreted, ~65× behind.

### Compile time, binary size, memory

Snapshot — M5 Pro, 2026-07-03, hyperfine `--warmup 1 --runs 10` (compile, cold via `--prepare`);
size and peak RSS are single deterministic samples.

| Compiler | Compile (cold) | Binary | Peak RSS |
|---|---|---|---|
| `clang -O3` | **43.9 ms** | **32.7 KiB** | **1.02 MiB** |
| `rustc -O` | 84.1 ms | 455.6 KiB | 1.05 MiB |
| **`karac build`** | **77.8 ms** | **33.4 KiB** | **1.03 MiB** |
| `go build` | — (excluded; mixes module + std-lib link) | 2434.1 KiB | 2.67 MiB |

Kāra emits a binary **~13.6× smaller than Rust** and line-ball with C (33.4 vs 32.7 KiB), and
ties C and Rust for peak RSS (~1.0 MiB, ~2.6× under Go and ~6.5× under CPython). Its cold compile
**edges `rustc -O`** (77.8 vs 84.1 ms) on both elapsed and peak compiler RSS (18.4 vs 26.5 MiB);
`clang`'s 43.9 ms / 2.5 MiB is the floor. Every figure lands within noise of
[#45](../45-jump-game-ii/)'s — the two katas compile the same shape of tiny integer kernel.

**No par lane — by construction.** The greedy solve is pure per iteration, but the checksum
reduction carries a loop-borne dependency, so karac's auto-par pass does not fire: the default
and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded.

---

**Bug ledger:** none — no compiler change was required for this kata (all three solvers
typechecked, ran, and built correctly on the first pass, and agree with the oracle under
`karac run`, `karac build`, and the default auto-par build). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl) for the cross-kata history.
