# 43. Multiply Strings

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Math, String, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/multiply-strings](https://leetcode.com/problems/multiply-strings/)

Given two non-negative integers as decimal strings `num1` and `num2`, return
their product as a string. You may **not** convert the inputs to integers
directly or use a bignum library — pure digit arithmetic.

```
"2"   * "3"    →  "6"
"123" * "456"  →  "56088"
```

**Constraints:** `1 ≤ num1.length, num2.length ≤ 200`; both contain only digits
and have no leading zero except `"0"` itself.

## Why this kata — the digit grid

The heavier sibling of the column-add katas
([#67 add-binary](../67-add-binary/), [#415 add-strings](../../401-500/415-add-strings/)).
Addition walks a single column; multiplication is an O(m·n) **grid** — every
digit of `a` against every digit of `b`, each partial product two columns wide.
It folds all three radix surfaces the lexer port leans on into one nested loop:

| Lexer surface | This kata |
|---|---|
| **digit char → value** (`from_str_radix`, the decimal int-literal arm) | `(b - b'0') as i64` over both operands' `bytes()` |
| **base-N accumulation / carry** | `sum = a[i]·b[j] + res[i+j+1]`; `res[i+j+1] = sum % 10`; `res[i+j] += sum / 10` |
| **value → digit glyph** (the inverse nibble map; §3 slice render) | `DIGITS[d..d+1]` one-byte zero-copy slice, `push_str` |
| **no-bignum constraint** | products exceed any native int width; arithmetic stays per-digit |

This is the stress pick from §4 of the
[lexer-stress order](../../../wip-lexer-stress.md) — "heavier digit-grid
arithmetic (stress, not just smoke)" — on top of the smoke-test radix katas
(#67/#415/#405/#171) it builds on. The grid slot can transiently exceed 9 (it is
summed across several `(i,j)` pairs); the `% 10` / `/ 10` redistribution on the
next column that reaches it keeps the per-digit invariant — a tighter carry
dance than the single-column adds.

## Approaches

Two styles, both byte-identical to the Python oracle across all 17 cases, under
`karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Grid — flat `Vec[i64]` of m+n columns** ★ | [`multiply_strings.kara`](multiply_strings.kara) | the canonical no-scratch form: `a[i]·b[j]` lands in columns `(i+j, i+j+1)`, carries ripple left in place, strip leading zeros, render |
| Add-and-shift | [`multiply_strings_addshift.kara`](multiply_strings_addshift.kara) | multiply `a` by each single digit of `b`, shift left by its column, and **add** the partials — `multiply` built directly on #415's column add as a subroutine |

The grid style is the tighter algorithm (one `Vec`, in-place carry); the
add-shift style is the more compositional one — it reuses the exact `add_strings`
column add from #415 as its accumulation step, `m` invocations over the digits of
`b`. Both read operands through the zero-copy [`bytes()`](../../../README.md)
view and emit each digit as a one-byte slice of the const table — no per-char
byte→char cast (which `karac check` rejects as `E_INT_AS_CHAR`; see #415/#67).

## What this kata uncovered

**Flat curve — no `karac` bug.** Like the radix katas it sits on, the whole
two-dimensional digit grid compiled and ran first-try under both backends: the
nested `Vec[i64]` accumulation, `res[lo] = sum % 10` / `res[hi] += sum / 10`
in-place column updates, `d1 · d2` partial products, the `DIGITS[d..d+1]` render,
and the long-operand cases — `"99…9"(20) * "99…9"(20)` and two 20-digit operands
— whose 40-digit products exceed any native int width (the no-bignum point: proof
the arithmetic really is per-digit). The add-shift style additionally exercised a
`String`-returning helper (`mul_one`) feeding `add_strings` `m` times, plus the
final `acc[p..len]` leading-zero strip — all on the same hardened zero-copy-slice
+ `push_str` path #722/#415 already cleared.

The run-path footgun the radix katas carried — `byte as char` being a typecheck
*error* (`E_INT_AS_CHAR`) that an older `karac run` ran through with a placeholder
([`B-2026-06-13-15`](../../../../kara/docs/bug-ledger.md), fixed `b59eb070`) — does
not bite here: the digit emit is a table slice by construction, and the kata is
gated on `karac check` before its `karac run` output is trusted.

## Benchmarks

Workload: a fixed 38-digit operand multiplied by `decimal(k)` for **`TOTAL=300 000`**
distinct `k`, every product-string concatenated into one growing buffer, then
byte-checksummed (sink `742 591 719`). Persisting the output defeats
allocation-elision — a per-result byte-sum lets `rustc`/`clang`/`go` fold the heap
`String` away, but a buffer that is built up and then observed cannot be elided.
This is a **sequential string-building** workload (the lexer's real shape); the
build carries a loop-borne dependency on the buffer, so it does not
auto-parallelize (seq-only by construction). Apple M5 Pro; `bench/bench.sh`
(`hyperfine`).

### Seq lane — runtime (single-threaded grid multiply + string build)

| | C | Go | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 92 ms | 233 ms | 200 ms | 229 ms | **272 ms** | 6995 ms |
| vs Kāra | 2.96× faster | 1.17× faster | 1.36× faster | 1.19× faster | — | 25.7× slower |

**The arithmetic-bound counterpoint to [#415](../../401-500/415-add-strings/).**
Add-strings was allocation-bound — the overflow-safety tax was ~0 (`-C
overflow-checks=on` moved Rust only 181→184 ms) and Kāra tied Rust at equal
safety. The multiply **grid** flips that: each product does ~380 `d1·d2` partial
products + carry redistributions (m·n, not m+n), so the work is genuinely
arithmetic-heavy, and the overflow-safety tax is now **real** — `-C
overflow-checks=on` costs Rust **200 → 229 ms (+15 %)**. Kāra traps on overflow by
default (design.md § Arithmetic Overflow); `rustc -O` silently wraps, so the
200 ms figure is apples-to-oranges. **At equal overflow safety Kāra is 1.19× Rust**
(272 vs 229 ms) — the residual is not the arithmetic but the same small-object-allocation + codegen gap
the radix-render katas name ([#405](../../401-500/405-convert-a-number-to-hexadecimal/)'s
`~1.4×`, [phase-7-codegen.md](../../../../kara/docs/implementation_checklist/phase-7-codegen.md)),
here riding on top of the grid's per-result `Vec[i64]` allocation. C is the
no-heap floor (2.97×): it renders into a stack buffer and never allocates per
result; Kāra/Rust/Go all build a `String`.

**No par lane — by construction (like its add-sibling #415).** This is a string
*build*: `out.push_str(product)` carries a loop-borne dependency on the buffer,
so karac's auto-par-on-reduction pass does not fire — verified here, the default
and `KARAC_AUTO_PAR=0` binaries agree on the sink and both run single-threaded
(cpu 99 %). The property that makes the output un-elidable (you must build the
whole buffer before observing it) also makes it un-parallelizable. The grid's
inner double loop *is* compute-dense, but it feeds one shared accumulator.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **15.9 MiB** | 16.3 MiB | 1.0 MiB | 48.3 MiB |
| binary size (seq) | **295 KiB** | 456 KiB | 33 KiB | 2434 KiB |
| compile elapsed | **92 ms** | 119 ms | 55 ms |

Same shape as #415's memory counterpoint: both hold the ~14 MB product buffer,
and Kāra's `String`/`Vec` growth now tracks Rust's almost exactly
— **0.97× Rust's RSS** (15.9 vs 16.3 MiB), a hair *under*. Compile still favors Kāra — cold compile
92 ms edges `rustc -O` (119 ms), and the 295 KiB binary is 1.5× smaller than
Rust's 456 KiB (and 8× smaller than Go's 2.4 MiB).

**Where this lands.** An arithmetic-bound digit grid: Kāra trails Rust 1.19× at
equal overflow safety (vs the 1.36× wrap-vs-trap headline) while now **tying Rust on memory**
(0.97×, a hair under) — the small-object-allocation gap shows only in runtime now — while beating Rust on compile and binary.
The honest pairing with #415: the same render path, but moving the workload from
allocation-bound (where Kāra ties) to arithmetic-bound (where the checked-arith +
small-alloc residual shows) maps exactly where Kāra's codegen still has road left.

## Kāra features exercised

- **`bytes()` byte scan + indexing** — nested reverse walk over both operands,
  `b'0'` byte literal, `(b - b'0') as i64` widening cast.
- **Two-dimensional carry arithmetic** — `Vec[i64]` of m+n columns, in-place
  `res[lo] = sum % 10` / `res[hi] += sum / 10`, transient slot > 9 redistributed
  on the next column; correct for products wider than any native int.
- **Digit-table render** — `DIGITS[d..d+1]` one-byte zero-copy slice +
  `push_str`, the inverse nibble map of digit parsing (both styles).
- **Compositional reuse** — the add-shift style reuses #415's `add_strings`
  column add verbatim as its accumulation subroutine, plus a single-digit×bignum
  `mul_one` carry chain with a `10^shift` trailing-zero factor.

---

**Bug ledger:** the codegen/radix-grid surface was a flat curve (no miscompile);
shares **`B-2026-06-13-15`** with #67/#415 (the `karac run` type-leniency footgun
on the `byte as char` digit emit) — already fixed (`b59eb070`). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
