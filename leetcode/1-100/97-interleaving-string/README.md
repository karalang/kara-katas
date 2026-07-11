# 97. Interleaving String

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String · Dynamic Programming &nbsp;·&nbsp; **Source:** [leetcode.com/problems/interleaving-string](https://leetcode.com/problems/interleaving-string/)

Given strings `s1`, `s2`, and `s3`, decide whether `s3` is formed by **interleaving** `s1` and `s2` — weaving their characters together while preserving the left-to-right order *within* each string. Formally `s3` must have length `|s1|+|s2|` and split into a subsequence equal to `s1` (in order) and the complementary subsequence equal to `s2` (in order).

```
s1 = "aabcc", s2 = "dbbca", s3 = "aadbbcbcac"  ->  true
s1 = "aabcc", s2 = "dbbca", s3 = "aadbbbaccc"  ->  false
s1 = "",      s2 = "",      s3 = ""            ->  true
```

**Constraints:** `0 ≤ |s1|, |s2| ≤ 100`, `0 ≤ |s3| ≤ 200`; all lowercase English letters.

## Approaches

| Approach | Kāra | Python |
|---|---|---|
| **2D DP table** ★ | [`interleave.kara`](interleave.kara) ✓ | [`interleave.py`](interleave.py) ✓ |
| **1D rolling DP** (O(\|s2\|) space) | [`interleave_rolling.kara`](interleave_rolling.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter (`karac run --interp`), JIT (`karac run`), and codegen (`karac build`) produce identical output for both approaches, under the default (auto-par on) build and `KARAC_AUTO_PAR=0` alike; the two Kāra approaches agree with **each other** and with the Python mirror. An independent **brute-force ground-truth check** confirms the DP: it matches a recursive try-all-interleavings solver on the case battery **and on 20,000 randomised fuzz cases** (real interleavings and perturbed near-misses), zero mismatches. Both solvers compile with zero diagnostics.

## Why a 2D table — and how to collapse it

The subproblem is `dp[i][j]` = "can the first `i` characters of `s1` and the first `j` of `s2` interleave to form the first `i+j` of `s3`?". The last character of that prefix, `s3[i+j-1]`, had to come from **one** of the two strings — from `s1` (so `s1[i-1]` matches it and `dp[i-1][j]` already held) or from `s2` (`s2[j-1]` matches and `dp[i][j-1]` held):

```
dp[i][j] = (dp[i-1][j] && s1[i-1] == s3[i+j-1])
        || (dp[i][j-1] && s2[j-1] == s3[i+j-1])
```

with `dp[0][0] = true` and an immediate `false` when `|s1|+|s2| ≠ |s3|`.

**2D table** ([`interleave.kara`](interleave.kara), the ★) fills a flat `Vec[bool]` of `(|s1|+1)·(|s2|+1)` cells row by row — the clearest statement of the recurrence, O(|s1|·|s2|) time and space.

**1D rolling** ([`interleave_rolling.kara`](interleave_rolling.kara)) notices the recurrence only ever reads row `i-1` and the cell immediately left in row `i`, so a single `Vec[bool]` of length `|s2|+1` suffices: sweeping `j` left-to-right and overwriting `dp[j]` in place, at the update point `dp[j]` still holds row `i-1`'s value (the "from `s1`" term) while `dp[j-1]` already holds row `i`'s (the "from `s2`" term). Same answers, O(|s2|) memory — a distinct surface that proves the recurrence two ways.

## Kāra features exercised

- **`String.bytes()` + byte indexing** — both solvers read `s1`/`s2`/`s3` as byte sequences and compare `a[i] == c[k]` in the hot loop (bounds-checked index reads).
- **`Vec[bool]` as a DP grid** — a flat boolean table indexed `i*stride + j` (2D) or a rolling row (1D), pushed to length then written in place with `dp[k] = …`.
- **`and` / `or` short-circuit booleans** — the recurrence is a disjunction of two conjunctions; Kāra spells these `and`/`or` (not `&&`/`||`), which the compiler's diagnostic points out directly.
- **String-literal arrays + data-dependent indexing** — the case battery is a `["…", …]` array of string literals indexed by a runtime value.

**v1 note.** Sizes stay within the `|s3| ≤ 200` constraint. The sink folds each case's boolean verdict into a running polynomial hash (order-sensitive). Both solvers verified byte-identical under `karac run` (JIT), `karac run --interp` (tree-walk), and `karac build` (AOT), including the default auto-parallelising build and `KARAC_AUTO_PAR=0`; they agree with each other, the Python mirror, and the brute-force + fuzz ground truth.

## Running

```bash
# Kāra — interpreter, JIT, and codegen produce the same output today.
karac run   interleave.kara
karac build interleave.kara && ./interleave

# The 1D rolling variant (identical output):
karac run interleave_rolling.kara

# Python
python3 interleave.py

# Verify they all agree
diff <(karac run interleave.kara) <(python3 interleave.py)             && echo OK
diff <(karac run interleave.kara) <(karac run interleave_rolling.kara) && echo OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`interleave.{kara,rs,c,py}`, `go-seq/main.go`).

> **Machine.** The canonical numbers below are a shared **x86-64 Linux cloud-container** reference run — [`bench/results.container-x86.json`](bench/results.container-x86.json). The corpus's canonical **Apple M5 Pro** numbers ([`bench/results.json`](bench/results.json)) are folded in separately; absolute times/sizes/RSS are **not** comparable across the two hosts (different ISA + toolchains + a noisy shared host), only within-file cross-language ratios are the signal. Re-run `bench.sh` on the M5 to refresh the canonical table.

**Workload.** A single interleaving check on ≤ 24-char strings is instant, so the bench runs **K = 400,000** reps of the O(|s1|·|s2|) 2D DP. The case is **data-dependent** (`idx = acc%12`, seeded by the running hash), so the per-rep verdict can't be hoisted or CSE'd — the anti-hoist lever of [#93](../93-restore-ip-addresses/)/[#96](../96-unique-binary-search-trees/). 12 pre-generated cases (|s1|, |s2| ≈ 18–24 over a 3-letter alphabet, a mix of true interleavings and perturbed near-misses); each call fills a **fresh** boolean table (Kāra `Vec[bool]`, C `calloc`, Rust `vec!`, Go slice — matched allocate-per-call idioms) and the verdict folds into a rolling polynomial hash. All five compiled mirrors must agree on `940211674` before timing.

**Equal safety.** Kāra checks integer overflow by default; `rustc -O` wraps silently. So alongside `rustc -O` the table includes a `rustc -O -C overflow-checks=on` row as the faithful like-for-like (kata [#69](../69-sqrtx/)'s discipline).

`--warmup 5 --runs 30 --shell=none`. All single-threaded. **x86-64 container numbers** (canonical M5 pending; see the machine note):

| Implementation | Wall time |
|---|---|
| c    interleave (clang -O3, calloc table)          | 258.3 ± 4.0 ms |
| rust interleave (rustc -O, Vec)                     | 361.2 ± 2.8 ms |
| rust interleave (rustc -O, overflow-checks=on)       | 481.9 ± 8.0 ms |
| go   interleave (slice, GC)                         | 492.0 ± 3.2 ms |
| **kāra interleave**                                 | **583.2 ± 5.5 ms** |

**On this container kāra trails — the honest cost of bounds-checking an index-dense inner loop.** Every DP cell does five-plus **bounds-checked array reads** — `dp[up]`, `dp[left]`, `s1[i-1]`, `s2[j-1]`, and `s3[i+j-1]` — and kāra checks all of them by default, while `clang -O3` and release Rust elide the checks entirely (and Go's are cheaper here). So kāra is **2.26× behind C**, **1.61× behind unchecked Rust**, and — the equal-safety line that usually saves it — still **1.21× behind `rustc -O -C overflow-checks=on`**. That last gap is the tell: overflow checks aren't the bottleneck here (they cost Rust ~33 %, 361 → 482 ms, and kāra clears checked Rust on the *arithmetic*-bound sibling [#96](../96-unique-binary-search-trees/)); it is the **per-element bounds check** on a loop that is almost nothing *but* array reads, where kāra has no compute to hide the check behind. This is the mirror image of #96 (arithmetic-heavy → kāra fastest of five): the two katas bracket where kāra's default safety is free (compute-bound) and where it bites (index-bound). Bounds-check *elision* on provably-in-range DP indices is the codegen headroom this kata points at. Go's slice bounds checks land it between the Rust builds and kāra (492 ms, at 7.4 MiB RSS vs kāra's 2.5 MiB); C's raw `calloc` table with no checks at all is the floor. Python (K = 20,000, a fraction of the compiled iterations, timed separately at **1131 ms**, not cross-checked) is the ergonomic foil.

**Flagged for the M5 re-bench** — the checked-vs-unchecked-indexing gap is a codegen property that should carry to the M5, but the corpus has seen container orderings compress on the wider out-of-order core, so treat the *margin* as a data point.

> **Binary size caveat.** As with the sibling katas, the kāra binary in `results.container-x86.json` measures large (heap-growing programs on this container build retain the backtrace-symbolizer tree `--gc-sections` should strip; a correct build is ~15 KB). It is a build-linkage artifact of this run, independent of the runtime numbers, flagged for the M5.

Compile-cold, binary size, and peak-RSS records are in [`bench/results.container-x86.json`](bench/results.container-x86.json) (x86 reference) and, once folded in, [`bench/results.json`](bench/results.json) (M5, canonical).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer, so the headline ratio is the codegen-vs-Rust gap — here on a byte-comparison-heavy 2D-DP + allocate-per-call shape, with the equal-safety comparison (Kāra's checked index/loop arithmetic vs `rustc -O -C overflow-checks=on`) the honest like-for-like. C calibrates the metal floor, Go the GC data point, Python (run at a fraction of the iteration count, timed separately, not cross-checked) the ergonomic foil.
