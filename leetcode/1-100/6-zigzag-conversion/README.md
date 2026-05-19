# 6. Zigzag Conversion

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/zigzag-conversion](https://leetcode.com/problems/zigzag-conversion/)

Given a string `s` and an integer `numRows`, write `s` in a zigzag pattern across `numRows` lines and return the string read row-by-row.

```
P   A   H   N
A P L S I I G       "PAYPALISHIRING", numRows = 3   →   "PAHNAPLSIIGYIR"
Y   I   R
```

**Constraints:** `1 ≤ s.length ≤ 1000`, `s` is ASCII (English letters, `','`, `'.'`), `1 ≤ numRows ≤ 1000`. (The kata also exercises `s.length == 0` because the algorithm is well-defined there.)

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Row buffers (visit-by-row) | O(n) time, O(n) space | [`row_buffers.kara`](row_buffers.kara) ✓ via `karac run` / `karac build` | [`row_buffers.py`](row_buffers.py) ✓ |

`✓` runs end-to-end today. Both interpreter and codegen render `println(c)` for a `char` as the UTF-8 glyph; Python mirrors with `print(c)`. The char-printing parity here landed in karac [`61b1bf3`](../../../../karac-rust/) (`render char as glyph in println / f-string, fix CharLit zero`); pre-fix the kata had to round-trip through integer codepoints to stay diff-clean.

### Why row buffers

Two textbook approaches exist:

1. **Row buffers (this kata).** Walk the input left-to-right, tracking a `cur` row index that bounces between `0` and `numRows - 1`. Each character is appended to its row's `Vec[char]`. After the walk, concatenating the rows row-major yields the answer. O(n) time, O(n) extra space.
2. **Direct math/stride.** For each row `r`, characters in that row sit at positions `r, r + 2(numRows−1), r + 2(numRows−1) − 2r, r + 2(numRows−1), ...` — a two-stride alternating pattern. O(n) time, O(1) extra space (you can write the result directly).

The math/stride form is *constant-factor* better on memory but requires reasoning about two interleaved arithmetic progressions per row, including the special-case handling for the top and bottom rows (which have only one stride, not two). Row buffers express the same algorithm as a one-pass walk with a single direction flag, which is easier to read, easier to test, and matches LeetCode's canonical "Approach 1" almost line for line. For the problem's `n ≤ 1000` constraint, the O(n) extra space is negligible.

### Why flip direction *before* the step

```
if cur == 0 or cur == num_rows - 1 {
    going_down = not going_down;
}
if going_down {
    cur = cur + 1;
} else {
    cur = cur - 1;
}
```

Flipping before stepping makes the seed state `(cur = 0, going_down = false)` work: on the first iteration we hit `cur == 0`, flip `going_down` to `true`, and step down to row 1. The alternative ("seed `going_down = true`, flip after the step") leaves a subtle off-by-one on the very first step when `numRows == 2` (the only case where the bottom rail is also row 1). With the pre-flip ordering the same loop body works for every `numRows ≥ 2` without a special case.

### Edge cases collapsed by the guard

```
if num_rows <= 1 or num_rows >= n {
    // return s unchanged
}
```

- `num_rows == 1` — no zigzag shape; the answer is `s`. The main loop would also handle it (every char goes to row 0), but the row-flip logic divides by `num_rows - 1 == 0` conceptually if you ever read it as a period. Bailing early is clearer.
- `num_rows >= n` — every char gets its own row, so reading by row returns the input. The main loop also handles this correctly, but exits with `num_rows − n` empty rows, which we'd just skip in the flatten. Bailing early avoids the allocation of the empty buffers.

Both cases are exercised in the test driver (`"A", 1`, `"AB", 1`, `"ABCDEFG", 100`).

## Kāra features exercised

- **`Vec[Vec[char]]`** — per-row character buffers built explicitly with `Vec.new()` + `push` rather than a vec literal. The literal form would need to clone an empty inner Vec for each row, which hits the same coercion gap as kata [#5]'s `chars().collect()`. The explicit form lowers to a straightforward `karac_vec_with_capacity` + per-element write loop.
- **`ref String` parameter + `for c in s.chars()`** — read-only string borrow, iterated per Unicode scalar value. Same backbone as katas [#3](../3-longest-substring-without-repeating-characters/) and [#5](../5-longest-palindromic-substring/) — codegen lowers `chars()` to an inline byte-offset loop with a runtime UTF-8 decode helper (`karac_string_decode_char`).
- **Snapshot pattern** — `for c in s.chars() { chars.push(c); }` snapshots into a `Vec[char]` so we can ask for `len()` once and index in O(1). The iterator returned by `s.chars()` doesn't expose a `len()` and re-iterating `ref String` is cheap but wouldn't help for the indexed reads later. Same pattern as kata [#5].
- **`if cond or cond` short-circuit** — used in the early-return guard (`num_rows <= 1 or num_rows >= n`) and the rail check (`cur == 0 or cur == num_rows - 1`). Lowered to `select` over both branches with a short-circuit branch when the LHS is true.
- **Mutable boolean accumulator (`let mut going_down`)** — flipped with `not going_down` at each rail. Same shape as the mutable counters in kata [#5]'s expand loops, just on `bool`.
- **`Vec[char]` indexed read + push** — both the per-row buffer fills (`rows[cur].push(chars[i])`) and the flatten loop (`out.push(rows[r2][k])`). Bounds checks fire on each indexed read; the codegen-vs-Rust ratio for this shape is the kata-[#5] data point (1.21× of Rust on a tight indexed loop) — see [#5 § Runtime](../5-longest-palindromic-substring/README.md#runtime--close-to-native) for the gap breakdown.
- **`println(c)` glyph print** — direct char printing renders the UTF-8 glyph. Same shape as the Python `print(c)` mirror. The char-display arm in `compile_print` routes the i32 codepoint through `karac_string_encode_char` and prints the 1–4 byte UTF-8 sequence — see the karac commit message at [`61b1bf3`](../../../../karac-rust/) for the codegen-side detection and dispatch.

No `Map`, no `Set`, no shared structs.

## API shape

Each Kāra solution exposes `convert(s: ref String, num_rows: i64) -> Vec[char]` returning the zigzag-rewritten chars in row-major order, plus a thin `report` that prints. `main` calls `report` per test case. The Python file mirrors this with `convert(s, num_rows) -> list[str]` and the same `report` / `main` shape.

The case-driver in `main` binds each literal to a local before calling `report`:

```rust
let c1 = "PAYPALISHIRING"; report(c1, 3);
```

rather than `report("PAYPALISHIRING", 3)` inline — same `ref T` rvalue-coercion sugar gap as katas [#3](../3-longest-substring-without-repeating-characters/#api-shape) and [#5](../5-longest-palindromic-substring/#api-shape).

## Output format

**One glyph per line, then `---` as a case separator.** The result of zigzag conversion is a string; we print it one char per line rather than as a single line for two reasons:

1. **Empty-input visibility** — case 5 (`""`, `numRows = 3`) has an empty result. A whole-string print would emit a single blank line that visually merges with surrounding output; the separator-after-each-case shape makes the empty case unambiguously `---` alone.
2. **No `String.push(char)` dependency** — building the zigzag result as a single `String` would need to push individual chars into a `String`, which currently has no method on the codegen side. `Vec[char]` + per-element `println(c)` works today and matches the Python side directly.

The `---` separator is an arbitrary sentinel that doesn't collide with the LeetCode constraint set (English letters, `','`, `'.'`); it could also be a blank line, but `---` is more obvious when scanning long output.

```
P                 ← case 1: "PAYPALISHIRING", 3  →  PAHNAPLSIIGYIR
A
H
…
R
---
P                 ← case 2: "PAYPALISHIRING", 4  →  PINALSIGYAHRPI
…
---
A                 ← case 3: "A", 1
---
A                 ← case 4: "AB", 1
B
---
---               ← case 5: ""     (empty result, separator alone)
…
```

The Kāra binary (codegen or interpreter) and the Python reference produce identical output (64 lines total across the nine test cases) so `diff ./row_buffers <(python3 row_buffers.py)` is silent.

## Running

```bash
# Kāra — codegen and interpreter both print glyphs since karac 61b1bf3.
karac run   row_buffers.kara
karac build row_buffers.kara && ./row_buffers

# Python
python3 row_buffers.py

# Verify they agree
diff <(./row_buffers) <(python3 row_buffers.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 3 --runs 10` across the three binaries. Inputs: N = 10,000 ASCII chars from a repeating `"PAYPALISHIRING"` pattern; `num_rows = 4`; K = 10,000 outer iterations; per-iter rotation `off = k % R` with R = 1,000 to defeat the cross-iteration CSE that would otherwise hoist the pure `convert_off` call out of the loop and reduce the bench to `multiply by K`.
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size + runtime memory + compile memory** — straight `wc` / `time -l` reads.

| File | What it does |
|---|---|
| [`bench/row_buffers.kara`](bench/row_buffers.kara) | N = 10,000, num_rows = 4, R = 1,000, K = 10,000, rotated 14-char ASCII pattern |
| [`bench/row_buffers.py`](bench/row_buffers.py) | Algorithmic mirror — same N, num_rows, R, K, same offset+length API |
| [`bench/row_buffers.rs`](bench/row_buffers.rs) | Algorithmic mirror; compiled with `rustc -O` |

All three print the same sum-of-(first + last codepoint) sink (`1_514_240` at the default parameters) so the algorithm's output participates in I/O and can't be elided.

### Runtime — parity with Rust (within run-to-run variance)

Snapshot — M5 Pro, 2026-05-19, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`. Requires karac at commit [`2370935`](../../../../karac-rust/) (per-target CPU baseline) or later, on top of [`9d9c3ce`](../../../../karac-rust/) (`Vec.extend_from_slice`), [`c8fd7c4`](../../../../karac-rust/) (`Vec.with_capacity`), and [`60ad643`](../../../../karac-rust/) (auto-par cost-model gate).

| Run | Mean ± σ |
|---|---|
| `kara row_buffers` (codegen) | 99.9 ± 0.4 ms |
| `py   row_buffers` | 3201 ± 23 ms |
| `rust row_buffers` | 98.9 ± 1.0 ms |

This kata is **at parity with Rust** within run-to-run variance. Three readings across two days on the same rust binary (unchanged across all three) and current kara binary landed at: **kara 1.03× faster** (2026-05-18 morning, kara 101.9 / rust 104.8 ms), **rust 1.03× faster** (2026-05-18, hot system after batched benches, kara 97.9 / rust 95.1 ms), and **rust 1.01× faster** (2026-05-19 clean, the snapshot above). The directional ratio bounces between samples; the honest claim is parity. Within-batch σ (≤1.0 ms) is tight, but thermal/scheduler effects on a ~100 ms workload accumulate across runs more than within-batch σ implies.

The trajectory from initial measurement to parity lands in three steps, in order of magnitude:

1. **Cost-model fix** ([`60ad643`](../../../../karac-rust/), 2026-05-17) — the analyzer was firing a spurious par-dispatch on the constant-init `let r2 = 0i64` paired with the outer `while` loop, turning a tight sequential algorithm into a per-iter dispatch that paid scheduling overhead without delivering parallelism. The gate now skips par-dispatch when N−1 stmts in the group are constant-init. **361.9 → 143.9 ms.**
2. **Vec drop / allocator pathway fix** — the same drop pathway that closed kata [#88](../88-merge-sorted-array/#runtime-memory-peak)'s 16 MiB headroom and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak)'s 16 MiB headroom also tightened this kata's σ from ±22 ms to ±1 ms.
3. **`Vec.with_capacity` + `Vec.extend_from_slice` stdlib additions** ([`c8fd7c4`](../../../../karac-rust/) + [`9d9c3ce`](../../../../karac-rust/), 2026-05-18) — let the kata source mirror its rust source line-for-line: `let mut out: Vec[char] = Vec.with_capacity(len);` instead of `Vec.new()`, and `out.extend_from_slice(rows[r2])` instead of a per-char `while k < row_len { out.push(rows[r2][k]); }` loop. **143.9 → 101.9 ms.**

Total: **361.9 → ~100 ms (~3.6× speedup)**, ending at rough parity with Rust. See § How we got here below.

### How we got here

The first measurement on this bench (2026-05-17) read **3.6× of Rust** at 360.2 ± 3.8 ms vs 100.3 ± 0.5 ms. After the cost-model fix landed, the kara number dropped to **1.43× of Rust** at 143.9 ± 1.0 ms — a 2.5× speedup that closed the auto-par scheduling overhead but left a real residual gap.

Empirical investigation of that 1.43× residual:

1. **`sample row_buffers_kara 1`** — time concentrated in `main` (karac inlines `convert_off` via the internal-linkage fix), with hot stacks at `_platform_memmove` and `_xzm_free`. Signature points at reallocation + free churn, not algorithm time.
2. **Source diff vs `row_buffers.rs`** — two idiom asymmetries surfaced:
   - **Output buffer growth.** Rust used `Vec::with_capacity(len)` for `out` — zero reallocations. Kara used `Vec.new()` then `out.push(...)` len times — log₂(len) ≈ 14 reallocations per outer iter, ~140K across the full bench.
   - **Flatten step.** Rust used `out.extend_from_slice(row)` per row — 4 memcpys per outer iter. Kara used an inner `while k < row_len { out.push(rows[r2][k]); k = k + 1; }` — 10K per-char pushes per outer iter, ~10⁸ total push calls across the run.
3. **Stdlib surface audit** — neither `Vec.with_capacity` nor `Vec.extend_from_slice` existed in kara's stdlib (verified against the dispatch tables in `src/codegen/vec_method.rs` and `src/interpreter/method_call_seq.rs`). The kata source was forced into the slower idiom because the fast idiom wasn't available, not because karac's codegen was emitting slow code.

Two experimental variants quantified the gap before the stdlib work shipped:

| Variant | Mean ± σ | vs Rust |
|---|---|---|
| `kara orig` (`Vec.new` + push everywhere) | 142.5 ± 1.0 ms | 1.43× |
| `kara fast` (`Vec.filled` + indexed write — `out` only) | 109.0 ± 0.4 ms | 1.10× |
| `kara faster` (`Vec.filled` + indexed write — `out` AND rows, flat layout) | 99.2 ± 0.9 ms | 1.00× (parity) |
| `rust` | 99.6 ± 0.8 ms | 1.0× |

The `_fast` variant (only `out` pre-allocated) closed 76% of the gap with one source change. The `_faster` variant (both `out` and rows pre-allocated via a flat single-buffer workaround for the karac limitation that `rows[cur][end] = X` nested indexed-assign errors with "Index assignment target must be a variable") reached exact parity with Rust. Both demonstrated that the gap was 100% allocator pressure, not codegen quality.

The stdlib additions ([`c8fd7c4`](../../../../karac-rust/) for `Vec.with_capacity`, [`9d9c3ce`](../../../../karac-rust/) for `Vec.extend_from_slice`) let the kata source switch to the natural push-based form that mirrors rust line-for-line. The resulting binary lands **at parity with Rust** — the 2026-05-18 capture read 1.03× ahead (101.9 vs 104.8 ms, within noise) and a 2026-05-19 clean re-bench read 1.01× behind (99.9 vs 98.9 ms, also within noise). Both readings agree the gap is below the run-to-run variance floor; the kata reaches rust on the metric, neither systematically ahead nor behind.

The lesson worth keeping: **investigate before assuming codegen quality**. The 1.43× gap looked like a hard codegen ceiling but was a stdlib surface gap; two methods totaling ~880 lines of karac changes (incl. 18 tests across interpreter + codegen + ASAN) turned a 43% deficit into parity.

### Runtime memory — parity with Rust

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara row_buffers` (codegen) | 1.7 MiB |
| `py   row_buffers` | 8.0 MiB |
| `rust row_buffers` | 1.6 MiB |

Kāra peak RSS is **at parity with Rust** (1.7 vs 1.6 MiB, ~1× — within steady-state expectations of the 11K-char `chars` buffer + one iter's working set). Karac beats Python by a ~4.7× margin because Python's interpreter base RSS is heavier than the kata's allocator pressure. The May-17 snapshot read 2.3 MiB for kara; the drop to 1.7 MiB came from the same drop-pathway fix that closed kata [#88](../88-merge-sorted-array/#runtime-memory-peak) and kata [#121](../121-best-time-to-buy-and-sell-stock/#runtime-memory-peak).

The first revision of this bench measured **474 MiB** peak RSS (316× Rust). The arithmetic at that revision was 474 MiB / 10K iter = 47 KiB / iter, which lined up with one iter's full allocation pool (4 inner `Vec[char]` + 1 outer `Vec[Vec[char]]` + 1 output `Vec[char]`). The leak rooted in two places in karac's auto-par codegen — see commit [`daaf2cc`](../../../../karac-rust/) (`codegen: close per-iter Vec/String leak on auto-par branch + slot paths`) for the full diagnosis: (1) `emit_par_branch_fn` was running branch-body compile against an empty `scope_cleanup_actions` stack, so `track_vec_var` silently no-op'd for every let inside the branch; (2) the parent-function's slot-load alloca wasn't `track_vec_var`-registered (a prior pass had disabled it to avoid a `Holder { items: a }`-followed-by-`return` double-free in a shape no test exercises). The fix re-enabled both, with a cap-zero suppression on slot-source allocas to avoid double-freeing the heap data the slot-write loop has already moved.

A follow-up fix ([`3c77a10`](../../../../karac-rust/), `codegen: suppress RC dec for par-branch return-slot sources`) extended that suppression to RC-bearing types (shared structs / `Option[shared T]`), which had hit a separate hang on kata [#2](../2-add-two-numbers/) before this kata exposed it.

Three new ASAN regression tests in `tests/memory_sanitizer.rs` (`asan_auto_par_*`) cover the function-local Vec, Vec[Vec[char]], and Vec[char]-return shapes — all built from this bench's minimal repro.

### Codegen vs Python

Same snapshot:

| Run | Mean ± σ | Gap vs Rust |
|---|---|---|
| `kara row_buffers` (codegen) | 99.9 ± 0.4 ms | **1.01× (parity within σ)** |
| `rust row_buffers` | 98.9 ± 1.0 ms | 1.0× |
| `py   row_buffers` | 3201 ± 23 ms | **32×** |

Python is **~32× slower than Kāra codegen**. CPython's per-iter overhead (function-call + `list.append` + per-char bytecode dispatch) dominates, even though Python's underlying `list` is C-implemented. The kara-vs-python ratio widened from the May-17 snapshot's ~9× as the cost-model fix and the stdlib additions landed; the python side is essentially unchanged.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-18, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build row_buffers.kara` | 67.1 ± 1.5 ms | 33.0 KiB |
| `rustc -O row_buffers.rs` | 110.3 ± 1.8 ms | 455.8 KiB |

Kāra compiles this kata **1.64× faster** than `rustc -O` and produces a binary **~93% smaller** (14× the size disparity, vs the ~35% disparity measured against the same source on 2026-05-17). The much smaller binary tracks the cross-archive LTO + DCE work landed 2026-05-12. Consistent with kata [#4](../4-median-of-two-sorted-arrays/#compile-time-and-binary-size), [#88](../88-merge-sorted-array/#compile-time-and-binary-size), and [#121](../121-best-time-to-buy-and-sell-stock/#compile-time-and-binary-size).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. The current result — **parity with Rust, within run-to-run variance** — caps a ~3.6× speedup from the initial 360 ms / 3.6× of-Rust measurement, achieved via three karac changes (auto-par cost-model gate, Vec drop pathway fix, `Vec.with_capacity` + `Vec.extend_from_slice` stdlib additions). The directional ratio bounces between samples (kara 1.03× faster, rust 1.03× faster, rust 1.01× faster across three readings); the load-bearing claim is parity. See § How we got here.
