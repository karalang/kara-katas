# 1. Two Sum

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Hash Table &nbsp;·&nbsp; **Source:** [leetcode.com/problems/two-sum](https://leetcode.com/problems/two-sum/)

Given an array of integers `nums` and an integer `target`, return the indices of the two numbers such that they add up to `target`.

You may assume each input has exactly one solution, and you may not use the same element twice.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Brute force (nested loops) | O(n²) time, O(1) space | [`brute_force.kara`](brute_force.kara) ✓ | [`brute_force.py`](brute_force.py) ✓ |
| Hash map (single pass) | O(n) time, O(n) space | planned — needs `Map` in interpreter | [`hash_map.py`](hash_map.py) ✓ |

`✓` runs end-to-end today.

## Kāra features exercised

`brute_force.kara` uses fixed-size `Array[i64, N]`, `Slice[i64]` parameter coercion, `Slice.len()`, indexed access, `for` loops over half-open `0..n` / `(i+1)..n` range expressions, and array-literal tail returns. No `Vec`, `Map`, or strings yet.

## API shape

Each Kāra solution exposes a pure `two_sum(nums, target) -> Array[i64, 2]` (or equivalent return type) and a thin `report` that prints. `main` calls `report` with the test cases. The Python files mirror this with `two_sum` / `report` / `main`. This keeps logic separate from I/O so the functions are testable once a harness exists.

The Kāra brute force currently returns `Array[i64, 2]` with `[-1, -1]` as the "not found" sentinel. The Python equivalents return `tuple[int, int] | None`. When `Option[T]` is solid in the Kāra interpreter, refactor to `Option[(i64, i64)]` and drop the sentinel.

## Output format

Each `report` call emits two integers, one per line — the two indices, or two `-1`s if no pair is found. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
0
1
1
2
0
1
```

## Running

```bash
# Kāra
karac run brute_force.kara

# Python (any version with PEP 604 union syntax — 3.10+)
python3 brute_force.py
python3 hash_map.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust files with `rustc -O` and the Kāra files with `karac build` (both cached in `bench/target/`, gitignored), then runs `hyperfine --warmup 3 --runs 10` across all six implementations of the same workload:

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | N=5000 deterministic input, K=10 outer iterations, sentinel target so brute force never short-circuits (full 12,497,500 inner-loop comparisons per call) |
| [`bench/hash_map.kara`](bench/hash_map.kara) | Same N, K, target; single-pass `Map[i64, i64]` |
| [`bench/brute_force.py`](bench/brute_force.py) | Algorithmic mirror — same N, K, target |
| [`bench/hash_map.py`](bench/hash_map.py) | Same; single-pass dict |
| [`bench/brute_force.rs`](bench/brute_force.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/hash_map.rs`](bench/hash_map.rs) | Same; uses `std::collections::HashMap` |

All six print `-20` (sum-of-results sink so the algorithm's output participates in I/O and can't be elided).

### Codegen vs Rust (the headline)

Snapshot — M1, 2026-05-06, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `brute_force` | 101.8 ± 0.8 ms | 34.7 ± 0.9 ms | **2.9× of Rust** |
| `hash_map` | 3.1 ± 0.2 ms | 2.2 ± 0.1 ms | **1.4× of Rust** |

Two regimes show up cleanly:

- **Algorithm-dominated (`hash_map`, ~50 K ops).** Kāra is within **1.4×** of Rust. The gap here is the type-erased runtime collection (`Map[K, V]` dispatches through function pointers and stores keys/values as byte blobs). The 2026-05-06 indirection microbench attributed ~75% of this gap to erasure tax — closes to ~1.07× once Phase 4 monomorphizes Map/Set/Vec at the call-site type.
- **Inner-loop-dominated (`brute_force`, ~125 M comparisons).** Kāra is at **2.9× of Rust** — the inner loop hits a runtime bounds-check on every indexed read, which currently blocks LLVM's autovectorizer from firing. Closes once bounds-check elision lands (planned P0; rationale in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)).

### Codegen vs Python and the wider picture

Same snapshot, all seven viable rows (interpreter `brute_force` row omitted — see below):

| Run | Mean ± σ |
|---|---|
| `kara hash_map` (codegen) | 3.1 ± 0.2 ms |
| `kara brute_force` (codegen) | 101.8 ± 0.8 ms |
| `rust hash_map` | 2.2 ± 0.1 ms |
| `rust brute_force` | 34.7 ± 0.9 ms |
| `py hash_map` | 17.0 ± 0.4 ms |
| `py brute_force` | 2147 ± 417 ms |
| `kara hash_map` (interp) | 5824 ± 88 ms |

Python is **5.5×** slower than Kāra codegen on `hash_map` and **21×** slower on `brute_force` — the gap CPython opens against any compiled-with-codegen language at workload sizes that put algorithm time above interpreter-startup floors.

### What the compile pipeline costs today (interpreter context)

`karac run file.kara` re-runs the entire front-end every invocation (lex → parse → resolve → typecheck → effects → ownership) before tree-walking. At N=5000:

- `kara hash_map (interp)` = 5.8 s — 1860× slower than `kara hash_map (codegen)`. Pipeline rerun + tree-walk dispatch on every AST node.
- `kara brute_force (interp)` is dropped from the table at N=5000: tree-walk × 12.5 M comparisons takes ~7 minutes per run, which doesn't add information beyond "tree-walk doesn't scale to N²." If you want to time it, run that one row directly with `--runs 3`.

The interpreter-vs-codegen gap is **not** a Kāra-vs-X comparison — it's the cost of skipping `karac build`. Future work in this space is the tree-walk → bytecode → JIT progression tracked in the [interpreter perf brainstorm](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md).

### Why Rust is in the harness

Rust is Kāra's *semantic peer* — same family of compiled-with-ownership languages. Python is the ergonomic foil ("is the perf cliff worth the syntax?"); Rust is the convergence target ("are we approaching native compiled performance?"). The headline ratio for v1 is the codegen-vs-Rust gap above; that's the milestone the Phase 7 work targets.
