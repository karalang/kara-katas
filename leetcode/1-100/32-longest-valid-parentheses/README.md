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
Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded sliding-window scan)

| | C | Rust (`-O`) | **Kāra** | Rust (`overflow-checks=on`) | Go | Python |
|---|---|---|---|---|---|---|
| time | 198.4 ms | 308.9 ms | **326.8 ms** | 379.9 ms | 661.0 ms | 21444 ms |
| vs Kāra | 1.65× faster | 1.06× faster | — | **1.16× slower (Kāra wins at = safety)** | 2.02× slower | 66× slower |

**The allocation-*churn* middle ground between [#31](../31-next-permutation/) and
[#43](../43-multiply-strings/).** #31 was pure in-place compute (no heap → Kāra
ties Rust/C). #43 was allocation-*growth* (a per-result `Vec` + a 14 MB output
`String` → Kāra trailed 1.37× on the small-object path). #32 allocates a small
stack **per call and frees it immediately** — churn, not growth — so the allocator
hands back the same block and there is no sustained heap pressure. The result:
**at equal overflow safety Kāra (326.8 ms) beats Rust (379.9 ms) by 1.16×.** Kāra
traps on overflow by default (design.md § Arithmetic Overflow); the honest peer is
`rustc -C overflow-checks=on`, and Kāra's checked codegen is *cheaper* here than
Rust's (Rust's checks cost it 308.9 → 379.9 ms, +23 %; Kāra's land at 326.8). Only
wrapping `rustc -O` edges ahead (1.06×), and C's no-GC stack-`malloc` floor is
1.65× — the residual is the per-call allocation, present in every language but
cheapest in C.

**No par lane — by construction.** Although each window is computed
independently, karac's auto-par-on-reduction pass does **not** fire on this loop
(the per-call allocation + modulo reduction): verified, the default and
`KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded
(cpu 99.6 %). Per the bench-lane discipline, rayon/go-par comparators are built
only when auto-par actually fires — it does not here, so the seq lane is the whole
story.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 1.08 MiB | 1.09 MiB | **1.03 MiB** | 10.0 MiB |
| binary size (seq) | **49.6 KiB** | 456.0 KiB | 32.7 KiB | 2434.1 KiB |
| compile elapsed | **76.3 ms** | 94.6 ms | 45.7 ms |
| compile peak RSS | **13.5 MiB** | 26.8 MiB | 2.6 MiB |

The churn-not-growth shape shows in memory too: 330K per-call allocations leave
Kāra's runtime RSS (1.08 MiB) **tied with Rust** (1.09) and within rounding of C
(1.03) — the allocator recycles the freed blocks, so there is no resident slack to
surface (the opposite of #43, where holding a growing buffer surfaced 2.4× Rust's
RSS). Go's GC heap is 10 MiB by contrast. The seq compute binary references no
`String`/par-scheduler runtime, so LTO + `-dead_strip` carve it to **49.6 KiB** —
9.2× under Rust. Compile still favors Kāra over `rustc -O` on both elapsed and
peak compiler RSS.

**Where this lands.** A per-call short-lived-allocation kernel: Kāra ties Rust/C
on memory, **beats Rust at equal overflow safety** (1.16×), trails only wrapping
`rustc -O` (1.06×) and C's no-GC floor (1.65×). With #31 (no-alloc, tied) and #43
(alloc-growth, 1.37× behind), #32 completes the picture — Kāra's small-object
residual bites only under *sustained* heap growth; transient per-call churn it
handles at the systems-language floor.

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
