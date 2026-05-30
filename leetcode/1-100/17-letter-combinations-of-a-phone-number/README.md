# 17. Letter Combinations of a Phone Number

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Hash Table, String, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/letter-combinations-of-a-phone-number](https://leetcode.com/problems/letter-combinations-of-a-phone-number/)

Given a string `digits` containing characters from `'2'..'9'`, return every possible letter combination the digits could represent on a classic phone keypad (`2→abc`, `3→def`, `4→ghi`, `5→jkl`, `6→mno`, `7→pqrs`, `8→tuv`, `9→wxyz`). Empty input returns an empty list — the problem spec's "no combinations" sentinel.

```
("23")    → ["ad","ae","af","bd","be","bf","cd","ce","cf"]
("")      → []
("7")     → ["p","q","r","s"]
("7799")  → 256 combinations (4·4·4·4)
```

**Constraints:** `0 ≤ digits.length ≤ 4`, `digits[i] ∈ '2'..'9'`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Iterative BFS — frontier ×3 or ×4 per digit, fresh `String` per emitted combo | O(L · 4^L) time + output | [`letter_combinations.kara`](letter_combinations.kara) ✓ via `karac run` / `karac build` (after the workaround below) | [`letter_combinations.py`](letter_combinations.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all ten test cases — but only after a one-line workaround the kata surfaced in `karac build`; see § Karac issues surfaced.

## Why iterative BFS (and not backtracking)

Two shapes apply naturally — iterative BFS and recursive backtracking. Both are O(L · 4^L) time and produce the same output. The BFS shape lowers more cleanly here:

- **No recursion frame churn.** Backtracking pushes/pops a single buffer through L levels; BFS replaces the frontier wholesale per digit. The per-digit cost is a single `Vec[String].push` per emitted partial.
- **Output cardinality and alloc shape are explicit.** The frontier *is* the in-flight output — `next.len()` after the last digit equals the returned `Vec[String]`'s length. The allocator sees one `String.new()` + `push_str` + `push(letter)` per emitted combo, no recursion-frame overhead.
- **The auto-par bench's reduction sink fits.** `sum = sum + r.len()` is the slice-1 allow-list shape, recognized by default in `karac build`. Same shape kata [#14](../14-longest-common-prefix/) and [#15](../15-3sum/) use.

Letter groups live in a fixed `Vec[String]` of length 8, indexed by `(digit_byte - b'2')`. LeetCode restricts input to `'2'..'9'`, so the `(cast, index)` pair needs no bounds check — a malformed input would fail the problem precondition rather than the kata. The same one-pass-per-letter inner loop walks `letters.chars()` and emits one fresh `String` per (prefix, letter) pair via `push_str(prefix) + push(letter)` — the post-fix amortized-O(1) idiom kata [#71](../71-simplify-path/) introduced in karac commit `7ef42b9` (2026-05-25).

## Kāra features exercised

- **`Vec[String]` cartesian growth** — same `Vec.new() + push(String)` shape kata [#14](../14-longest-common-prefix/) uses to hold a `Vec[String]` of inputs, but with the Vec growing ×3 or ×4 per outer iter rather than being fixed-size. The per-digit alloc + scope-drop of the old `out` Vec is the workload's dominant memory term.
- **`String.push_str(other: String) + push(char)`** — same composite-build idiom as kata [#71](../71-simplify-path/)'s component reconstruction; both rely on the post-fix amortized-O(1) interpreter + codegen dispatch landed in karac `7ef42b9`. Surfaces the per-iter String-alloc cost in both the seq and auto-par lanes.
- **`for c in s.chars()`** on a String binding — same Unicode-scalar-value walk kata [#6](../6-zigzag-conversion/), [#14](../14-longest-common-prefix/), and [#71](../71-simplify-path/) use. The `letters.chars()` walk fires 3 or 4 times per outer iteration; the codegen lowers it to a `karac_string_decode_char` loop on the local's `{ptr, len}`.
- **`(u8 as i64) - (u8 as i64)` digit-to-index conversion** — same `(bytes[i] as i32) - (zero as i32)` shape kata [#91](../91-decode-ways/) uses for digit-byte arithmetic. Lowers to a plain `sub` on the byte value, no overflow guard needed (input bytes are in `'2'..'9'`).
- **Scalar `+` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`, scalar accumulator), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch. Same shape kata [#14](../14-longest-common-prefix/), [#15](../15-3sum/), and [#16](../16-3sum-closest/) use.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today (after the
# § Karac issues surfaced workaround).
karac run   letter_combinations.kara
karac build letter_combinations.kara && ./letter_combinations

# Python
python3 letter_combinations.py

# Verify they agree
diff <(./letter_combinations)              <(python3 letter_combinations.py) && echo OK
diff <(karac run letter_combinations.kara) <(python3 letter_combinations.py) && echo OK
```

## Karac issues surfaced

This kata's natural shape `for letter in groups[idx].chars()` (where `groups: Vec[String]` and `idx: i64`) silently iterates **zero times** under `karac build` while `karac run` works correctly. Root cause: the `.chars()` peel-off in `kara/src/codegen/control_flow_for.rs:92` recurses with the receiver as the new iterable; if the receiver is an `ExprKind::Index` it falls through to the `_ =>` arm at `control_flow_for.rs:216` (skip body, return 0). The literal-string, identifier, and field-receiver arms exist; the index-receiver arm doesn't.

The bug is **silent** — no error, no warning, just a zero-element loop. Per BENCH.md's correctness-first discipline, the kata surfaced this on the first `diff <(./letter_combinations) <(python3 letter_combinations.py)` run (expected 9 lines for `"23"`, got 0).

**Workaround applied in the kata source.** Bind the indexed receiver to a local `String` before the `.chars()` call:

```kara
// Buggy (codegen silently 0-iters):
for letter in groups[idx].chars() { … }

// Workaround (both paths agree):
let letters = groups[idx];
for letter in letters.chars() { … }
```

Same shape applies for `push_str(out[i])` → `let prefix = out[i]; s.push_str(prefix);` — the indexed-receiver path in argument position is not exercised by other katas in the corpus, and binding to a local is the conservative move. The bench source applies both bindings.

**Karac fix lane.** The codegen patch is small: in `src/codegen/control_flow_for.rs`, add an `ExprKind::Index { … }` arm to the `match &iterable.kind` block (after the `.chars()` peel-off) that compiles the indexed expression to a String struct value, extracts data+len, and calls `compile_for_string_chars_inner` — the same shape the `ExprKind::StringLit` arm at `control_flow_for.rs:137` uses. Same delta likely needed for `ExprKind::MethodCall` and `ExprKind::Call` receivers returning String. Tracked as a follow-up; this kata's first ship documents the finding.

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`letter_combinations.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct digit-strings of length 0..4 covering the full LeetCode constraint range: `""`, `"2"`, `"7"`, `"23"`, `"79"`, `"234"`, `"279"`, `"2349"` — the empty-input sentinel, single 3- and 4-letter groups, two-digit mixed shapes, and three- and four-digit cases that exercise the 4^L cardinality scaling. Per outer iter we rotate `idx = k % M` and call `letter_combinations` on that case. The output cardinality across the eight cases is `0 + 3 + 4 + 9 + 16 + 27 + 48 + 108 = 215`.

K = 100,000 outer iterations; the call is never loop-invariant (LLVM can't hoist it) and the eight distinct (digit-length, group-pattern) pairs keep any single output-cardinality assumption from holding. The sink — the running total of every returned Vec[String]'s length — is **2,687,500** = (K / M) × 215 across all five mirrors; bench.sh fails loudly on mismatch before timing starts. K dropped 10× vs kata 14/16's K=1M because per-call output cardinality scales as 4^L, not as 1 — the per-iter String alloc count averages ~27, so K=100k = 2.7 × 10⁶ String allocs is already the heaviest small-allocation workload in the 1-100 leetcode tranche.

This kata's per-iter body is **strictly heavier** than kata 14's on the alloc side — kata 14 emits one prefix String per call; kata 17 emits up to 108. That makes the seq-lane comparison directly about the allocator and the per-`push_str + push(char)` codegen, with the inner loop's compute cost a noise term against the memory-traffic dominant cost.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` emits a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-05-29, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time |
|---|---|
| c    letter_combinations (clang -O3)  | **43.1 ± 1.8 ms** |
| go   letter_combinations              | 47.0 ± 1.8 ms |
| rust letter_combinations              | 59.2 ± 1.7 ms |
| **kāra letter_combinations (seq)**    | **59.8 ± 1.5 ms** |

Allocation-dominated workload. **Kāra seq ties Rust within noise** (1.01×; the 0.6 ms delta is well inside σ). The C lead at 1.39× over Kāra is the allocator delta — `malloc`/`free` on small `char *` buffers with no intermediate struct vs Kāra's `Vec[String]` Vec-of-{ptr,len,cap} cycling — and the same delta to Rust (1.37×) confirms it's a C-allocator effect rather than a Kāra-specific gap. Go's 1.27× lead over Kāra/Rust is its escape-analysis + bump-allocator on short-lived `[]byte`-and-immediately-`string()` traffic, where the GC absorbs the per-iter churn without per-alloc free-list lookup.

Different shape from katas 14/15/16 (sort + two-pointer, allocator-light): there the headline is the codegen-quality compare against Rust; here it's the **allocator-pressure compare against C and Go**, with Rust's bsdmalloc-on-mac+`Vec<String>` paying the same overhead as Kāra's runtime allocator.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra letter_combinations (auto-par default)** | **13.7 ± 1.2 ms** | 123.2 ms |

The auto-par binary is **4.4× faster than the kāra seq binary** (59.8 → 13.7 ms), spreading the K=100k case-rotation reduction across the perf cores (~9.0× user-CPU-to-wall ratio on M5 Pro). Lower speedup ratio than allocator-light katas like #16 (7.6×) — the per-worker output-Vec allocation contends on the runtime's allocator surface, which serializes some of the parallel work. This is the legitimate-win case (BENCH.md kata #4 path): a real wall-time speedup with the `karac_par_reduce` machinery's +352 KiB binary delta.

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py letter_combinations` (K=10k) | 29.2 ± 1.0 ms |

Python at K=10k is 29 ms; projecting to the compiled mirrors' K=100k (~292 ms) puts it **~4.88× slower than kāra seq** and ~21.3× slower than the auto-par regime. Narrower than kata 14/16's Python-gap because CPython's interned-string + small-list allocators handle this workload's tight per-iter churn unusually well — the BFS `nxt.append(prefix + letter)` shape lowers to a hot interpreter path with no per-iter dict lookups.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 letter_combinations.c           | **44.7 ± 0.7 ms** |
| **karac build letter_combinations.kara**  | **82.7 ± 5.8 ms** |
| rustc -O letter_combinations.rs           | 99.4 ± 1.6 ms |

Kāra compiles **1.20× faster than `rustc -O`** and sits at **1.85× of clang -O3** — same shape as the rest of the corpus.

### Binary size

| Implementation | Size |
|---|---|
| c    letter_combinations            | 32.9 KiB |
| **kāra letter_combinations (seq)**  | **81.5 KiB** |
| **kāra letter_combinations (auto-par)** | **433.6 KiB** |
| rust letter_combinations            | 455.4 KiB |
| go   letter_combinations            | 2434.2 KiB |

Kāra seq lands at 81.5 KiB — **larger than kata 16's 33.0 KiB seq binary** because this workload pulls in the full `String.push_str` + `String.push(char)` + Vec[String] runtime archive surface, none of which kata 16 (numeric-only) touches. The auto-par row at 433.6 KiB is the seq surface + the `karac_par_reduce` worker-pool machinery; the **+352 KiB delta over seq** is the same shape kata 16's auto-par row carries (+327 KiB there).

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| rust letter_combinations            | 1.3 MiB |
| c    letter_combinations            | 1.3 MiB |
| go   letter_combinations            | 9.1 MiB |
| **kāra letter_combinations (seq)**  | **38.5 MiB** |
| **kāra letter_combinations (auto-par)** | **40.6 MiB** |

**Karac issue surfaced — runtime allocator retention.** C and Rust both land at 1.3 MiB peak — their `malloc`/`free` and `Vec<String>` drop cycles return pages to the OS aggressively, so the steady-state RSS reflects only the largest single iteration's live set (~108 strings × ~6 bytes ≈ 700 B). Kāra seq sits at **38.5 MiB — 30× higher**. With K=100k iterations × ~27 strings/iter × ~14 B retained per cycle, the runtime appears to hold onto freed pages rather than returning them to the OS. The auto-par row's 40.6 MiB is the seq footprint + ~2 MiB of per-worker scratch.

This is a runtime-allocator finding — the codegen is fine, but the heap-allocator strategy under heavy small-Vec churn is worth surfacing. Plausibly the runtime's `malloc` wrapper doesn't call `madvise(MADV_FREE)` on returned blocks, so the resident set grows with allocation-pattern history rather than instantaneous live set. Tracked as a follow-up alongside the `Vec[String][idx].chars()` codegen bug — both are kata-17-as-bug-finder results. Go's 9.1 MiB (vs C/Rust's 1.3) is its goroutine + GC heap floor, baseline for any Go program; Kāra's 38.5 MiB cannot be excused the same way (no GC, no green-thread runtime by default in the seq lane).

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 letter_combinations.c          | 2.6 MiB |
| **karac build letter_combinations.kara** | **10.7 MiB** |
| rustc -O letter_combinations.rs          | 28.3 MiB |

Kāra's compile-memory footprint is ~4.1× clang's and ~2.6× lower than rustc's on this kata — same shape as kata 15/16.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust 1.01× tie is the load-bearing result** — both pay the same `Vec<String>`-of-{ptr,len,cap} cycling cost in the per-iter alloc surface, and Kāra's codegen lowers `push_str + push(char)` to the same shape Rust's stdlib `String` does. The C and Go lead (1.39×, 1.27×) is the allocator surface, not the codegen — same delta to Rust as to Kāra. The runtime-memory finding (38.5 MiB vs C/Rust's 1.3 MiB) is the kata's clearer signal than the wall-time numbers; that lives in § Runtime memory (peak) above.
