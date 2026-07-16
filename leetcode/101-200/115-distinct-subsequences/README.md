# 115. Distinct Subsequences

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/distinct-subsequences](https://leetcode.com/problems/distinct-subsequences/)

Given strings `s` and `t`, count the number of **distinct subsequences of `s` that equal `t`** (a subsequence keeps relative order but may drop characters). A break from the tree run (#112–#114): a **string dynamic-programming** problem, and the corpus's first Hard of this stretch.

```
s = "rabbbit", t = "rabbit"  ->  3          s = "babgbag", t = "bag"  ->  5
    rabb b it                                    ba b g ba g
    rab b bit    (three ways to pick the                 (five ways to pick b,a,g
    ra b bbit     two b's that spell "rabbit")            in order out of "babgbag")
```

**Constraints:** `1 ≤ s.length, t.length ≤ 1000`; the answer fits in a signed 64-bit integer.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **2-D DP table** ★ | [`num_distinct.kara`](num_distinct.kara) ✓ | [`num_distinct.py`](num_distinct.py) ✓ |
| **Rolling 1-D DP** | [`num_distinct_rolling.kara`](num_distinct_rolling.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **ground-truth check** confirms the count three ways: the 2-D DP equals the rolling 1-D DP *and* a brute-force recursive count of subsequences (the literal definition), on a case battery **and 20,000 randomised (s, t) pairs** over a small alphabet, zero disagreements. Both solvers compile with zero diagnostics and are valgrind-clean.

## The recurrence

`dp[i][j]` = the number of distinct subsequences of the first `i` characters of `s` that equal the first `j` characters of `t`.

```
dp[i][0] = 1                       # the empty target is matched exactly one way
dp[0][j>0] = 0                     # a non-empty target has no match in an empty source
dp[i][j] = dp[i-1][j]              # SKIP s[i-1]
         + (s[i-1] == t[j-1] ? dp[i-1][j-1] : 0)   # ...or USE it to match t[j-1]
```

**2-D DP** ([`num_distinct.kara`](num_distinct.kara), the ★): fill an `(m+1)×(n+1)` `Vec[Vec[i64]]` table row-major; every cell it reads (`dp[i-1][j]`, `dp[i-1][j-1]`) is already final. O(m·n) time and space. Same table shape as kata [#72](../../1-100/72-edit-distance/).

**Rolling 1-D DP** ([`num_distinct_rolling.kara`](num_distinct_rolling.kara)): the recurrence only reads the previous row, so one `Vec[i64]` of length `n+1` suffices. For each character of `s`, update `dp` from `j = n` **down to** `1` — descending so `dp[j-1]` still holds the previous row's value when `dp[j] += dp[j-1]` fires. A distinct mechanism (one rolling row vs a full table) that must land on the identical count, mirroring [#72](../../1-100/72-edit-distance/)'s `edit_distance_rolling`.

## Kāra features exercised

- **`String.bytes()` byte indexing** — both solvers read `s.bytes()` / `t.bytes()` and compare `sb[r-1]` to `tb[c-1]` (inputs are ASCII, so byte indices are exact). Same idiom as kata [#72](../../1-100/72-edit-distance/) / [#97](../../1-100/97-interleaving-string/).
- **Nested `Vec[Vec[i64]]` DP table** — the ★ builds and fills a 2-D table with `dp[r][c] = dp[r-1][c] + dp[r-1][c-1]`; the rolling variant collapses it to one `Vec[i64]` updated in reverse.
- **`ref String` parameters** — both `num_distinct` signatures borrow their inputs (`s: ref String`), read-only.
- **Overflow-checked accumulation** — subsequence counts grow combinatorially; Kāra's default i64 overflow checking guards the `dp[r][c] = skip + dp[r-1][c-1]` add (the workload keeps counts within i64, as the problem guarantees).

**v1 note.** Strings stay within the `≤ 1000`-char constraint. The sink folds each pair's count into a running polynomial hash. Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the rolling + brute-force ground truth, and are valgrind-clean.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   num_distinct.kara
karac build num_distinct.kara && ./num_distinct

# The rolling 1-D variant (identical output):
karac run num_distinct_rolling.kara

# Python
python3 num_distinct.py

# Verify they all agree
diff <(karac run num_distinct.kara) <(python3 num_distinct.py)               && echo OK
diff <(karac run num_distinct.kara) <(karac run num_distinct_rolling.kara)   && echo OK

# Ground truth: 2-D DP == rolling 1-D == brute-force recursion (battery + 20k fuzz)
python3 ground_truth.py
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`num_distinct.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** Build 8 `(s, t)` string pairs once (distinct, small-alphabet so subsequence counts are non-trivial but bounded), then **K = 400,000** reps of the 2-D DP `num_distinct` on a **data-dependent-selected** pair (`idx = acc%8`, seeded by the running hash so nothing hoists), folding each count into a rolling hash. Compute-bound: each rep allocates a `~25×7` `Vec[Vec[i64]]` table and fills it O(m·n) — the nested-Vec DP regime (cf. [#72](../../1-100/72-edit-distance/)).

**Node representation & equal safety.** All mirrors use the **same nested 2-D structure** for parity: Kāra `Vec[Vec[i64]]`, Rust `Vec<Vec<i64>>` over `&[u8]`, Go `[][]int64`, **C `long**` with per-row `malloc`** (not a flat contiguous array — that would give C an unfair cache advantage over the row-of-rows the others build). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the DP add.

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time | DP table |
|---|---|---|
| c    num_distinct (clang -O3)                       | 203.3 ± 10.7 ms | `long**` (per-row malloc) |
| rust num_distinct (rustc -O, overflow-checks=on)     | 263.9 ± 13.4 ms | `Vec<Vec<i64>>` |
| rust num_distinct (rustc -O)                        | 272.9 ± 54.1 ms | `Vec<Vec<i64>>` |
| **kāra num_distinct**                               | **428.8 ± 16.6 ms** | **`Vec[Vec[i64]]`** |
| go   num_distinct (`[][]int64`)                     | 454.2 ± 19.2 ms | `[][]int64` |

**A nested-`Vec[Vec]` DP inner loop, and Kāra trails Rust on it — the per-cell-indexing regime.** Each interior cell does a handful of **doubly-indexed** reads/writes (`dp[r-1][c]`, `dp[r-1][c-1]`, `dp[r][c]`), so the tight loop is dominated by nested bounds-checked `Vec` indexing — outer-Vec index → row pointer → inner-Vec index, twice per cell. Kāra runs **1.63× behind the equal-safety Rust row** (264 ms) and **2.11× behind C** (203 ms), while landing just **ahead of Go** (454 ms). Overflow-checking is *not* the contributor here (the two Rust rows are within noise — a single add per matching cell, off the critical path); the gap is the nested-index density itself — Kāra re-derives the row pointers `dp[r-1]` / `dp[r]` per cell where LLVM hoists them for the raw-slice mirrors. This is the compute-bound counterpart to the read-only-traversal regime (#112): a tight loop with per-element overhead and nothing to amortize it against, so **leaner nested-`Vec` index lowering (row-pointer hoisting) is the headroom here** — flagged, not a defect. The alloc-bound siblings ([#113](../113-path-sum-ii/) / [#114](../114-flatten-binary-tree-to-linked-list/)) sit the other way (Kāra at-or-ahead of Rust) because allocation dominates. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **429 ms but ran K = 20,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (above C's 1.5 MiB and Rust's 2.2 MiB, a third of Go's 7.1 MiB). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (the per-rep `Vec[Vec]` allocation retains the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margin* as a data point. The direction (Kāra trailing Rust on a nested-`Vec` index-bound inner loop) is a codegen-density effect and should hold, but the size may compress.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched nested-`Vec` 2-D DP inner loop (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`), the per-cell nested-indexing regime where Kāra trails and leaner row-pointer hoisting is the headroom. C's `long**` (with per-row malloc, for structural parity) is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
