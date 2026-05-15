# 88. Merge Sorted Array

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array, Two Pointers, Sorting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/merge-sorted-array](https://leetcode.com/problems/merge-sorted-array/)

You are given two integer arrays `nums1` and `nums2`, sorted in non-decreasing order, and integers `m` and `n` representing the number of valid elements in each. `nums1` has length `m + n` — the first `m` slots are the sorted prefix, the last `n` are scratch. Merge so that `nums1` ends up sorted in non-decreasing order. The merge must be in-place; no value is returned.

**Constraints:** `0 ≤ m, n ≤ 200`, `nums1.length == m + n`, `nums2.length == n`, `-10⁹ ≤ nums1[i], nums2[i] ≤ 10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Two pointers from the back | O(m + n) time, O(1) extra space | [`two_pointer.kara`](two_pointer.kara) ✓ via `karac run` | [`two_pointer.py`](two_pointer.py) ✓ |

`✓` runs end-to-end today.

### Why write from the back

A forward merge would have to shift `nums1`'s prefix out of the way before reading it, costing O((m + n)²) or requiring an O(m + n) auxiliary buffer. Writing from the back side-steps this: the write head `k = m + n − 1` is always at or past both read heads `i` and `j` — every cell is written before it would be read, so no shifting and no aux buffer.

```
i = m - 1
j = n - 1
k = m + n - 1
while j >= 0:
    if i >= 0 and nums1[i] > nums2[j]:
        nums1[k] = nums1[i]
        i -= 1
    else:
        nums1[k] = nums2[j]
        j -= 1
    k -= 1
```

The loop runs while `j >= 0` rather than while both heads are valid: once `j` falls below zero, any remaining `nums1[0..=i]` entries are already in place. The opposite exhaustion (when `i` falls below zero with `j` still valid) is handled by the `i >= 0 and …` guard, which forces the else-branch to drain `nums2`.

## Kāra features exercised

- **`mut Slice[i64]` parameter** — `merge` mutates the caller's buffer in place. The LeetCode case-driver passes `Array[i64, N]` literals via `mut`; the bench passes a `Vec[i64]` via the same coercion.
- **Call-site `mut` marker** — `report(mut a1, 3, b1, 3)` marks the fresh `let mut` binding. Inside `report`, the call `merge(nums1, m, nums2, n)` forwards a `mut Slice` already in scope without the marker (design.md Feature 4 Part 1½, Rule 2).
- **Mixed `mut` and read-only slice params on one function** — `merge` takes one of each.
- **Short-circuit `and`** — the `i >= 0 and nums1[i] > nums2[j]` guard relies on left-to-right evaluation to keep `nums1[i]` from indexing with a negative `i`.
- **`while` loop with signed `i64` indices that can go negative** — the loop guards on `j >= 0` and decrements all three counters past zero before exit; this requires signed indexing throughout.

No `Map`, no strings, no shared structs.

## API shape

Each Kāra solution exposes `merge(nums1: mut Slice[i64], m: i64, nums2: Slice[i64], n: i64)` and a thin `report` that calls `merge` then prints the merged prefix. `main` calls `report` per test case. Logic is separate from I/O so the function is testable once a harness exists.

The Python file mirrors this with `merge(nums1, m, nums2, n) -> None` and the same `report` / `main` shape.

## Output format

One integer per line — every element of the merged array in order, one test case after another. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
1
2
2
3
5
6
1
1
1
2
3
4
5
6
1
2
3
4
5
6
```

## Running

```bash
# Kāra
karac run two_pointer.kara

# Python
python3 two_pointer.py
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

Snapshot — M1, 2026-05-15, hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Workload | Kāra (codegen) | Rust | Gap |
|---|---|---|---|
| `two_pointer` | 20.5 ± 1.7 ms | 16.4 ± 0.5 ms | **1.25× of Rust** |

The inner loop is dominated by an unpredictable branch with two indexed reads and one indexed write — a regime where neither frontend can vectorize (the data dependency on `i`/`j`/`k` is loop-carried) and the gap reduces to per-iteration overhead. The residual reflects Kāra's runtime bounds-check on every `nums1[i]` / `nums2[j]` / `nums1[k]` access; closes once bounds-check elision lands (planned P0; rationale in the [v62 brainstorm archive](../../../../karac-rust/brainstorming/archive/v62_interpreter_perf_and_binary_size.md)).

### Codegen vs Python

| Run | Mean ± σ |
|---|---|
| `kara two_pointer` (codegen) | 20.5 ± 1.7 ms |
| `rust two_pointer` | 16.4 ± 0.5 ms |
| `py two_pointer` | 681.4 ± 2.8 ms |

Python is **~33× slower** than Kāra codegen — the per-iteration CPython bytecode dispatch dominates everything else when the body is two compares, two reads, and one write.

### Compile time and binary size

Snapshot — M1, 2026-05-15, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build two_pointer.kara` | 61.4 ± 0.6 ms | 295.9 KiB |
| `rustc -O two_pointer.rs` | 88.6 ± 0.7 ms | 455.4 KiB |

Kāra compiles this kata **1.44× faster** than `rustc -O` and produces a binary **~35% smaller**.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara two_pointer` (codegen) | 48.2 MiB |
| `rust two_pointer` | 31.7 MiB |
| `py two_pointer` | 101.0 MiB |

The bench holds three `Vec[i64]`s simultaneously — `prefix_a` (1M × 8B = 8 MiB), `b` (8 MiB), and `workspace` (16 MiB) — for a 32 MiB steady-state baseline. Kāra's ~16 MiB headroom over Rust comes from `Vec[i64].push` doubling capacity on each grow: building the 16 MiB `workspace` allocates an 8 MiB transient that sits at peak. Rust's `vec![0; TOTAL]` short-circuits the doubling. Equivalent capacity-hint support in Kāra (e.g., `Vec.with_capacity(n)`) would close this gap; same story as the [`121` bench](../121-best-time-to-buy-and-sell-stock/README.md#runtime-memory-peak).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil.
