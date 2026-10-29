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

The naive sliding window shrinks `left` one step at a time on a duplicate — O(n) amortized but with a real factor-of-two penalty. The last-index variant turns each contraction into a single pointer jump: when character `c`'s previously-recorded index `prev` lies inside the current window (`prev >= left`), set `left = prev + 1` directly.

The `prev >= left` guard is the key invariant: a previous occurrence outside the current window is irrelevant and must not shrink the window. Without that guard, the second `a` in `"abba"` shrinks too aggressively and returns 2 instead of 3 (`"bba"`).

## Kāra features exercised

- **`ref String` + `s.chars()`** — read-only string borrow, iterated per Unicode scalar value via an inline byte-offset loop with a runtime UTF-8 decode helper.
- **`Map[char, i64]`** — `char` works as a hash key through the typechecker and the (now monomorphized) runtime Map; the whole algorithm is one Map.
- **`match Option[i64]` on `Map.get()`** — canonical "lookup and act on present/absent" idiom; `None => {}` is the no-op arm.
- **Mutable local accumulators** — `let mut left`, `let mut best`, `let mut right` updated by guarded `if` / `match`.

No `Vec`, no slices, no shared structs.

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
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Kāra file with `karac build`, and the Go module with `go build` (all cached in `bench/target/`, gitignored), then runs five passes per the [BENCH.md protocol](../../../BENCH.md):

1. **Sink agreement** — every compiled mirror's stdout must equal `520` (Python opt-in via `KARA_BENCH_INCLUDE_PY=1`).
2. **Runtime (short, compiled)** — `hyperfine --warmup 5 --runs 30 --shell=none` across kara/rust/c/go. Input is the 26-character lowercase alphabet repeated 4000 times (104_000 chars total). `K = 20` outer iterations; each call answers `26` (the longest non-repeating run is exactly one full alphabet cycle).
3. **Runtime (long, py)** — `hyperfine --warmup 2 --runs 10` for the Python mirror in its own batch.
4. **Compile elapsed (cold)** — `hyperfine` with a `--prepare` step that deletes the artifact before every run, so each measurement is a fresh `karac build` / `rustc -O` / `clang -O3` invocation. Go is excluded per BENCH.md — `go build`'s first run mixes module + std-lib link.
5. **Binary size, runtime memory, compile memory** — one row per comparator.

| File | What it does |
|---|---|
| [`bench/sliding_window.kara`](bench/sliding_window.kara) | 26-char alphabet × 4000 = 104K chars, K=20 outer iterations, `Map[char, i64]` last-index map |
| [`bench/sliding_window.rs`](bench/sliding_window.rs) | Algorithmic mirror; `HashMap<char, i64>`; compiled with `rustc -O` |
| [`bench/sliding_window.c`](bench/sliding_window.c) | Algorithmic mirror; heap-allocated open-addressing linear-probe hashmap keyed by `int32_t` codepoint (starts at capacity 16, doubles at 3/4 load); compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror; `map[rune]int64`; built with `go build` |
| [`bench/sliding_window.py`](bench/sliding_window.py) | Algorithmic mirror — same input, same K, `dict[str, int]` |

All five print the same sum-of-results sink (`K × 26 = 520`) so the algorithm's output participates in I/O and can't be elided.

This is a **seq-only kata**: the inner walk is data-dependent on `left` / `last_idx` across `right → right+1`, so it can't be parallelized; the outer `K=20` loop is too small to amortize dispatch. Per the [BENCH.md two-lane protocol](../../../BENCH.md#par-lane--when-the-workload-admits-parallelism), no par lane is shipped.

### Runtime

Snapshot — Apple M5 Pro (6P+12E), measured 2026-10-29 (UTC), `karac 0.1.0-dev.13686+g04628b0eb` (the v2/MIR backend, which replaced the legacy backend), rustc 1.95.0, Apple clang 21.0.0, go 1.26.3. hyperfine `--warmup 5 --runs 30 --shell=none`, native binaries via `karac build` (`KARAC_AUTO_PAR=0`, an honest seq build), `rustc -O`, `clang -O3`, and `go build`. Source of truth: [`bench/results.json`](bench/results.json). Python was not part of this run (opt-in via `KARA_BENCH_INCLUDE_PY=1`), so it has no row.

