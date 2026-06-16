# 28. Find the Index of the First Occurrence in a String

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Two Pointers, String, String Matching &nbsp;·&nbsp; **Source:** [leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string](https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string/)

Return the index of the first occurrence of `needle` in `haystack`, or `-1` if `needle` is not part of `haystack`. An empty needle matches at index `0` (the C `strstr` / `std` convention).

**Constraints:** `1 ≤ haystack.length, needle.length ≤ 10⁴`, both consist of lowercase English letters.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Brute-force sliding window | O(hn · nn) time, O(1) extra space | [`brute_force.kara`](brute_force.kara) ✓ | [`brute_force.py`](brute_force.py) ✓ |
| Knuth-Morris-Pratt (KMP) | O(hn + nn) time, O(nn) extra space | [`kmp.kara`](kmp.kara) ✓ | [`kmp.py`](kmp.py) ✓ |
| KMP, bounds-check-elided (`get_unchecked`) | O(hn + nn) time, O(nn) extra space | [`kmp_unchecked.kara`](kmp_unchecked.kara) ✓ | — (perf variant; see § Unchecked variant) |

## Why two approaches

Brute force tries every start position and compares the needle against the window byte-for-byte, bailing on the first mismatch. On typical text it's effectively linear (mismatches happen early), but its worst case is O(hn · nn): a haystack of repeated `a` searched for `aa…ab` matches the whole needle-minus-one at every position before failing on the last byte.

**KMP** removes that worst case. It precomputes, for each needle prefix, the length of its longest proper prefix that is also a suffix (the **LPS** / failure function). On a mismatch at needle position `j`, the scan resets `j` to `lps[j − 1]` instead of `0`, reusing the already-matched overlap so the haystack cursor `i` never backs up — O(hn + nn) guaranteed, at the cost of an `nn`-sized table. The two files share an identical adversarial bench input precisely so the wall-time gap is visible (see Benchmarks).

## Kāra features exercised

- **`ref String` parameters + `.bytes()` / `.len()`** — the surface solutions take `ref String` and scan the zero-copy `Slice[u8]` view; the LeetCode lowercase-letter constraint means byte index = char index, so no `Vec[char]` snapshot is needed.
- **`-1` sentinel return on `i64`** — the not-found path returns a negative index, exercising signed-return plumbing.
- **Short-circuit `and` guarding an indexed read** — brute force's `j < nn and haystack[i + j] == needle[j]` relies on left-to-right evaluation so the indexed read is skipped once `j == nn`.
- **`Vec[i64]` built and indexed inside a helper** — KMP's `build_lps` allocates the failure table with `Vec.filled`, fills it with a non-trivial recurrence (the `len = lps[len − 1]` fallback), and returns it by value.
- **Two-cursor loop with asymmetric advance** — KMP advances `i`/`j` together on a match, rewinds only `j` on a mismatch, exercising the conditionally-updated-cursor shape.

## Running

```bash
karac run brute_force.kara
karac run kmp.kara
diff <(karac run kmp.kara) <(python3 kmp.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup) and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust files with `rustc -O`, the C files with `clang -O3`, the Go mirrors with `go build`, and the Kāra files with `karac build` (all cached in `bench/target/`, gitignored), then runs runtime, compile-cost (cold, via a `--prepare` delete step), binary-size, and peak-RSS passes.

| File | What it does |
|---|---|
| [`bench/brute_force.kara`](bench/brute_force.kara) | Adversarial input, O(hn · nn) sliding window |
| [`bench/kmp.kara`](bench/kmp.kara) | Same input, O(hn + nn) KMP |
| `bench/{brute_force,kmp}.{py,rs,c}`, `bench/go-seq/{brute_force,kmp}` | Algorithmic mirrors (Python, `rustc -O`, `clang -O3`, `go build`) |

**Workload (shared by both approaches):** haystack = `N − 1` `'a'` bytes + one `'b'` (N = 2_000_000), needle = `M − 1` `'a'` bytes + `'b'` (M = 16), K = 100 searches. The needle occurs only at the very end (index `N − M`), so every start position matches `M − 1` bytes before failing on the last — the **brute-force worst case** (O(N · M)) and a deep-partial-match stress for KMP's fallback. All five mirrors step identical bytes (97 = `'a'`, 98 = `'b'`) over a `Slice[u8]` so the O(N) setup is a uniform bulk fill, not a runtime-dependent per-byte append. Sink = `K × (N − M)` = 199_998_400, a real returned index that proves the full scan ran; bench.sh fails loudly on mismatch. The search is read-only (the per-call result would be loop-invariant), but bounds-checked indexing keeps it off LLVM's `readonly` list, so LICM leaves the K calls in the loop — the same property kata [#5](../5-longest-palindromic-substring/README.md)'s bench relies on. Python is benched on KMP only (pure-Python brute force at O(N · M) = 320M byte compares is minutes per run); kāra interp lanes are omitted (tree-walk over the adversarial scan is impractical — interp parity is covered by the kata-root `diff` test on the `String` form).

### Codegen vs Rust (the headline)

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 5 --runs 30 --shell=none`. Seq-only kata — `strStr` is a read-only scan with a loop-carried needle cursor, no auto-par surface. (Light background load; the kāra≈rust≈c ratios are the load-immune signal.)

