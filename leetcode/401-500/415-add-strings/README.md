# 415. Add Strings

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math, String, Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/add-strings](https://leetcode.com/problems/add-strings/)

Given two non-negative integers as decimal strings `num1` and `num2`, return
their sum as a string. You may **not** convert the inputs to integers directly
or use a bignum library — pure digit arithmetic.

```
"11"  + "123"  →  "134"
"456" + "77"   →  "533"
```

**Constraints:** `1 ≤ num1.length, num2.length ≤ 10⁴`; both contain only digits
and have no leading zero except `"0"` itself.

## Why this kata — base-10 radix arm + digit table

The base-10 sibling of [#67 add-binary](../../1-100/67-add-binary/). Same
column-add carry machinery, but base 10 brings in the piece base 2 didn't need:
a **digit table**. The emitted digit indexes a const `"0123456789"`, the inverse
nibble map of digit *parsing* — exactly the render shape #405 convert-to-hex and
#168 excel-column use to turn a value back into a glyph.

| Lexer surface | This kata |
|---|---|
| **digit char → value** (`from_str_radix`, the decimal int-literal arm) | `(b - b'0') as i64` over the operands' `bytes()` |
| **base-N accumulation / carry** | `sum = carry + da + db`; `digit = sum % 10`; `carry = sum / 10` |
| **value → digit glyph** (the inverse nibble map; §3 slice render) | `DIGITS[d..d+1]` one-byte zero-copy slice, `push_str` |
| **no-bignum constraint** | operands exceed any native int width; arithmetic stays per-digit |

This is item #4 of the [lexer-stress order](../../../../kara/docs/implementation_checklist/phase-12-self-hosting.md),
paired with #67: base-2 isolates the carry; base-10 adds the 10-symbol table.

## Approaches

Two styles, both byte-identical to the Python oracle across all 14 cases,
under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Two-pointer — LSB-first + reverse** ★ | [`add_strings.kara`](add_strings.kara) | walk both ends inward; push digit values into a `Vec[i64]`, reverse and render through the digit table |
| Recursive descent | [`add_strings_recursive.kara`](add_strings_recursive.kara) | `add_at(i, j, carry) -> String` recurses on the higher-order digits first, then appends the current digit — MSB-first, no reversal |
| Reference oracle | [`add_strings.py`](add_strings.py) | known-correct LeetCode answer |

Both read the operands through the zero-copy [`bytes()`](../../../README.md)
view and emit each digit as a one-byte slice of the const table — no per-char
byte→char cast (which `karac check` rejects as `E_INT_AS_CHAR`; see below). The
two-pointer style buffers digit values LSB-first and reverses; the recursive
style lets the call stack carry the order and emits MSB-first.

## What this kata uncovered

**Flat curve — no `karac` bug.** Like its base-2 sibling, the whole base-10
surface compiled and ran first-try under both backends: `Vec[i64]` buffer,
`(b - b'0') as i64` widening, `% 10` / `/ 10` carry arithmetic, the
`DIGITS[d..d+1]` digit-table slice render via `push_str`, recursion with a
`(i, j, carry)` frame, and the long-operand cases that exceed any native int
width (the no-bignum point — proof the arithmetic really is per-digit). The
radix-render table sits on the same zero-copy-slice + `push_str` path #722
remove-comments already hardened.

The run-path footgun carried from #67 — [`B-2026-06-13-15`](../../../../kara/docs/bug-ledger.md):
emitting a digit with a `byte as char` cast is a typecheck *error*
(`E_INT_AS_CHAR`), but **`karac run` was type-lenient** — it downgraded hard type
errors to warnings and ran anyway with a placeholder value → silent wrong
output, exit 0. **Fixed in karac `b59eb070`:** `run` now aborts on the
value-corrupting cast family, matching `build`/`check` (soft type errors keep
their leniency). The emit is a digit-table slice regardless — the idiomatic form
— and the kata is gated on `karac check` before its `karac run` output is
trusted.

## Benchmarks
Workload: a fixed 38-digit operand added to `decimal(k)` for **`TOTAL=500 000`**
distinct `k`, every sum-string concatenated into one growing buffer, then
byte-checksummed (sink `1 000 513 006`). Persisting the output defeats
allocation-elision — a per-result byte-sum lets `rustc`/`clang`/`go` fold the
heap `String` away, but a buffer that is built up and then observed cannot be
elided. This is a **sequential string-building** workload (the lexer's real
shape); the build carries a loop-borne dependency on the buffer, so it does not
auto-parallelize (seq-only by construction). Apple M5 Pro; `bench/bench.sh`
(`hyperfine`).

### Seq lane — runtime (single-threaded string build)

M5 Pro, 2026-11-04, karac `0.8.0-dev.14370+gd33cb285d` (gd33cb285d, the v2/MIR backend), `KARAC_AUTO_PAR=0`:

| | C | Go | Rust (`-O`) | **Kāra** | Rust (`overflow-checks=on`) | Python |
|---|---|---|---|---|---|---|
| time | 32.8 ± 0.5 ms | 135.0 ± 2.9 ms | 201.0 ± 5.4 ms | **203.1 ± 7.3 ms** | 210.4 ± 7.5 ms | 1924 ms *(last measured 2026-06-15, not re-run)* |
| vs Kāra | 6.19× faster | 1.50× faster | 1.01× faster | — | 1.04× slower | not re-run |

**At equal overflow safety, Kāra reads 0.97× Rust, and 1.01× `rustc -O`**, from 1.16×
`rustc -O` on the 2026-07-28 feed. Exact counts are 0.90× legacy dd86e3955's
(`KARAC_AUTO_PAR=0`). Kāra traps on integer overflow by default (design.md § Arithmetic
Overflow); `rustc -O` silently wraps. Here that costs little —
`-C overflow-checks=on` moves Rust only 201 → 210 ms (+5 %) — because the work is
**allocation-bound, not arithmetic-bound**: the column add is a stream of single-digit
sums that never overflow. The `DIGITS[d..d+1]` render rides the same now-truly-zero-copy
`push_str`-borrow path (karac `08ae0140`) that #722 remove-comments and #405
convert-to-hex measured — appended through a `{ptr, len, cap: 0}` view, no temp
per digit. C is the bare-metal floor (6.19×): it renders into a stack buffer and
**never allocates per result at all**, and its mirror keeps a running byte-sum rather
than a growing buffer, so the gap is "Kāra/Rust build a `String`; C doesn't," not the
same task.

**No par lane — by construction (unlike its slice-partner [#722](../../701-800/722-remove-comments/)).**
This is a string *build*: `out.push_str(r)` carries a loop-borne dependency on
the buffer, so karac's auto-par-on-reduction pass does not fire — verified here,
(on gd33cb285d, 2026-11-04) the default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run
single-threaded. The same property that makes the output un-elidable (you must
build the whole buffer before observing it) also makes it un-parallelizable.
#722's outer reduction over *independent* passes is the shape that auto-pars; an
accumulate-into-one-buffer render, like #415 and #405, is sequential.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | 20.6 MiB | **20.6 MiB** | 1.0 MiB | 62.2 MiB |
| binary size (seq) | **66.9 KiB** | 455.7 KiB | 32.8 KiB | 2434.2 KiB |
| compile elapsed | 110.1 ms | 96.7 ms | 49.0 ms | — |

The honest counterpoint to #722 (where Kāra was the memory floor): here Kāra's
peak RSS is **at parity with Rust's** (20.6 MiB each). Both hold the ~19 MB output
buffer, and the per-object slack that the **small-object-allocation overhead** target
names ([`phase-7-codegen.md`](../../../../kara/docs/implementation_checklist/phase-7-codegen.md))
does not separate them on memory here. Wall clock is level too (1.01× `rustc -O`, 0.97×
at equal overflow safety), so that overhead no longer shows on speed in this run. Cold
compile takes 1.14× `rustc -O`'s time (110.1 vs 96.7 ms), and the 68,536 B binary is
6.8× smaller than Rust's.

**Where this lands.** A clean allocation-bound string-build: Kāra is level with Rust
on speed at equal overflow safety and on memory, smaller on binary, and slightly behind
on compile. The render is the lexer's `from_str_radix`-inverse glyph path, on the
hardened zero-copy slice.

## Kāra features exercised

- **`bytes()` byte scan + indexing** — two-pointer reverse walk, `b'0'` byte
  literal, `(b - b'0') as i64` widening cast.
- **Base-10 carry arithmetic** — `sum % 10` / `sum / 10`, the decimal
  `from_str_radix` core; correct across operands wider than any native int.
- **Digit-table render** — `DIGITS[d..d+1]` one-byte zero-copy slice +
  `push_str`, the inverse nibble map of digit parsing (two-pointer + recursive
  both).
- **`Vec[i64]` accumulate + reverse** — buffer digit values LSB-first, walk
  back to front (two-pointer style).
- **Recursion with a scalar frame** — `add_at(i, j, carry)` recurses on the
  high-order digits before appending the current one (recursive style).

---

**Bug ledger:** the codegen/radix surface was a flat curve (no miscompile);
shares **`B-2026-06-13-15`** with #67 (the `karac run` type-leniency footgun on
the `byte as char` digit emit) — fixed (`b59eb070`): `run` now aborts on
value-corrupting casts. See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
