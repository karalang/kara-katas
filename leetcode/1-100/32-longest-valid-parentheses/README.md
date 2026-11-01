# 32. Longest Valid Parentheses

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String, Dynamic Programming, Stack &nbsp;·&nbsp; **Source:** [leetcode.com/problems/longest-valid-parentheses](https://leetcode.com/problems/longest-valid-parentheses/)

Given a string of only `'('` and `')'`, return the length of the longest
**well-formed** (balanced, properly nested) substring.

```
"(()"      →  2     (the trailing "()")
")()())"   →  4     (the middle "()()" )
""         →  0
```

**Constraints:** `0 ≤ s.length ≤ 3·10⁴`; `s[i]` is `'('` or `')'`.

## Why this kata — the sequel to #20

[#20 valid-parentheses](../20-valid-parentheses/) asked *is the whole string
valid?* with a stack of expected **closers**. #32 asks *how long is the longest
valid run?* — and that one change forces the stack to remember **positions**
instead of bracket types. It is a small step in statement and a large step in
technique, which is why #20 is Easy and #32 is Hard. Three classic lenses solve
it, and the kata implements all three:

| Lens | Idea | Space |
|---|---|---|
| **Stack of indices** ★ | seed with a `-1` base; push opener indices, on a closer pop and measure `i - top` to the boundary below | O(n) |
| **Two-pass counters** | `left`/`right` scalar counts L→R then R→L; a balanced run is `left == right`, an unrecoverable one resets | **O(1)** |
| **DP** | `dp[i]` = longest valid run ending at `i`; closers reach back across `dp[i-1]` to find their opener and glue on `dp[j-1]` | O(n) |

The unifying insight: a valid-substring length is the gap between the current
index and the **last unmatched boundary** to its left. The stack stores those
boundaries explicitly; the two-pass form detects them implicitly via the
counter-tie; DP computes the matching opener's index from the run length it
already stored. Same answer, three different ways to locate the boundary.

## Approaches

Three styles, all byte-identical to the Python oracle across all 20 cases, under
`karac run` **and** `karac build` (the oracle additionally cross-checks the three
algorithms agree on every case).

| Approach | File | Shape |
|---|---|---|
| **Stack of indices** ★ | [`longest_valid_parentheses.kara`](longest_valid_parentheses.kara) | a `Vec[i64]` stack seeded with `-1`; push opener indices, on a closer pop then measure `i - stack.top()` to the new boundary — the canonical form, the positional sibling of #20's closer stack |
| Two-pass counters | [`longest_valid_parentheses_twopass.kara`](longest_valid_parentheses_twopass.kara) | two scalar counters, L→R then R→L; the **O(1)-space** form — the two passes are duals (L→R misses left-heavy tails like `"(()"`, R→L misses right-heavy tails like `"())"`; together they cover both) |
| Dynamic programming | [`longest_valid_parentheses_dp.kara`](longest_valid_parentheses_dp.kara) | `dp[i]` = longest valid run ending at `i`; the `dp[i-1] + 2 + dp[j-1]` recurrence stitches an outer match across its inner run and the run preceding the opener |

The stack is the most intuitive and the natural continuation of #20; the two-pass
is the space-optimal trick (no auxiliary structure at all); the DP is the
index-arithmetic counterpart to the stack — where the stack *reads* the boundary
off the top, DP *computes* the matching opener's index directly.

## What this kata uncovered

**Flat curve — no `karac` bug.** All three algorithms — the index stack
(`Vec[i64]` push/`pop`/`is_empty`/`stack[len-1]` peek), the dual counter passes,
and the DP recurrence with its `i - dp[i-1] - 1` opener back-reference and
`if i >= 2 { dp[i-2] } else { 0 }` if-expression guards — compiled and ran
first-try under **both** backends. This rides the hardened `Vec`-as-stack surface
that #20 and [#71 simplify-path](../71-simplify-path/) already cleared (including
the `Option[u8]` payload-narrowing codegen fix #20 surfaced); the `let _ =
stack.pop();` discard-the-Option idiom and the `s.bytes()` zero-copy scan both
behaved. Nothing new for the front-end or codegen to trip on.

## Benchmarks

Workload: build one fixed pseudo-random parens buffer of length `L = 4096` once,
then run the ★ index-stack `longest_valid` over a **sliding window**
`[start, start+2048)` of it **`TOTAL = 330 000`** times, the window offset varying
with the iteration index so no comparator can hoist the pure call out of the
loop, folding each window's answer into a checksum (sink `675510162`). The stack
is allocated **fresh per call** — so the bench includes the stack approach's real
per-call small-`Vec` allocation, 330K times over, not an amortized reuse. The
accumulator carries a loop-borne dependency, so it does not auto-parallelize.
Apple M5 Pro; `bench/bench.sh` (`hyperfine`). Figures below are the 2026-10-31
re-bench (results.json `measured_at` 2026-11-01T01:55Z), measured with **karac
0.9.0-dev.14057+g6697158fa** — the v2/MIR backend (the legacy backend was deleted
2026-10-23).

### Seq lane — runtime (single-threaded sliding-window scan)

| | C | Rust (`-O`) | **Kāra** | Rust (`overflow-checks=on`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 229.0 ± 2.3 ms | 362.3 ± 12.6 ms | **380.9 ± 33.7 ms** | 442.8 ± 5.4 ms | 868.8 ± 4.8 ms | 21027 ms (last measured 2026-06-15, not re-run) |
| vs Kāra | 1.66× faster | 1.05× faster | — | **1.16× slower (Kāra wins at = safety)** | 2.28× slower | 66× slower than the 2026-06-15 Kāra figure |

Kāra's ±33.7 ms σ is hyperfine's outlier warning on this run (its user time,
379.4 ms, sits on the mean); the comparators' σ are 0.6–3.5 %.

**The allocation-*churn* middle ground between [#31](../31-next-permutation/) and
[#43](../43-multiply-strings/).** #31 was pure in-place compute (no heap → Kāra
ties Rust/C). #43 was allocation-*growth* (a per-result `Vec` + a 14 MB output
`String` → Kāra trailed on the small-object path). #32 allocates a small
stack **per call and frees it immediately** — churn, not growth — so the allocator
hands back the same block and there is no sustained heap pressure. The result:
**at equal overflow safety Kāra (380.9 ms) beats Rust (442.8 ms) by 1.16×.** Kāra
traps on overflow by default (design.md § Arithmetic Overflow); the honest peer is
`rustc -C overflow-checks=on`, and Kāra's checked codegen is *cheaper* here than
Rust's (Rust's checks cost it 362.3 → 442.8 ms, +22 %; Kāra's land at 380.9). Only
wrapping `rustc -O` edges ahead (1.05×), and C's no-GC stack-`malloc` floor is
1.66× — the residual is the per-call allocation, present in every language but
cheapest in C.

**MIR vs the previous feed (legacy karac 0.1.0, 2026-06-15), in language ratios:**
Kāra/Rust 1.03× → 1.05×, Kāra/C 1.62× → 1.66×, Kāra/Go 0.48× → 0.44× — flat
(every comparator, Kāra included, ran ~16–31 % slower in absolute ms this session).

**No par lane — by construction.** Although each window is computed
independently, karac's auto-par-on-reduction pass does **not** fire on this loop
(the per-call allocation + modulo reduction): verified, the default and
`KARAC_AUTO_PAR=0` binaries are **byte-identical** (re-checked on the 2026-10-31
MIR build: same 302,888 B, same sha) and both run single-threaded
(cpu 99.9 %). Per the bench-lane discipline, rayon/go-par comparators are built
only when auto-par actually fires — it does not here, so the seq lane is the whole
story.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.06 MiB | 1.08 MiB | **1.03 MiB** | 11.70 MiB |
| binary size (seq) | 295.8 KiB | 456.0 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 119.3 ms | 86.8 ms | **45.7 ms** |
| compile peak RSS | 56.9 MiB | 26.7 MiB | **2.6 MiB** |

The churn-not-growth shape shows in memory too: 330K per-call allocations leave
Kāra's runtime RSS (1.06 MiB) **tied with Rust** (1.08) and within rounding of C
(1.03) — the allocator recycles the freed blocks, so there is no resident slack to
surface (the same flat-heap profile #43 now reaches once its RC-aliasing slack was
fixed). Go's GC heap is 11.70 MiB by contrast. Every MIR Kāra binary is ~300–390 KB
where the legacy backend's were ~34 KB (kara ledger
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)); this one is **295.8 KiB**
(302,888 B, was 34,120 B on legacy), 1.54× under Rust and 9.0× over C. On the MIR
backend compile no longer favors Kāra: karac is 1.37× slower than `rustc -O`
(119.3 vs 86.8 ms) and peaks at 2.1× its compiler RSS (56.9 vs 26.7 MiB); on the
legacy build it was 75.9 ms / 13.3 MiB, ahead of rustc on both.

**Where this lands.** A per-call short-lived-allocation kernel: Kāra ties Rust/C
on memory, **beats Rust at equal overflow safety** (1.16×), trails only wrapping
`rustc -O` (1.05×) and C's no-GC floor (1.66×). With #31 (no-alloc, tied) and #43
(alloc-growth, behind), #32 completes the picture — Kāra's small-object
residual bites only under *sustained* heap growth; transient per-call churn it
handles near the systems-language floor.

## Kāra features exercised

- **`Vec[i64]` as an index stack** — `push`/`pop` (Option, discarded via
  `let _ = stack.pop();`)/`is_empty`/`stack[stack.len()-1]` peek, the positional
  stack #20/#71 use, here storing `i64` indices for length measurement.
- **`s.bytes()` zero-copy scan** — O(1)-indexed `Slice[u8]` view over the
  String's storage; single-byte `b'('` / `b')'` alphabet, no per-char allocation.
- **`if`-expression guards** — the DP style's `if i >= 2i64 { dp[i-2i64] } else
  { 0i64 }` boundary guards as `let`-bound expressions.
- **Dual-counter O(1) sweep** — the two-pass style's mirrored L→R / R→L scalar
  counters with the overtake-reset, zero auxiliary allocation.

---

**Bug ledger:** flat curve — the `Vec`-stack + two-pass + DP surface produced no
miscompile or front-end gap (no `B-ID` minted). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
