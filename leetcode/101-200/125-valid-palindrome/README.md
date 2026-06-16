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

## Benchmarks

Workload: check a fixed palindrome (`"A man, a plan, a canal: Panama"` × 8,
which filters to the palindrome core `amanaplanacanalpanama` × 8 — itself a
palindrome, so every pass does the **full** scan) `ITERS=3M` times, reducing to
the palindrome count (sink `3 000 000`). The benched algorithm is the
**allocating filter variant** (build a normalized `Vec[u8]`, then compare): a
pure two-pointer over a fixed input is loop-invariant and the optimizer folds
the 3M iterations to one, so — exactly as #394 benches its allocating decode —
the per-pass allocation is what keeps the reduction honest. Apple M5 Pro;
`bench/bench.sh` (`hyperfine`). **Seq lane** = single-threaded (Kāra built
`KARAC_AUTO_PAR=0`).

### Seq lane — runtime (single-threaded, apples-to-apples)

| | C | **Kāra (seq)** | Go | Rust |
|---|---|---|---|---|
| time | 415.5 ms | **796.6 ms** | 643.6 ms | 734.4 ms |
| vs Kāra | 1.92× faster | — | 1.24× faster | 1.08× faster |

On this allocation-light byte-scan + predicate + case-fold workload, **Kāra's
single-threaded codegen trails the pack** — `clang -O3` by 1.92×, `go build` by
1.24×, and `rustc -O` by 1.08×. The tight classify/compare inner loop with a
per-pass `Vec[u8]` allocation lands Kāra at the back here; it's in the same
order of magnitude as Rust and Go, but behind all three compiled comparators on
this shape.

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **78.8 ms** | 96.6 ms | 47.5 ms |
| compile peak RSS | 13.5 MiB | 27.6 MiB | 2.5 MiB |
| binary (seq) | **33.3 KiB** | 455.6 KiB | 32.7 KiB |

Kāra's cold compile (79 ms) edges `rustc -O` (97 ms) at half its peak memory,
and emits a **C-sized 33 KiB binary** — **13.7× smaller than Rust** and **74×
smaller than Go** (2.4 MiB, runtime+GC in every binary). Runtime peak RSS is a
clean **1.2 MiB**, tying Rust and within 1.1× of C — no leak (unlike #394's
String-return-binding leak; this kata's allocations all free at scope exit).

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The check is sequential within one pass, but the outer reduction over `ITERS`
independent passes is embarrassingly parallel. All implementations parallelize
that *same* reduction across the machine's cores — the difference is what the
programmer had to write:

| | parallel code written | time | total CPU |
|---|---|---|---|
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 38.5 ms | 574 ms |
| **Kāra (auto-par)** | **none** — the compiler recognized the `sum += pass` reduction | **66.3 ms** | 1036 ms |
| Rust + rayon | `rayon` crate dependency + `.into_par_iter()` rewrite | 60.4 ms | 1031 ms |
| Go goroutines | manual chunking + `sync.WaitGroup` + partial-merge | 224.8 ms | 1011 ms |

**Kāra's auto-par lands within 1.10× of hand-tuned rayon (66.3 vs 60.4 ms) and
runs 3.4× faster than hand-written goroutines — with no parallel source at
all**, sitting within 1.72× of the raw-pthreads "metal floor." It spends
slightly more total CPU than rayon (1036 ms vs 1031 ms) to get there. The
default `karac build` emits a
`karac_par_reduce` dispatch off the plain sequential `sum += pass(input)` loop;
the Rust, Go, and C programmers each had to opt in and restructure. Speedup over
Kāra's own seq lane: **12.0×** (796.6 ms → 66.3 ms) across the machine's free cores.
(Multi-core within the par lane; per [`BENCH.md`]'s two-lane discipline, *not*
comparable to the single-thread seq rows above.)

**Buyer reframe.** The parallel speedup that costs a Rust team a crate, an API
rewrite, and a new class of data-race bugs to chase — and a Go team a hand-rolled
chunk/merge that here still ran 3.4× slower — Kāra delivers from the same
single-threaded source, landing within 1.10× of rayon's throughput at
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
- **Auto-parallelized reduction** — `sum += pass(input)` lowered to a
  `karac_par_reduce` dispatch with no parallel source (par lane).

---

**Bug ledger:** this kata surfaced `B-2026-06-13-14` — see the [`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
