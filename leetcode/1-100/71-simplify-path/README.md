# 71. Simplify Path

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/simplify-path](https://leetcode.com/problems/simplify-path/)

Given an absolute Unix-style path, return its canonical form.

A canonical path:

- starts with `/`,
- has each adjacent pair of directories separated by exactly one `/`,
- contains no `.` or `..` navigation tokens,
- does not end with a trailing `/` unless the result is the root itself.

```
"/home/"                            →  "/home"
"/home//foo/"                       →  "/home/foo"
"/home/user/Documents/../Pictures"  →  "/home/user/Pictures"
"/../"                              →  "/"
"/.../a/../b/c/../d/./"             →  "/.../b/d"   ("..." is a name, not a navigation token)
```

**Constraints:** `1 ≤ path.length ≤ 3000`; `path` consists of English letters, digits, `'.'`, `'/'`, `'_'`; `path` is an absolute path starting with `/`.

## Approaches

| Approach | Complexity | Kāra | Python | Rust | C | Go |
|---|---|---|---|---|---|---|
| One-pass scan + (start, end) index stack | O(n) time, O(n) space | [`simplify.kara`](simplify.kara) ✓ via `karac run` / `karac build` | [`simplify.py`](simplify.py) ✓ | [`bench/simplify.rs`](bench/simplify.rs) ✓ (bench quint) | [`bench/simplify.c`](bench/simplify.c) ✓ (bench quint) | [`bench/go-seq/main.go`](bench/go-seq/main.go) ✓ (bench quint) |

Interpreter and codegen produce identical output to the Python mirror across all 24 test cases in `main`.

## Why a stack — and why index pairs, not strings

The canonical form is determined by what's left on the stack after walking the input. Components fall into three classes:

| Component | Action |
|---|---|
| `'.'` | skip — same directory |
| `'..'` | pop one entry (or stay at root if empty) |
| anything else | push |

A naïve implementation would split the input on `/` into a `Vec[String]`, then push/pop those strings. That works, but allocates a fresh `String` per component and keeps both the input *and* the parts buffer live for the whole walk. The stack here instead holds **`(start, end)` index pairs into the snapshotted input chars** — 16 bytes per entry regardless of how long the component is, and no per-component allocation. The output walk reads characters back out of the input buffer at the recorded positions.

The length is part of the discriminator on purpose. `"..."` is a three-character file name and must be pushed, not interpreted as "parent of parent" — the `/.../a/../b/c/../d/./` LeetCode example exists to catch implementations that look only at the leading byte.

## What this kata uncovered

The first version of this kata couldn't call `Vec.pop` at all — the typechecker accepted it and codegen lowered it, but `karac run` panicked with "method 'pop' not found on type 'unknown'": the interpreter's Vec-method dispatch arm covered `pop_back` / `pop_front` but not the bare `pop` synonym. The kata was the first thing in the corpus to want stack-style push/pop on a `Vec[i64]`, so it surfaced the gap on its first probe.

Per the project's `no workarounds — fix the compiler` discipline, the interpreter dispatch was extended (commit [`7ebb8dd`](../../../../karac-rust/) — `pop` aliased to `pop_back` in `src/interpreter/method_call_seq.rs:207` plus a matching arm in `eval_vec_deque_method`) rather than the kata staying on a `top`-counter simulation of pop. This kata is now the natural integration test for that arm — drop the dispatch and the `'..'` cases (`/../`, `/a/../../b`, `/a/b/c/../..`) immediately panic.

**The bench then surfaced a second, deeper gap.** The 2026-05-25 bench (see § Benchmarks § Pre-fix snapshot) made the cost of the only available String-builder shape — f-string self-append `out = f"{out}{c}"` — visible as a wall-clock number: 17.58× behind C, 1.87× behind Rust on the seq lane, with auto-par recovering only half of the gap. The shape itself is **O(n²)**: each `f"{...}"` allocates a fresh String and copies all of the previous `out` into it. C escapes the cost by writing into a stack `char[64]`; Rust and Go via amortized-O(1) builder methods (`String::push` / `strings.Builder`); Kāra had no equivalent in the stdlib.

Per the same `no workarounds — fix the compiler` discipline, karac was extended (commit [`7ef42b9`](../../../../karac-rust/), 2026-05-25) with `String.push(char)` end-to-end (typechecker / interpreter / codegen, reusing the existing `karac_string_encode_char` runtime helper for 1–4 UTF-8 byte encoding) plus a `push_str` interpreter dispatch arm that closed a side gap (push_str typechecked + codegened cleanly but `karac run` panicked). The kata source was rewritten to the natural shape `out.push_str("/")` + `out.push(cs[p])`; the post-fix bench is recorded in § Benchmarks above.

## Kāra features exercised

- **`ref String` + `for c in s.chars()`** — read-only string borrow iterated per Unicode scalar; ASCII input means `chars` and `bytes` would both work, `chars` chosen so f-string append in the output loop avoids a `u8 as char` round-trip.
- **`Vec[char]` snapshot for random access** — `s.chars()` has no `len()` and no random access, but the algorithm needs both (`cs[i + 1]` for the second dot, post-scan position-indexed reads).
- **Parallel `Vec[i64]` start/end stacks with safe-on-empty `pop`** — `Vec.pop` returns `None` on an empty Vec, so the saturate-at-root rule needs no explicit guard; the two stacks stay in lockstep because pushes always go to both together.
- **`and` short-circuit inside `while` and `let` conditions** — `while i < n and cs[i] == slash` is the boundary-safe slash-skip; `is_dotdot` shortcuts the second `cs[]` read when the length doesn't match.
- **`String.push_str(&str)` + `String.push(char)` as the String-builder** — `out.push_str("/")` for the separator and `out.push(c)` for each component byte; both mutate `out` in place with amortized O(1) per call. Kāra's first version of this kata used f-string self-append (`out = f"{out}{c}"`) because `String.push(char)` wasn't on the stdlib surface; the bench made the O(n²) cost visible (see § Benchmarks § Pre-fix snapshot) and the surface was added in karac commit [`7ef42b9`](../../../../karac-rust/) (2026-05-25). `String + String` is still tracked in [`phase-8-stdlib-floor.md`](../../../../karac-rust/docs/implementation_checklist/phase-8-stdlib-floor.md) but is no longer load-bearing for this kata.

No `Map`, no shared structs, no `Vec[String]`.

## Running

```bash
# Kāra — interpreter and codegen both produce the same output today.
karac run   simplify.kara
karac build simplify.kara && ./simplify

# Python
python3 simplify.py

# Verify they agree
diff <(./simplify) <(python3 simplify.py) && echo OK
diff <(karac run simplify.kara) <(python3 simplify.py) && echo OK
```

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go, and karac
./bench/bench.sh
```

`bench/bench.sh` builds the Rust file with `rustc -O`, the C file with `clang -O3`, the Go file with `go build`, and the Kāra file twice — default `karac build` (auto-par regime) plus a second `KARAC_AUTO_PAR=0 karac build` (seq lane, apples-to-apples with `rustc -O` / `clang -O3` / `go build`). All cached in `bench/target/`, gitignored. Hyperfine runs the two lanes as separate sub-runs; straight `wc` / `time -l` reads cover binary size + memory. Python is timed in a long-workload pass at the same K = 1M.

| File | What it does |
|---|---|
| [`bench/simplify.kara`](bench/simplify.kara) | N = 8 distinct inputs cycled by `k % N` (every component class exercised), K = 1,000,000 outer iters, sink = sum of simplified-output i64 lengths |
| [`bench/simplify.py`](bench/simplify.py) | Algorithmic mirror — same N, K, same input set, same sink formula |
| [`bench/simplify.rs`](bench/simplify.rs) | Algorithmic mirror; compiled with `rustc -O` |
| [`bench/simplify.c`](bench/simplify.c) | Algorithmic mirror, hand-rolled scalar baseline with a stack-allocated `char[64]` output buffer — no malloc on the hot path; compiled with `clang -O3` |
| [`bench/go-seq/main.go`](bench/go-seq/main.go) | Algorithmic mirror using `strings.Builder`; compiled with `go build` |

The N = 8 inputs are picked to exercise every disposition the inner state machine can take — short trailing-slash (`"/home/"`), single-`..` backtrack (`"/home/user/Documents/../Pictures"`), multi-dot-name + interleaved pops (`"/.../a/../b/c/../d/./"`), heavy tail backtrack (`"/a/b/c/../.."`), heavy slash + dot churn (`"/a//b////c/d//././/.."`), simple alphabet with underscores (`"/abc_123"`), pop-past-root + new push (`"/a/b/../c/../../d"`), and multi-dot file name (`"/...hidden"`). Per-cycle the simplified outputs have total length 5+19+8+2+6+8+2+10 = 60, so K = 1M / 8 cycles × 60 = **7,500,000** at the default parameters. All five compiled impls print the same sink before timing.

### Runtime — seq lane (apples-to-apples, single-threaded)

Snapshot — M5 Pro, 2026-05-25 post-fix, hyperfine `--warmup 5 --runs 30 --shell=none`. Per BENCH.md's two-lane discipline, the kara binary here is built with `KARAC_AUTO_PAR=0` so the comparison is per-core codegen-quality only — directly stackable against `rustc -O`, `clang -O3`, and `go build`. Requires karac at commit [`7ef42b9`](../../../../karac-rust/) (the `String.push(char)` + `push_str` interpreter dispatch slice landed earlier the same day) or later.

| Run | Mean ± σ | User |
|---|---|---|
| `kara simplify` (seq, KARAC_AUTO_PAR=0) | 122.2 ± 1.6 ms | 118.9 ms |
| `rust simplify` | 120.8 ± 3.5 ms | 117.8 ms |
| `c    simplify` | 13.0 ± 0.3 ms | 11.9 ms |
| `go   simplify` | 55.1 ± 1.0 ms | 53.0 ms |

Single-thread kara is at **parity with Rust** (1.01× behind, well within σ), 2.22× ahead of Go, and 9.4× behind C — the same final ordering as kata 65's seq lane. C's 9.4× lead is the stack-allocated `char[64]` output buffer shape (no allocation per byte vs the kara/rust heap-`String::push`); on a workload where the algorithm doesn't need a heap-owned output, C will always win this lane. The post-fix kara seq picture reads as **codegen-quality parity with Rust on a heap-String workload** — the gap to C is the cost of the algorithmic shape, not the compiler.

### Runtime — auto-par regime (kara default, multi-core)

Default `karac build` output: karac's auto-par-on-reduction recognizes the `sum = sum + simplify(inputs[idx]).len()` reduction in main's K=1M loop and emits a `karac_par_reduce` dispatch. Hyperfine `--warmup 10 --runs 50` to absorb worker-pool init noise. Same hardware + date as the seq lane.

| Run | Mean ± σ | User | User / wall |
|---|---|---|---|
| `kara simplify` (auto-par default) | 20.7 ± 1.4 ms | 238.8 ms | 11.5× |

Auto-par is **5.90× faster than kara's own seq baseline**, **5.83× faster than rust**, **2.66× faster than go**, **1.58× slower than c**, and **36.7× faster than python**. The User / wall ratio of 11.5× says ~11–12 cores are doing useful work on the M5 Pro (6 P-cores + ~6 E-cores). Per-core efficiency = (118.9 ms seq User) / (238.8 ms auto-par User) = **50%** — lower than kata 65's 94% because each worker still hits the system malloc on every `simplify` call (Vec[char] snapshot + the two Vec[i64] stacks), and the post-fix String build no longer holds the slow lane. The remaining 1.58× gap to C is now the **algorithmic difference** (stack `char[64]` vs heap String), not a stdlib hole. NOT directly comparable to the single-thread rows above per BENCH.md's two-lane discipline — reported separately so the production-default Kara behavior stays visible.

The outer loop body that lights this up:

```kara
let r: String = simplify(inputs[idx]);
sum = sum + r.len();
```

Rust, C, and Go stay single-threaded — none of `rustc -O`, `clang -O3`, or `go build` auto-parallelizes the analogous for-loop without explicit rayon / OpenMP / goroutine annotation.

### Pre-fix snapshot — how the O(n²) String hole surfaced

**Pre-2026-05-25 snapshot** (same hardware, same K, karac before commit [`7ef42b9`](../../../../karac-rust/)): kara seq 225.9 ± 5.4 ms / kara auto-par 28.5 ± 2.0 ms. The kata's per-output-char shape

```kara
out = f"{out}/";
out = f"{out}{c}";
```

was the only available String-builder pattern in the stdlib — f-string interpolation builds a fresh String per call (cost proportional to current `out` length), giving **O(L²)** total work per `simplify` call for an output of length L. C escapes the cost by writing into a stack-allocated `char[64]` (no allocation per byte); Rust's `String::push(char)` writes into a heap buffer with amortized power-of-two growth (O(L)); Go's `strings.Builder` does the same. The 17.58× seq slowdown vs C and the 1.87× seq slowdown vs Rust pre-fix were **not** a karac codegen gap — they were a stdlib feature gap that the codegen was faithfully lowering.

Per the project's `no workarounds — fix the compiler` discipline (same posture as the [Vec.pop dispatch fix](#what-this-kata-uncovered) above), karac was extended (commit [`7ef42b9`](../../../../karac-rust/), 2026-05-25) with `String.push(char)` on the full pipeline (typechecker / interpreter / codegen), reusing the existing `karac_string_encode_char` runtime helper for the 1–4 UTF-8 byte encoding and sharing `push_str`'s power-of-two growth + heap-free geometry. The kata source was then rewritten to use the natural shape

```kara
out.push_str("/");
out.push(cs[p]);
```

which is amortized O(1) per call. Closing the gap dropped this kata's seq wall from **225.9 ms → 122.2 ms (1.85× speedup)** and the auto-par wall from **28.5 ms → 20.7 ms (1.38× speedup)**, moving kara from 1.87× behind Rust to **parity with Rust on the seq lane** and from 4.23× ahead on auto-par to **5.83× ahead on auto-par**. The gap to C narrowed from 2.23× slower to 1.58× slower on the auto-par lane — what's left is the algorithmic shape (heap-owned String vs stack buffer), not a karac limitation.

### Codegen vs Python

Python is **36.7× slower than Kāra auto-par** at the same K (760.4 ms vs 20.7 ms) and **6.22× slower than Kāra seq** (760.4 ms vs 122.2 ms). The post-fix serial-vs-serial Kāra/Python ratio widened from 3.30× (pre-fix) to 6.22× because closing the stdlib hole halved Kāra's seq cost while CPython's per-iter cost was unchanged. Kata [#7](../7-reverse-integer/#codegen-vs-python)'s gap was ~2,220× because the inner body there is a few integer ops — interpreter overhead dominates a much larger fraction of CPython's cost when the per-iter work is light.

### Runtime memory — seq slightly above C, auto-par +2.5 MiB

Same snapshot:

| Run | Peak RSS |
|---|---|
| `kara simplify` (seq) | 1.3 MiB |
| `kara simplify` (auto-par) | 3.8 MiB |
| `rust simplify` | 1.5 MiB |
| `c    simplify` | 1.1 MiB |
| `go   simplify` | 8.5 MiB |
| `py   simplify` | 6.9 MiB |

Kara seq at 1.3 MiB is now slightly **below** Rust's 1.5 MiB — both 0.2-0.4 MiB above C's stack-buffer baseline, the cost of the heap String/Vec churn. Auto-par adds ~2.5 MiB on top because each worker thread holds its own per-thread allocator state (libmalloc tcache) for the per-call allocation rate; pre-fix this delta was ~2.7 MiB so closing the O(n²) hole pulled it down marginally (the per-iter alloc count dropped from ~L+5 to ~5). Acceptable cost for the 5.90× wall-clock win, and the seq lane stays available for embedded / constrained-memory targets where the worker pool isn't worth paying for. Go's 8.5 MiB reflects GC heap reservation overhead independent of the actual working set.

The +2.5 MiB delta is **steady-state**, not a leak — verified by running at K=100K, 1M, 10M (RSS 3.5 / 3.6 / 4.1 MiB; only 0.7 MiB of growth across a 100× K-increase, which is steady-state allocator metadata + minor heap fragmentation). Users who need to trade parallelism for memory can dial the worker count down via `KARAC_PAR_WORKERS=N` (karac commit [`d33b389`](../../../../karac-rust/), 2026-05-25 — same ergonomic shape as `RAYON_NUM_THREADS` / `OMP_NUM_THREADS` / `GOMAXPROCS`):

| Setting | Auto-par RSS | Wall (relative) |
|---|---|---|
| (default, ~13 workers) | 3.8 MiB | 1.0× |
| `KARAC_PAR_WORKERS=4` | 1.8 MiB | ~2.5× slower |
| `KARAC_PAR_WORKERS=2` | 1.5 MiB | ~5× slower |
| `KARAC_PAR_WORKERS=1` | 1.3 MiB | matches seq lane (single-worker fast path) |

`KARAC_PAR_WORKERS=1` engages `karac_par_reduce`'s single-worker fast path, so the worker pool's per-thread tcache disappears entirely and RSS lands exactly at the seq lane's 1.3 MiB — useful for container CPU quotas, multi-tenant servers, or M-series battery-aware runs (`KARAC_PAR_WORKERS=6` keeps work off the E-cores). Invalid or `0` values fall back to the auto-detect default.

The deeper fix — per-worker scratch buffers in `karac_par_reduce` so the worker pool stops paying the per-iter allocation cost in the first place — is queued under [phase-7-codegen.md § Auto-par runtime: per-worker scratch buffers](../../../../karac-rust/docs/implementation_checklist/phase-7-codegen.md). That one addresses the root cause (closing the alloc-rate-driven tcache scaling) rather than masking it via reduced parallelism.

### Compile time and binary size

Snapshot — M5 Pro, 2026-05-25 post-fix, hyperfine `--warmup 1 --runs 10` with `--prepare 'rm -f <artifact>'` so each measurement is cold:

| Compiler | Compile time | Binary size |
|---|---|---|
| `karac build simplify.kara` (auto-par default) | 71.6 ± 0.2 ms | 295.9 KiB |
| `rustc -O simplify.rs` | 123.2 ± 1.8 ms | 455.7 KiB |
| `clang -O3 simplify.c` | 45.8 ± 0.5 ms | 32.8 KiB |

Kāra compiles this kata **1.72× faster** than `rustc -O` and produces an auto-par binary **1.46× smaller** than `rustc -O`'s. Clang is **1.56× faster** and produces a binary **9.5× smaller** — the same lower-floor C reference shape as kata [#65](../65-valid-number/#compile-time-and-binary-size). The seq-build kara binary is **33.1 KiB** (auto-par dispatch dead-code-eliminated when `KARAC_AUTO_PAR=0`), bringing the kara/rust binary-size ratio to **9.3× smaller** when the runtime weight isn't paid for. The +263 KiB delta between seq and auto-par kara binaries is the `karac_par_reduce` runtime + thread-pool helpers — identical in shape to kata [#65](../65-valid-number/), [#7](../7-reverse-integer/), and [#8](../8-string-to-integer-atoi/), and the cost of the 5.90× wall-clock win.

Compile memory: karac peaks at **10.3 MiB** vs rustc's **32.3 MiB** vs clang's **2.6 MiB** — ~3.1× lower compile-time RAM than rustc, ~4.0× higher than clang. Same ordering as the rest of the suite.

### Why Rust, C, and Go are in the harness

Same rationale as kata [#65](../65-valid-number/#why-rust-c-and-go-are-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware) and the headline ratio for v1 is the codegen-vs-Rust gap; C is the **lower-floor reference** for "what a hand-rolled scalar baseline looks like" with no heap String type; Go is the **GC + builder-tuned-stdlib peer** anchoring the seq lane on the high end. The current result — **seq lane at parity with Rust (1.01× behind), 2.22× ahead of Go, 9.4× behind C on algorithmic shape; auto-par 5.83× faster than Rust on wall, 2.66× faster than Go, 1.58× slower than C; 1.46× smaller binary than Rust on auto-par (9.3× smaller on seq); 1.72× faster compile than Rust; ~3.1× lower compile RAM than Rust; 1.3 MiB seq RSS (below Rust's 1.5), 3.8 MiB auto-par RSS for the worker thread pool** — is the kata that surfaced the **O(n²) String-builder hole**, drove the `String.push(char)` + `push_str` stdlib fix in karac commit [`7ef42b9`](../../../../karac-rust/), and validated the fix end-to-end via the pre/post snapshots above. The auto-par User/wall reading (~11.5×) is concrete evidence that `karac_par_reduce` scales on workloads heavier than the DFA / arithmetic shapes of katas 7/8/65 — heap allocation per iter narrows the per-core efficiency from kata 65's 94% to ~50%, but the multi-core win is still substantial.
