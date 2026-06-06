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
| Iterative BFS — frontier ×3 or ×4 per digit, fresh `String` per emitted combo | O(L · 4^L) time + output | [`letter_combinations.kara`](letter_combinations.kara) ✓ via `karac run` / `karac build` | [`letter_combinations.py`](letter_combinations.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all ten test cases.

## Why iterative BFS (and not backtracking)

Two shapes apply naturally — iterative BFS and recursive backtracking. Both are O(L · 4^L) time and produce the same output. The BFS shape lowers more cleanly here:

- **No recursion frame churn.** Backtracking pushes/pops a single buffer through L levels; BFS replaces the frontier wholesale per digit. The per-digit cost is a single `Vec[String].push` per emitted partial.
- **Output cardinality and alloc shape are explicit.** The frontier *is* the in-flight output — `next.len()` after the last digit equals the returned `Vec[String]`'s length. The allocator sees one `String.new()` + `push_str` + `push(letter)` per emitted combo, no recursion-frame overhead.
- **The auto-par bench's reduction sink fits.** `sum = sum + r.len()` is the slice-1 allow-list shape, recognized by default in `karac build`. Same shape kata [#14](../14-longest-common-prefix/) and [#15](../15-3sum/) use.

Letter groups live in a fixed `Vec[String]` of length 8, indexed by `(digit_byte - b'2')`. LeetCode restricts input to `'2'..'9'`, so the `(cast, index)` pair needs no bounds check — a malformed input would fail the problem precondition rather than the kata. The same one-pass-per-letter inner loop walks `groups[idx].chars()` and emits one fresh `String` per (prefix, letter) pair via `push_str(prefix) + push(letter)` — the post-fix amortized-O(1) idiom kata [#71](../71-simplify-path/) introduced in karac commit `7ef42b9` (2026-05-25).

## Kāra features exercised

- **`Vec[String]` cartesian growth** — same `Vec.new() + push(String)` shape kata [#14](../14-longest-common-prefix/) uses to hold a `Vec[String]` of inputs, but with the Vec growing ×3 or ×4 per outer iter rather than being fixed-size. The per-digit alloc + scope-drop of the old `out` Vec is the workload's dominant memory term — the kata-as-bug-finder result here was the `out = next` outer-buffer leak, see § Karac fixes the kata drove.
- **`String.push_str(other: String) + push(char)`** — same composite-build idiom as kata [#71](../71-simplify-path/)'s component reconstruction; both rely on the post-fix amortized-O(1) interpreter + codegen dispatch landed in karac `7ef42b9`. Surfaces the per-iter String-alloc cost in both the seq and auto-par lanes.
- **`for c in groups[idx].chars()`** on an indexed `Vec[String]` element — the inline `vec[idx].chars()` shape kata 17 was the trigger for codegen fixing (see § Karac fixes), now lowers identically to the bare-String-variable case. The walk fires 3 or 4 times per outer iteration; codegen lowers it to a `karac_string_decode_char` loop on the indexed element's `{ptr, len}`.
- **`(u8 as i64) - (u8 as i64)` digit-to-index conversion** — same `(bytes[i] as i32) - (zero as i32)` shape kata [#91](../91-decode-ways/) uses for digit-byte arithmetic. Lowers to a plain `sub` on the byte value, no overflow guard needed (input bytes are in `'2'..'9'`).
- **Scalar `+` reduction in the bench** — `sum = sum + r.len()` is the slice-1 auto-par-on-reduction allow-list shape (associative + commutative `+`, scalar accumulator), recognized by default in `karac build` and lowered to a `karac_par_reduce` dispatch. Same shape kata [#14](../14-longest-common-prefix/), [#15](../15-3sum/), and [#16](../16-3sum-closest/) use.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   letter_combinations.kara
karac build letter_combinations.kara && ./letter_combinations

# Python
python3 letter_combinations.py

# Verify they agree
diff <(./letter_combinations)              <(python3 letter_combinations.py) && echo OK
diff <(karac run letter_combinations.kara) <(python3 letter_combinations.py) && echo OK
```

## Karac fixes the kata drove

Per BENCH.md's "katas are bug-finders" discipline, the kata-17 first ship documented two karac issues; both shipped on 2026-05-29 as part of the kata-17 work and are reflected in the post-fix § Benchmarks numbers below.

1. **`for c in groups[idx].chars()` silent-zero codegen bug.** The `.chars()` peel-off in `codegen/control_flow_for.rs:92` recursed via `compile_for(…, object, body)` with the receiver as the new iterable. The recursed call's dispatcher only matched Identifier (via `string_vars`), StringLit, InterpolatedStringLit, and FieldAccess receivers; any other shape that yields a String — Index, MethodCall, Call — fell through to the silent `_ =>` arm and the body never ran. **Fix:** handle the receiver directly at the peel-off site rather than recursing into the shape-keyed dispatcher; the bare-String dispatch handles every receiver shape uniformly. Test: `test_e2e_for_in_indexed_vec_string_chars`. Karac commit landing this slice: see `kara/src/codegen/control_flow_for.rs`'s 2026-05-29 commit.

2. **`x = rhs;` outer-buffer leak for tracked Vec / String LHS with move/fresh RHS.** The eager-free in `codegen/stmts.rs`'s Assign arm only fired for `InterpolatedStringLit` RHS. Identifier-RHS to a different tracked binding (`out = next;`) and Call/MethodCall/StructLiteral RHS shapes that materialize a fresh +1 transfer all skipped the free, leaking the OLD outer `{ptr,len,cap}` buffer per iteration. Kata-17 at K=100k measured **38.5 MiB peak RSS pre-fix** (vs C/Rust's 1.3 MiB), with K=10k → 5.2 MiB and K=1k → 1.7 MiB confirming linear growth before the fix. **Fix:** extend the eager-free trigger to fire on any RHS that orphans the LHS buffer (gated against self-alias `x = x`). Outer-buffer free only; inner heap-owning elements (String/Vec) get reached via the existing per-alias scope-exit cleanup that the let-bindings register at their own sites. Post-fix RSS plateaus at 1.3 MiB across K=1k/10k/100k.

The inner-element half of the recursive drop is left to the scope-exit `FreeVecBuffer` walker, which runs at function exit when all per-alias cleanups have drained. The kata's inner loop binds `let prefix = out[i]` per iteration — this is a deliberate memory-discipline pattern, not a workaround: each per-iter `let`-binding registers a scope-exit cleanup that frees that indexed String's char buffer at end-of-iter. A version of the kata that *omits* the per-iter binding compiles correctly but leaks the per-iter inner Strings (re-measured 2026-06-06 on current karac: 15.7 MiB at K=100k vs 1.6 MiB as shipped, identical sink); this is an existing ownership limitation — move-overwrite (`out = next`) drops the replaced value's outer buffer but not its inner heap-owning elements, while scope-exit drop is deep — tracked in kara `docs/implementation_checklist/phase-7-codegen.md` § "Move-overwrite inner-element drop" (filed 2026-06-06 with isolation probes; names this kata as its natural-pull trigger: when it lands, the per-iter binding and both its comment blocks simplify away, re-bench ceremony applies).

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`letter_combinations.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** M = 8 distinct digit-strings of length 0..4 covering the full LeetCode constraint range: `""`, `"2"`, `"7"`, `"23"`, `"79"`, `"234"`, `"279"`, `"2349"` — the empty-input sentinel, single 3- and 4-letter groups, two-digit mixed shapes, and three- and four-digit cases that exercise the 4^L cardinality scaling. Per outer iter we rotate `idx = k % M` and call `letter_combinations` on that case. The output cardinality across the eight cases is `0 + 3 + 4 + 9 + 16 + 27 + 48 + 108 = 215`.

K = 100,000 outer iterations; the call is never loop-invariant (LLVM can't hoist it) and the eight distinct (digit-length, group-pattern) pairs keep any single output-cardinality assumption from holding. The sink — the running total of every returned Vec[String]'s length — is **2,687,500** = (K / M) × 215 across all five mirrors; bench.sh fails loudly on mismatch before timing starts. K dropped 10× vs kata 14/16's K=1M because per-call output cardinality scales as 4^L, not as 1 — the per-iter String alloc count averages ~27, so K=100k = 2.7 × 10⁶ String allocs is already the heaviest small-allocation workload in the 1-100 leetcode tranche.

This kata's per-iter body is **strictly heavier** than kata 14's on the alloc side — kata 14 emits one prefix String per call; kata 17 emits up to 108. That makes the seq-lane comparison directly about the allocator and the per-`push_str + push(char)` codegen, with the inner loop's compute cost a noise term against the memory-traffic dominant cost.

Two-lane kata (BENCH.md § Implicit auto-par): the `sum = sum + r.len()` accumulator is the slice-1 allow-list reduction shape, so `karac build` emits a `karac_par_reduce` dispatch by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline.

### Runtime — seq lane

Snapshot — M5 Pro, 2026-06-05, hyperfine `--warmup 5 --runs 30 --shell=none`. All four comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. Numbers below are with both karac fixes landed (see § Karac fixes the kata drove for what shipped). The 2026-05-29 snapshot read 66.3±7.0 / 68.2±7.3 / 46.2 / 45.4 — that batch's kāra/rust σ was ~3× today's on byte-identical rust/c binaries, so the ~8% downshift is the noisy old batch, not a code change.

| Implementation | Wall time |
|---|---|
| go   letter_combinations              | **44.0 ± 1.2 ms** |
| c    letter_combinations (clang -O3)  | 44.2 ± 3.0 ms |
| **kāra letter_combinations (seq)**    | **60.7 ± 2.2 ms** |
| rust letter_combinations              | 61.6 ± 2.0 ms |

**Kāra seq leads Rust by 1.01× — within σ**, a tie on this allocation-dominated workload. The 0.9 ms delta is well inside the run-to-run noise. C and Go lead Kāra/Rust by ~1.38× — the same delta to Kāra as to Rust, confirming it's the C-allocator / Go-bump-allocator + escape-analysis advantage on the small-buffer churn rather than a Kāra-specific gap. Different shape from katas 14/15/16 (sort + two-pointer, allocator-light): there the headline is the codegen-quality compare against Rust; here it's the **allocator-pressure compare against C and Go**, with Rust's bsdmalloc-on-mac+`Vec<String>` paying the same overhead as Kāra's runtime allocator.

### Runtime — auto-par regime

The `sum = sum + r.len()` reduction is auto-par-eligible; the default `karac build` recognizes it and emits a `karac_par_reduce` dispatch. NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra letter_combinations (auto-par default)** | **13.5 ± 0.8 ms** | 145.4 ms |

The auto-par binary is **4.5× faster than the kāra seq binary** (60.7 → 13.5 ms), spreading the K=100k case-rotation reduction across the perf cores (~10.8× user-CPU-to-wall ratio on M5 Pro). Still above the kata-17 first ship's 4.4× (pre-allocator-fix); the eager-free reduces per-iter alloc/free contention on the runtime allocator surface, so workers spend more time on combinatorial enumeration and less waiting for free-list locks. (The 05-29 snapshot read 12.6±0.7 / 5.3×; today's 13.5±0.8 is ~1σ adrift on a content-changed runtime archive — the June scheduler work that *improved* kata #13's reduction by 10% — and the ratio compresses further because the seq denominator moved down with the batch. Watch on the next re-bench: a confirmed +1 ms on this allocation-heavy par shape would be worth bisecting; a single ~1σ reading is not.)

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py letter_combinations` (K=10k) | 27.1 ± 0.4 ms |

Python at K=10k is 27 ms; projecting to the compiled mirrors' K=100k (~271 ms) puts it **~4.5× slower than kāra seq** and ~20× slower than the auto-par regime. Narrower than kata 14/16's Python-gap because CPython's interned-string + small-list allocators handle this workload's tight per-iter churn unusually well — the BFS `nxt.append(prefix + letter)` shape lowers to a hot interpreter path with no per-iter dict lookups.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 letter_combinations.c           | **50.5 ± 1.3 ms** |
| **karac build letter_combinations.kara**  | **83.4 ± 0.9 ms** |
| rustc -O letter_combinations.rs           | 104.2 ± 1.1 ms |

Kāra compiles **1.25× faster than `rustc -O`** and sits at **1.65× of clang -O3** — same shape as the rest of the corpus. (05-29 read 77.6 / 48.0 / 104.5 — karac and clang drifted up ~6% this batch while rustc held flat; same-compiler single-digit drift, not a toolchain change.)

### Binary size

| Implementation | Size |
|---|---|
| c    letter_combinations            | 32.9 KiB |
| **kāra letter_combinations (seq)**  | **33.1 KiB** |
| **kāra letter_combinations (auto-par)** | **295.9 KiB** |
| rust letter_combinations            | 455.4 KiB |
| go   letter_combinations            | 2434.2 KiB |

Kāra seq lands at **33.1 KiB — +152 bytes over C** — with the full `String.push_str` + `String.push(char)` + `Vec[String]` runtime surface compiled in. The auto-par row at 295.9 KiB sits right on the **documented auto-par floor (~295.7 KiB)**: the `karac_par_reduce` dispatch is what pulls the runtime archive's libstd retinue (panic infrastructure + DWARF symbolizer) past `-dead_strip`, and that floor dominates the +262.8 KiB delta over seq (see kata [#15](../15-3sum/) § Binary size for the floor's anatomy — there it's `sort_by` rather than auto-par that pulls it).

> **Correction vs the 2026-05-29 snapshot.** That snapshot read 81.5 KiB (seq) / 433.6 KiB (auto-par), and this section explained the seq excess as the String runtime surface. Wrong on both counts: the runtime archive linked that day had been rebuilt with plain `cargo build` (rlib + staticlib co-emit defeats fat-LTO DCE — the same incident corrected in katas #14/#15/#16 § Binary size), inflating the seq lane by exactly +49,616 B of DWARF symbolizer and the par lane by +140,960 B. The String machinery costs ~0.2 KiB over C, not ~48 KiB. Today's numbers are the true floor.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| rust letter_combinations            | 1.2 MiB |
| c    letter_combinations            | 1.3 MiB |
| **kāra letter_combinations (seq)**  | **1.3 MiB** |
| **kāra letter_combinations (auto-par)** | **4.0 MiB** |
| go   letter_combinations            | 9.6 MiB |

**Kāra seq is byte-identical to C at 1,327,392 B** (Rust ~48 KiB lower) — same working set, no retained pages. Sharp reversal from the kata-17 first ship measurement of 38.5 MiB seq / 40.6 MiB auto-par; the codegen `x = rhs` eager-free fix (§ Karac fixes #2) closed the outer-buffer leak that grew linearly with K. The auto-par row's 4.0 MiB is the seq baseline + per-worker scratch + workers' freshly-allocated per-iter outputs, which sit in the page cache until the reduce drains; still 2.4× lower than Go's 9.6 MiB GC-heap floor.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 letter_combinations.c          | 2.5 MiB |
| **karac build letter_combinations.kara** | **10.9 MiB** |
| rustc -O letter_combinations.rs          | 28.3 MiB |

Kāra's compile-memory footprint is ~4.3× clang's and ~2.6× lower than rustc's on this kata — same shape as kata 15/16. (+0.4 MiB vs 05-29 — within the content-independent karac compile-mem floor band tracked across the corpus.)

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio is the codegen-vs-Rust gap. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this kata the **Kāra/Rust tie at ~1.01× (within σ) is the load-bearing wall-time result** — both pay the same `Vec<String>`-of-{ptr,len,cap} cycling cost in the per-iter alloc surface, and Kāra's codegen lowers `push_str + push(char)` to the same shape Rust's stdlib `String` does. The C and Go lead is the allocator surface, not the codegen — same delta to Rust as to Kāra. The **runtime-memory result (1.3 MiB matching C/Rust) is the more durable kata-17 outcome**: it pinned down two karac codegen bugs that the previous corpus hadn't surfaced (silent-zero `.chars()` on indexed receivers; outer-buffer leak on Vec/String move-overwrite), both landed alongside this kata's first iteration.
