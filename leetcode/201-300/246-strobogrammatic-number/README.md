# 246. Strobogrammatic Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Hash Table · Two Pointers · String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/strobogrammatic-number](https://leetcode.com/problems/strobogrammatic-number/) &nbsp;·&nbsp; 🔒 **LeetCode Premium**

A number is **strobogrammatic** if it reads the same after rotating the page 180°.

```
"69"   ->  true      rotate: 6 becomes 9, 9 becomes 6, order flips  ->  "69"
"88"   ->  true
"962"  ->  false     2 is not legible upside down
```

**Constraints:** `1 ≤ num.length ≤ 50`; digits only; `num` has no leading zeros except `"0"` itself.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| two pointers, `rot(num[lo]) == num[hi]` ★ | O(n) time, O(1) space | [`strobogrammatic.kara`](strobogrammatic.kara) ✓ | [`strobogrammatic.py`](strobogrammatic.py) ✓ |
| build the rotated string, compare | O(n) time, O(n) space | [`strobogrammatic_rotate.kara`](strobogrammatic_rotate.kara) ✓ | — |

`✓` marks agreement with the Python mirror under **interpreter** (`karac run --interp`), **JIT** (`karac run`), and **codegen** (`karac build`), under the default auto-parallelising build and `KARAC_AUTO_PAR=0` alike — on the 26 spec cases below *and* on 6,000 randomized cases (see § What it found).

## The mechanism

**Rotation does two things at once, and the whole problem is remembering the second.** Each digit turns into another digit, *and* the string reverses. Only five digits survive the first half:

```
0 -> 0     1 -> 1     8 -> 8     6 -> 9     9 -> 6
```

`2 3 4 5 7` become nothing legible, so one occurrence anywhere is fatal — no pairing argument needed, the answer is `false` on sight.

Get the reversal wrong and you have written a *different, easier* problem: "are all digits individually rotatable?". That version accepts `"6996"`, which is wrong — rotating it gives `"6996"` → map → `"9669"` → reverse → `"9669"` ≠ `"6996"`. Both `"6996"` (false) and `"6009"` (true) are in the test set precisely because they differ only in that check.

The **two-pointer** form closes in from the ends and asks `rot(num[lo]) == num[hi]`. The loop condition is `lo <= hi`, not `lo < hi`, and that single character carries real weight: on an odd-length number the centre pairs with **itself**, which is exactly what forbids 6 and 9 in the middle — `rot('6')` is `'9'`, and `'9' != '6'`. A `lo < hi` loop skips the centre and wrongly accepts `"696"`. `"689"` (true, centre 8) and `"69896"` (false, would pass a centre-skipping check) are the cases that separate the two.

The **build-and-compare** form performs the rotation instead of testing it — `reverse(map(num)) == num` — which makes the reversal impossible to forget because you have to write it down. It costs O(n) space and two passes, so it is the slower way to answer, but it is an independent implementation and a distinct compiler surface: `Vec[char]` construction, `.reverse()`, and element-wise comparison rather than index-pair arithmetic.

## What it found

**No compiler bugs**, and this time the claim is built on a differential from the start rather than bolted on afterwards.

[`differential.kara`](differential.kara) and its twin [`differential.py`](differential.py) run 6,000 shared-LCG cases through **both** algorithms, which must agree with each other and with Python:

```
algorithms disagree on 0 of 6000 cases
accepted 1938 of 6000 (3018 constructed, 1488 then corrupted)
439356090
```

The same three lines come back from `karac run --interp`, `karac run`, `karac build` (auto-par, the default) and `KARAC_AUTO_PAR=0 karac build`.

**How the cases are drawn matters more than how many there are.** A uniform draw over ten digits makes nearly every string of length > 3 a reject, so the accepting path would only ever be tested on very short inputs — 6,000 cases that all exit on the first forbidden digit test almost nothing. So half the cases are **constructed** strobogrammatic strings (pairs from the rotatable set, an odd centre from `0/1/8`), and half of *those* are then **corrupted at one random position**. That puts near-misses — strings one character away from legal — at every length from 1 to 8, which is where a pairing or centre-handling bug would actually live. The accept rate went from 7% under a uniform draw to 32% with this shape, and 1,488 of the cases are single-character corruptions. The other half stays uniform over 5 rotatable + 2 forbidden digits, because construction never produces a forbidden digit and that reject path needs covering too.

This is the second kata in a row to come back clean, and that is worth stating rather than glossing: the shapes here — `chars().collect()`, `Vec[char]` indexing, `.reverse()`, `Option[char]` returns, `char` equality — are well-trodden by the corpus. A clean result on a differential designed to be adversarial is evidence; a clean result on hand-picked inputs would not have been.

