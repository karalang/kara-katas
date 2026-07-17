# 119. Pascal's Triangle II

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/pascals-triangle-ii](https://leetcode.com/problems/pascals-triangle-ii/)

Given a non-negative integer `rowIndex`, return the `rowIndex`-th (0-indexed) row of Pascal's triangle — using only **O(rowIndex) extra space**. Where [#118](../118-pascals-triangle/) built the whole nested triangle, this one keeps a **single row** and rolls it forward in place.

```
rowIndex = 3  ->  [1, 3, 3, 1]
rowIndex = 4  ->  [1, 4, 6, 4, 1]

one row, updated in place right-to-left:   row[k] = row[k] + row[k-1]
```

**Constraints:** `0 ≤ rowIndex ≤ 33` — every entry fits a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **In-place rolling row** ★ | [`get_row.kara`](get_row.kara) ✓ | [`get_row.py`](get_row.py) ✓ |
| **Binomial — `C(n,j) = C(n,j-1)·(n-j+1)/j`** | [`get_row_binomial.kara`](get_row_binomial.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the row three ways: the in-place rolling recurrence equals the binomial multiplicative form *and* the `C(n,j)` definition (Python's exact-integer `math.comb`), for every `row_index` in 0…80. Zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two mechanisms

**In-place rolling** ([`get_row.kara`](get_row.kara), the ★): start with a row of all `1`s, then for each row number `i` from 2 up, update the row **in place from right to left** — `row[k] = row[k] + row[k-1]` for `k` from `i-1` down to `1`. Descending `k` is what keeps it correct: when `row[k]` is updated, `row[k-1]` still holds the previous row's value. O(rowIndex) space, O(rowIndex²) time, and — unlike #118 — a **single `Vec[i64]`**, no nested container.

**Binomial multiplicative** ([`get_row_binomial.kara`](get_row_binomial.kara)): the row is `C(rowIndex, j)`, so it comes out left-to-right with one running value and no in-place update — `C(n, 0) = 1`, `C(n, j) = C(n, j-1) · (n - j + 1) / j`, each intermediate an exact integer. A distinct mechanism (a forward multiply, no index-assignment) that must produce the identical row — same `row_hash`.

## Kāra features exercised

- **In-place index-assignment** — `row[k] = row[k] + row[k-1]` reads two elements and writes one back on the same `Vec[i64]`, the core surface of a rolling-1D DP. (This is the pattern that surfaced the performance gap below.)
- **Descending counted loop** — `while k >= 1 { ..; k = k - 1 }`, a backward index walk.
- **Exact integer division in the binomial form** — `c = c * (n - j) / (j + 1)`, relying on the binomial-coefficient divisibility identity.

**v1 note.** `rowIndex` stays within the `≤ 33` constraint (the sink folds rows for `rowIndex = 0…33`). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the binomial + `C(n,j)`-definition ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   get_row.kara
karac build get_row.kara && ./get_row

# The binomial variant (identical output):
karac run get_row_binomial.kara

# Python
python3 get_row.py

# Verify they all agree
diff <(karac run get_row.kara) <(python3 get_row.py)             && echo OK
diff <(karac run get_row.kara) <(karac run get_row_binomial.kara) && echo OK

# Ground truth: in-place == binomial == C(n,j) definition (row_index 0..80)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`get_row.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Each rep computes the `rowIndex`-th row for a **data-dependent** `rowIndex` (`30 + acc%20`, so 30…49, seeded by the running hash so `get_row()` can't be hoisted out of the loop), building one `Vec[i64]` of length `rowIndex+1` and updating it in place right-to-left, folding every entry — **K = 440,000** reps. This is the **in-place index-assignment regime**: a single small `Vec` per rep, dominated by the O(k²) in-place `row[k] = row[k] + row[k-1]` updates.

**Node representation & equal safety.** All mirrors use one flat array: Kāra `Vec[i64]`, Rust `Vec<i64>`, Go `[]int64`, C `long[]` (one `malloc` per rep). Kāra checks integer overflow **and array bounds** by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow (Rust's bounds checks are elided by LLVM in this loop — see below).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Store |
|---|---|---|
| c    get_row (clang -O3)                             | 239.0 ± 9.2 ms | `long[]` |
| rust get_row (rustc -O)                             | 274.4 ± 10.7 ms | `Vec<i64>` |
| rust get_row (rustc -O, overflow-checks=on)          | 311.3 ± 5.5 ms | `Vec<i64>` |
| **kāra get_row**                                    | **416.2 ± 15.3 ms** | **`Vec[i64]`** |
| go   get_row (`[]int64`)                            | 439.4 ± 12.7 ms | `[]int64` |

**Kāra trails here — 1.34× behind equal-safety Rust and 1.74× behind C — and this kata found *why*: a bounds check the compiler doesn't eliminate on the in-place update loop.** 🐛 It is filed as a compiler gap, not worked around here — [kara `B-2026-07-17-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl). asm isolation of the AOT binary pins it precisely:

- The hot loop `while k >= 1 { row[k] = row[k] + row[k-1]; k = k-1 }` emits, per iteration, `cmp %rbx,%rdx; ja <panic>` (a **bounds check** — one check covers both `row[k]` and `row[k-1]`, since `k-1 < k`) followed by `jo <panic>` (the overflow check).
- The **sibling** `row_hash` fold loop (`while j < row.len() { .. row[j] .. }`) in the *same binary* has **no** bounds check — kāra's BCE fired there. So the pass handles the canonical forward `j < v.len()` (and the binary-search `mid`, [kata #34](../../1-100/34-find-first-and-last-position-of-element-in-sorted-array/)), but **not** this pattern: `k` is bounded by the *outer* loop variable (`k ≤ i-1`, `i ≤ rowIndex`, `len = rowIndex+1`), so `k < len` holds only **transitively**.
- The overflow check is **not** the gap: it is present in both Kāra and the equal-safety Rust row, and Rust's own overflow tax is only ~13% (`rustc -O` 274 ms → `overflow-checks=on` 311 ms). The residual 311 → 416 ms is the bounds check LLVM elides for Rust and kāra keeps.

So on a rolling-1D-DP shape, Kāra pays a per-iteration bounds check its optimizer can't yet prove redundant — the same BCE class as the *fixed* binary-search gap ([kara `B-2026-06-16-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)), a distinct index-derivation pattern. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **1115 ms but ran K = 22,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.3 MiB** peak RSS (above C's 1.5 MiB, level with Rust's 2.1 MiB, a third of Go's 7.7 MiB). The kāra binary measures **324 KiB** here — the heap-growth backtrace-symbolizer artifact (one `Vec` allocated + freed per rep retains it, cf. [#115](../115-distinct-subsequences/)/[#118](../118-pascals-triangle/)), ~15 KiB on a correct build, flagged for the M5.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The direction — Kāra behind C and equal-safety Rust because of the un-eliminated bounds check — is a codegen fact, not a microarchitectural quirk, so it should hold until `B-2026-07-17-1` is addressed.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched in-place rolling-1D DP (`Vec[i64]` vs `Vec<i64>`), where the equal-safety comparison exposes a **bounds-check-elimination** gap: LLVM proves the in-place index in-range and drops the check, kāra's BCE does not yet (filed as `B-2026-07-17-1`). That is exactly the dogfood loop's job — a natural in-place DP surfaced a concrete, isolated codegen improvement. C's unchecked `long[]` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
