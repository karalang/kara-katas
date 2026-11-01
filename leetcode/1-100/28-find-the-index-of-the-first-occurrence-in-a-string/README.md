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

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **8%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **1.9%** margin against `rustc -O` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

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

M5 Pro, 2026-10-31 (`results.json` `measured_at` 2026-11-01T01:47Z), karac 0.9.0-dev.14057+g6697158fa (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. The seq rows below are single-threaded; the kāra rows are `KARAC_AUTO_PAR=0` seq twins. Inside one `strStr` the needle cursor is loop-carried, so KMP has no auto-par surface; brute force's K = 100 outer searches are independent, so its default build also runs in a par lane (below). (σ on the KMP rows is ~10% this session; the kāra≈rust≈c ratios are the load-immune signal.)

**Brute force** (O(N · M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    brute_force (clang -O3) | 303.2 ± 12.5 ms | 1.00× ahead of kāra |
| **kāra brute_force (codegen, seq)** | **304.0 ± 10.9 ms** | — |
| rust brute_force | 304.5 ± 11.6 ms | kāra 1.00× ahead |
| rust brute_force (`overflow-checks=on`) | 307.6 ± 16.8 ms | kāra 1.01× ahead |
| go   brute_force | 1040.9 ± 32.6 ms | kāra 3.42× ahead |

**KMP** (O(N + M)):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    kmp (clang -O3) | 118.0 ± 17.6 ms | 1.38× ahead of kāra |
| rust kmp (`overflow-checks=on`) | 158.4 ± 16.9 ms | 1.03× ahead of kāra |
| rust kmp | 160.3 ± 17.3 ms | 1.02× ahead of kāra |
| **kāra kmp (codegen, seq)** | **163.3 ± 15.9 ms** | — |
| go   kmp | 232.0 ± 10.0 ms | kāra 1.42× ahead |

**Brute force, par lane** (default build, auto-par; comparators are hand-parallel mirrors):

| Run | Mean ± σ | User CPU | Gap |
|---|---|---|---|
| rust brute_force (rayon) | 70.4 ± 1.7 ms | 1084.6 ms | 1.46× ahead of kāra |
| c    brute_force (pthreads) | 93.5 ± 3.9 ms | 636.6 ms | 1.10× ahead of kāra |
| **kāra brute_force (auto-par)** | **102.5 ± 3.8 ms** | 1417.1 ms | — |
| go   brute_force (goroutines) | 173.2 ± 14.9 ms | 1111.0 ms | kāra 1.69× ahead |

The auto-par build runs 2.97× faster than its own seq twin (304.0 → 102.5 ms). The par lane is verified in the emitted IR (`KARAC_MIR_LL`): the default build calls `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` twin does not.

Every ratio is flat against the 2026-07-28 legacy feed (Kāra/Rust brute-force seq 1.01× → 1.00×, KMP 0.98× → 1.02×, brute-force par 1.36× → 1.46×; Kāra/C 1.00× → 1.00×, 1.27× → 1.38×, 1.14× → 1.10×), while every comparator ran 3–17% slower in absolute ms this session — compare ratios, not milliseconds.

**Brute force is a three-way kāra ≈ Rust ≈ C tie** (all three within 0.5%, inside σ), and **KMP is kāra ≈ Rust** with C 1.38× ahead (the no-bounds-check raw-pointer floor on the tight `lps[]`-indexed loop). Both rows are single-thread `KARAC_AUTO_PAR=0` seq twins. Both hold *with* integer-overflow trapping on by default (design.md § Arithmetic Overflow) — the only arithmetic in either hot loop is cursor `i++`/`j++`, whose overflow checks fold (loop-bounded), so there's no trapping cost. The algorithmic point lands plainly: kāra KMP (163 ms, O(N + M)) beats kāra brute force (304 ms, O(N · M)) on the same 2M-byte haystack at this M = 16 adversarial input — the failure-function fallback earns its keep, both running single-thread. Go trails on both — its per-element bounds checks aren't eliminated on these tight loops.

### Unchecked variant — `Slice.get_unchecked` closes the C gap

On the legacy backend, C's 1.30× KMP lead was purely the two bounds checks the safe scan can't shed: `needle[j]` and `lps[j-1]`. Neither is foldable by the compiler — `j` rewinds via the LPS table on a mismatch, so it's not a monotone induction variable, and proving `j < nn` would need an interprocedural "every `lps` value is `< nn`" analysis (see [karac phase-7 § BCE table-range tier](../../../../kara/docs/implementation_checklist/phase-7-codegen.md)). But the `j < nn` invariant *is* true for every input — `j` starts 0, `j == nn` returns, and the rewind preserves it — so the programmer can assert it. [`kmp_unchecked.kara`](kmp_unchecked.kara) does exactly that, reading both cells through `unsafe { … .get_unchecked(…) }` (`Slice.get_unchecked` for `needle[j]`, `Vec.get_unchecked` for `lps[j-1]`), each with a `// Safety:` rationale. The hot scan loop emits zero bounds checks (verified by disassembly on the legacy backend; only `build_lps`'s once-per-call setup check remains; not re-checked on v2/MIR).

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR backend), same `--warmup 5 --runs 30 --shell=none` run (the kāra-vs-C/Rust ratios are the load-immune signal):

| Run | Mean ± σ | Gap |
|---|---|---|
| c    kmp (clang -O3) | 118.0 ± 17.6 ms | 1.37× ahead of kāra-unchecked |
| rust kmp (safe) | 160.3 ± 17.3 ms | 1.01× ahead of kāra-unchecked |
| **kāra kmp_unchecked (codegen)** | **161.1 ± 10.7 ms** | — |
| kāra kmp (safe) | 163.3 ± 15.9 ms | the checked baseline |

**On v2/MIR the unchecked variant no longer closes the gap:** it is 1.01× faster than the safe build (163.3 → 161.1 ms), 1.37× behind C and level with safe Rust. On the 2026-06-07 legacy snapshot, skipping the two checks took kāra from **1.30× behind C to 1.11×** (and from Rust-parity to **1.17× faster than safe Rust**; the 2026-07-28 legacy feed read unchecked 0.87× Rust) — sound, because the programmer carries the `j < nn` proof the compiler can't. The reason is the backend, not the kata: v2/MIR lowers `get_unchecked` through the same bounds-checked path as an ordinary index, so `kmp_unchecked`'s IR carries the same bounds compares and abort calls as `kmp`'s ([`B-2026-10-31-45`](../../../../kara/docs/bugs-v2.md), open). Same binary size (295.9 KiB on v2/MIR, 16 B over the safe build; on legacy 33.3 KiB — the check removal nets ~0 bytes since the panic-site infra is shared). The safe [`kmp.kara`](kmp.kara) stays the canonical answer; `kmp_unchecked` is the manual escape hatch for the residual the automatic BCE passes provably can't reach. (`Slice.get_unchecked` landed karac `fac9f85d`, 2026-06-07 — the by-value read form; the `_mut`/write form is future v2 work.)

### Codegen vs Python (KMP)

| Run | Mean ± σ |
|---|---|
| `kara kmp` (codegen) | 163.3 ± 15.9 ms |
| `rust kmp` | 160.3 ± 17.3 ms |
| `py kmp` — last measured 2026-06-07, not re-run | 9981.2 ± 514.6 ms |

Python is not in the 2026-10-31 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the ratio here is from the 2026-06-07 snapshot, when Python was **~72× slower** than Kāra codegen on KMP — per-iteration CPython bytecode dispatch over a 2M-byte scan.

### Compile time and binary size

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR backend), hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | brute_force | kmp | Binary (bf / kmp) |
|---|---|---|---|
| `karac build` | 153.2 ± 3.8 ms | 120.3 ± 2.9 ms | 295.8 / 295.9 KiB |
| `rustc -O` | 83.8 ± 1.5 ms | 94.3 ± 2.6 ms | 455.4 / 455.4 KiB |
| `clang -O3` | 47.3 ± 0.7 ms | 46.4 ± 0.5 ms | 32.8 / 32.8 KiB |
| `go build` | — | — | 2434.1 / 2434.1 KiB |

