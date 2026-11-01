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

> ✅ **M5 re-bench (2026-11-01).** The canonical numbers below are the corpus's **Apple M5 Pro** run (6P+12E, Darwin 25.6.0; **karac g6697158fa** (0.9.0-dev.14057, the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, `go 1.26.3`, hyperfine 1.20) — [`bench/results.json`](bench/results.json). Against the 2026-07-27 legacy-backend M5 snapshot kāra **improved against every comparator**: kāra/Rust 1.29× → 1.17×, kāra/equal-safety Rust 1.29× → 1.15×, kāra/C 1.46× → 1.31×, kāra/Go 1.96× → 1.42×. An earlier shared **x86-64 Linux cloud-container** run, which this section originally reported as canonical, is kept below as history (with its decomposition); absolute times/sizes/RSS are **not** comparable across the two hosts, only within-file cross-language ratios are the signal.

**Workload.** Build 8 `(s, t)` string pairs once (distinct, small-alphabet so subsequence counts are non-trivial but bounded), then **K = 400,000** reps of the 2-D DP `num_distinct` on a **data-dependent-selected** pair (`idx = acc%8`, seeded by the running hash so nothing hoists), folding each count into a rolling hash. Compute-bound: each rep allocates a `~25×7` `Vec[Vec[i64]]` table and fills it O(m·n) — the nested-Vec DP regime (cf. [#72](../../1-100/72-edit-distance/)).

**Node representation & equal safety.** All mirrors use the **same nested 2-D structure** for parity: Kāra `Vec[Vec[i64]]`, Rust `Vec<Vec<i64>>` over `&[u8]`, Go `[][]int64`, **C `long**` with per-row `malloc`** (not a flat contiguous array — that would give C an unfair cache advantage over the row-of-rows the others build). Kāra checks integer overflow by default; the `rustc -O -C overflow-checks=on` row is the like-for-like on the DP add.

`--warmup 5 --runs 30 --shell=none`. Single-threaded mirrors, ~99.7 % CPU (the default kāra build emits no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`), same as its `KARAC_AUTO_PAR=0` twin; Go's runtime runs at 161 % CPU, 212.4 ms user). **Apple M5 Pro numbers, karac g6697158fa, 2026-11-01** (canonical; sink `878576102` agreed by all five mirrors):

| Implementation | Wall time | DP table |
|---|---|---|
| go   num_distinct (`[][]int64`)                     | 203.2 ± 2.3 ms | `[][]int64` |
| c    num_distinct (clang -O3)                       | 219.9 ± 9.2 ms | `long**` (per-row malloc) |
| rust num_distinct (rustc -O)                        | 246.5 ± 6.7 ms | `Vec<Vec<i64>>` |
| rust num_distinct (rustc -O, overflow-checks=on)     | 250.5 ± 8.3 ms | `Vec<Vec<i64>>` |
| **kāra num_distinct**                               | **288.8 ± 12.1 ms** | **`Vec[Vec[i64]]`** |

**On the M5 (2026-11-01, v2/MIR) Kāra is last of five, but the gap has narrowed.** Kāra runs **1.17× behind stock Rust** (246.5 ms) and **1.15× behind equal-safety Rust** (250.5 ms), **1.31× behind C** (219.9 ms), and **1.42× behind Go** (203.2 ms wall, 212.4 ms user — Go's GC handles the per-rep row allocation well on this host, unlike the container below). kāra holds **1.09 MiB** peak RSS (C 1.03, Rust 1.16) vs Go's **9.84 MiB**. Binary size: c 32.8 KiB, **kāra 295.8 KiB**, rust 455.5 KiB, go 2.38 MiB; every MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (the legacy M5 kāra binary here was 33.6 KiB), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). Compile-cold on the M5 is clang 52.8 ms < rustc 104.3 ms < **karac 133.4 ms** (2.5× clang, 1.28× rustc).

**x86-64 container numbers** (history: the 2026-07-16 container run this section first reported; [`bench/results.container-x86.json`](bench/results.container-x86.json) now holds a later 2026-10-30 container run, not reproduced here):

| Implementation | Wall time | DP table |
|---|---|---|
| c    num_distinct (clang -O3)                       | 203.3 ± 10.7 ms | `long**` (per-row malloc) |
| rust num_distinct (rustc -O, overflow-checks=on)     | 263.9 ± 13.4 ms | `Vec<Vec<i64>>` |
| rust num_distinct (rustc -O)                        | 272.9 ± 54.1 ms | `Vec<Vec<i64>>` |
| **kāra num_distinct**                               | **428.8 ± 16.6 ms** | **`Vec[Vec[i64]]`** |
| go   num_distinct (`[][]int64`)                     | 454.2 ± 19.2 ms | `[][]int64` |

**On this container run Kāra trails Rust — and the cost is the nested-`Vec[Vec]` structure's *per-row `malloc`*, not the DP indexing and not `push`-growth realloc.** Kāra runs **1.63× behind the equal-safety Rust row** (264 ms) and **2.11× behind C** (203 ms), just **ahead of Go** (454 ms). A reproduced decomposition (hyperfine, 30 runs, this x86 container) pins it — and *disproves* the natural first guess of "nested inner-loop indexing" **and** an earlier (wrong) guess that push-growth reallocation was the driver:

- **A flat `Vec[i64]` table (indexed `dp[r*w+c]`) runs the same DP in 0.235 s** — **1.81× faster than the nested `Vec[Vec]` (0.426 s)** (still a touch above C's nested `long**` at 0.203 s). So Kāra's raw indexing + arithmetic is not the problem; the row-of-rows *structure* — one `malloc` per row, `m+1` mallocs per rep — is what costs.
- **Pre-sizing the rows is a *measured no-op*.** Each row is `Vec.new()` + a counted `push` loop that reallocs ~log₂(n+1) times, but the rows are tiny (n ≤ 6, so `0→4→8`). Reserving `Vec.with_capacity(n+1)` gives **420 ms — indistinguishable from the 426 ms baseline (1.00×)**; a 60×-amplified microbench (5000-element rows) shows the realloc chain is real but worth only **~1.07×**. So the earlier "~1.7× of the gap is push-growth realloc, `with_capacity` drops Kāra to 0.26 s" claim **does not reproduce** — corrected here. The realloc chain is negligible; the per-row `malloc` *count* is the cost.

Overflow-checking is *not* a contributor (the two Rust rows are within noise). So the headroom is **the nested container's per-row allocation, not indexing and not realloc**: the only lever that actually moves it is a **flat backing store** (`Vec[i64]` indexed `dp[r*w+c]`, 1.81×) — a data-structure choice no auto-transform performs. The compiler *does* now auto-pre-size counted `push`-loops (the sequential collect-tabulate lowering, [kara `B-2026-07-16-11`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl), plus the balanced-if/DP-base-case extension [`B-2026-07-16-17`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.jsonl) this kata's rows exercise) — but on rows this small that pre-size is, as measured, a no-op. This contrasts with the read-only-traversal regime (#112, genuinely per-element codegen density); here the DP compute is cheap and the table build dominates. The alloc-bound siblings ([#113](../113-path-sum-ii/) / [#114](../114-flatten-binary-tree-to-linked-list/)) sit the other way (Kāra at-or-ahead of Rust) because their allocation is amortized differently. Verified correct **and** valgrind-clean (`0 errors, 0 bytes in use at exit`). Python is listed at **429 ms (earlier container run, not re-run 2026-11-01) but ran K = 20,000 — 1/20 of the compiled iterations** (pure-Python is ~20× slower per rep; timed separately, not cross-checked), so its wall-clock is not comparable.

kāra holds **2.4 MiB** peak RSS (above C's 1.5 MiB and Rust's 2.2 MiB, a third of Go's 7.1 MiB). The kāra binary measures **324 KiB** here — a build-linkage artifact of this container run (the per-rep `Vec[Vec]` allocation retains the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KiB), independent of the runtime numbers, flagged for the M5 — vs C's 16 KiB and Go's 2.2 MiB.

**Flagged for the M5 re-bench** — container orderings can shift on the M5's wider core (see [#97](../../1-100/97-interleaving-string/)); treat the *margin* as a data point. The direction (Kāra trailing Rust on nested-`Vec[Vec]` table construction) reflects allocation cost, not a microarchitectural quirk, so it should hold; the size may compress. (2026-11-01 note: on the M5 v2/MIR run the direction holds and the size compressed — 1.15× equal-safety Rust vs the container's 1.63× — but Kāra is now also behind Go, 1.42×, where the container had it just ahead; see the M5 table above.)

Compile-cold, binary size, and peak-RSS records are in [`bench/results.json`](bench/results.json) (M5, canonical) and [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../../1-100/1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here at a matched nested-`Vec` 2-D DP (`Vec[Vec[i64]]` vs `Vec<Vec<i64>>`), where Kāra trails on the *table construction* — the nested container's per-row `malloc` (not the indexing, and not `push`-growth realloc, which is a measured no-op on rows this small); a flat backing store is the only lever that reaches parity, a data-structure choice. C's `long**` (with per-row malloc, for structural parity) is the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
