# 20. Valid Parentheses

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String, Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/valid-parentheses](https://leetcode.com/problems/valid-parentheses/)

Given a string `s` of just the characters `(`, `)`, `{`, `}`, `[`, `]`, decide whether it is **valid**: every opener is closed by a bracket of the *same type*, and brackets close in the right (LIFO) order.

```
"()"       → true
"()[]{}"   → true
"(]"       → false      (wrong type)
"([)]"     → false      (right types, wrong order)
"{[]}"     → true       (nested)
"("        → false      (unclosed opener)
")"        → false      (closer with no opener)
```

**Constraints:** `1 ≤ s.length ≤ 10⁴`, characters drawn from `{(, ), {, }, [, ]}`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Stack of *expected closers*: push the closer each opener demands; on a closer it must equal `stack.pop()`; an empty stack at the end means all matched | O(n) time, O(n) space | [`valid_parentheses.kara`](valid_parentheses.kara) ✓ via `karac run` / `karac build` | [`valid_parentheses.py`](valid_parentheses.py) ✓ |

`✓` runs end-to-end today. Interpreter and codegen produce identical output to the Python mirror across all twelve test cases.

## Why a stack — and why push the *closer*

Bracket matching is the textbook stack problem: an opener is a promise that a matching closer will arrive, and the most-recently-opened bracket must be the first to close (LIFO). A stack is the data structure that *is* "last in, first out", so the algorithm is one pass:

1. **Opener** (`(` `[` `{`) → push.
2. **Closer** → it must match whatever is on top. Pop; if the popped bracket doesn't match (or the stack was empty — a closer with no opener), the string is invalid.
3. **End** → the stack must be empty. A leftover entry is an unclosed opener.

The one design choice is *what* to push. Push the **opener** and the closer branch has to translate — "does `)` close `(`? does `]` close `[`?" — a six-way correspondence test on every closer. Push the **expected closer** instead (an `(` pushes `)`, a `[` pushes `]`, a `{` pushes `}`) and the closer branch collapses to a single equality: `stack.pop() == current`. The stack already speaks the closer's alphabet, so no translation table is ever consulted. This is the same "store the thing you'll compare against, not the thing you have" move that keeps kata [#13](../13-roman-to-integer/)'s value lookup to a flat byte test.

The empty-stack cases fall out for free: `Vec.pop()` on an empty stack returns `None`, which is *exactly* the "closer with no opener" condition — the `None` arm handles it with no separate emptiness guard, the same way kata [#71](../71-simplify-path/)'s `..` pop saturates at root on an empty stack.

## Kāra features exercised

- **`Vec[u8]` as a stack** — `Vec.new()` / `push` / `pop` (→ `Option[u8]`) / `is_empty()`. The same index/positional `Vec` stack kata [#71](../71-simplify-path/) uses for path components, narrowed here to single bytes. `pop`'s `Option` return makes the empty-stack case a `None` arm, not a length check.
- **`s.bytes()` returning a `Slice[u8]`** — zero-copy O(1)-indexed view over the `String` storage; LeetCode #20's alphabet is exactly `()[]{}`, all single-byte ASCII, so the byte view is exact and a `Vec[char]` snapshot would only add cost. Same primitive kata [#13](../13-roman-to-integer/) and kata [#8](../8-string-to-integer-atoi/) scan.
- **`b'('`-style byte literals + `top != b` byte equality** — pushing the expected closer (`b')'` / `b']'` / `b'}'`) and comparing it against the current byte are all `u8` operations; no char `match`, no string comparison.
- **`match stack.pop() { Some(top) => …, None => … }`** — `Option[u8]` destructure in a match arm, with the `None` arm as the "closer with no opener" early-return.

> **This kata is a compiler bug-finder.** It is the first kata to pop a `u8` off a `Vec[u8]` and compare it against another `u8` (`top != b`). That surfaced a `karac` codegen bug: an `Option[u8]` payload word is i64 in the variant word stream, and the `Some(top)` binding wasn't narrowing it back to i8, so the comparison emitted `icmp ne i64, i8` and tripped LLVM module verification ("Both operands to ICmp instruction are not of the same type!"). The interpreter accepted the same program, so it showed only under `karac build`. Fixed in `karac` ([`83c4ac99`](../../../../Kara/kara/)): `reconstruct_payload_value` now narrows *every* sub-64-bit `Option` payload binding (`u8`/`i8`/`u16`/`i16`/`u32`/`i32`/`char`) back to its surface width — the integer analogue of the pre-existing `bool` → i1 narrowing — with the typechecker recording the surface name in both the match-arm and let-binding paths. Both `karac run` and `karac build` now produce identical output across all twelve cases.

No `Map`, no `Set`, no shared structs, no sort. The demo validates a `ref String` via `s.bytes()` to stay LeetCode-faithful; the [bench](bench/) builds and validates a `Vec[u8]` buffer directly so the measured work is the bracket-stack algorithm itself, not UTF-8 String machinery.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   valid_parentheses.kara
karac build valid_parentheses.kara && ./valid_parentheses

# Python
python3 valid_parentheses.py

# Verify they agree
diff <(./valid_parentheses)              <(python3 valid_parentheses.py) && echo OK
diff <(karac run valid_parentheses.kara) <(python3 valid_parentheses.py) && echo OK
```

## Benchmarks
Wall-clock + compile-cost comparison across same-shape implementations in Kāra, Rust, C, Go, and Python. Driver is [`bench/bench.sh`](bench/bench.sh); per-mirror sources sit alongside it (`valid_parentheses.{kara,rs,c,py}`, `go-seq/main.go`).

**Workload.** `depth = 1000`, so each input is a 2000-byte nested run — `depth` openers followed by `depth` closers (`"(((…)))"`), valid by construction. The bracket *type* rotates `kind = k % 3` over `()`, `[]`, `{}` so the branch predictor can't memorize one opener/closer pair. On 1/7 of the iters (`k % 7 == 0`) the final closer is flipped to a wrong type, so the validator pushes all `depth` openers, pops `depth-1` correct closers, then mismatches on the last — exercising the `false` early-return path on a near-full stack. `K = 500,000` iters. Each iteration builds a fresh `Vec[u8]` (grown from empty — allocator traffic) and validates it with a fresh `Vec[u8]` stack (push `depth`, pop `depth`). The sink is the count of *valid* inputs: corrupt fires on `k % 7 == 0` (⌈500000/7⌉ = 71429 iters), so the count is `500000 − 71429` = **428,571**; all four compiled mirrors must agree before timing. The demo validates a `ref String`; the bench operates on a byte buffer so all four mirrors run byte-for-byte over the bracket-stack algorithm itself.

**Two-lane kata** (BENCH.md § Implicit auto-par): the per-iter `if is_valid_bytes(buf) { count += 1 }` is a count-reduction over independent iterations, so `karac build` recognizes it and spawns tasks (`karac_mir_task_spawn` in the v2/MIR IR) by default. The bench builds two kara binaries — `KARAC_AUTO_PAR=0` for the within-lane seq comparison, default for the auto-par regime — and reports them in separate tables per the two-lane discipline. This is the **alloc/scan/stack peer** to the corpus: where kata [#71](../71-simplify-path/) builds one component stack per call, this builds an input buffer *and* a validation stack per iter, with no sort to pull in the panic-symbolizer surface (contrast kata [#15](../15-3sum/)).

### Runtime — seq lane

M5 Pro, 2026-11-02 (`results.json` `measured_at` 2026-11-02T15:02Z), karac 0.8.0-dev.14215+g96fca5370 (v2/MIR backend), hyperfine `--warmup 5 --runs 30 --shell=none`. All comparators single-threaded; the kāra row is `KARAC_AUTO_PAR=0`. The `rust -C overflow-checks=on` row is the equal-safety comparator, since Kāra checks overflow by default.

| Implementation | Wall time |
|---|---|
| **kāra valid_parentheses (seq)** | **781.2 ± 20.7 ms** |
| c    valid_parentheses (clang -O3) | 1164.6 ± 21.1 ms |
| rust valid_parentheses           | 1235.8 ± 20.3 ms |
| rust valid_parentheses (overflow-checks=on) | 1242.8 ± 22.7 ms |
| go   valid_parentheses           | 1480.0 ± 23.3 ms |

On the seq lane **Kāra is the fastest** — it leads **C by 1.49×**, **Rust by 1.58×** (1.59× against the overflow-checked build), and **Go by 1.89×**. Kāra/Rust read 0.74× and Kāra/C 0.79× on the 2026-07-28 legacy feed and 0.90× and 0.97× on g6697158fa (2026-10-31); they are now 0.63× and 0.67×. The instruction excess g6697158fa carried on this kernel (1.41× legacy's) is measured fixed on g96fca5370, filed as [`B-2026-10-31-42`](../../../../kara/docs/bugs-v2.md): the MIR build now executes 0.97× legacy dd86e3955's instructions and 0.98× its cycles (`KARAC_AUTO_PAR=0`). Those counts, not the wall-clock ratios, are the comparison with legacy: the ratios also carry the comparators' session-to-session drift. This is an allocator + stack-churn workload (build a fresh 2000-byte `Vec[u8]` and run a `Vec[u8]` push/pop stack over it, 500k times), with no arithmetic kernel and no sort, so it measures exactly the two things this kata stresses: small-`Vec` allocation/grow traffic and `push`/`pop`. Kāra's `Vec` grow path and the (now byte-narrowed) `pop` land it ahead of `clang -O3`'s manual doubling-`realloc` mirror — the LLVM-backend floor — and clear of Rust's `Vec<u8>` growth + per-`push` capacity checks. The gap to Rust is the load-bearing number: Kāra's semantic peer, same backend, and Kāra wins the per-core comparison on pure collection churn. Go trails at 1.89× on `append` + GC bookkeeping.

### Runtime — auto-par regime

The per-iter `if is_valid_bytes(buf) { count += 1 }` is a count-reduction over independent iterations; the default `karac build` recognizes it and spawns tasks (`karac_mir_task_spawn` in the v2/MIR IR). NOT comparable to the single-thread rows above (BENCH.md two-lane discipline) — reported separately so the production-default Kāra behavior stays visible:

| Implementation | Wall time | User-CPU |
|---|---|---|
| **kāra valid_parentheses (auto-par default)** | **92.3 ± 4.2 ms** | 1352.1 ms |
| c    valid_parentheses (pthreads)  | 132.6 ± 6.5 ms | 2022.8 ms |
| rust valid_parentheses (rayon par_iter) | 136.9 ± 6.0 ms | 2221.8 ms |
| go   valid_parentheses (goroutines + WaitGroup) | 1306.4 ± 13.2 ms | 3037.2 ms |

The auto-par binary is **8.5× faster than the kāra seq binary** (781.2 → 92.3 ms), spreading the K=500k count-reduction across the cores at a ~14.7× user-CPU-to-wall ratio on M5 Pro. Against the parallel comparators it now leads: **0.67× rayon and 0.70× C pthreads** (1.06× / 1.10× on g6697158fa, 0.68× / 0.71× on the 2026-07-28 feed), and 14.2× ahead of Go. The par loss on g6697158fa was the same seq gap ([`B-2026-10-31-42`](../../../../kara/docs/bugs-v2.md)), since that build's instruction count was flat across worker counts (26.33G at 1 worker, 26.39G at 18), so the dispatch was not the cost; it went with the seq fix. This is the legitimate-win case (BENCH.md kata #4 path): each iteration's buffer build + validate is fully independent, so the reduction parallelizes cleanly — a better ratio than the sort+allocate body of kata [#15](../15-3sum/) (4.5× on the 2026-10-31 toolchain), because here there's no shared sort runtime and the per-worker work is a clean alloc/scan. The cost is the task-spawn (`karac_mir_task_spawn`) + worker-pool runtime surface (see § Binary size, § Runtime memory).

### Runtime — Python

| Run | Mean ± σ |
|---|---|
| `py valid_parentheses` (K=100k) — last measured 2026-06-05, not re-run | 6.517 ± 0.112 s |

Python is not in the 2026-11-02 feed (the run did not set `KARA_BENCH_INCLUDE_PY`); the figure and ratios in this paragraph are from the 2026-06-05 snapshot. Python at K=100k was 6.52 s; projecting to the compiled mirrors' K=500k (~32.6 s) put it **~35× slower than kāra seq** at the time. The hot path is a per-byte Python-level loop with a dict lookup and a list `append`/`pop` per character — exactly the interpreter-bound shape with no C-builtin to hide behind (contrast kata [#15](../15-3sum/), where `sorted()` keeps the gap to ~14×), so the gap is wide and typical of the corpus's pure-iteration katas. Against the auto-par regime the cross-lane ratio was ~357×.

### Compile elapsed (cold)

`--warmup 1 --runs 10 --prepare 'rm -f <artifact>' --shell=none`:

| Compiler | Time |
|---|---|
| clang -O3 valid_parentheses.c           | **47.4 ± 0.7 ms** |
| rustc -O valid_parentheses.rs           | 82.5 ± 1.1 ms |
| **karac build valid_parentheses.kara**  | **152.8 ± 2.9 ms** |

Kāra compiles **1.85× slower than `rustc -O`** and at **3.22× of clang -O3** on the v2/MIR backend. (The 2026-06-05 legacy snapshot read 77.2 ms, 1.18× faster than rustc.)

### Binary size

| Implementation | Size |
|---|---|
| c    valid_parentheses            | 32.8 KiB |
| **kāra valid_parentheses (seq)**  | **50.8 KiB** |
| **kāra valid_parentheses (auto-par)** | **377.3 KiB** |
| rust valid_parentheses            | 455.6 KiB |
| go   valid_parentheses            | 2434.2 KiB |

The v2/MIR Kāra binaries sit above the legacy backend's ~34 KB, tracked as [`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md): today's seq binary is 50.8 KiB (295.8 KiB on g6697158fa) and the auto-par row 377.3 KiB (83% of Rust's 455.6 KiB). The rest of this paragraph is the legacy backend's history. Kāra's seq binary was **33.3 KiB — within 600 B of C's 32.8 KiB**. This kata calls no `sort_by`, so it never links the runtime's libstd floor (panic infrastructure + DWARF symbolizer) that dominates the sort-using katas (15 / 16 / 18, ~295 KiB) — a no-sort `Vec[u8]` stack program was as small as the C mirror (see [kata 16 § Binary size](../16-3sum-closest/README.md) for the breakdown). The auto-par row at **296.1 KiB sat exactly on the documented auto-par floor** — the `karac_par_reduce` + worker-pool / threading surface plus the libstd retinue it keeps reachable — and landed **at ~65% of Rust's 455.6 KiB**. (The 2026-05-30 snapshot read 417.6 KiB for the auto-par row; −124,864 B of that was rlib contamination in a mis-built runtime archive, the same incident corrected across katas #14–#18. The seq binary was unaffected — it reproduced bit-for-bit today — because a no-sort, no-par program reaches none of the contaminated surface.) C's 32.8 KiB (no runtime archive) is the floor; Go's 2.4 MiB carries its runtime.

### Runtime memory (peak)

| Implementation | Peak |
|---|---|
| rust valid_parentheses            | 1.2 MiB |
| c    valid_parentheses            | 1.2 MiB |
| **kāra valid_parentheses (seq)**  | **1.2 MiB** |
| **kāra valid_parentheses (auto-par)** | **4.3 MiB** |
| go   valid_parentheses            | 10.3 MiB |

Kāra seq's peak RSS (1,245,520 B) is level with Rust (1,245,496 B) and below C (1,294,648 B) on this run — single-shot `/usr/bin/time -l` samples, so treat the trio's relative ordering as sample noise at this granularity. The per-iter input buffer and stack are allocated, used, and freed inside the loop, so steady state stays flat across all 500,000 iterations. The auto-par regime's 4.3 MiB (4,473,264 B) is the worker pool's per-thread scratch + partials — level with rayon's 4.3 MiB (4,489,552 B) and below C pthreads' 5.6 MiB; single-sample, so directionally promising but unconfirmed. Go's 10.3 MiB carries its GC arena + scheduler.

### Compile memory (cold)

| Compiler invocation | Peak |
|---|---|
| clang -O3 valid_parentheses.c          | 2.6 MiB |
| rustc -O valid_parentheses.rs          | 26.8 MiB |
| **karac build valid_parentheses.kara** | **62.5 MiB** |

Kāra's compile-memory footprint on the v2/MIR backend is ~23.9× clang's and 2.33× rustc's on this kata. (The 2026-06-05 legacy snapshot read 13.5 MiB, ~2× below rustc.)



### Why Rust is in the harness

Same rationale as [`1-two-sum/README.md § Why this kata is in the harness`](../1-two-sum/README.md#why-this-kata-is-in-the-harness): Rust is Kāra's semantic peer (compiled, ownership-aware, same LLVM backend), so the headline ratio is the codegen-vs-Rust gap on the seq lane. C calibrates the LLVM-backend floor, Go is the cross-runtime data point, and Python is the ergonomic foil. The auto-par regime is reported separately and never headlined against the single-threaded rows, per BENCH.md's two-lane discipline.

## Calibration re-probe (2026-10-06)

Re-probed with new phrasings, on all four surfaces plus valgrind, as part of a ten-kata calibration batch (katas 1-49, against kata 352's probing). Added [`differential.kara`](differential.kara) with a Python mirror: the stack check against pair deletion over 3000 random bracket strings (clean everywhere). Gaps found, in the kara bug ledger:

- **B-2026-10-06-86** — a value enum carrying a unit-only enum payload is refused (`E_ENUM_NESTED_ENUM_PAYLOAD`).
- The kata-3 `chars()` chain row (B-2026-10-06-80) and the kata-1 predicate row (B-2026-10-06-74) were hit again.

## Bug ledger

**Surfaced [`B-2026-10-31-42`](../../../../kara/docs/bugs-v2.md)** (perf, open). On g6697158fa (2026-10-31) `bench/valid_parentheses.kara` executed 1.41× legacy's instructions (26.26G vs 18.59G, 1.37× the cycles, `KARAC_AUTO_PAR=0`), with the seq lane at 0.90× `rustc -O` (0.74× on legacy) and the par lane at 1.06× rayon (0.68× on legacy); the par build's instructions were flat across worker counts, so the par loss was the same seq gap. Measured fixed on g96fca5370 (2026-11-02): 0.97× legacy dd86e3955's instructions and 0.98× its cycles, seq 0.90× → 0.63× `rustc -O`, par 1.06× → 0.67× rayon.
