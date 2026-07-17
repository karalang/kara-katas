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

- **In-place index-assignment** — `row[k] = row[k] + row[k-1]` reads two elements and writes one back on the same `Vec[i64]`, the core surface of a rolling-1D DP. (This is the pattern that surfaced — and drove the fix of — the bounds-check gap `B-2026-07-17-1`; the loop now sits at Rust parity. See Benchmarks.)
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

**Workload.** Each rep computes the `rowIndex`-th row for a **data-dependent** `rowIndex` (`30 + acc%20`, so 30…49, seeded by the running hash so `get_row()` can't be hoisted out of the loop), building one row of `rowIndex+1` ones and updating it in place right-to-left, folding every entry — **K = 440,000** reps. This is the **in-place index-assignment regime**: a single small `Vec` per rep, dominated by the O(k²) in-place `row[k] = row[k] + row[k-1]` updates. **Fill parity:** both mirrors bulk-fill the initial ones — Kāra `Vec.filled(n, 1)`, Rust `vec![1i64; n]` — so the O(k) fill is the same algorithm on both sides (an earlier version filled Kāra with a `Vec.new()` + push loop, which raced a scalar fill against Rust's tuned bulk-fill and distorted the margin; see the note below).

**Node representation & equal safety.** All mirrors use one flat array: Kāra `Vec[i64]`, Rust `Vec<i64>`, Go `[]int64`, C `long[]` (one `malloc` per rep). Kāra checks integer overflow **and array bounds** by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on overflow.

`--warmup 8 --runs 40`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note — this container run is noisy, σ up to ±10 %, so read the *ratios*, not the absolute ms):

| Implementation | Wall time | Store |
|---|---|---|
| c    get_row (clang -O3)                             | 230 ± 2 ms | `long[]` |
| rust get_row (rustc -O)                             | 230 ± 24 ms | `Vec<i64>` |
| rust get_row (rustc -O, overflow-checks=on)          | 293 ± 28 ms | `Vec<i64>` |
| **kāra get_row**                                    | **355 ± 12 ms** | **`Vec[i64]`** |
| go   get_row (`[]int64`)                            | 445 ± 21 ms | `[]int64` |

**The DP loop this kata is *about* is now at Rust parity — and getting there corrected two prior misreadings.** The hot loop is `while k >= 1 { row[k] = row[k] + row[k-1]; k = k-1 }`, an in-place descending update.

**Bounds check — FIXED ([kara `B-2026-07-17-1`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), fix `6474a73`).** Kāra used to emit a per-iteration `cmp; ja <panic>` bounds check on `row[k]` that LLVM elides for Rust but kāra kept — because `k` is bounded by the *outer* loop variable only **transitively** (`k ≤ i-1`, `i ≤ rowIndex`, `len = rowIndex+1`), a chain LLVM's interval passes can't derive. The compiler now recognises this rolling-1D-DP shape (`compute_descending_skips`) and proves `k ≤ k_init = i-1 ≤ rowIndex-1 < rowIndex+1 = row.len()` from a length pin + the enclosing counter's bound, then skips the upper-half check kara-side. With it gone, an **isolated** in-place-update microbench measures **1.01×** vs equal-safety Rust, and the update-loop asm is byte-identical to Rust's. The DP loop is no longer the gap.

**Two red herrings, recorded honestly.** The equal-safety margin above (~1.21× vs `rustc -O -C overflow-checks=on`) is **not** the DP loop:
- **The `cmp $1` loop guard was a mirage ([kara `B-2026-07-17-14`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), now `invalid`).** kāra lowers `while k >= 1` to `dec; cmp $1; ja` where Rust folds the guard into `dec; jne` (one fewer instruction). It *looks* like a gap, but a drift-immune A/B of two binaries differing only in that lowering showed **0 % wall-clock difference** — the loop is counter-dependency-bound and the branch predictor hides the extra compare. Filed, then invalidated after measurement.
- **The residual is the O(k) fill + per-rep alloc/free, plus container noise.** Both `Vec.filled` and Rust's `vec![1;n]` vectorize (`movaps`/`movups`); Rust merely unrolls 2× more. There is **no single isolable codegen gap** left here — when Rust is switched to a matching push-fill loop, *kāra is 1.45× faster*. The margin is fill/alloc overhead spread thin, dominated by measurement noise on this host.

Python (pure-Python, ~20× slower per rep, run at a fraction of K, timed separately, not cross-checked) is not comparable and omitted. kāra holds a small peak RSS (level with Rust, a fraction of Go's).

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)), and this run was noisy; treat the *margins* as data points. The load-bearing result — kāra's DP update loop at Rust parity after `B-2026-07-17-1` — is an asm-level fact, not a microarchitectural quirk.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched in-place rolling-1D DP (`Vec[i64]` vs `Vec<i64>`). The equal-safety comparison drove a real **bounds-check-elimination** fix (`B-2026-07-17-1`), after which the DP loop sits at Rust parity; the two follow-on suspects (a `cmp $1` loop guard and a bulk-fill gap) both dissolved under measurement — the guard costs nothing (`B-2026-07-17-14`, invalidated) and `Vec.filled` already vectorizes. That is the dogfood loop working as intended: one real codegen win landed, two plausible-but-false leads caught before they became folklore. C's unchecked `long[]` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
