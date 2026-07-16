# 118. Pascal's Triangle

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Array · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/pascals-triangle](https://leetcode.com/problems/pascals-triangle/)

Given an integer `numRows`, return the first `numRows` of Pascal's triangle. Row `i` has `i+1` entries; the two edges are `1` and every interior entry is the sum of the two entries diagonally above it. A shift from the tree/next-pointer stretch (#112–#117) back to **nested-`Vec[Vec]` construction** — the same family as [#115](../115-distinct-subsequences/)'s DP table.

```
                1                 row 0
              1   1               row 1
            1   2   1             row 2
          1   3   3   1           row 3          row[j] = prev[j-1] + prev[j]
        1   4   6   4   1         row 4          (edges are 1)
      1   5  10   10  5   1       row 5
```

**Constraints:** `1 ≤ numRows ≤ 30` — every entry fits a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **Additive — each row from the previous** ★ | [`generate.kara`](generate.kara) ✓ | [`generate.py`](generate.py) ✓ |
| **Binomial — `C(i,j) = C(i,j-1)·(i-j+1)/j`** | [`generate_binomial.kara`](generate_binomial.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the triangle three ways: the additive recurrence equals the binomial multiplicative form *and* the `C(i,j) = i!/(j!(i-j)!)` definition (Python's exact-integer `math.comb`), for every `num_rows` in 0…60 — well past the `≤ 30` constraint, stress-testing the multiplicative form's exactness as the coefficients grow. Zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## Two construction mechanisms

**Additive** ([`generate.kara`](generate.kara), the ★): build each row from the one already in the table — `row[0] = row[i] = 1`, and `row[j] = tri[i-1][j-1] + tri[i-1][j]` for the interior. O(numRows²) time and space, a natural row-by-row `Vec[Vec[i64]]` fill.

**Binomial multiplicative** ([`generate_binomial.kara`](generate_binomial.kara)): each row is a row of binomial coefficients, so `C(i, j)` comes straight from its left neighbour with **no dependence on the previous row** — `C(i, 0) = 1`, `C(i, j) = C(i, j-1) · (i - j + 1) / j`. Every intermediate is an exact integer (a binomial coefficient), so the integer division is exact. A distinct mechanism that must produce the identical triangle — same `triangle_hash`.

## Kāra features exercised

- **Nested `Vec[Vec[i64]]` row-major construction** — the ★ builds and fills a triangular table row by row (`tri.push(row)` after each inner `row.push(..)` loop); the same nested-container surface as [#115](../115-distinct-subsequences/).
- **Balanced `if`/`else` push rows, auto-pre-sized by the compiler** — each row is `while j <= i { if j == 0 or j == i { row.push(1) } else { row.push(..) } }`, exactly the balanced-if push loop the pre-sizing pass recognizes (kara [`B-2026-07-16-17`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)); `karac` reserves each row's capacity up front, so no growth-doubling reallocs — see the benchmark.
- **`or` boolean operator** — the edge test `j == 0 or j == i` (Kāra uses `or`/`and`, not `||`/`&&`).
- **Exact integer division in the binomial form** — `c = c * (i - j) / (j + 1)`, relying on the binomial identity that the product is always divisible.

**v1 note.** `numRows` stays within the `≤ 30` constraint (the sink folds triangles for `numRows = 1…30`). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the binomial + `C(i,j)`-definition ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   generate.kara
karac build generate.kara && ./generate

# The binomial variant (identical output):
karac run generate_binomial.kara

# Python
python3 generate.py

# Verify they all agree
diff <(karac run generate.kara) <(python3 generate.py)              && echo OK
diff <(karac run generate.kara) <(karac run generate_binomial.kara) && echo OK

# Ground truth: additive == binomial == C(i,j) definition (num_rows 0..60)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`generate.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Each rep generates a full triangle of a **data-dependent** row count (`rows = 30 + acc%16`, so 30…45, seeded by the running hash so the whole `generate()` can't be hoisted out of the loop) as a nested `Vec[Vec[i64]]` built row by row with the additive recurrence, folding every entry into a rolling hash — **K = 80,000** reps. This is the **nested-Vec construction regime**: ~40 row `Vec`s and ~800 entries allocated per rep, dominated by the row builds (cf. [#115](../115-distinct-subsequences/)).

**Node representation & equal safety.** All mirrors use the **same nested structure** for parity: Kāra `Vec[Vec[i64]]`, Rust `Vec<Vec<i64>>`, Go `[][]int64`, **C `long**` with per-row `malloc`** (not a flat contiguous array — that would give C an unfair cache edge over the row-of-rows the others build). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the additive sum.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | Table |
|---|---|---|
| c    generate (clang -O3)                           | 379.4 ± 3.8 ms | `long**` (per-row malloc) |
| **kāra generate**                                   | **482.6 ± 7.9 ms** | **`Vec[Vec[i64]]`** |
| go   generate (`[][]int64`)                         | 679.3 ± 29.7 ms | `[][]int64` |
| rust generate (rustc -O)                            | 959.5 ± 12.6 ms | `Vec<Vec<i64>>` |
| rust generate (rustc -O, overflow-checks=on)         | 1042.5 ± 19.4 ms | `Vec<Vec<i64>>` |

**Kāra runs 1.27× behind raw-`malloc` C and ~2× *ahead* of Rust's `Vec<Vec<i64>>` — and the reason is the pre-sizing pass.** At these row sizes (30…45 elements) the `Vec.new()` + counted-`push` growth-doubling reallocation is a real cost, and Kāra's compiler eliminates it automatically: the rows are balanced-if push loops the pre-sizing pass recognizes (kara [`B-2026-07-16-17`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl)), so each row is reserved to exact capacity up front. A clean decomposition, all on this host:

- **Kāra's pre-size is automatic and complete:** Kāra as-written (`Vec.new()` + push) is **485 ms**, and hand-writing `Vec.with_capacity(i+1)` gives **493 ms** — statistically identical (1.01×). The compiler already reserved the capacity.
- **Rust pays for the same source shape:** Rust's identical `Vec::new()` + push is **1042 ms**; hand-writing `Vec::with_capacity` drops it to **545 ms** — a **1.91×** push-growth tax that `rustc` does not remove. Even against *hand-pre-sized* Rust (545 ms) Kāra (485 ms) stays **1.13× ahead**.

So on the natural `new()`-plus-`push` idiom both languages are handed, Kāra's codegen pre-sizes and Rust's does not — the headline ~2× gap to Rust is that optimization, not a microarchitectural fluke. (This is the same pre-size pass that was a *no-op* on [#115](../115-distinct-subsequences/)'s ≤7-element rows; at 30–45 elements the realloc chain is finally long enough to matter.) C's per-row `malloc` (exact size, no growth) is the metal floor. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **617 ms but ran K = 4,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (above C's 1.5 MiB and level with Rust's 2.3 MiB, a third of Go's 7.7 MiB). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (the per-rep nested-`Vec[Vec]` allocation retains the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — the same heap-growth artifact as [#115](../115-distinct-subsequences/), and unlike the zero-growth tree katas ([#114](../114-flatten-binary-tree-to-linked-list/)/[#116](../116-populating-next-right-pointers-in-each-node/)/[#117](../117-populating-next-right-pointers-in-each-node-ii/)) whose binaries stayed ~15 KiB.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margins* as data points. The direction — Kāra behind C, ahead of Go and well ahead of Rust's un-pre-sized `Vec<Vec>` — reflects the pre-sizing codegen difference, not a microarchitectural quirk, so it should hold.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched nested-`Vec` construction (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`) built with the identical `new()`-plus-`push` idiom, where Kāra's codegen auto-pre-sizes the rows and `rustc` leaves the growth reallocs, so Kāra comes out ~2× ahead (and 1.13× ahead of even hand-pre-sized Rust). C's per-row `malloc` is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
