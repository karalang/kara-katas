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

[`bench/`](bench/) — `bash bench/bench.sh`. Numbers below are from an x86_64
Linux container (see caveats; read [`../../../BENCHMARKS.md`](../../../BENCHMARKS.md)
before quoting any of them).

**Workload.** Build-once + punch: a 4000-byte haystack is built once (25
repeating chars plus a single `'z'` at the very end, so the answer sits at the
worst-case scan position), then 2000 punches each mutate one byte and run both
`first_uniq_char` and the `keys()`-walking `unique_count`. Re-deriving a
`String` per iteration would be a vectorizable refill loop that swamps the
measurement. Sink = `8000000`, identical across all five languages.

### Runtime — 30 runs, 5 warmup

| Lane | mean ± σ | vs kāra |
|---|---|---|
| c | 50.7 ms ± 5.2 | **2.89× faster** |
| **kāra** | **146.6 ms ± 14.9** | — |
| go | 434.1 ms ± 23.8 | 2.96× slower |
| rust (overflow-checks=on) | 562.8 ms ± 27.3 | 3.84× slower |
| rust | 574.3 ms ± 39.5 | 3.92× slower |

### ⚠️ The 3.9× over Rust is mostly the hash function, not codegen

Kāra hashes an integer key with a single Fibonacci multiply
(`runtime/src/map.rs`: `(v as u64).wrapping_mul(0x9E37_79B9_7F4A_7C15)`). Rust's
default `HashMap` uses SipHash-1-3, which is **DoS-resistant**; Kāra's is not.
Comparing them directly is a safety mismatch on the hashing axis — the same
category of error as benchmarking against `rustc -O`'s silent wrapping.

[`bench/first_unique_char_fasthash.rs`](bench/first_unique_char_fasthash.rs)
swaps Rust onto the *same* Fibonacci multiply. Measured in one hyperfine run,
same protocol:

| Lane | mean ± σ | ratio |
|---|---|---|
| kāra | 143.7 ms ± 12.8 | — |
| rust (Fibonacci multiply, **equal-hash**) | 161.2 ms ± 18.7 | kāra **1.12 ± 0.16×** faster |
| rust (SipHash, default) | 570.2 ms ± 27.8 | kāra 3.97 ± 0.40× faster |

**On equal hashing the two are a statistical tie** — the ±0.16 uncertainty spans
1.0. Roughly 72% of the headline gap is hasher choice. The honest claim is that
kāra's map lowering is competitive with Rust's, *not* that it is 4× better. This
lane is deliberately kept out of `results.json`: `scripts/bench-graph.py` has a
fixed `LANGS` set and silently drops unknown lanes.

**C's 2.9× lead has its own caveat.** Its map is a fixed 64-slot stack array
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
- Python is not in `results.json` — `KARA_BENCH_INCLUDE_PY` defaults to `0`
  corpus-wide. Run with `KARA_BENCH_INCLUDE_PY=1` to include it.
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