| Run | Mean ± σ |
|---|---|
| `c    sliding_window` (clang -O3) | **2.4 ± 0.1 ms** |
| **`kara sliding_window` (codegen)** | **13.8 ± 1.3 ms** |
| `rust sliding_window` (rustc -O)  | 16.4 ± 0.5 ms |
| `rust sliding_window` (rustc -O `-C overflow-checks=on`) | 16.7 ± 0.1 ms |
| `go   sliding_window` (go build)  | 20.4 ± 1.3 ms |

**Kāra now beats Rust, equal-safety Rust and Go on this kata.** Kāra runs at **0.84× of `rustc -O`'s time** (1.19× faster), **1.21× faster than equal-safety Rust** (`-C overflow-checks=on`, which is what Kāra actually does — it checks integer overflow by default where `rustc -O` silently wraps), and **1.48× faster than Go**. C runs **5.6× faster than Kāra**.

#### Re-bench 2026-10-29 — what moved

Compared against the previous recording (karac `0.1.0-dev.8508+gc9032a670`, 2026-09-08), same host, same kata source:

- **Kāra runtime: 31.9 → 13.8 ms (−57%). A real improvement.** It is attributable to the Map-path fixes on the compiler since the 2026-09-08 recording — the Map probe now runs in-line at the call site, and the `get`-then-`insert` pair on one key hashes once instead of twice. The hash itself is unchanged (still SipHash-1-3); the old reading of "Kāra 1.79× slower than equal-safety Rust" is retired.
- **Comparators: host drift only.** C 3.0 → 2.4 ms (−19%), Rust 17.2 → 16.4 ms (−5%), equal-safety Rust 17.8 → 16.7 ms (−7%), Go 21.7 → 20.4 ms (−6%). Their binaries are byte-identical in size to the previous recording; none of them moved anywhere near Kāra's −57%, so the sign flip against Rust and Go is Kāra's own.
- **Kāra binary: +50 KB** (296.1 → 345.5 KiB), the new backend's runtime/codegen footprint; still ~24% smaller than Rust's.
- **Kāra compile time: flat** (147 → 155 ms).
- **Kāra compile memory: 30 → 67 MiB — a regression**, tracked in the kara bug ledger as `B-2026-10-28-37`. It takes Kāra from below rustc's cold-compile footprint to 1.77× above it.

**Where the time goes.** The body of `length_of_longest_substring` walks 104K chars × 20 outer iterations ≈ 2.08M chars, each doing one `Map.get` and one `Map.insert` on a table of at most 26 entries. At 13.8 ms that is ~6.6 ns per char (both Map operations), against ~15.3 ns on 2026-09-08. The table still fits in L1 and the hash is the same; what shrank is the work around it — no out-of-line probe call, and one hash per char instead of two.

**History of this kata's headline.** Earlier versions of this file led with "Kāra is ~2.3× faster than Rust here." That lead was largely a hasher asymmetry: Kāra's Map used FxHash under a compile-time-constant seed while Rust paid for SipHash-1-3. karac `59c8d30cd` (2026-08-22) closed that hash-flooding hole by moving Kāra to per-process-seeded SipHash-1-3, and on 2026-09-08 the kata read 1.79× *slower* than equal-safety Rust (kara `B-2026-09-07-42`, `B-2026-09-07-53`). The current lead is therefore at hash parity — both sides run SipHash-1-3 — which makes it a codegen result rather than a hasher one. Further back, the pre-monomorphization snapshot (2026-05-15, M1) read Kāra 98× *slower* than Rust; monomorphized `Map[char, i64]` (phase-7 line 362, slices 1+2, `537e5d2` through `48e4963`) plus the codegen cleanup that followed (`daaf2cc`, `9d878ae` / `8b13048` / `d329023`, `919cfe0`) closed that gap.

**Where C wins.** The C mirror is no longer a presized static table: `f73df9b` replaced it with a heap-allocated map that starts at capacity 16, doubles with a full rehash at the same 3/4 load factor Kāra's `Map` uses, and hashes with FxHash under the compiler's old seed. It allocates, grows and rehashes on the same policy as Kāra's `Map`, so the comparison is apples-to-apples on structure. What C does *not* pay is SipHash-1-3 — its hash is a multiply, Kāra's is ~92 instructions on an 8-byte key — and that, rather than a representation mismatch, is the bulk of the 5.6× gap. It is a real gap on a tiny-table hash workload, but it is a DoS-resistance cost Kāra has chosen to pay, the same one Rust and Go pay.

