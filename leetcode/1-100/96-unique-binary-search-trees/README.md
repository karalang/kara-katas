# 96. Unique Binary Search Trees

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math · Dynamic Programming · Tree · Binary Search Tree · Binary Tree &nbsp;·&nbsp; **Source:** [leetcode.com/problems/unique-binary-search-trees](https://leetcode.com/problems/unique-binary-search-trees/)

Given an integer `n`, return **how many** structurally unique BSTs (binary *search* trees) store exactly the integers `1..n`. This is the counting sibling of [#95](../95-unique-binary-search-trees-ii/), which *materialises* the trees this one only tallies — and the answer is the *n*th **Catalan number**.

```
n = 1  ->  1
n = 3  ->  5
n = 19 ->  1767263190     (the largest that fits in a signed 32-bit int — hence the constraint)
```

**Constraints:** `1 ≤ n ≤ 19`.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Catalan recurrence DP** ★ | [`num_trees.kara`](num_trees.kara) ✓ | [`num_trees.py`](num_trees.py) ✓ |
| **Closed-form multiplicative Catalan** | [`num_trees_math.kara`](num_trees_math.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **brute-force ground-truth check** confirms the formula: for `n = 1..9` the counts equal the number of BSTs an actual recursive enumeration (the [#95](../95-unique-binary-search-trees-ii/) generator) produces — `1, 2, 5, 14, 42, 132, 429, 1430, 4862`. Both solvers compile with zero diagnostics.

## Counting without building — two ways

The key insight (shared with [#95](../95-unique-binary-search-trees-ii/)) is that the number of BST *shapes* over a contiguous value range depends only on the range's **size**. Pick a root `r` over `1..n`: its left subtree holds the `r-1` smaller values and its right the `n-r` larger, and the two choices are independent — so the counts *multiply*, and summing over every root gives a recurrence.

**Catalan recurrence DP** ([`num_trees.kara`](num_trees.kara), the ★) fills a table bottom-up:

```
dp[0] = 1                                   # the empty tree
dp[k] = sum over r in 1..k of dp[r-1] * dp[k-r]
```

`dp[n]` is the answer — an O(n²) fill of a `Vec[i64]`, the textbook DP for this problem.

**Closed-form multiplicative Catalan** ([`num_trees_math.kara`](num_trees_math.kara)) skips the table entirely: successive Catalan numbers satisfy

```
C(0) = 1,   C(k) = C(k-1) * 2*(2k-1) / (k+1)
```

so one running value carried up to `n` gives the answer in O(n) with no allocation. The product `C(k-1) * 2 * (2k-1)` is always divisible by `k+1` (Catalan numbers are integers), so the integer division is exact — a genuinely distinct mechanism from the DP table, and a check that Kāra's default-checked integer arithmetic handles the multiplicative form without spurious overflow (the intermediate stays well inside `i64` for `n ≤ 19`).

## Kāra features exercised

- **`Vec[i64]` as a DP table** — the ★ pushes each `dp[k]` onto a growing `Vec` and indexes `dp[r-1]` / `dp[k-r]` in the inner sum (bounds-checked index reads in a hot loop).
- **Checked integer arithmetic** — both forms lean on Kāra's default overflow checking; the closed-form's `C(k-1) * 2 * (2k-1)` exercises a multiply that would overflow `i32` (hence LeetCode's `n ≤ 19` cap) but stays exact in `i64`, and the benchmark's equal-safety row measures what those checks cost.
- **Exact integer division** — the closed-form relies on `… / (k+1)` being exact, a property of the Catalan sequence rather than a language feature, but it exercises `i64` division in the hot path.
- **Two independent algorithms, one oracle** — an O(n²) table and an O(n) closed form that must agree byte-for-byte across every surface, the same dual-surface discipline as the sibling katas.

**v1 note.** `n ≤ 19` keeps every count inside signed 64-bit range (the answer fits `i32` by construction; the DP's inner products stay far inside `i64`). The sink folds every `n`'s count into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the brute-force enumeration ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   num_trees.kara
karac build num_trees.kara && ./num_trees

# The closed-form variant (identical output):
karac run num_trees_math.kara

# Python
python3 num_trees.py

# Verify they all agree
diff <(karac run num_trees.kara) <(python3 num_trees.py)         && echo OK
diff <(karac run num_trees.kara) <(karac run num_trees_math.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`num_trees.{kara,rs,c,py}`, `go-seq/main.go`).

> ✅ **M5 re-bench (2026-11-01).** Measured on the corpus's **Apple M5 Pro** (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). The first M5 snapshot (2026-07-12, legacy backend `karac 0.1.0`) is superseded. A shared x86-64 Linux cloud-container reference run is kept alongside in [`bench/results.container-x86.json`](bench/results.container-x86.json); absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. This kata's cross-language *ordering* differs sharply between the two hosts — see the note below the table.

**Workload.** A single `num_trees(19)` is ~361 multiplies — instant — so the bench runs **K = 5,000,000** reps of the O(n²) DP-table. Crucially the size is **data-dependent** (`m = 2 + acc%18`, seeded by the running hash), so the trip counts are unknowable at compile time and the per-rep result cannot be hoisted or CSE'd — the same anti-hoist lever as [#93](../93-restore-ip-addresses/)'s data-dependent length. Each call fills a **fresh table** (Kāra `Vec[i64]`, C `malloc`/`free`, Rust `Vec`, Go slice — matched allocate-per-call idioms) and the count folds into a rolling polynomial hash. All five compiled mirrors must agree on `460214735` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline) — and this kata's multiplies (`dp[r-1] * dp[k-r]`) are exactly where those checks bite.

`--warmup 5 --runs 30 --shell=none`. All single-threaded, ~99.9 % CPU (the default build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01.**

| Implementation | Wall time |
|---|---|
| c    num_trees (clang -O3, malloc table)            | 295.7 ± 4.9 ms |
| go   num_trees (slice, GC)                          | 331.7 ± 3.9 ms |
| **kāra num_trees**                                  | **378.3 ± 23.8 ms** |
| rust num_trees (rustc -O, Vec)                      | 577.3 ± 29.8 ms |
| rust num_trees (rustc -O, overflow-checks=on)        | 667.1 ± 35.0 ms |

**The equal-safety-vs-Rust headline holds and widened; C and Go still lead.** kāra checks integer overflow by default and still **beats both Rust `Vec` builds — 1.53× ahead of unchecked `rustc -O` and 1.76× ahead of equal-safety `rustc -O -C overflow-checks=on`** (kāra-*with*-checks beats Rust-*without*, the same result as on the container and the checked-arithmetic siblings [#69](../69-sqrtx/)/[#93](../93-restore-ip-addresses/)). The overflow-check tell is intact: adding `-C overflow-checks=on` slows Rust ~16 % (577 → 667 ms) on the hot `dp[r-1] * dp[k-r]` multiply. **C (1.28× ahead) and Go (1.14× ahead) lead**, where on the x86 container kāra was outright fastest and C was *slowest* native. Against the 2026-07-12 legacy-backend snapshot, the v2/MIR backend moved kāra up on every comparator: kāra/Rust 0.92× → 0.66×, kāra/C 1.83× → 1.28×, kāra/Go 1.67× → 1.14× (the comparators themselves ran 10–15 % slower this session, so the ratios, not the milliseconds, carry the comparison). kāra's row is the noisiest here (σ 23.8 ms, 6 %), as is Rust's (σ 29.8 ms); the gaps are many σ wide either way.

**Why C and Go lead on the M5: this is a 5-million-allocation kata, and the M5's allocator is cheap.** Each of the K = 5 M reps builds a **fresh DP table** (`Vec.push` / `malloc`), and on the container that per-call allocation dominated — C's raw `malloc`/`free` was so costly there that it landed 4th (817 ms), *behind* kāra. On the M5 that allocation is comparatively cheap, so the bottleneck becomes the **inner loop**, and there C's unchecked scalar multiply-add plus Go's bump-allocator out-run kāra's per-iteration **overflow-checked multiply + two bounds-checked `Vec` reads** (`dp[r-1]`, `dp[k-r]`). C's cost was allocator-bound on the container and collapsed on the M5 (817 → 263 ms on the July snapshot), so the reversal was a story about C and Go speeding up on the M5, not about kāra slowing down — and kāra still clears its semantic peer, Rust, at equal safety. Go's 116 % CPU (331 ms user + 55 ms system) is concurrent-GC help, and it pays **9.7 MiB** peak RSS against kāra's **1.08 MiB** (C 1.14 MiB, Rust 1.11 MiB). Binary size: c 32.7 KiB, **kāra 295.8 KiB**, rust 455.7 KiB, go 2.39 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Python (K = 300,000, a fraction of the compiled iterations, timed separately at **618 ms**, last measured 2026-07-12, not re-run; not cross-checked) is the ergonomic foil.

Compile-cold on the M5 is clang 46.2 ms < rustc 86.0 ms < **karac 114.4 ms** (2.5× clang, 1.33× rustc). Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here on a small-DP + allocate-per-call shape where the equal-safety comparison (Kāra's checked multiplies vs `rustc -O -C overflow-checks=on`) is the honest like-for-like. C calibrates the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
