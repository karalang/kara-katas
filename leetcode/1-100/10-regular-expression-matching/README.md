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

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, and Go. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`regex.{kara,rs,c,py}`, `go-seq/main.go`).

Per [`../../../BENCH.md`](../../../BENCH.md) § *Implicit auto-par*, this kata exercises karac's auto-par-on-reduction path: the K = 10,000,000 outer loop's `sum = sum + (if r { 1i64 } else { 0i64 })` accumulator is a textbook associative + commutative reduction, which the slice-1 concurrency analyzer recognizes and slice-3b codegen lowers to a `karac_par_reduce` dispatch *by default*. To honor BENCH.md's two-lane discipline (cross-lane wall-time ratios are not meaningful) the bench builds **two** kara binaries:

- **`regex_kara_seq`** — built with `KARAC_AUTO_PAR=0` (codegen.rs Slice 6 gate — the documented mechanism for side-by-side seq-vs-par benchmarking of the same source). The within-lane row directly comparable to rustc -O / clang -O3 / go build.
- **`regex_kara`** — default `karac build` output. Picks up auto-par dispatch (~13.4 cores active on this workload). Reported separately so the production-default Kara behavior stays visible.

**Workload.** N = 8 (string, pattern) pairs cycled by `k % N`, each chosen to exercise a different branch of the recursive matcher so no single shape dominates the predictor's history. K = 10,000,000 outer iters, sink = count of `is_match(strs[k % N], pats[k % N])` widened to i64. All four compiled mirrors agree on `7500000` (six of the eight pairs match × K / N) before any timing runs; `bench.sh` fails loudly on mismatch.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 5 --runs 30 --shell=none`:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra regex** (`KARAC_AUTO_PAR=0`) | **127.5 ms ± 1.2 ms** | 125.0 ms | 99% |
| rust regex (rustc -O) | **112.9 ms ± 0.8 ms** | 111.0 ms | 99% |
| c    regex (clang -O3) | **114.2 ms ± 1.2 ms** | 112.0 ms | 99% |
| go   regex | **182.2 ms ± 4.0 ms** | 179.0 ms | 99% |

Kāra, Rust, and C are within **13% of each other** — a three-way per-core codegen-quality comparison on a recursion-heavy workload. Kāra is slowest of the three this run (127.5 vs Rust's 112.9 and C's 114.2 ms), Rust's row being the tightest (σ 0.8 ms), so the gap is a real per-core lag for Kāra here, not noise — roughly 1.13× behind Rust and 1.12× behind C. The recursive matcher's hot path (load `p[j]`, branch on `*`, peek and conditional-tail-call) is exactly the shape where rustc's mid-2026 inliner opens up a small lead via aggressive specialization; karac's post-`bdac0d8` internal-linkage inlining heuristic lands close but not level on this workload.

The Go gap (~1.43× of Kāra-seq) reflects per-call slice-header reconstruction at each recursive frame (`[]byte(s)` happens fresh per `isMatch` call in the bench main, whereas rust/c/kara hold the byte view as a function-local across the recursion) plus the per-iter `idx % n` and `int → int64` widening overhead Go can't SROA across the predicate body.

### Runtime — auto-par regime (kara default, multi-core)

Same snapshot, default `karac build` output:

| Implementation | Wall time | User-CPU | CPU% |
|---|---|---|---|
| **kāra regex** (auto-par on reduction) | **10.9 ms ± 1.1 ms** | 146.0 ms | ~1339% (~13.4 cores) |

Karac's auto-par-on-reduction recognizes the K=10M reduction in `main` and emits a `karac_par_reduce` dispatch — the binary carries `karac_par_reduce` + `karac_reduce_combine_add_i64` + `karac_reduce_worker_0` symbols, ~13.4 cores active during the run. The wall-time win *over the seq-lane Kāra row above* is **11.7×** (127.5 / 10.9); total CPU time goes up 17% (125.0 → 146.0 ms user) as the cost of dispatch + per-worker fixed overhead. (The auto-par row's σ is ~1.1 ms — short multi-core runs are dispatch-noise-dominated.) Net: real production wall-time speedup on this workload's shape, paid for in additional CPU and a +263 KiB binary footprint (see § *Binary size* below).

**Not headlined against the C / Rust / Go rows above.** Per BENCH.md's two-lane discipline, cross-lane wall-time ratios are not meaningful — naming "kara is 11× faster than rust" here would conflate per-core codegen quality with whether the comparator opted into parallelism. The seq-lane table is the within-lane codegen-quality comparison; the auto-par row is what Kāra delivers as a *language-level* choice on top of that codegen-quality baseline (no source-level annotation; the analyzer recognizes the natural serial reduction). A follow-up CR can add a true par lane (`rayon::par_iter` + goroutines variants of the outer reduction) so this number lands against in-lane parallel comparators.

