# 387. First Unique Character in a String

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String, Hash Map, Counting &nbsp;·&nbsp; **Source:** [leetcode.com/problems/first-unique-character-in-a-string](https://leetcode.com/problems/first-unique-character-in-a-string/)

Given a string `s`, return the index of the first non-repeating character. If
there is none, return `-1`.

```
"leetcode"      →  0     ('l')
"loveleetcode"  →  2     ('v')
"aabb"          →  -1
```

**Constraints:** `1 ≤ s.length ≤ 10⁵`; `s` consists of lowercase English
letters only.

## Approaches

Two passes either way — tally, then scan for the first count of 1. The two
implementations differ in *where* the tally lives, and that difference is the
point: each is a distinct codegen surface.

| Approach | File | Shape |
|---|---|---|
| **Map tally** ★ | [`first_unique_char.kara`](first_unique_char.kara) | `Map[i64, i64]` keyed by byte; general, no alphabet assumption |
| Fixed-alphabet counts | [`first_unique_char_counts.kara`](first_unique_char_counts.kara) | 26-slot `Vec[i64]`; uses the lowercase-only constraint |
| Reference oracle | [`first_unique_char.py`](first_unique_char.py) | known-correct LeetCode answer |

Both also compute `unique_count` — the number of characters appearing exactly
once. In the Map version that drives a **`for k in counts.keys()` walk**, which
is deliberate: it is the surface the inline map bucket walk lowers (ledger
B-2026-07-24-2, `bef6bbc`), so this kata is live regression coverage for it. In
the counts version the same total comes from a plain indexed scan, giving a
same-answer cross-check across two very different lowerings.

## Why this kata

Chosen by **compiler surface, not sequence**. Small map-and-string programs have
been finding a disproportionate share of `karac` defects — this session, 13
sequential array/DP katas surfaced nothing while two collection/string katas
produced three ledger entries including a high-severity use-after-free. This one
adds coverage for scalar-keyed map iteration specifically.

It found no new bugs, which is itself the useful signal: the scalar map path is
in good shape after `bef6bbc`.

## Verification

| Surface | Result |
|---|---|
| `karac run --interp` | ✅ matches `first_unique_char.py` |
| `karac run` (LLJIT) | ✅ |
| `karac build` (auto-par default) | ✅ |
| `karac build` + `KARAC_AUTO_PAR=0` | ✅ |

Both implementations, all four surfaces, byte-identical to the oracle —
including the empty-string and single-character edge cases.

## Benchmarks
[`bench/`](bench/) — `bash bench/bench.sh`. Read
[`../../../BENCHMARKS.md`](../../../BENCHMARKS.md) before quoting any of these.

> **Host:** measured on the shared **x86-64 Linux cloud container**, so the run
> is committed as `bench/results.container-x86.json`, not `results.json`. Per
> the corpus convention, `results.json` is reserved for the canonical Apple M5
> Pro numbers and is the only file `scripts/consolidate-bench.sh` feeds into the
> top-level `bench-results.json`. **This kata has no M5 run yet**, so it is
> deliberately absent from the consolidated feed rather than mixing a
> container measurement into an M5-measured chart. Absolute times here are not
> comparable to other katas' `results.json`; only the **within-file
> cross-language ratios** are the signal.

**Workload.** Build-once + punch: a 4000-byte haystack is built once (25
repeating chars plus a single `'z'` at the very end, so the answer sits at the
worst-case scan position), then 2000 punches each mutate one byte and run both
`first_uniq_char` and the `keys()`-walking `unique_count`. Re-deriving a
`String` per iteration would be a vectorizable refill loop that swamps the
measurement. Sink = `8000000`, identical across all five languages.

### Runtime — 30 runs, 5 warmup

Apple M5 Pro, karac `0.1.0-dev.8616+g4a9297ad0`, measured 2026-09-09.

| Lane | mean ± σ | vs kāra |
|---|---|---|
| c | 14.0 ms ± 0.5 | **14.88× faster** |
| go | 162.3 ms ± 1.6 | 1.28× faster |
| rust | 182.7 ms ± 0.7 | 1.14× faster |
| rust (overflow-checks=on) | 181.9 ms ± 0.3 | 1.14× faster |
| **kāra** | **207.9 ms ± 5.6** | — |

Re-run 2026-09-09 against the typed hash entry point (`9ce695e9e`) and the
runtime control-byte group scan (`6cc029853`): **1.14× behind equal-safety Rust,
against 1.18× before them**. Inside this kata's own run-to-run spread, so the
honest reading is unchanged rather than improved — neither landing moves a
scalar-keyed map, which takes codegen's monomorphized probe and never reaches
the runtime path the group scan sits on. kāra `B-2026-09-07-53`.

### ✅ The hasher mismatch this section warned about is now CLOSED — and the warning was right

Every revision of this file before 2026-09-08 led with **"the 3.9× over Rust is
mostly the hash function, not codegen."** That was correct, and it has since
been settled by the compiler rather than by argument.

As written: Kāra hashed an integer key with a single Fibonacci multiply
(`(v as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)`) while Rust's default
`HashMap` used **DoS-resistant** SipHash-1-3, so comparing them directly was
"a safety mismatch on the hashing axis — the same category of error as
benchmarking against `rustc -O`'s silent wrapping."
[`bench/first_unique_char_fasthash.rs`](bench/first_unique_char_fasthash.rs) put
Rust on the same multiply and measured a **statistical tie**:

| Lane | mean ± σ | ratio |
|---|---|---|
| kāra | 143.7 ms ± 12.8 | — |
| rust (Fibonacci multiply, **equal-hash**) | 161.2 ms ± 18.7 | kāra **1.12 ± 0.16×** faster |
| rust (SipHash, default) | 570.2 ms ± 27.8 | kāra 3.97 ± 0.40× faster |

That analysis put ~72% of the headline gap on hasher choice and concluded kāra's
map lowering was "competitive with Rust's, *not* 4× better."

**karac `59c8d30cd` (2026-08-22) removed the mismatch at the source.** The
Fibonacci multiply is gone; both backends now hash with per-process-seeded
SipHash-1-3 — because that multiply's seed was a compile-time constant in the
compiler's own source, so colliding keys could be generated offline. The main
table above is therefore the equal-hash comparison, and the `fasthash.rs` arm is
retained as history rather than as a claim.

The outcome at genuine parity is **1.14× behind** equal-safety Rust — the
prediction was a tie, and the measurement landed just outside it on the
unfavourable side. Both the old 3.9× lead and the "72% of it is the hasher"
decomposition are now history; what survives is the section's actual thesis,
that kāra's map is in the same class as `std::collections::HashMap`. See kara
`B-2026-09-07-42` (bisect) and `B-2026-09-07-53` (twelve katas, corpus-wide).

**C's 15.3× lead has its own caveat.** Its map is a fixed 64-slot stack array
that fits in L1 with no allocation, no resizing, and no rehash — a real
implementation advantage over every heap-allocating stdlib map here. It is still
an open-addressed hash map (not a direct-address count table, which would have
been a different algorithm and would have flattered C further).

**Overflow checks are free here** (562.8 vs 574.3 ms, well inside σ): this
workload is map-dominated, not arithmetic-dominated, so the usual equal-safety
tax does not appear. The hashing axis, not the arithmetic axis, is what matters
for this kata.

### Compile, size, memory

| Metric | kāra | rust | c | go |
|---|---|---|---|---|
| Compile (cold) | 377.0 ms ± 29.8 | 298.5 ms ± 7.6 | 131.9 ms ± 9.8 | — |
| Binary size | **336.9 KiB** | 3886.7 KiB | 15.7 KiB | 2166.2 KiB |
| Runtime peak RSS | 2.3 MiB | 2.1 MiB | 1.7 MiB | 5.6 MiB |
| Compile peak RSS | **90.3 MiB** | 126.2 MiB | 97.2 MiB | — |

Kāra's binary is ~11.5× smaller than Rust's and ~6.4× smaller than Go's, and it
compiles in less memory than either rustc or clang while staying within 1.3× of
`rustc -O` on wall time.

### Measurement caveats

- Virtualized x86_64 container. hyperfine flags statistical outliers on the
  kāra and C lanes **even on an idle re-run**, so the ~10% σ is intrinsic to the
  host, not interference. Means reproduced within 1–2% across two independent
  full runs, which is the reason to trust them; the σ is the reason not to read
  anything into differences smaller than ~10%.
- The Python mirror is the correctness oracle, not a measured lane — it stays
  behind the `KARA_BENCH_INCLUDE_PY` gate by design.
- Measured with a release `karac` built from the same commit as the archives.

## Kāra features exercised

- **`Map[i64, i64]` insert / get / `keys()`** — the scalar-halved map path,
  which lowers to an inline bucket walk with no runtime iterator call.
- **`bytes()` byte view + `b'a'` byte literals** — index arithmetic on the
  zero-copy view rather than per-char decoding.
- **`match` on `Option` with a `0` fallback arm** — the counter-increment idiom.
- **Early `return` from inside a loop** in a `ref String`-taking function.
- **Indexed `Vec[i64]` accumulate** (`counts[idx] = counts[idx] + 1`) in the
  fixed-alphabet variant.
