# 125. Valid Palindrome

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Two Pointers, String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/valid-palindrome](https://leetcode.com/problems/valid-palindrome/)

A string is a valid palindrome if, after lowercasing letters and dropping
every non-alphanumeric character, it reads the same forwards and backwards.

```
"A man, a plan, a canal: Panama"  →  true
"race a car"                       →  false
" "                                →  true   (empty after filtering)
```

**Constraints:** `1 ≤ s.length ≤ 2·10⁵`; `s` is printable ASCII. The check is
case-insensitive and ignores everything that isn't a letter or digit.

## Why this kata — the lexer's identifier/keyword scan surface

The most direct corpus exercise of the self-hosted lexer's **byte
classification + ASCII case-fold** predicates (`kara-katas` lexer string-scan
shape § 1). Every move this kata makes is one the lexer makes on every token:

| Lexer surface | This kata |
|---|---|
| **`is_alpha` / `is_ascii_digit`** byte predicates (the scan's inner classify) | `is_alnum(b)` over `b'0'..b'9'` / `b'a'..b'z'` / `b'A'..b'Z'` |
| **ASCII case-fold** (keyword/ident normalization before dispatch) | `to_lower(b)` = `'A'..'Z' + (b'a' - b'A')` |
| **byte-indexed scan + advance** (the core loop) | two pointers walking the `bytes()` view inward |
| **token-text materialization** (lowercased ident / radix-stripped number) | the filter style's normalized `Vec[u8]` buffer |

## Approaches

Three styles, all byte-identical to the Python oracle across all 16 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Two-pointer, in-place** ★ | [`valid_palindrome.kara`](valid_palindrome.kara) | classify + case-fold + compare in place; no allocation |
| Filter-then-compare (index-heavy) | [`valid_palindrome_filter.kara`](valid_palindrome_filter.kara) | build a normalized `Vec[u8]`, then symmetric-index compare |
| Recursive two-pointer | [`valid_palindrome_recursive.kara`](valid_palindrome_recursive.kara) | `check(bytes, i, j)` skips + recurses on `(i+1, j-1)` |
| Reference oracle | [`valid_palindrome.py`](valid_palindrome.py) | known-correct LeetCode answer |

All three follow the [lexer string-scan shape](../../../README.md): scan the
zero-copy `bytes()` view with `b'…'` byte literals, classify, and case-fold via
byte arithmetic — never a `char`-level API. The two-pointer style is
allocation-free (the lexer's fast path); the filter style materializes a
normalized buffer (the lexer's token-text path).

## What this kata uncovered — a HIGH codegen bug in narrow-int branch merges

The byte-scan **correctness** surface looked simple, but it flushed a
significant `karac` codegen bug — invisible to the interpreter, wrong only
under `karac build`. The kata's `to_lower`:

```kara
fn to_lower(b: u8) -> u8 {
    if b >= b'A' and b <= b'Z' { b + (b'a' - b'A') } else { b }
}
```

**always returned 0 under `karac build`** (correct under `karac run`), so every
palindrome check reported `true`. The defect generalizes to any value
`if` / `match` / `if let` whose arms **mix a bare narrow-int value with a
narrow-int arithmetic expression**.

**Root cause.** `compile_narrow_int_binop` range-checks `b + 32u8` to the
declared `u8` width but **leaves the value at the i64 it computes at** (boundary
coercion narrows it later — its design contract). So the `then` branch was a
*runtime* i64 sitting beside the i8 `else` branch. The phi-merge only builds a
phi when the two branch LLVM types agree; otherwise it silently returns a
const-0 **placeholder** — so the whole `if` evaluated to 0. The earlier
self-hosting-#7 fix (`unify_int_branch_widths`) reconciled this width mismatch
**only for compile-time-constant** wide branches, its comment asserting a
non-constant wide branch was "typechecker-impossible" — but narrow-int
arithmetic makes it routine. `match` had **no** width reconciliation at all;
`if let` shared the gap.

**Fix** ([`32ad0c84`] in `karac`). `unify_int_branch_widths` now truncates the
wider branch whether const **or runtime**, emitting the `trunc` in the
*predecessor* block (before its branch to the merge) so the phi operand
dominates its incoming edge. Value-preserving: the typechecker has unified both
branches to one Kāra type, so a width mismatch means the wide side is a
widened-narrow value whose low bits *are* the value. A new N-ary sibling
`unify_int_match_arm_widths` applies the same across `match` arms. The bug was
**latent in the current self-hosted lexer** (it widens to `i64` before
arithmetic — `hex_val -> i64` does `(c as i64) - …`), so this kata flushed a
general codegen gap ahead of the parser port or a more idiomatic narrow-arith
rewrite. Regression test `tests/codegen.rs::test_e2e_narrow_int_arith_branch_phi_width`
(if/else both directions + 3-arm `match` + `if let`); recorded as the #7
follow-on in `phase-12-self-hosting.md`.

[`32ad0c84`]: ../../../../kara/

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **8%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.3%** margin against `go build` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmarks
Workload: check a fixed palindrome (`"A man, a plan, a canal: Panama"` × 8,
which filters to the palindrome core `amanaplanacanalpanama` × 8 — itself a
palindrome, so every pass does the **full** scan) `ITERS=3M` times, reducing to
the palindrome count (sink `3 000 000`). The benched algorithm is the
**allocating filter variant** (build a normalized `Vec[u8]`, then compare): a
pure two-pointer over a fixed input is loop-invariant and the optimizer folds
the 3M iterations to one, so — exactly as #394 benches its allocating decode —
the per-pass allocation is what keeps the reduction honest. Apple M5 Pro;
`bench/bench.sh` (`hyperfine`), karac g6697158fa (v2/MIR backend), measured
2026-11-01. **Seq lane** = single-threaded (Kāra built `KARAC_AUTO_PAR=0`).

### Seq lane — runtime (single-threaded, apples-to-apples)

| | C | Go | **Kāra (seq)** | Rust (overflow-checks=on) | Rust |
|---|---|---|---|---|---|
| time | 491.6 ± 4.3 ms | 757.4 ± 45.9 ms | **767.1 ± 12.5 ms** | 873.9 ± 15.4 ms | 875.6 ± 32.3 ms |
| vs Kāra | 1.56× faster | 1.01× faster | — | 1.14× slower | 1.14× slower |

On this allocation-light byte-scan + predicate + case-fold workload, **Kāra's
single-threaded codegen is now ahead of Rust and level with Go** — 0.88× of
`rustc -O` (and of `overflow-checks=on` Rust), 1.01× of `go build`, and 1.56×
behind `clang -O3`. That is a real gain, not session drift: every comparator ran
10–16% slower in this session than in the previous feed (legacy karac,
2026-07-28) while Kāra ran 8% faster, so the ratios moved — Kāra/Rust 1.04× →
0.88×, Kāra/C 1.94× → 1.56×, Kāra/Go 1.28× → 1.01×. C's lead is the tight
classify/compare inner loop with a per-pass allocation at its leanest.

Note (2026-11-07, karac g97681763d): the re-run reads seq Kāra 0.95× `rustc -O`, 0.94× equal-safety Rust, 1.67× C and 1.12× Go (behind Go now, not level); par Kāra 75.5 ms against rayon's 174.3 ms.

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **157.5 ms** | 94.2 ms | 49.5 ms |
| compile peak RSS | 57.5 MiB | 27.6 MiB | 2.6 MiB |
| binary (seq) | **295.8 KiB** | 455.6 KiB | 32.7 KiB |
| binary (par) | 377.1 KiB | 454.0 KiB (rayon) | 32.9 KiB (pthreads) |

Kāra's cold compile (158 ms) is now 1.67× `rustc -O`'s (94 ms) at 2.1× its peak
memory. The seq binary is 302,896 B — 1.54× smaller than Rust's and 8.2× smaller
than Go's (2.4 MiB, runtime+GC in every binary), but no longer C-sized: every
v2/MIR Kāra binary is ~300–390 KB where legacy's were ~34 KB (legacy built this
kata to 34,320 B), tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md).
Runtime peak RSS is a clean **1.1 MiB**, tying Rust and within 1.08× of C — no
leak (unlike #394's String-return-binding leak; this kata's allocations all free
at scope exit).

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The check is sequential within one pass, but the outer reduction over `ITERS`
independent passes is embarrassingly parallel. All implementations parallelize
that *same* reduction across the machine's cores — the difference is what the
programmer had to write:

| | parallel code written | time | total CPU |
|---|---|---|---|
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 53.8 ± 1.9 ms | 776 ms |
| **Kāra (auto-par)** | **none** — the compiler recognized the `sum += pass` reduction | **200.0 ± 9.2 ms** | 2941 ms |
| Rust + rayon | `rayon` crate dependency + `.into_par_iter()` rewrite | 172.3 ± 13.5 ms | 2822 ms |
| Go goroutines | manual chunking + `sync.WaitGroup` + partial-merge | 324.7 ± 6.0 ms | 1168 ms |

**Kāra's auto-par lands within 1.16× of hand-tuned rayon (200.0 vs 172.3 ms) and
runs 1.62× faster than hand-written goroutines — with no parallel source at
all**, sitting 3.72× behind the raw-pthreads "metal floor." It spends 1.04× the
total CPU rayon does (2941 ms vs 2822 ms) to get there. Against the previous
feed (legacy karac, 2026-07-28) that is Kāra/rayon 1.08× → 1.16× (flat), Kāra/Go
0.84× → 0.62× (better), Kāra/C 3.98× → 3.72×. The default `karac build` emits a
task-spawn dispatch (one `karac_mir_task_spawn` call in its emitted IR,
`KARAC_MIR_LL`; the `KARAC_AUTO_PAR=0` seq build has none) off the plain
sequential `sum += pass(input)` loop; the Rust, Go, and C programmers each had
to opt in and restructure. Speedup over Kāra's own seq lane: **3.84×** (767.1 ms
→ 200.0 ms) across the machine's free cores. (Multi-core within the par lane;
per [`BENCH.md`]'s two-lane discipline, *not* comparable to the single-thread
seq rows above.) Measured 2026-11-01: pinned to exactly two workers
(`KARAC_THREADS=2`) the par build is slower than at one worker (1.29–1.51 s vs
0.79–0.91 s), [`B-2026-11-01-17`](../../../../kara/docs/bugs-v2.md); the
published default-worker row above is unaffected.