### Codegen vs Python

CPython at K = 1M takes **758.6 ± 10.5 ms** (single-core); projected to K = 10M that's ~7.59 s. Both Kāra rows beat the projection by wide margins, but the cross-lane caveat applies symmetrically: Kāra-seq vs CPython is the within-lane per-core comparison (~60× faster), and Kāra-auto-par vs CPython is the cross-lane regime comparison (~696× faster). The Python mirror is here as the ergonomic-foil data point per BENCH.md § *Comparison baselines*, not as a headline.

### Compile elapsed (cold)

Snapshot — M5 Pro, 2026-05-31, hyperfine `--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Workload | Kāra (`karac build`) | Rust (`rustc -O`) | C (`clang -O3`) |
|---|---|---|---|
| `regex` | **82.1 ± 1.5 ms** | 92.0 ± 1.9 ms | 46.1 ± 1.7 ms |

Karac is **1.12× faster than rustc -O** and **1.78× slower than clang -O3**. All three rose vs the 2026-05-25 snapshot (karac +5.4, rustc +15.8, clang +6.5 ms) under heavier background load this run — compile *elapsed* is the load-confounded metric; the deterministic signals (byte-identical binaries, compile-memory floor) held. Single-file invocations only — `go build`'s first run mixes module resolution + std-lib link and isn't comparable to a single-file `rustc` / `clang` / `karac` invocation; excluded per BENCH.md.

### Binary size

| Implementation | Bytes | KiB |
|---|---|---|
| c    regex | 33,512 | 32.7 |
| **kāra regex (seq)** | **34,024** | **33.2** |
| kāra regex (auto-par) | 303,128 | 296.0 |
| rust regex | 466,376 | 455.4 |
| go   regex | 2,492,546 | 2,434.1 |

The seq-lane Kāra binary sits **within 0.5 KiB of clang's** (33.2 vs 32.7 KiB) — the cross-archive LTO + DCE work (landed 2026-05-12) plus the post-`e76f42b` `__TEXT,__jittmpl` segment compaction has the seq binary at C-class minimum. The auto-par variant grows +263 KiB to carry the `karac_par_reduce` machinery (per-branch trampolines + reduction-combine globals + worker-pool registration) — same +263 KiB ballast kata [#4](../4-median-of-two-sorted-arrays/#binary-size), [#8](../8-string-to-integer-atoi/#binary-size), and [#9](../9-palindrome-number/#binary-size) carry when their outer reductions go auto-par. Here too the ballast pays for a real within-language wall-time win.

### Runtime memory (peak)

| Implementation | Bytes | MiB |
|---|---|---|
| **kāra regex (seq)** | **1,065,248** | **1.0** |
| c    regex | 1,081,632 | 1.0 |
| rust regex | 1,130,784 | 1.1 |
| kāra regex (auto-par) | 1,491,256 | 1.4 |
| go   regex | 2,900,496 | 2.8 |

Kāra-seq's peak sits **16 KiB under C** (1,065,248 vs 1,081,632) and 64 KiB under Rust. (All five RSS figures shifted by 16 KiB-page multiples vs the 2026-05-25 snapshot — peak-footprint is quantized to the 16 KiB page on Apple Silicon, so Kāra-seq lands one page below C this run; that's measurement granularity, not a regression.) The recursive matcher allocates nothing inside the loop (the input `Vec[String]` is fixed at ~~~~200 bytes total of string-header storage, the recursion lives entirely on the call stack), so steady state is dominated by libc + Mach-O loader overhead. Auto-par Kāra adds ~0.5 MiB for the lazy-init worker thread stacks — tunable downward via `KARAC_PAR_WORKERS` for memory-constrained targets. Go's 2.9 MiB carries its GC roots + scheduler arena overhead.

### Compile memory (cold)

| Compiler | Bytes | MiB |
|---|---|---|
| clang -O3 regex.c | 2,638,136 | 2.5 |
| karac build regex.kara | 14,582,216 | 13.9 |
| rustc -O regex.rs | 28,246,640 | 26.9 |

Karac peaks at **13.9 MiB** vs rustc's **26.9 MiB** (1.9× lower) and clang's **2.5 MiB** (5.6× higher). The kara number includes the auto-par recognition pass + reduction codegen, which is bounded constant work per recognized site — the seq build path would shave a small constant off but not materially change the ratio. (The +0.9 MiB vs the 2026-05-25 snapshot is the documented fixed per-compile floor from karac feature-growth over the window — content-independent, byte-identical output, tracked benign across katas #6–#10.)

### Numbers published here are reference data

The CI gate's source-of-truth aggregate lives in [`karac-rust/bench/compile_speed/`](../../../../karac-rust/bench/compile_speed/) (different corpus: curated subset + synthetic 10K-LOC stress program).