## Kāra features exercised

- **`num.chars().collect()` into `Vec[char]`** — the corpus's standard string-to-characters idiom (as in [#205](../205-isomorphic-strings/)), here on both a borrowed parameter and a locally built `String`.
- **`Option[char]` as a total rotation map** — `rotate_digit` returns `None` for a digit that does not survive, so "illegible" is a value rather than a sentinel character, and the caller's `match` makes the reject path explicit.
- **`char` literals and equality** (`c == '6'`, `r != cs[hi]`) — comparison on a primitive `char`, distinct from the `String` equality the #243–245 family leans on.
- **`Vec[char].reverse()`** — in-place reversal (rotate variant), then element-wise comparison against the original.
- **`String.push(char)`** — building a `String` one character at a time in the differential, the inverse of `chars().collect()`.
- **Index-assign into `Vec[char]`** (`chars[lo] = a`) including the two-ended write `chars[lo] = a; chars[hi] = b` that constructs a strobogrammatic string.
- **`lo <= hi` two-pointer convergence** where the inclusive bound is load-bearing for correctness, not a style choice.

## Benchmarks

### How to run

```bash
brew install hyperfine    # one-time, also needs rustc (rustup), clang, go
./bench/bench.sh
```

[`bench/`](bench/) carries a scaled cross-language variant — same algorithm, same LCG, all five agreeing on the sink (`325454619`). Build-once + punch: 20,000 length-32 numbers built **once**, then 100 passes of the two-pointer check over all of them — 2,000,000 calls, ~30M pair-checks.

**The corpus is deliberately mostly accepting.** A uniform digit draw would make almost every number reject on its *first* character, so the benchmark would measure loop entry and early return rather than the scan. Every number is therefore constructed strobogrammatic, with 1 in 8 corrupted at one random position — which rejects, but on average halfway through, so a reject still does real work and no branch predictor learns a fixed answer.

**All five lanes index bytes in place.** Kāra refuses `s[i]` outright, with a diagnostic that names both alternatives and their cost — *"`s[i]` would hide an O(n) scan … use `s.char_at(i)` (O(n)) or `s.bytes()[i]` (O(1))"*. The input is ASCII digits, so `bytes()` is correct and is exactly what C, Go (`num[i]`) and Rust (`as_bytes()[i]`) do naturally. An earlier draft had Kāra materialising a `Vec[char]` per call while C indexed in place; that would have made the Kāra lane do strictly more work and reported the difference as codegen quality.

### Runtime — sequential lane

Container x86-64, **re-measured 2026-08-05** on `karac` 239c5e4f, hyperfine 30 runs, `KARAC_AUTO_PAR=0`, all lanes 99–101% CPU.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| Rust @ x86-64-v3, overflow-checked | 23.9 ± 0.8 ms | 0.53× |
| Rust `-O` | 24.5 ± 2.5 ms | 0.54× |
| Rust overflow-checked | 25.4 ± 3.5 ms | 0.56× |
| C `clang -O3` @ x86-64-v3 | 36.7 ± 2.8 ms | 0.82× |
| C `clang -O3` | 37.1 ± 1.2 ms | 0.82× |
| **Kāra (codegen)** | **45.0 ± 1.5 ms** | 1.00× |
| Go | 304.4 ± 4.4 ms | 6.76× |

> **Re-measured 2026-08-05** against `karac` 239c5e4f, which carries the three-slice
> bounds-check elimination described below. Every lane moved a little (the whole
> table was re-run on one karac, so the rows stay mutually comparable); Kāra's
> 49.7 → 45.0 ms is **not** all attributable to that fix — an A/B on one binary
> puts the elision's own share at ~3%, and the rest is container drift between
> the two sessions. That is why the attribution below rests on the `KARAC_BCE_INTERPROC=0`
> A/B and the disassembly rather than on this table.

> **Corrected 2026-08-04.** The Kāra row first read **53.9 ms** against a lane
> that built its corpus as 20,000 separately heap-allocated `String`s while C,
> Rust and Go each streamed one contiguous 640 KB buffer. The punch loop was
> therefore chasing scattered pointers in Kāra and walking a flat array
> everywhere else — a cache-locality difference introduced by the *mirror*, not
> a codegen property. The lane now uses one flat `Vec[u8]` indexed by offset,
> matching `malloc(N*LEN)` / `vec![0u8; N*LEN]` / `make([]byte, n*length)`
> exactly. Sink unchanged (`325454619`), so it is the same computation.
>
> **The correction was worth about 8%** (53.9 → 49.7 ms), which is smaller than
> the asymmetry looked like it should cost and does *not* account for the gap.
> The C ratio moves from 1.40× to **1.30×**; the rest is bounds-check
> elimination — confirmed below, kara `B-2026-08-04-8`.

