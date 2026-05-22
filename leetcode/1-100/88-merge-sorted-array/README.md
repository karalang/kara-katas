# 88. Merge Sorted Array

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-sorted-array](https://leetcode.com/problems/merge-sorted-array/)

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and integers `m` and `n` representing the number of valid elements in each. `nums1` has length `m + n` — the first `m` slots are the sorted prefix, the last `n` are scratch. Merge so that `nums1` ends up sorted in non-decreasing order. The merge must be in-place; no value is returned.

**Constraints:** `0 ≤ m, n ≤ 200`, `nums1.length == m + n`, `-10⁹ ≤ nums1[i], nums2[i] ≤ 10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Two pointers from the back | O(m + n) time, O(1) extra space | [`two_pointer.kara`](two_pointer.kara) ✓ | [`two_pointer.py`](two_pointer.py) ✓ |

## Why write from the back

A forward merge would have to shift `nums1`'s prefix out of the way before reading it, costing O((m + n)²) or requiring an O(m + n) auxiliary buffer. Writing from the back side-steps this: the write head `k = m + n − 1` is always at or past both read heads `i` and `j` — every cell is written before it would be read, so no shifting and no aux buffer. The loop runs while `j >= 0` rather than while both heads are valid: once `j` falls below zero, any remaining `nums1[0..=i]` entries are already in place. The opposite exhaustion (when `i` falls below zero with `j` still valid) is handled by the `i >= 0 and …` guard, which forces the else-branch to drain `nums2`.

## Kāra features exercised

- **`mut Slice[i64]` parameter** — `merge` mutates the caller's buffer in place.
- **Call-site `mut` marker** — `report(mut a1, 3, b1, 3)` marks the fresh `let mut`; inside `report`, the `merge` call forwards an in-scope `mut Slice` without the marker (design.md Feature 4 Part 1½, Rule 2).
- **Mixed `mut` and read-only slice params on one function** — `merge` takes one of each.
- **Short-circuit `and`** — the `i >= 0 and nums1[i] > nums2[j]` guard relies on left-to-right evaluation to keep `nums1[i]` from indexing with a negative `i`.
- **Signed `i64` indices that go negative** — all three counters decrement past zero before exit.

## Running

```bash
karac run two_pointer.kara
python3 two_pointer.py
diff <(karac run two_pointer.kara) <(python3 two_pointer.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 5 --runs 30` across the three binaries. `m = n = 1_000_000` (total `2_000_000`), `K = 10` outer iterations. Each iteration refills the front `m` slots of the workspace from a pre-built sorted prefix, then calls `merge`. The merge mutates in place, so without the refill subsequent iterations would be no-ops; the refill is O(m) and is counted in the measured time, identically in all three implementations.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact (`bench/target/two_pointer_kara` and `bench/target/two_pointer`).

| File | What it does |
|---|---|
| [`bench/two_pointer.kara`](bench/two_pointer.kara) | m = n = 1_000_000 maximally-alternating inputs (`prefix_a = [0, 2, …, 2m−2]`, `b = [1, 3, …, 2n−1]`), K = 10 outer iterations, refill + merge each iter |
| [`bench/two_pointer.py`](bench/two_pointer.py) | Algorithmic mirror — same m, n, K, alternation |
| [`bench/two_pointer.rs`](bench/two_pointer.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sum-of-results sink (`K × workspace[total − 1] = 10 × 1_999_999 = 19_999_990`) so the algorithm's output participates in I/O and can't be elided. The maximally-alternating input forces the inner branch to flip every iteration, which is the worst case for the predictor and stresses the compare + conditional store.

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `two_pointer` | 14.6 ± 0.6 ms | 16.6 ± 0.5 ms | **1.14× faster than Rust** |

The inner loop is dominated by an unpredictable branch with two indexed reads and one indexed write — a regime where neither frontend can vectorize (the data dependency on `i`/`j`/`k` is loop-carried) and the gap reduces to per-iteration overhead. The maximally-alternating input is the worst case for the branch predictor, so both frontends are emitting essentially the same compare + conditional store sequence; karac's tight inner-loop emission now matches or slightly exceeds rustc here. Bounds-check elision (still planned P0; rationale in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)) would push the margin further but is no longer the headline story.

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 14.6 ± 0.6 ms |
| `rust two_pointer` | 16.6 ± 0.5 ms |
| `py two_pointer` | 693.3 ± 2.9 ms |

Python is **~47× slower** than Kāra codegen — the per-iteration CPython bytecode dispatch dominates everything else when the body is two compares, two reads, and one write.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 56.1 ± 0.9 ms | 32.9 KiB |
| `rustc -O two_pointer.rs` | 88.6 ± 1.3 ms | 455.4 KiB |

Kāra compiles this kata **1.58× faster** than `rustc -O` and produces a binary **~93% smaller** (14× the size disparity, vs the ~35% disparity measured against the same source on 2026-05-15). The much smaller binary tracks the much narrower runtime surface this workload reaches — `Vec.filled` + indexed read/write, `Slice[i64]` indexing, `println(i64)` — and nothing else. The cross-archive LTO + DCE work landed 2026-05-12 elides the rest of the runtime (HTTP, JSON, tokio subgraph, `Map`, `String`, shared structs) cleanly when downstream features aren't reached. Same shape as kata [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size).

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 31.7 MiB |
| `rust two_pointer` | 31.7 MiB |
| `py two_pointer` | 100.8 MiB |

**Parity with Rust on memory**, byte-for-byte. The bench holds three `Vec[i64]`s simultaneously — `prefix_a` (1M × 8B = 8 MiB), `b` (8 MiB), and `workspace` (16 MiB) — for a 32 MiB steady-state baseline. The May-15 snapshot measured kara at 48.2 MiB against the same `Vec.filled(total, 0)` source; the 16 MiB headroom traced to a karac drop / allocator pathway that has since been fixed, and the current build matches Rust's `vec![0; TOTAL]` allocation profile exactly. Same story as kata [#4](../4-median-of-two-sorted-arrays/#runtime-memory-peak) and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
