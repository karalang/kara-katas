# 895. Maximum Frequency Stack

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Hash Table, Stack, Design &nbsp;·&nbsp; **Source:** [leetcode.com/problems/maximum-frequency-stack](https://leetcode.com/problems/maximum-frequency-stack/)

`push(x)` adds an element; `pop()` removes and returns the **most frequent**
element, breaking ties toward the one pushed **most recently**.

```
push 5, 7, 5, 7, 4, 5     →  freq: 5→3, 7→2, 4→1
pop → 5    (only element with frequency 3)
pop → 7    (7 and 5 both at 2; 7 was pushed later)
pop → 5
pop → 4
```

**Constraints:** `0 ≤ x ≤ 10⁹`; at most `2·10⁴` calls; `pop` is only called on
a non-empty stack.

## Why this kata — a container nested in a container

The textbook solution keeps two maps and a running maximum:

| | |
|---|---|
| `freq: Map[i64, i64]` | live count per value |
| `buckets: Map[i64, Vec[i64]]` | for each frequency `f`, the values that reached `f`, in push order |
| `maxfreq` | largest `f` with a non-empty bucket |

`push` bumps `freq[x]` to `f` and appends `x` to `buckets[f]`; `pop` takes the
**last** element of `buckets[maxfreq]` — exactly the most-recent among the
most-frequent. Both are O(1).

That makes `Map[K, Vec[V]]` the point of the exercise: a container nested
inside a container, living on a struct, mutated through a `mut ref self`
method. It is the shape where a stale bucket handle or an over-eager temp drop
shows up as a **wrong sum** rather than a crash, which is why the stress driver
prints a checksum rather than just "ok".

## What it found

The idiomatic one-liner does not run:

```kara
self.buckets.entry(f).or_insert(Vec.new()).push(x);   // check passes, every backend fails
```

`karac check` accepts it; the interpreter then says *"method 'push' not found
on type 'unknown'"* and codegen says *"no handler for method 'push' on
non-identifier receiver"*. The same chain over a **local** map works
everywhere — the variable is the receiver's root being a struct **field**.
Filed as `B-2026-08-18-34`; `entry_chain_gap.kara` is the standing minimal
probe, with the working local and the failing field spelling side by side.

So `freq_stack.kara` uses the get/modify/insert round-trip instead. That is a
real canonical spelling, not a contortion to dodge the bug — but it copies the
bucket out and back, turning this problem's signature O(1) append into O(n).

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.
> Comparative claims below ("ahead of C", "leads Rust", ratios) were true of the snapshot and have **not** been re-verified against the current feed — treat them as historical, not as the standing result.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

> **Corroborating host only.** Linux/x86-64 container numbers from
> [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus publishes from
> the canonical Apple-silicon feed (`bench/results.json`), which this kata does not have yet —
> `bench.sh` refuses to write it from the wrong host rather than silently mixing them. Read
> [`BENCHMARKS.md`](../../../BENCHMARKS.md) before quoting any of this.

### Par lane — auto-par vs hand-tuned

All three parallelize the **same** reduction over independent rounds. kāra got there with
**no parallel source at all**: `karac build` recognized `checksum = checksum + round(r, steps)`
and emitted a `karac_par_reduce` dispatch. Rust needed `rayon`'s `into_par_iter`; Go needed
goroutine chunking, a `WaitGroup`, and a partial merge.

| | mean | |
|---|---:|---|
| **kāra — auto-par, no parallel code** | 10.0 ms ± 2.2 | — |
| Go — goroutines + WaitGroup | 11.6 ms ± 1.3 | 1.16× slower |
| Rust — rayon `par_iter` | 12.0 ms ± 1.7 | 1.20× slower |

kāra auto-par is **2.7× faster than its own sequential build** and edges out both
hand-written parallel versions. The loop body allocates — a fresh `FreqStack` with two maps per
round — so this exercises auto-par over heap-churning work rather than an arithmetic kernel.

### Seq lane — single-threaded, per-core codegen quality

| | mean | vs kāra |
|---|---:|---:|
| C `clang -O3` | 6.6 ms ± 0.3 | 4.03× faster |
| kāra `karac build` | 26.5 ms ± 1.0 | — |
| Go `go build` | 27.8 ms ± 1.7 | 1.05× slower |
| Rust `-C overflow-checks=on` (equal safety) | 34.7 ms ± 1.8 | 1.31× slower |
| Rust `rustc -O` | 35.3 ms ± 2.6 | 1.33× slower |

Workload: 120 rounds × 3,000 LCG-driven push/pop steps over a 12-value domain, sink `3299190`.
**kāra beats `rustc -O` and edges Go** on work that is almost entirely hash-map traffic.

> **This ordering does not survive the M5.** On the canonical Apple M5 Pro lane
> ([`bench/results.json`](bench/results.json), 2026-08-28) the row above
> **inverts**: kāra 28.4 ms against rust 15.3, rust_ovf 15.6, go 15.9, c 3.6 —
> kāra is **1.86× behind `rustc -O`** and 1.78× behind Go, not ahead of either.
> Container→M5, Rust improved 2.2× and C 1.8× while kāra went 26.5 → 28.4 ms,
> i.e. it took no benefit from the faster host at all. That "only kāra doesn't
> move" signature points at allocator-bound behaviour (the loop body builds a
> fresh `FreqStack` with two maps per round) rather than codegen, which is a
> hypothesis worth chasing and not a settled cause. Treat the sentence above as
> an x86-container result only.

Two caveats on the C row, both cutting against reading it as a like-for-like win:

- The C mirror hand-rolls an open-addressing table with a multiply-and-mask hash. Same
  *algorithm* — the corpus rule — but a far simpler map than Rust's SwissTable or Go's, and with
  12 distinct keys it sits entirely in L1. Closer to a floor for "what this costs with an ideal
  map" than an ergonomic competitor. It is also single-threaded: the par-lane kāra binary (10.0
  ms) is within striking distance of it.
- An earlier draft of that mirror indexed plain arrays by value instead of hashing — a different
  data structure, so not the same algorithm. It was rewritten before these numbers were taken.
## Files

| File | |
|---|---|
| `freq_stack.kara` | the kata, plus a 600-step deterministic stress |
| `freq_stack_explicit.kara` | the same algorithm with the bucket updated via an explicit `match` on `get` — the other canonical spelling, and a distinct lowering |
| `entry_chain_gap.kara` | standing probe for `B-2026-08-18-34` |
| `freq_stack.py` | the oracle mirror, same algorithm step for step |
| `bench/` | the harness: `bench.sh` (generated by `scripts/new-bench.sh`) plus C, Rust, Go and Python mirrors, a `rayon/` and a `go-par/` par-lane comparator |

Verified identical across `karac run --interp`, `karac run` (JIT), `karac
build`, and `KARAC_AUTO_PAR=0 karac build`, against the Python oracle —
including the stress checksum `5913`.
