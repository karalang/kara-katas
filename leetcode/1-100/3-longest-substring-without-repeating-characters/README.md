# 3. Longest Substring Without Repeating Characters

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Hash Map, Sliding Window &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-substring-without-repeating-characters](https://leetcode.com/problems/longest-substring-without-repeating-characters/)

Given a string `s`, find the length of the longest substring without duplicate characters.

**Constraints:** `0 ≤ s.length ≤ 5 × 10⁴`, `s` consists of English letters, digits, symbols, and spaces.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Sliding window with last-index map | O(n) time, O(min(n, σ)) space | [`sliding_window.kara`](sliding_window.kara) ✓ via `karac run` / `karac build` | [`sliding_window.py`](sliding_window.py) ✓ |

`✓` runs end-to-end today. `σ` is the alphabet size; for ASCII input the space bound is O(min(n, 128)).

### Why one map jump is enough

A naive sliding window expands `right` by one, and when a duplicate appears, shrinks `left` one step at a time until the offender is removed — that's O(n) amortized but with a real factor-of-two penalty in practice. The last-index variant turns each contraction into a single pointer jump: when we see a character `c` whose previously-recorded index `prev` lies inside the current window (`prev >= left`), set `left = prev + 1` directly. Each character is visited *exactly once* and the running maximum of `right − left + 1` is the answer.

```
left = 0
best = 0
last_idx = {}
for right, c in enumerate(s):
    prev = last_idx.get(c)
    if prev is not None and prev >= left:
        left = prev + 1
    last_idx[c] = right
    best = max(best, right - left + 1)
return best
```

The `prev >= left` guard is the key invariant: a previous occurrence outside the current window is irrelevant — it can't make the new window invalid — so we don't shrink in that case. Without that guard, you'd shrink too aggressively on the second `a` in `"abba"` and return 2 instead of the correct 3 (`"bba"`).

## Kāra features exercised

- **`ref String` parameter + `for c in s.chars()`** — read-only string borrow, iterated per Unicode scalar value. Codegen lowers chars iteration to an inline byte-offset loop with a runtime UTF-8 decode helper (`karac_string_decode_char`); see [`phase-7-codegen.md`](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md) for the slice that landed this.
- **`Map[char, i64]`** — `char` as a hash key works through the typechecker (`type_supports_hash` / `type_supports_eq` both list `Type::Char`) and the type-erased runtime Map. The whole algorithm is a single Map.
- **`match Option[i64]` on `Map.get()`** — the canonical idiom for "lookup and act on present/absent." `Some(prev)` binds the previous index; `None => {}` is the no-op arm.
- **Mutable local accumulators** — `let mut left`, `let mut best`, `let mut right` updated by guarded `if` / `match`.

No `Vec`, no slices, no shared structs.

## API shape

Each Kāra solution exposes a pure `length_of_longest_substring(s: ref String) -> i64` and a thin `report` that prints. `main` calls `report` per test case. The Python file mirrors this with `length_of_longest_substring(s: str) -> int` and the same `report` / `main` shape.

The case-driver in `main` binds each literal to a local before calling `report`:

```rust
let c1 = "abcabcbb"; report(c1);
```

rather than `report("abcabcbb")` inline. This is a workaround for a pre-existing codegen gap: karac's call-site `ref T` coercion at [`src/codegen.rs:16710`](../../../../karac-rust/src/codegen.rs#L16710) only fires for `Identifier` arguments — string literals as rvalues trip the calling-convention verifier ("Call parameter type does not match function signature"). Tracked as a follow-up in [`phase-7-codegen.md`](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md); shape of the fix is to alloca the rvalue and pass the pointer.

## Output format

One integer per line — the answer for each test case. Kāra and Python output is line-for-line identical so the files can be diffed directly.

```
3
1
3
0
1
2
3
5
```

## Running

```bash
# Kāra (compiled or interpreted — both work)
karac run   sliding_window.kara
karac build sliding_window.kara && ./sliding_window

# Python
python3 sliding_window.py
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O` and the Kāra file with `karac build` (both cached in `bench/target/`, gitignored), then runs three passes:

1. **Runtime** — `hyperfine --warmup 3 --runs 10` across the three binaries. Input is the 26-character lowercase alphabet repeated 4000 times (104_000 chars total). `K = 20` outer iterations; each call answers `26` (the longest non-repeating run is exactly one full alphabet cycle).
2. **Compile (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` invocation.
3. **Binary size** — bytes / KiB of the produced artifact.

| File | What it does |
|---|---|
| [`bench/sliding_window.kara`](bench/sliding_window.kara) | 26-char alphabet × 4000 = 104K chars, K=20 outer iterations, `Map[char, i64]` last-index map |
| [`bench/sliding_window.py`](bench/sliding_window.py) | Algorithmic mirror — same input, same K, `dict[str, int]` |
| [`bench/sliding_window.rs`](bench/sliding_window.rs) | Algorithmic mirror; `HashMap<char, i64>`; compiled with `rustc -O` |

All three print the same sum-of-results sink (`K × 26 = 520`) so the algorithm's output participates in I/O and can't be elided.

### Runtime — and what the gap measures

Snapshot — M1, 2026-05-15, hyperfine `--warmup 3 --runs 10 --shell=none`, native binaries via `karac build` and `rustc -O`:

| Run | Mean ± σ |
|---|---|
| `kara sliding_window` (codegen) | 1620 ± 23 ms |
| `py sliding_window` | 112.1 ± 1.4 ms |
| `rust sliding_window` | 16.5 ± 0.1 ms |

This kata is **98× of Rust** — the largest codegen-vs-Rust gap in the kata suite, and **larger than Python's gap** (Python is 6.8× of Rust here). That gap is real and worth understanding.

**Where the time goes.** The body of `length_of_longest_substring` is ~2M Map operations: 104K chars × 20 outer iterations × (one `Map.get`, one `Map.insert`) per char. Everything else — the UTF-8 char decode, the `if prev >= left` jump, the `right - left + 1` arithmetic — is negligible by comparison.

**Why Kāra's Map is slow today.** `runtime/src/map.rs` is a type-erased C runtime — `Map[K, V]` operations dispatch through function pointers (a generic `hash_fn` / `eq_fn` indirection per element) and store keys and values as raw byte blobs (no specialization on `i64` vs `String` element width). Rust's `HashMap<char, i64>` is fully monomorphized at the call site: direct `char.hash()` calls, inlined comparisons, packed key/value cells.

The indirection microbench (`karac-rust/bench/indirection_cost/`, 2026-05-06) measured this on an i64-keyed map and attributed ~75% of the gap to erasure tax — that's for `Map[i64, i64]`. For `Map[char, i64]` the gap should be similar in nature; the absolute Kāra/Rust ratio is bigger here because the workload is map-dominated (vs. coin_change / brute_force where indexed array reads dilute the contribution).

**The fix that closes this gap.** Phase 4 monomorphized collections — tracked at [`phase-7-codegen.md:362`](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md) (entry "Monomorphized collections — runtime restructure", P1 post-v1, P0 design-property). The existing codegen infrastructure already monomorphizes user generic functions (`generic_fns`, `generated_monos`, `mangle_mono_name`, `type_subst`); the same machinery extends to `Map[K, V]` / `Set[T]` / `Vec[T]` when the runtime is restructured as compile-per-crate source rather than a type-erased C archive. Estimated ratio after monomorphization: ~1.07× of `std::HashMap` based on the indirection microbench data. **This kata is the natural-pull validation workload — re-run after monomorphization lands and the bench number is the headline.**

**Why Python is faster than Kāra here.** CPython's `dict` is C-implemented and heavily tuned for string-like keys; the per-op overhead beats Kāra's runtime-dispatched Map by a wide margin on small-element-width keys. This isn't a Python-vs-Kāra story; it's a "tuned C dict beats type-erased C map" story. It flips once monomorphization lands — Kāra codegen will then beat CPython on this workload by the usual compiled-vs-interpreted multiple (~30× per the [`121` bench](../121-best-time-to-buy-and-sell-stock/README.md#codegen-vs-python)).

### Compile time and binary size

Snapshot — M1, 2026-05-15, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build sliding_window.kara` | 59.9 ± 0.6 ms | 296.2 KiB |
| `rustc -O sliding_window.rs` | 119.4 ± 0.5 ms | 457.1 KiB |

Kāra compiles this kata **1.99× faster** than `rustc -O` and produces a binary **~35% smaller**. Consistent with the other katas — the cross-archive LTO + DCE work landed 2026-05-12 keeps the runtime contribution to binary size tight when downstream features (HTTP, JSON, tokio subgraph) aren't reached.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `kara sliding_window` (codegen) | 1.8 MiB |
| `rust sliding_window` | 1.3 MiB |
| `py sliding_window` | 7.0 MiB |

The 104K-char String is ~104 KB; the Map holds at most 26 entries; neither dominates allocation. Kāra's ~0.5 MiB headroom over Rust is the type-erased Map's per-call buffer churn (the Map structure reuses a transient growth buffer that sits at peak between iterations); closes when monomorphized collections land — the same one-allocator-per-instantiation that Rust does.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. Python is the ergonomic foil. The "98× of Rust" gap here is the most concrete measurement in the suite of the type-erasure tax — and the most concrete justification for prioritizing monomorphized collections.