**Brute force** (O(N · M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| **kāra brute_force (codegen, seq)** | **267.8 ± 4.5 ms** | — |
| c    brute_force (clang -O3) | 269.9 ± 4.3 ms | kāra 1.01× ahead |
| rust brute_force | 270.2 ± 5.3 ms | kāra 1.01× ahead |
| go   brute_force | 900.8 ± 8.0 ms | kāra 3.36× ahead |

**KMP** (O(N + M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    kmp (clang -O3) | 107.2 ± 7.9 ms | 1.30× ahead of kāra |
| **kāra kmp (codegen, seq)** | **139.2 ± 8.6 ms** | — |
| rust kmp | 139.5 ± 8.1 ms | kāra 1.00× |
| go   kmp | 200.0 ± 3.2 ms | kāra 1.44× ahead |

**Brute force is a three-way kāra ≈ Rust ≈ C tie** (kāra a hair ahead of both), and **KMP is kāra ≈ Rust** with C 1.30× ahead (the no-bounds-check raw-pointer floor on the tight `lps[]`-indexed loop). Both rows are single-thread `KARAC_AUTO_PAR=0` seq twins. Both hold *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow) — the only arithmetic in either hot loop is cursor `i++`/`j++`, whose overflow checks fold (loop-bounded), so there's no trapping cost. The algorithmic point lands plainly: kāra KMP (139 ms, O(N + M)) beats kāra brute force (268 ms, O(N · M)) on the same 2M-byte haystack at this M = 16 adversarial input — the failure-function fallback earns its keep, both running single-thread. Go trails on both — its per-element bounds checks aren't eliminated on these tight loops.

### Unchecked variant — `Slice.get_unchecked` closes the C gap

C's 1.30× KMP lead is purely the two bounds checks the safe scan can't shed: `needle[j]` and `lps[j-1]`. Neither is foldable by the compiler — `j` rewinds via the LPS table on a mismatch, so it's not a monotone induction variable, and proving `j < nn` would need an interprocedural "every `lps` value is `< nn`" analysis (see [karac phase-7 § BCE table-range tier](../../../../kara/docs/implementation_checklist/phase-7-codegen.md)). But the `j < nn` invariant *is* true for every input — `j` starts 0, `j == nn` returns, and the rewind preserves it — so the programmer can assert it. [`kmp_unchecked.kara`](kmp_unchecked.kara) does exactly that, reading both cells through `unsafe { … .get_unchecked(…) }` (`Slice.get_unchecked` for `needle[j]`, `Vec.get_unchecked` for `lps[j-1]`), each with a `// Safety:` rationale. The hot scan loop emits zero bounds checks (verified by disassembly; only `build_lps`'s once-per-call setup check remains).

Snapshot — M5 Pro, 2026-06-07, same `--warmup 5 --runs 30 --shell=none` run (moderate background load; the kāra-vs-C/Rust ratios are the load-immune signal):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    kmp (clang -O3) | 107.2 ± 7.9 ms | 1.11× ahead of kāra-unchecked |
| **kāra kmp_unchecked (codegen)** | **119.2 ± 7.2 ms** | — |
| kāra kmp (safe) | 139.2 ± 8.6 ms | the checked baseline |
| rust kmp (safe) | 139.5 ± 8.1 ms | **kāra-unchecked 1.17× faster** |

Skipping the two checks takes kāra from **1.30× behind C to 1.11×** (and from Rust-parity to **1.17× faster than safe Rust**) — sound, because the programmer carries the `j < nn` proof the compiler can't. Same binary size (33.3 KiB; the check removal nets ~0 bytes since the panic-site infra is shared). The safe [`kmp.kara`](kmp.kara) stays the canonical answer; `kmp_unchecked` is the manual escape hatch for the residual the automatic BCE passes provably can't reach. (`Slice.get_unchecked` landed karac `fac9f85d`, 2026-06-07 — the by-value read form; the `_mut`/write form is future v2 work.)

### Codegen vs Python (KMP)

| Run | Mean ± σ |
|---|---|
| `kara kmp` (codegen) | 139.2 ± 8.6 ms |
| `rust kmp` | 139.5 ± 8.1 ms |
| `py kmp` | 9981.2 ± 514.6 ms |

Python is **~72× slower** than Kāra codegen on KMP — per-iteration CPython bytecode dispatch over a 2M-byte scan.

### Compile time and binary size

Snapshot — M5 Pro, 2026-06-07, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | brute_force | kmp | Binary (bf / kmp) |
|---|---|---|---|
| `karac build` | 84.2 ± 1.2 ms | 81.7 ± 0.5 ms | 33.3 / 33.2 KiB |
| `rustc -O` | 96.4 ± 1.8 ms | 104.3 ± 3.8 ms | 455.4 / 455.4 KiB |
| `clang -O3` | 49.9 ± 0.7 ms | 50.4 ± 0.4 ms | 32.8 / 32.8 KiB |
| `go build` | — | — | 2434.1 / 2434.1 KiB |

Kāra compiles **1.14–1.28× faster** than `rustc -O` and produces binaries **~93% smaller** than Rust's — **within ~0.4–0.5 KiB of C** (the delta is the overflow-trap landing pads). Same lean profile as the array katas: the workload reaches `Vec.filled` + indexed read/write, `Slice[u8]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | brute_force | kmp |
|---|---|---|
| `kara` (codegen) | 2.9 MiB | 3.0 MiB |
| `c` | 2.9 MiB | 3.0 MiB |
| `rust` | 3.0 MiB | 3.0 MiB |
| `go` | 5.0 MiB | 5.0 MiB |
| `python` | — | 10.7 MiB |

**Parity with C** — the working set is the 2M-byte haystack (≈2 MiB) plus the tiny needle and (KMP) a 16-entry `i64` LPS table. Go's +2 MiB is GC arena + runtime; Python's 10.7 MiB is the CPython baseline plus the `bytearray`.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra ties it on brute force; C's 1.30× KMP lead is the no-bounds-check loop), Go is the cross-runtime data point, and Python is the ergonomic foil.
