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

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** A single `num_trees(19)` is ~361 multiplies — instant — so the bench runs **K = 5,000,000** reps of the O(n²) DP-table. Crucially the size is **data-dependent** (`m = 2 + acc%18`, seeded by the running hash), so the trip counts are unknowable at compile time and the per-rep result cannot be hoisted or CSE'd — the same anti-hoist lever as [#93](../93-restore-ip-addresses/)'s data-dependent length. Each call fills a **fresh table** (Kāra `Vec[i64]`, C `malloc`/`free`, Rust `Vec`, Go slice — matched allocate-per-call idioms) and the count folds into a rolling polynomial hash. All five compiled mirrors must agree on `460214735` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline) — and this kata's multiplies (`dp[r-1] * dp[k-r]`) are exactly where those checks bite.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time |
|---|---|
| **kāra num_trees**                                  | **589.9 ± 12.3 ms** |
| go   num_trees (slice, GC)                          | 631.7 ± 6.6 ms |
| rust num_trees (rustc -O, Vec)                      | 771.7 ± 8.6 ms |
| c    num_trees (clang -O3, malloc table)            | 817.1 ± 2.3 ms |
| rust num_trees (rustc -O, overflow-checks=on)        | 921.2 ± 19.9 ms |

**Kāra is fastest of five — and the equal-safety gap is the headline.** With integer-overflow checking *on by default*, kāra is **1.07× ahead of Go**, **1.31× ahead of unchecked `rustc -O`**, and **1.56× ahead of equal-safety `rustc -O -C overflow-checks=on`** — i.e. kāra-*with*-checks beats Rust-*without*. The tell is what the checks cost each compiler: adding `-C overflow-checks=on` slows Rust by **~19 %** (772 → 921 ms) because the DP's hot `dp[r-1] * dp[k-r]` multiply gets a checked-mul + branch on every one of ~5 M × O(n²) iterations, whereas kāra folds the same guard into its codegen at no measured penalty (it is already the fastest, checks included). This is the branch-and-arithmetic-latency-bound regime the checked-arithmetic siblings ([#69](../69-sqrtx/), [#93](../93-restore-ip-addresses/)) live in — the inner loop is a dependent chain of multiplies and adds, so kāra's higher IPC absorbs the extra check instructions. It even edges the raw-`malloc` C floor here (**1.39×**): the per-call table allocation (5 M `malloc`/`free` pairs) is a real cost C pays in full, and kāra's `Vec` allocation on this shape is no slower while its checked inner loop keeps pace. Python (K = 300,000, a fraction of the compiled iterations, timed separately at **1660 ms**, not cross-checked) is the ergonomic foil.

> **Binary size caveat.** The kāra binary measures large in `results.container-x86.json` (≈ 332 KB vs C's 16 KB) — but that is a **build-linkage artifact of this container run, not kāra's real footprint**. The moment a program grows a heap collection (`Vec.push` / `String.push_str`, i.e. anything that links a runtime allocation function) this build retains the full Rust std support + backtrace-*symbolizer* tree (~308 KB of `.text`) that `--gc-sections` should strip; a heap-growth-free program on the same toolchain is 15.7 KB, and sibling katas that push shipped at ~15 KB, so the strip is expected to hold on a correctly-linked build (e.g. the M5 re-bench). It is the symbolizer-retention issue documented in the compiler's build notes and is **independent of the runtime numbers above** — flagged here for the M5 re-bench to confirm the real size, not treated as a kāra-vs-C size result.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here on a small-DP + allocate-per-call shape where the equal-safety comparison (Kāra's checked multiplies vs `rustc -O -C overflow-checks=on`) is the honest like-for-like. C calibrates the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