### Compile time and binary size

Snapshot — Apple M5 Pro, 2026-10-29, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `clang -O3 sliding_window.c`      | 50.9 ± 2.8 ms | 32.8 KiB |
| **`karac build sliding_window.kara`** | **154.7 ± 3.6 ms** | **345.5 KiB** |
| `rustc -O sliding_window.rs`      | 120.6 ± 1.5 ms | 457.1 KiB |
| `go build` (Go module)            | — (excluded; mixes module + std-lib link) | 2434.4 KiB |

Kāra compiles this kata **1.28× slower** than `rustc -O` and produces a binary **~24% smaller than Rust**. `clang -O3` compiles 3.0× faster than Kāra — C carries no stdlib runtime to link, just libc; Kāra's binary carries the karac runtime support functions (Map mono, String UTF-8 walker, panic infrastructure) that stay linked even when LTO trims hard.

### Runtime memory (peak)

| Run | Peak RSS |
|---|---|
| `c    sliding_window` | 1.2 MiB |
| `rust sliding_window` | 1.2 MiB |
| **`kara sliding_window` (codegen)** | **1.4 MiB** |
| `go   sliding_window` | 2.7 MiB |

The 104K-char String is ~104 KB; the Map holds at most 26 entries; neither dominates allocation. Kāra sits ~0.1 MiB above both Rust and C — the per-`{K, V}` monomorphized Map allocates in the same shape as Rust's `HashMap<char, i64>`. Go's 2.7 MiB reflects its statically-linked runtime + GC scheduler footprint (visible in the 2.4 MiB binary too).

### Compile memory (cold)

| Compiler | Peak RSS |
|---|---|
| `clang -O3 sliding_window.c`      | 2.6 MiB |
| **`karac build sliding_window.kara`** | **67.1 MiB** |
| `rustc -O sliding_window.rs`      | 37.9 MiB |

Kāra's cold-compile footprint is **1.77× larger than rustc** and 26× larger than clang. This is a regression: on 2026-09-08 it was 30.1 MiB, below rustc. The jump came with the current compiler and is tracked as kara `B-2026-10-28-37`; until it is fixed, this table should not be read as Kāra's settled compile-memory cost.

### Why Rust / C / Go / Python are in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness) and the [BENCH.md comparator policy](../../../BENCH.md#comparison-baselines):

- **Rust** is Kāra's semantic peer (compiled, ownership-aware, LLVM-backed), so the headline ratio for v1 is the codegen-vs-Rust gap above. This kata used to be the worst codegen-vs-Rust gap in the suite (98× *slower*) and so the most concrete justification for monomorphized collections; it then read faster than Rust on a hasher asymmetry, slower again once that asymmetry was removed, and now reads **0.84× of `rustc -O`'s time (1.21× faster at equal safety)** with both sides on SipHash-1-3.
- **C** is the codegen calibration point — same LLVM backend as Kāra and Rust, no language runtime overhead. Since `f73df9b` the C mirror's map follows the same growth policy as Kāra's, so its remaining 5.6× lead is mostly the cost of a cryptographic-strength hash it does not pay.
- **Go** is the cross-runtime data point — GC + scheduler + statically-linked runtime, but a thoroughly-tuned native compiler. Standing baseline since 2026-05-21 (BENCH.md update). Kāra now reads **1.48× faster** than Go.
- **Python** is the ergonomic foil — the "is the perf cliff worth the syntax?" framing. Gated behind `KARA_BENCH_INCLUDE_PY=1` in the sink check; always run in its own hyperfine batch so it doesn't slow feedback on the compiled lane. It was not run for the 2026-10-29 snapshot.

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Added [`differential.kara`](differential.kara) with a Python mirror: a last-seen map and a `Set` sliding window against brute force over random strings (clean everywhere). Gaps found, in the kara bug ledger:

- **B-2026-10-06-79** — `s[a..b].to_string()` / `.clone()` on a `ref String` param is refused by `karac build`.
- **B-2026-10-06-80** — `for (i, c) in s.chars().enumerate()` and other method-rooted chains are refused by `karac build`, with a misleading hint.