**Do not read the Go row as a Kāra win. It is a Go compiler artifact, and it was chased down rather than published.**

A 5.72× lead over Go on a byte-scanning loop is not credible on its face — C, Rust and Kāra cluster within 2.2× of each other and Go sits 6–13× away, which is the signature of a mirror problem, not a language fact. Three hypotheses were tested and **rejected**: constant-modulo strength reduction (removing the `% 1000000007` changes nothing, 0.30 s either way), inlining (`go build -gcflags=-m` confirms `rotateByte` and `isStrobogrammatic` are both inlined), and bounds checks (passing a `*[32]byte` with static bounds instead of a slice changes nothing).

The cause is the **5-way `switch` on a byte**. LLVM turns it into a table or a branchless sequence; Go's compiler emits a compare chain and evaluates it ~30M times:

| Go `rotateByte` shape | Time |
|---|---|
| 5-way `switch` (as published, matching every other lane's source) | 0.31 s |
| explicit `[256]byte` lookup table | **0.03 s** |

So with a lookup table Go runs at ~30 ms and **leads Kāra**, and the honest summary of this kata's Go lane is: *Go's codegen for a small value switch is ~10× worse than LLVM's here, and that single difference dominates the measurement.* The switch is kept in all five mirrors because it is the source-level algorithm they share and it is what anyone would write — but the resulting number says nothing about Kāra versus Go.

**What the C and Rust rows do say.** Kāra is **1.40× behind ISA-matched C** and **2.11× behind equal-safety Rust** — and this is the first kata in the recent run where Rust is clearly ahead rather than level or behind. Overflow checks cost Rust nothing (27.0 vs 28.0 ms, inside σ), matching [#243](../243-shortest-word-distance/) and [#245](../245-shortest-word-distance-iii/) and unlike [#244](../244-shortest-word-distance-ii/)'s 2.28× — though see § *What the gap actually is* below for **why** they cost Rust nothing here, which turns out to be the whole story. Kāra's gap here is **not** the 5-way map, which was the obvious suspect and was tested. An isolated probe — 60M `rotate_byte` calls over a digit array, `KARAC_AUTO_PAR=0` — puts Kāra's `if`-chain and its `match` form at **0.03 s each**, against **0.08 s** for the equivalent C `switch` under `clang -O3`. The work is real (doubling the iteration count doubles the time, so nothing is folded or hoisted). So `karac` handles a small value map over `u8` at least as well as LLVM does for C, and both spellings compile to the same thing. `bytes()` is ruled out too — it returns a `Slice[u8]` view rather than allocating, and the flat-corpus lane never calls it.

### What the gap actually is

**Corrected 2026-08-05 — it is *not* bounds-check elimination.** Filed as kara **`B-2026-08-05-21`**; the earlier attribution to `B-2026-08-04-8` is withdrawn there. This section previously stated that bounds checks "account for the entire gap," on the strength of the control experiment below. That experiment showed adding bounds checks to C is *sufficient* to cost ~1.28×; it did not show they were what cost **Kāra** 1.28×. Once `B-2026-08-05-6` (kara `c87f488`) eliminated the callee-side checks, the discriminating experiment became possible — remove the suspect from the *subject* rather than add it to the *control* — and it refutes the claim.

With both punch-loop bounds checks provably gone (disassembly: **21 → 18** instructions, **2 → 0** `cmp $0x9c400`), the kata moved **45.12 → 43.71 ms**, about **3%**. The elision is real and sound, and nearly worthless here.

**The residual is Kāra's integer-overflow check on the index add `base + lo`**, which sits on the loop-carried critical path. C's mirror never computes that add — it passes `corpus + i*LEN`, folding the base into the pointer — so this was never an equal-safety comparison on the axis the old text assumed. Six-way control, hyperfine `--warmup 10 --runs 80`, min:

| variant | min | vs C |
|---|---|---|
| C, pointer-folded (as shipped) | 35.16 ms | 1.00× |
| C, `base+idx`, **unchecked** | 35.15 ms | 1.00× — the address form is free |
| C, `base+idx` + `__builtin_add_overflow` | 43.04 ms | **1.23×** — the check is the cost |
| Kāra, `base+idx`, BCE **on** | 43.71 ms | 1.25× |
| Kāra, `base+idx`, BCE off | 45.12 ms | 1.29× |
| **Kāra, `Slice` row-view** | **35.07 ms** | **1.00×** |

Rewriting C into Kāra's `base+idx` shape costs *nothing* (35.15 vs 35.16). Adding only the overflow check lands it on Kāra within 1.6%. That also explains the Rust row: `rust` (23.03 ms) and `rust_ovf` (23.21 ms) are a tie because Rust indexes a row **slice** by `lo` alone — there is no `base + i` add for a check to apply to. Overflow checking is not expensive here; checking an add that exists only because the row was addressed by offset is.

**Kāra reaches full C parity today** with the row-view spelling — `fn is_strobogrammatic(row: Slice[u8], len: i64)` called as `corpus[i*len .. i*len + len]` compiles to C's exact 15-instruction loop with neither check, at 35.07 ms. That is *not* a workaround and the kata keeps the `base+idx` form, which is the surface that exposes the gap; the slice form is an additional canonical spelling, and it is verified sound rather than assumed (handing the helper an 8-element view while claiming `len = 40` traps correctly on both AOT and the interpreter). The compiler-side fix is narrow: BCE has already *proven* `0 <= base + i < corpus.len()`, and that fact entails the add cannot overflow — the `jo` is provably dead and emitted anyway.

#### The 2026-08-04 evidence, kept

The measurements below all still reproduce; it was the *inference* from them that was wrong, so they are retained rather than deleted. Filed at the time as kara **`B-2026-08-04-8`**. An earlier revision recorded a 7-vs-3 branch count across the whole of `main` as a *hypothesis*, because that count also covers corpus construction and so does not isolate the punch loop.

**1. The two punch loops are isomorphic except for the checks.** Both binaries fully inline `is_strobogrammatic` into `main`. Kāra's loop is **21 instructions**, C's is **15**, and the 6-instruction excess is exactly `2 × (lea; cmp $0x9c400; jae <panic>)` — 100% bounds checking. Every other instruction matches one-for-one, including the 5-way rotate map, which LLVM table-izes identically in both (`add $0xd0; cmp $0x9; ja; bt <mask 0x343>; jae;` + table load). That independently re-confirms the map is not the gap. *(Still accurate as an instruction count — but the 6 excess instructions turned out not to be what costs the time.)*

**2. A control experiment pins the cost.** Adding Kāra-equivalent bounds checks to the C mirror makes `clang` emit a loop instruction-for-instruction isomorphic to Kāra's — 21 instructions, same order, differing only in register allocation and the rotate table's element width. Timing (hyperfine, 80 runs, min):

| binary | min | vs C |
|---|---|---|
| C | 65.1 ms | 1.00× |
| C **+ bounds checks** | 83.2 ms | **1.28×** |
| Kāra | 83.0 ms | **1.28×** |

Kāra is statistically indistinguishable from equal-safety C. **On this kata `karac`'s codegen is at `clang -O3` parity once safety is equalized** — that conclusion survives, and the six-way table above strengthens it. What does *not* survive is the next step the original text took: inferring from this that bounds checks were the gap. Two different per-iteration checks with similar cost are indistinguishable by an experiment that only ever *adds* one to the control.

**3. Minimal probes isolate the exact trigger.** Five variants over an identical corpus, differing only in the scan loop:

| probe | scan shape | checks |
|---|---|---|
| A | `while lo < len { v[base+lo] }` — base + ascending | 0 ✅ |
| B | `while lo <= hi { v[base+lo]; v[base+hi] }` — base + **converging** | **2** ❌ |
| C | `while lo <= hi { v[lo]; v[hi] }` — converging, no base | 0 ✅ |
| D | `while hi >= 0 { v[base+hi] }` — base + descending | 0 ✅ |
| E | `while lo+lo < len { v[base+lo]; v[base+len-1-lo] }` — base, both ends from **one** ascending IV | 0 ✅ |

Neither ingredient alone breaks it; only a base offset *combined with* a converging two-variable guard does.

**Fixed in three slices, 2026-08-04/05 (kara `e94e6bd9` + `55f3d4a3` + `c87f488`).** `karac` elides both halves when the loop and its buffer live in the same function: on a work-identical single-function probe the loop drops from 17 to 14 instructions with both checks gone, worth 1.20×. A second slice lifted the restriction that killed the length pin as soon as the buffer was passed to a helper *at all*, taking this kata's **construction** loop from 3 check sites to 1. A third closed the callee case. Below is what each blocker was, and what closing it was worth here — the answer, measured rather than assumed, is *3%*:

- **The punch loop was in a callee.** `is_strobogrammatic(corpus, base, len)` has no local fact relating `base` to `corpus.len()` — the bound holds only because every caller passes `base = k*len` with `k < n` — so no per-function analysis could prove it, and every analysis in `bce_length_pin.rs` is per-function by construction. The shape failed post-inline too: the control experiment above is `clang -O3` with full post-inline visibility, keeping the checks. LLVM's IRCE does not reach it either — it is absent from the `default<O2>` pipeline `karac` runs, so enabling it looked like a one-line win, but `default<O2>` and `default<O2>,function(loop-simplify,lcssa,irce),default<O2>` produce byte-identical assembly on this kata's IR. **Closed 2026-08-05** by kara `c87f488` (`B-2026-08-05-6`), which infers the callee's precondition and discharges it at the call sites — worth the 3% recorded above.
- **Construction now elides, but it runs once** — against the punch loop's 100 passes. Measured 42.8 → 42.0 ms, **1.02×**, inside noise, exactly as predicted before measuring. The one surviving construction check is `corpus[base + pos]` with `pos = (state/65536) % len`, which needs modulo-range reasoning rather than this shape.

**E is the decisive probe** *for the bounds-check question specifically* — same memory accesses as B, same base offset, same trip count, same result (`-607711579`), differing only in deriving both indices from one induction variable instead of two converging ones. E runs **28.1 ms**, B **54.2 ms**: the missing elimination alone costs **1.93×** on a work-identical program. This kata shows only 1.28× because its loop body does more per iteration, diluting the check.

This is the flat / row-major 2D traversal shape, so it recurs well beyond #246 — this kata's own *construction* loop is the same shape, which is why the fix reaches it. The kata is **not** rewritten to dodge any of this: it stays the natural converging two-pointer, and probe E is diagnostic evidence only, not a suggested phrasing.

### Caveats

Container-x86 lane, ~1.15× noise floor per [`BENCHMARKS.md`](../../../BENCHMARKS.md) — the two C rows are a tie with each other, as are the three Rust rows. The 1.30× C gap and 1.90× Rust gap clear the floor. The Go row is excluded from any comparative claim for the reason above.

The **3%** attributed to bounds-check elimination does **not** clear that floor on its own; it is reported as a bounded effect, not a win. It is stated with confidence only because it comes from an A/B on one binary via `KARAC_BCE_INTERPROC=0` with the elision confirmed in the disassembly — the disassembly is the evidence, the 3% is just its price. The 1.23× overflow-check result *does* clear the floor and is corroborated by an independent control (the C mirror rebuilt in Kāra's shape) rather than by timing alone.

The **M5 Pro host lane (`results.json`) has not been measured**, so this kata stays out of the consolidated feed and graphs until an Apple-silicon run is done.

## Running

```bash
# Kāra — both variants, all backends, same output.
karac run   strobogrammatic.kara
karac run   strobogrammatic_rotate.kara
karac build strobogrammatic.kara && ./strobogrammatic

# Bench lane — two spellings of the same workload, same sink (325454619).
# `bench/strobogrammatic.kara`       row by base+index — the form that exposes B-2026-08-05-21
# `bench/strobogrammatic_slice.kara` row as a Slice view — the form at C parity
cd bench && for v in strobogrammatic strobogrammatic_slice; do
    KARAC_AUTO_PAR=0 karac build $v.kara >/dev/null && ./$v
done

# Python
python3 strobogrammatic.py

# Verify they agree
for v in strobogrammatic strobogrammatic_rotate; do
    diff <(karac run $v.kara) <(python3 strobogrammatic.py) && echo "$v OK"
done

# Randomized differential: 6,000 cases, two algorithms, must match Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"
```

## Notes

Verified byte-identical under `karac run --interp` (tree-walk), `karac run` (JIT), and `karac build` (AOT) — including the default auto-parallelising build and `KARAC_AUTO_PAR=0` — with both Kāra variants agreeing with the Python mirror on the spec cases and the differential.

**Why the test set looks the way it does.** Every entry earns its place against a specific wrong implementation: `"6"` and `"9"` alone catch "is this digit rotatable" (both rotate, neither is strobogrammatic); `"6996"` vs `"6009"` catch a missing reversal; `"689"` and `"69896"` catch a `lo < hi` loop that skips the odd centre; `"10501"` catches a forbidden digit hidden between legal pairs; `"18"` catches assuming self-mapping digits pair with each other. That is 26 cases chosen as counterexamples rather than as coverage — the breadth comes from the differential.
