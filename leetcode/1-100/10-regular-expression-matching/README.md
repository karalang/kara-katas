# 10. Regular Expression Matching

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/regular-expression-matching](https://leetcode.com/problems/regular-expression-matching/)

Implement regex matching against a string `s` with pattern `p` supporting two metacharacters:

- `.` — matches any single character.
- `*` — matches zero or more of the preceding element.

The match must cover the **entire** input string, not a prefix.

```
("aa",          "a")              →  false   (one 'a' can't match two)
("aa",          "a*")             →  true    (`a*` matches any 'a' run)
("ab",          ".*")             →  true    (`.*` matches anything)
("aab",         "c*a*b")          →  true    (`c*` zero-matches, `a*` eats "aa", then 'b')
("mississippi", "mis*is*p*.")     →  false   (no way to span "ippi")
```

**Constraints:** `1 ≤ s.length ≤ 20`, `1 ≤ p.length ≤ 20`. `s` contains lowercase letters only; `p` contains lowercase letters plus `.` and `*`. Every `*` is preceded by a valid character that it can match.

## Approaches

| Approach | Complexity | Kāra | Python | Rust |
|---|---|---|---|---|
| Recursive matcher with `.` / `*` branching | O(2^(m+n)) time, O(m+n) recursion depth | [`regex.kara`](regex.kara) ✓ via `karac run` / `karac build` | [`regex.py`](regex.py) ✓ | [`bench/regex.rs`](bench/regex.rs) ✓ (bench triad) |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all 22 test cases.

## Why recursion (and not bottom-up DP)

A bottom-up `dp[i][j]` table closes the worst-case to O(m·n) time, but allocates an `(m+1)·(n+1)` Vec/Vec for every call — even the ~21-cell table that a 4-char × 4-char case wants. At the LeetCode constraint ceiling of `|s|, |p| ≤ 20` the table is at most ~441 cells, well within what a recursive matcher's call-stack visits in practice. The bench workload exercises the recursive branching exponent without ever hitting genuinely pathological inputs (the closest is `("aaaaaaaaaab", "a*a*a*a*a*b")` — five chained `*` quantifiers that each backtrack, but the leading-`a` constraint collapses every branch except the one that yields `true`).

Recursion also keeps the code the same shape across all five languages — `is_match_at(s, i, p, j)` is identical-looking in Kāra / Rust / C / Go / Python, which makes the seq-lane comparison a pure codegen-quality measurement.

## Two recursive cases — the entire algorithm

```
fn is_match_at(s, i, p, j):
    if j == m:
        return i == n                               // pattern done; matched iff s done
    first_match = i < n and (p[j] == s[i] or p[j] == '.')
    if j + 1 < m and p[j + 1] == '*':
        return is_match_at(s, i, p, j + 2)          // skip the "x*" (zero matches)
            or (first_match and is_match_at(s, i + 1, p, j))  // consume one s char, keep "x*"
    return first_match and is_match_at(s, i + 1, p, j + 1)
```

`first_match` is a one-character peek. When the next-after-current pattern char is `*`, both branches of the `or` get a turn: either drop the entire `x*` (zero matches) or eat one `s` char on a `first_match` and keep the `x*` for a possible further match. Otherwise it's a strict 1-for-1 advance gated by the peek.

Two subtle correctness anchors:

- **Empty-pattern base case** anchors all recursion. At `j == m` the answer is `i == n` — every recursive return eventually reaches this through pattern-advancing edges (each non-`*` step reduces `m − j` by 1; each `*`-skip reduces it by 2).
- **`first_match` gates the consume-branch.** Without it, `a*` against `"b"` would recurse forever (eat 'b', keep `a*`, eat… nothing left, etc.). Gating on `first_match` makes the consume-branch a no-op when the leading `s` char doesn't match `x`, collapsing back to the skip-branch.

## Kāra features exercised

- **Recursion across two `Slice[u8]` byte views** — `fn is_match_at(s: Slice[u8], i: i64, p: Slice[u8], j: i64) -> bool` recurses up to ~m+n deep on the bench's longest input (`("aaaaaaaaaab", "a*a*a*a*a*b")`, ~22 deep). Same shape works in `karac run` and `karac build`.
- **Index-offset pattern over slices** — instead of `s[1..]` subslicing, the recursion threads `i` and `j` cursors and indexes `bytes[j]` / `bytes[j + 1i64]` directly. Same approach as kata [#91 decode-ways](../91-decode-ways/) — Kāra's `Slice[u8]` doesn't have an in-place range-slice syntax today, and even if it did the offset pattern is zero-allocation.
- **`bool`-returning predicate composed of `and`/`or` short-circuits** — the `j + 1i64 < m and p[j + 1i64] == b'*'` peek short-circuits on the bounds check; the `first_match and is_match_at(...)` consume-branch short-circuits when there's no leading match.
- **f-string interpolation of two `ref String` args** — `f"is_match(\"{s}\", \"{p}\"): {r}"` interleaves two string args and a bool, all in one print call. Codegen lowers each arm independently (String → strdup of the contents, bool → "true"/"false" via the dedicated branch in `compile_fstr_part_to_cstr`).
- **`Slice[u8]` parameter to a recursive helper** — same idiom as [kata #5](../5-longest-palindromic-substring/) and [kata #91](../91-decode-ways/), but here the function calls itself rather than being called from a loop. Tests the codegen's handling of slice parameters across recursive call frames.

No `Vec` allocations inside the recursion (the input `Vec[String]` lives in `main`; `bytes()` is a zero-copy view); no `String` building; no `HashMap` for memoization (the LeetCode inputs are small enough that the recursive branching is bounded in practice).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   regex.kara
karac build regex.kara && ./regex

# Python
python3 regex.py

# Verify they agree
diff <(./regex) <(python3 regex.py) && echo OK
diff <(karac run regex.kara) <(python3 regex.py) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`regex.{kara,rs,c,py}`, `go-seq/main.go`, plus the par-lane mirrors).

Snapshot for every table below unless marked otherwise: Apple M5 Pro (6P+12E), karac `0.9.0-dev.14057+g6697158fa` (the v2/MIR backend; the legacy backend was deleted 2026-10-23), `rustc 1.95.0`, Apple clang 21.0.0, go 1.26.3, hyperfine 1.20.0, measured 2026-10-31 (feed `measured_at` 2026-11-01T00:50Z UTC). Source of truth: [`bench/results.json`](bench/results.json).

> **Re-bench 2026-10-31 — what moved.** Quoted as language ratios, because every comparator ran 7–36% slower in absolute terms this session (machine state).
>
> - **Seq lane: Kāra/Rust 1.11× → 1.60×, Kāra/C 1.09× → 1.59×, Kāra/Go 0.71× → 1.03×** (previous feed: 2026-07-28, legacy backend). A real MIR-backend regression: MIR runs 1.37× legacy's instructions and 1.50× its cycles on the regex DP, filed as [`B-2026-10-31-40`](../../../../kara/docs/bugs-v2.md) — see [Bug ledger](#bug-ledger).
> - **Par lane: Kāra/rayon 1.15× → 1.79×, Kāra/C-pthreads 1.04× → 1.42×, Kāra/Go 0.71× → 1.01×** — the same seq-path loss carried into each worker.
> - **Binary size: 33.5 → 295.8 KiB (seq)** — see [Binary size](#binary-size).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + (if r { 1i64 } else { 0i64 })` accumulator is a textbook associative + commutative reduction, which the concurrency analyzer recognizes and codegen parallelizes *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`regex_kara_seq`** — built with `KARAC_AUTO_PAR=0` (the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build. Its IR carries no call of `karac_mir_task_spawn`, verified in the emitted IR (`KARAC_MIR_LL`).
- **`regex_kara`** — default `karac build` output, whose IR carries the `karac_mir_task_spawn` call. Picks up auto-par dispatch (~13.3 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 8 (string, pattern) pairs cycled by `k % N`, each chosen to exercise a different branch of the recursive matcher so no single shape dominates the predictor's history. K = 10,000,000 outer iters, sink = count of `is_match(strs[k % N], pats[k % N])` widened to i64. All four compiled mirrors agree on `7500000` (six of the eight pairs match × K / N) before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

M5 Pro, 2026-10-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust regex (rustc -O -C overflow-checks=on, equal-safety) | **105.4 ms ± 2.1 ms** | 104.0 ms | 99% |
| rust regex (rustc -O) | **124.2 ms ± 1.6 ms** | 122.7 ms | 100% |
| c    regex (clang -O3) | **124.7 ms ± 1.9 ms** | 122.9 ms | 99% |
| go   regex | **193.2 ms ± 4.2 ms** | 191.1 ms | 100% |
| **kāra regex** (`KARAC_AUTO_PAR=0`) | **198.7 ms ± 7.6 ms** | 195.6 ms | 99% |

Kāra is now last of the five: **1.60× behind `rustc -O`, 1.59× behind C and 1.88× behind equal-safety Rust**, and level with Go (1.03×, inside Kāra's ±7.6 ms band). On the legacy backend (2026-07-28 feed) the three compiled-native rows were within ~11% of each other (Kāra 1.11× Rust, 1.09× C) and Kāra was 1.40× ahead of Go. (The equal-safety Rust build runs faster than wrapping `rustc -O` on this kata, as it did on the legacy feed — 98.0 vs 114.8 ms then.) The loss is the backend, not noise: MIR executes 1.37× legacy's instructions and 1.50× its cycles here ([`B-2026-10-31-40`](../../../../kara/docs/bugs-v2.md)). The recursive matcher's hot path (load `p[j]`, branch on `*`, peek and conditional-tail-call) is exactly the shape where rustc's mid-2026 inliner opens up a lead via aggressive specialization.

The Go row's shape (Go at 0.97× of Kāra-seq this run, 1.40× on the legacy feed) reflects per-call slice-header reconstruction at each recursive frame (`[]byte(s)` happens fresh per `isMatch` call in the bench main, whereas rust/c/kara hold the byte view as a function-local across the recursion) plus the per-iter `idx % n` and `int → int64` widening overhead Go can't SROA across the predicate body.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output, hyperfine `--warmup 10 --runs 50`. All four languages parallelize the same K = 10M reduction; the difference is what the programmer wrote.

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| rust regex (rayon) | **10.6 ms ± 0.3 ms** | 129.8 ms | ~1326% |
| c    regex (pthreads) | 13.3 ms ± 1.8 ms | 139.5 ms | ~1059% |
| go   regex (goroutines) | 18.7 ms ± 3.8 ms | 189.8 ms | ~1026% |
| **kāra regex** (auto-par on reduction) | **18.9 ms ± 0.8 ms** | 247.1 ms | ~1331% (~13.3 cores) |

Karac's auto-par recognizes the K=10M reduction in `main` and dispatches it across workers, ~13.3 cores active during the run. **Kāra with zero parallel source is 1.79× behind rayon, 1.42× behind C+pthreads and level with Go (1.01×, inside Go's ±3.8 ms band)** — on the legacy backend it was 1.15× / 1.04× and 0.71×. The wall-time win *over the seq-lane Kāra row above* is **10.5×** (198.7 / 18.9); total CPU time goes up 26% (195.6 → 247.1 ms user) as the cost of dispatch + per-worker fixed overhead. Net: real production wall-time speedup on this workload's shape, paid for in additional CPU and a +81 KiB binary footprint (see § *Binary size* below).

**Not headlined against the seq rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 6× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the par table is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction), set against the hand-written parallel mirrors.

### Codegen vs Python

Last measured 2026-05-31, not re-run (this run did not set `KARA_BENCH_INCLUDE_PY`). CPython at K = 1M took **758.6 ± 10.5 ms** (single-core); projected to K = 10M that's ~7.59 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: at that snapshot Kāra-seq vs CPython was the within-lane per-core comparison (~60× faster), and Kāra-auto-par vs CPython the cross-lane regime comparison (~696× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

M5 Pro, 2026-10-31, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `regex` | **168.8 ± 3.5 ms** | 91.5 ± 1.0 ms | 46.0 ± 0.6 ms |

Karac is now **1.84× slower than rustc -O** and **3.67× slower than clang -O3**; on the legacy backend (2026-07-28 feed) it was 1.26× of rustc's time, and 1.12× faster than rustc in the 2026-05-31 snapshot. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    regex | 33,512 | 32.7 |
| **kāra regex (seq)** | **302,872** | **295.8** |
| kāra regex (auto-par) | 386,152 | 377.1 |
| rust regex | 466,376 | 455.4 |
| go   regex | 2,492,546 | 2,434.1 |

Every v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (tracked as kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); the seq binary was 34,264 B on the legacy backend, within ~0.7 KiB of clang's. It is 1.54× under Rust's 455.4 KiB. The auto-par variant carries +81 KiB over seq for the parallel-dispatch machinery.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| c    regex | 1,048,888 | 1.0 |
| **kāra regex (seq)** | **1,081,656** | **1.0** |
| rust regex | 1,130,808 | 1.1 |
| c    regex (pthreads) | 1,343,800 | 1.3 |
| kāra regex (auto-par) | 1,556,936 | 1.5 |
| rust regex (rayon) | 1,966,416 | 1.9 |
| go   regex | 2,916,808 | 2.8 |
| go   regex (goroutines) | 4,440,568 | 4.2 |

Kāra-seq's peak sits **32 KiB over C** (1,081,656 vs 1,048,888) and 48 KiB under Rust — two 16 KiB pages either way; peak-footprint is quantized to the 16 KiB page on Apple Silicon. The recursive matcher allocates nothing inside the loop (the input `Vec[String]` is fixed at ~200 bytes total of string-header storage, the recursion lives entirely on the call stack), so steady state is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.5 MiB for the lazy-init worker thread stacks — under rayon's 1.9 MiB, and tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets. Go's 2.8 MiB carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 regex.c | 2,736,416 | 2.6 |
| rustc -O regex.rs | 28,246,568 | 26.9 |
| karac build regex.kara | 64,438,848 | 61.5 |

Karac now peaks at **61.5 MiB** vs rustc's **26.9 MiB** (2.28× higher) and clang's **2.6 MiB**; on the legacy backend (2026-07-28 feed) it peaked at 24.9 MiB, under rustc. The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site — the seq build path would shave a small constant off but not materially change the ratio.

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Gaps found, in the kara bug ledger:

- **B-2026-10-06-81** — `--interp` built every slot of `vec![row; n]` over one shared buffer, so the bottom-up DP table answered `"aa" ~ "a": true`. A fix is in flight.
- **B-2026-10-06-82** — `--interp` built a non-empty `Set[..]` literal as a `Vec`, so an NFA arm's `out.insert(q)` ran `Vec.insert(index)`. A fix is in flight.
- **B-2026-10-06-83** — `vec![row; 3]` with a NAMED row double-frees compiled.
- **B-2026-10-06-84** — a named `Set` / `Map` by-value param that is returned segfaults compiled.

## Bug ledger

**Surfaced [`B-2026-10-31-40`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the v2/MIR backend this kata's regex DP runs 1.37× legacy's instructions and 1.50× its cycles: the seq lane went from 1.11× to 1.60× `rustc -O`, and the par lane from 1.15× to 1.79× rayon.