**Buyer reframe.** The parallel speedup that costs a Rust team a crate, an API
rewrite, and a new class of data-race bugs to chase — and a Go team a hand-rolled
chunk/merge that here still ran 1.62× slower — Kāra delivers from the same
single-threaded source, landing within 1.16× of rayon's throughput at
comparable CPU. Colorless parallelism: fewer lines, no `unsafe`/`Send`/`Sync`
reasoning, no goroutine-leak or partial-merge bugs, at near-rayon throughput.
Less engineering and fewer concurrency incidents per unit of performance.

[`BENCH.md`]: ../../../BENCH.md

## Kāra features exercised

- **`bytes()` byte classification** — `b'0'`/`b'9'`/`b'a'`/`b'z'`/`b'A'`/`b'Z'`
  byte-literal range predicates (`is_alnum`), no `char`-level API.
- **ASCII case-fold via byte arithmetic** — `b + (b'a' - b'A')` (the bug this
  kata flushed: narrow-int arithmetic in a value-`if` branch).
- **Two-pointer in-place scan** — allocation-free inward walk over the
  zero-copy byte view (the lexer's fast path).
- **`Vec[u8]` accumulator** — `push` + symmetric-index compare (filter style;
  the lexer's normalized-token-text path).
- **Recursion over a `Slice[u8]` argument** — `check(bytes, i, j)` with byte
  indexing (recursive style).
- **Auto-parallelized reduction** — `sum += pass(input)` lowered to
  task spawns (`karac_mir_task_spawn` in the v2/MIR IR) with no parallel source (par lane).

## Bug ledger

This kata surfaced `B-2026-06-13-14` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).

**Surfaced [`B-2026-11-01-17`](../../../../kara/docs/bugs-v2.md)** (perf, open). With exactly two workers (`KARAC_THREADS=2`) the auto-par binary runs slower than with one (1.29–1.51 s against 0.79–0.91 s), on 3.5× the cycles for 1.6% more instructions. The published par row uses the default worker count and is unaffected. This kata is the row's second instance; the first is [#71](../../1-100/71-simplify-path/#bug-ledger). Measured 1 Nov 2026 with karac g6697158fa.
