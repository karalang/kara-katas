# 22. Generate Parentheses

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Dynamic Programming, Backtracking &nbsp;·&nbsp; **Source:** [leetcode.com/problems/generate-parentheses](https://leetcode.com/problems/generate-parentheses/)

Given `n` pairs of parentheses, generate **all combinations of well-formed parentheses**. The result count is the n-th Catalan number (1, 2, 5, 14, 42, … for n = 1…5), each string of length 2n.

```
n = 3  → ["((()))", "(()())", "(())()", "()(())", "()()()"]
n = 1  → ["()"]
```

**Constraints:** `1 ≤ n ≤ 8` (Catalan(8) = 1430 strings of length 16).

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Recursive backtracking: two counters (`open < n` admits `(`, `close < open` admits `)`), each child call gets an owned f-string-extended snapshot | O(Catalan(n) · n) time / output | [`backtracking.kara`](backtracking.kara) ✓ via `karac run` / `karac build` | [`backtracking.py`](backtracking.py) ✓ |
| Closure-number DP (bottom-up): every well-formed string decomposes uniquely as `"(" A ")" B`; build `f(m)` from all `(i, m-1-i)` splits in a `Vec[Vec[String]]` table | O(Catalan(n) · n) time / output | [`closure_number.kara`](closure_number.kara) ✓ via `karac run` / `karac build` | [`closure_number.py`](closure_number.py) ✓ |

`✓` runs end-to-end today. Both forms produce identical output under the interpreter and codegen against their Python mirrors across all five test cases (n = 1, 2, 3, 4, and the spec-bound n = 8 — 1430 strings printed in full); the two styles emit the same *set* in different orders (closure-number's enclosed-size-ascending order is, for n = 3, exactly backtracking's reverse). The **backtracking** form is the benchmarked one.

## Why two counters generate exactly the valid strings

The backtracking invariant needs no stack and no validity re-check: a partial string with `open` openers and `close` closers placed can be extended by `(` while `open < n` and by `)` while `close < open`. Every string reachable under these rules is a prefix of some well-formed combination, and every combination is reached exactly once — the recursion tree *is* the answer set, with zero pruning waste. `close == n` is the single completion test (close can never pass open, open never passes n).

This is the generator dual of kata [#20](../20-valid-parentheses/): #20 *consumes* a candidate and validates LIFO bracket discipline with an explicit stack; #22 *produces* exactly the valid strings by construction. The `close < open` rule plays the role of #20's stack-emptiness check — with one bracket type, the stack's contents carry no information beyond its height, so an integer counter replaces it.

The closure-number form replaces the recursion with a unique decomposition: the first character is necessarily `(`, and its matching `)` — at the first position where the running balance returns to zero (the *closure number*) — splits the string into enclosed part `A` and trailing part `B`, both well-formed. Uniqueness of that split position makes `f(m) = { "(" A ")" B }` over all `(i, m-1-i)` pair-count splits a partition, so each string is built exactly once, bottom-up, no backtracking.

## Kāra features exercised

- **Owned `String` parameter threaded through recursion** — `backtrack(cur: String, …)` takes the partial by value and extends it via `f"{cur}("` into a fresh String for the child call: the immutable-snapshot backtracking shape, where undo is "the parent's copy was never touched" rather than a pop. A completed string moves into the accumulator by `out.push(cur)`.
- **`mut ref Vec[String]` accumulator + call-site marker** — the root call writes `backtrack("", 0, 0, n, mut out)` (fresh owned binding → marker required); interior recursive calls forward the already-`mut ref` `out` unmarked, per design.md Feature 4 Part 1½.
- **`Vec[Vec[String]]` table (closure_number)** — nested-Vec rows built once and *re-read* across later iterations (`table[i][ai]` element reads straight into `push_str`, no per-element `let` — contrast kata [#17](../17-letter-combinations-of-a-phone-number/)'s deliberate free-early `let prefix = out[i]` discipline for a frontier that is discarded each round).
- **`loop` with interior `return` as a value-producing tail** — `generate_parenthesis` ends in a `loop { … if m == n { return row; } … }`; the answer row is returned by move and never enters the table.
- **Post-fix amortized-O(1) string assembly** — `"(" + A + ")" + B` in four `push_str` appends into one fresh String (kata [#17](../17-letter-combinations-of-a-phone-number/) / [#71](../71-simplify-path/) idiom).

> **This kata is the corpus's biggest single-kata compiler-bug haul: four distinct karac codegen/analysis bugs, every one interpreter-clean.** It is the first kata to thread an owned `String` param through recursion and move it into a `mut ref Vec[String]` accumulator, and the first whose natural shape ends a value-returning function with a `loop`. All four fixed on the spot (karac `c8e42f76` + `baa210e2`, 2026-06-06):
> 1. **Auto-par raced `mut`-passed call args.** The concurrency analyzer's write-collector had no `Call` arm, so `add_one(mut out); println(out.len())` in `main` looked like two reads — the statements were par-grouped and the Vec header captured into the par env *by value*, so the callee's push writeback vanished. Default builds silently printed `0`; `KARAC_AUTO_PAR=0` and `karac run` were correct. Now both the call-site `mut` marker and the callee's declared `mut ref` param mode record the argument root as a write.
> 2. **Owned `String`/`Vec` params retained-by-alias (UAF/double-free family).** The call ABI passes owned headers by value while the *caller* keeps the buffer's free — so `out.push(cur)` at the base case, `return s`, `Some(s)` payloads, and struct-field captures of a param all dangled or double-freed (exit 133). `fn id(s: String) -> String { s }` aborted. Retaining consume sites now deep-copy a param-rooted buffer (`emit_vecstr_defensive_copy`, runtime `cap > 0` guard, recursive for heap-owning elements), matching the checker's copy semantics for element reads. The f-string sibling (`v.push(f"…")` leaving the staged accumulator cleanup armed while the vec took the buffer) was closed at the same consume sites.
> 3. **Value-returning fn with a `loop` tail emitted `ret void`** — LLVM module verification failure on closure_number's exact shape. The dead tail after a loop whose every exit is an interior `return` now emits `unreachable`.
> 4. **Untyped `let combos = generate_parenthesis(n)` lost String-element method dispatch** — `combos[j].len()` fell through because the typechecker spells the element type `"str"` in its binding side-table and `is_string_type_expr` only accepted `"String"`. Now accepts both spellings, like every other String/str consumer in codegen.
>
> Full record + follow-up trackers (Map/Set-insert siblings, method-arg mut-ref gap) in the compiler's `docs/implementation_checklist/phase-7-codegen.md` § kata-22 cluster. Regression pins: 2 analysis tests in `tests/concurrency.rs`, 8 E2E tests in `tests/codegen.rs`.

## Running

```bash
# Kāra — interpreter and codegen agree on both forms.
karac run   backtracking.kara
karac build backtracking.kara && ./backtracking
karac run   closure_number.kara
karac build closure_number.kara && ./closure_number

# Python
python3 backtracking.py
python3 closure_number.py

# Verify they agree (per style — the two styles emit different orders)
diff <(./backtracking)                <(python3 backtracking.py)   && echo OK
diff <(karac run backtracking.kara)   <(python3 backtracking.py)   && echo OK
diff <(./closure_number)              <(python3 closure_number.py) && echo OK
diff <(karac run closure_number.kara) <(python3 closure_number.py) && echo OK

# Cross-style set equality
diff <(python3 backtracking.py | sort) <(python3 closure_number.py | sort) && echo SETS-OK
```

## Benchmarks

Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`backtracking.{kara,rs,c,py}`, `go-seq/main.go`). Figures below are the 2026-10-31 re-bench (results.json `measured_at` 2026-11-01T01:24Z), measured with **karac 0.9.0-dev.14057+g6697158fa** — the v2/MIR backend (the legacy backend was deleted 2026-10-23).

**Workload.** K = 150 iterations; each generates the **full combination set for n = 10** (Catalan(10) = 16,796 strings of length 20) into a fresh container, then folds every emitted string's byte length into the sink. Per iteration that is ~58k recursion nodes, each allocating a fresh string snapshot (f-string concat in Kāra, `format!` in Rust, `cur + "("` in Go/Python, exact-size `malloc`+`memcpy` in C), plus 16,796 leaf inserts — a pure allocator/string-build stress with no arithmetic kernel and no sort. Sink = `150 · 16796 · 20` = **50,388,000**; all four compiled mirrors must agree before timing. (n = 10 exceeds LeetCode's n ≤ 8 spec bound — bench-only scaling, same move as kata [#20](../20-valid-parentheses/)'s depth = 1000.)

**Two-lane kata** (BENCH.md § Implicit auto-par): the default `karac build` links the par-dispatch surface (the per-iter byte-length fold is reduction-shaped), so the bench builds the dual binaries and reports them separately. Lane verification: the default build carries a `karac_mir_task_spawn` call in its emitted IR (`KARAC_MIR_LL`) and the `KARAC_AUTO_PAR=0` seq twin does not.

### Runtime — seq lane

M5 Pro, 2026-10-31, karac g6697158fa (v2/MIR), `bench.sh` (hyperfine `--warmup 5 --runs 30 --shell=none`, structured-JSON emit). All compiled rows single-threaded; the kāra row is `KARAC_AUTO_PAR=0`.

| Implementation | Wall time | vs Kāra |
|---|---|---|
| go   backtracking                  | 228.3 ± 2.7 ms | 0.93× |
| **kāra backtracking**              | **245.3 ± 8.1 ms** | **1.00×** |
| c    backtracking (clang -O3)      | 251.2 ± 15.7 ms | 1.02× |
| rust backtracking                  | 788.6 ± 23.5 ms | 3.21× |
| rust backtracking (`-C overflow-checks=on`) | 790.5 ± 25.0 ms | 3.22× |

**Kāra leads Rust by 3.21×, is level with C (Kāra/C 0.98×, inside C's ±15.7 ms σ), and sits 1.07× behind Go.** The Rust gap has a precise cause: the snapshot idiom's per-node allocation goes through `format!("{cur}(")`, whose `fmt::Arguments` machinery is a runtime formatting interpreter — Kāra's `f"{cur}("` lowers to one exact-size `malloc` + per-part `memcpy`s, no formatting layer. (A Rust mirror hand-tuned to `cur.clone()` + `push('(')` would close most of that gap; the mirrors deliberately use each language's native interpolation idiom for the same source shape.) Go's tuned string-concat runtime (exact-size allocation, no formatting layer) is the natural peer. The 2026-06-06 snapshot put Kāra 1.18× behind C and attributed that residual to the leaf defensive copy (each completed string is copied once into the accumulator — the soundness cost of the owned-param ABI documented in the bug-finder note) plus the accumulator's per-evaluation header traffic; on the MIR backend that residual no longer shows in wall time.

**MIR vs the previous feed (karac g77e559e2c, 2026-09-07), in language ratios:** Kāra/C 1.16× → 0.98×, Kāra/Go 1.30× → 1.07×, Kāra/Rust 0.37× → 0.31× — Kāra gained ~16% against every comparator.

**The 2026-06-06 snapshot was the *post-optimization* one.** The first run of this bench read **kāra 333.3 ± 7.3 ms — 2.06× behind C** — and attributed the gap to the f-string accumulator growing twice per node (first append sizes the buffer to exactly `cur.len()`, the one-byte second append re-grows and re-copies: two mallocs + two full copies where C pays one of each). That finding was fixed in karac the same day (`d93eca59`): f-strings whose parts are all side-effect-free now render every part first, `malloc` once at the summed size, and `memcpy` each part at its running offset. Controlled same-load A/B on this bench binary: **350.8 → 196.5 ms, 1.78×**. The win applies to every f-string-heavy program, not just this kata — the kata was the bug-finder (and here, the perf-finder).

### Runtime — kara default build

Par lane: the default (auto-par) kāra build against same-lane parallel mirrors.

| Implementation | Wall time | User CPU | vs Kāra |
|---|---|---|---|
| c    backtracking (pthreads)         | 49.9 ± 3.2 ms | 584 ms | 0.99× |
| **kāra backtracking (default build)** | **50.2 ± 3.7 ms** | **662 ms** | **1.00×** |
| go   backtracking (goroutines + WaitGroup) | 81.7 ± 1.3 ms | 520 ms (+120 ms sys) | 1.63× |
| rust backtracking (rayon `par_iter`) | 117.6 ± 12.2 ms | 1830 ms | 2.34× |

**Kāra's default build is level with C pthreads (Kāra/C 1.01×, within σ), 1.63× ahead of Go and 2.34× ahead of rayon**, and runs 4.88× faster than its own seq twin. In the previous feed (2026-09-07) Kāra par sat 1.50× behind C and 1.07× behind Go; in ratios, Kāra/C went 1.50× → 1.01×, Kāra/Go 0.93× → 0.61×, Kāra/Rust 0.56× → 0.43×. (The 2026-06-06 snapshot recorded the default build at 21.7 ± 1.5 ms with no same-lane comparators; that figure is history.)

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| py backtracking (same K=150) — last measured 2026-06-06, not re-run | 552.7 ± 3.5 ms |

Not re-run on 2026-10-31 (the bench did not set `KARA_BENCH_INCLUDE_PY`); the ratios in this paragraph are against the 2026-06-06 compiled figures. **At that snapshot this was the corpus's narrowest Python gap: 2.92× — and Python matched the Rust mirror.** Unlike most katas, Python runs the *full* K here (no scale-down). The workload is exactly CPython's best case: `cur + "("` is a C-level exact-size allocate-and-memcpy with no per-character bytecode, so the interpreter only pays for the ~58k call frames per iteration while all the actual work happens in C. (Before the f-string pre-sizing fix the gap was 1.67× — Python briefly matched *Kāra* on this workload, which is what made the grow-twice pathology impossible to ignore.) Compare kata [#20](../20-valid-parentheses/)'s ~35× (per-byte bytecode loop) — the two parenthesis katas bracket Python's best and worst cases between them.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 backtracking.c           | **47.4 ± 1.7 ms** |
| rustc -O backtracking.rs           | 90.3 ± 1.4 ms |
| **karac build backtracking.kara**  | **153.8 ± 1.6 ms** |

On the MIR backend karac compiles **1.70× slower than `rustc -O`** and sits at **3.24× of clang -O3** (the 2026-06-06 legacy build was 1.10× faster than rustc, at 75.0 ms vs 93.8 ms).

### Binary size

| Implementation | Size |
|---|---|
| c    backtracking                  | 32.9 KiB |
| **kāra backtracking (seq)**        | **295.8 KiB** |
| **kāra backtracking (default)**    | **377.1 KiB** |
| rust backtracking                  | 456.4 KiB |
| go   backtracking                  | 2434.1 KiB |

Every MIR Kāra binary is ~300–390 KB where the legacy backend's were ~34 KB (kara ledger [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); the seq binary is **295.8 KiB** (302,880 B, was 34,992 B in the 2026-09-07 feed), 1.54× under Rust's 456.4 KiB and 9.0× over C's 32.9 KiB. The default build is **377.1 KiB** (386,160 B), +81.3 KiB over the seq twin for the `karac_mir_task_spawn` worker/dispatch machinery, at ~83% of Rust's rayon binary (453.9 KiB). The par mirrors: C pthreads 33.1 KiB, Go 2451.1 KiB.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| c    backtracking                  | 1.92 MiB |
| **kāra backtracking (seq)**        | **2.17 MiB** |
| rust backtracking                  | 2.48 MiB |
| go   backtracking                  | 9.09 MiB |
| c    backtracking (pthreads)       | 14.2 MiB |
| **kāra backtracking (default)**    | **23.0 MiB** |
| rust backtracking (rayon)          | 26.1 MiB |
| go   backtracking (goroutines)     | 35.7 MiB |

Each iteration's 16,796-string set (~340 KB of payload + headers) is allocated, folded, and fully freed inside the loop — steady state is flat across all 150 iterations (a leaking build would exceed 100 MB). Kāra seq's ~0.25 MiB over C (262,168 B; ~0.7 MiB at the 2026-06-06 snapshot) is the leaf's compiler-inserted defensive copy (each completed string is copied once into the accumulator — the soundness cost of the owned-param ABI documented in the bug-finder note; the move-ABI follow-up tracked in karac's owned-temp spike would retire it) plus allocator slack. Go's 9.1 MiB carries its GC arena + scheduler. On the par lane each worker holds its own in-flight string set, so every parallel mirror sits higher; Kāra's default build lands between C pthreads and rayon.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 backtracking.c          | 2.5 MiB |
| rustc -O backtracking.rs          | 27.7 MiB |
| **karac build backtracking.kara** | **57.3 MiB** |

On the MIR backend karac's compile-memory peak is **2.1× rustc's** and ~23× clang's (the 2026-06-06 legacy build peaked at 13.3 MiB, ~2.1× under rustc).

### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware, same LLVM backend), so the headline ratio is the codegen-vs-Rust gap on the seq lane. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. On this string-build-bound kata **Kāra leads Rust by 3.21×** (its `format!` runtime-formatting layer vs Kāra's pre-sized single-malloc f-string lowering), is **level with C** (0.98×), and sits 1.07× behind Go (the natural exact-size-concat peer). The first-run 2.06×-behind-C reading drove the f-string pre-sizing fix into karac the same day — see § Runtime for the before/after.