Binary sizes are the seq builds. The par-lane binaries are kāra 377.1 KiB (auto-par), rayon 453.1 KiB, C pthreads 33.0 KiB, Go 2451.0 KiB; `karac build kmp_unchecked.kara` takes 121.4 ± 3.7 ms.

On the v2/MIR backend Kāra compiles **1.28–1.83× slower** than `rustc -O` and produces seq binaries at 65% of Rust's. Every v2/MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md). The rest of this paragraph is the legacy backend's history: on the 2026-06-07 snapshot Kāra compiled **1.14–1.28× faster** than `rustc -O` and produced binaries **~93% smaller** than Rust's — **within ~0.4–0.5 KiB of C** (the delta was the overflow-trap landing pads). Same lean profile as the array katas: the workload reaches `Vec.filled` + indexed read/write, `Slice[u8]` indexing, `println(i64)` — and nothing else; cross-archive LTO + DCE elides the rest of the runtime.

### Runtime memory (peak)

| Run | brute_force | kmp |
|---|---|---|
| `kara` (codegen) | 3.0 MiB | 3.0 MiB |
| `c` | 2.9 MiB | 2.9 MiB |
| `rust` | 3.0 MiB | 3.0 MiB |
| `go` | 4.7 MiB | 4.7 MiB |
| `python` — last measured 2026-06-07, not re-run | — | 10.7 MiB |

Seq builds; brute force's par lane peaks at kāra 3.4 MiB, rayon 3.5 MiB, C pthreads 3.2 MiB, Go 5.9 MiB.

**Parity with C** — kāra reads 3,113,296 / 3,129,680 B against C's 3,080,504 B (+32–48 KiB) and Rust's 3,129,656 / 3,146,040 B. The working set is the 2M-byte haystack (≈2 MiB) plus the tiny needle and (KMP) a 16-entry `i64` LPS table. Go's +1.7 MiB is GC arena + runtime; Python's 10.7 MiB is the CPython baseline plus the `bytearray`.

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why Rust is in the harness`](../1-two-sum/README.md#why-rust-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware), so the headline ratio for v1 is the codegen-vs-Rust gap above. C calibrates the LLVM-backend floor (kāra ties it on brute force; C leads KMP by 1.38× on the 2026-10-31 feed, a lead that on the legacy backend was the no-bounds-check loop), Go is the cross-runtime data point, and Python is the ergonomic foil.

## Bug ledger

**Surfaced [`B-2026-10-31-45`](../../../../kara/docs/bugs-v2.md)** (codegen-gap, open). On the v2/MIR backend `unsafe { xs.get_unchecked(i) }` is bounds-checked like an ordinary index, so the escape hatch does nothing: `kmp_unchecked` gains 1.01× over the safe `kmp` where it gained 1.14× on legacy. Found 31 Oct 2026 with karac g6697158fa.
