# 38. Count and Say

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** String, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/count-and-say](https://leetcode.com/problems/count-and-say/)

The **count-and-say** sequence starts at `countAndSay(1) = "1"`; each later term is the
**run-length encoding** of the previous one, read aloud as `"<count><digit>"` for every
maximal run of equal digits. Read `"3322251"` as *"two 3s, three 2s, one 5, one 1"* →
`"23321511"`. So each term literally **says** the one before it:

```
n   countAndSay(n)        read the previous term aloud
1   1
2   11                    one 1
3   21                    two 1s
4   1211                  one 2, one 1
5   111221                one 1, one 2, two 1s
6   312211                three 1s, two 2s, one 1
7   13112221              one 3, one 1, two 2s, two 1s
```

**Constraints:** `1 ≤ n ≤ 30`. Each term is a digit string; the transform is pure string
work — no arithmetic beyond counting.

## Why this kata — pure string transformation, three ways to read a run

After [#36](../36-valid-sudoku/) and [#37](../37-sudoku-solver/) — both **allocation-free**
fixed-grid integer compute — #38 is the deliberate counterpoint: it is **all string
building**. Each step reads the previous term character by character and writes a *growing*
new term, so the work is per-`char` iteration plus `String` heap growth, not stack
arithmetic. There is no search and no math; the only question is **how you read a run** and
**how you unfold the n steps**.

A "run" is a maximal stretch of one repeated digit. Encoding a term is: find each run,
emit its length then its digit. Two axes vary across the three styles — **how the run is
measured** (a streaming state machine vs an explicit two-pointer span) and **how the n-1
encodes are unfolded** (a loop vs recursion) — and everything else (start from `"1"`, emit
`<count><digit>`) is shared.

| Lens | Idea |
|---|---|
| **Streaming state machine** ★ | one left-to-right pass carrying `(run_digit, run_len)`; extend the run on a match, else flush `"<len><digit>"` and open a new run; one final flush |
| **Recursive unfolding** | the definition written literally — `countAndSay(1) = "1"`, `countAndSay(n) = say(countAndSay(n-1))`; same streaming encode, recursion replaces the loop |
| **Indexed two-pointer** | collect the term into a `Vec[char]` for O(1) access, then group runs with indices: left pointer `i` at a run's start, right pointer `j` walks while `chars[j] == chars[i]`; the run length is `j - i` |

## Approaches

Three styles, all agreeing with the Python oracle for `countAndSay(1..12)` under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Streaming state machine** ★ | [`count_and_say.kara`](count_and_say.kara) | `for c in s.chars()`, carry `(run_digit, run_len)`, flush `"<len><digit>"` on each run boundary; loop the encode n-1 times |
| Recursive unfolding | [`count_and_say_rec.kara`](count_and_say_rec.kara) | `if n == 1 { "1" } else { say(count_and_say(n-1)) }` — the same streaming `say`, recursion instead of a loop |
| Indexed two-pointer | [`count_and_say_indexed.kara`](count_and_say_indexed.kara) | `let chars: Vec[char] = s.chars().collect();` then `while j < n and chars[j] == chars[i] { j += 1 }`, emit `"<j-i><chars[i]>"` |

The streaming form is the tightest (one pass, no materialization); the recursive form is the
most literal transcription of the sequence's definition; the indexed form makes the run
boundaries visible as index spans, at the cost of materializing each term as a `Vec[char]`
for random access. All three are O(total output length) per step and agree on every term.

## What this kata surfaced

**`s.chars().collect()` into a `Vec[char]` failed codegen**
([`B-2026-06-18-1`](../../../../kara/docs/bug-ledger.jsonl), `kata:38`, codegen, **fixed
[`e272ed42`](../../../../kara/docs/bug-ledger.jsonl)**). The indexed two-pointer style needs
O(1) random access to the term's characters — and the idiomatic Kāra form for that is
exactly `let chars: Vec[char] = s.chars().collect()` (the pattern
[`valid_palindrome.kara`](../../../../kara/examples/leetcode/valid_palindrome.kara)
documents as *the* right one "whenever a loop needs `s[i]` and `s[j]`"). That form **ran**
fine under the interpreter but **built**-failed: *"no handler for method 'collect' on
non-identifier receiver."* Codegen has no general iterator/`collect` lowering — the
chars-iterator value is unsupported, and `collect` on a non-identifier receiver (here the
`.chars()` call) fell through to the dispatch-fail error. A program that runs should build,
so the run/build divergence was the defect.

**The fix lowers the idiom to a form codegen already handles.** `for c in s.chars() {
v.push(c) }` builds fine, so `compile_method_call` now detects `<string>.chars().collect()`
and synthesizes exactly that block — reusing the `.chars()` call verbatim as the loop
iterable — then compiles it. The `Vec[char]` annotation makes the let-binding handler
register the element type at codegen time (no typechecker dependency), so `push` dispatches
and the block's move-out hands back the freshly built Vec exactly as a `fn() -> Vec[char]`
would. No new low-level Vec/iterator codegen — it reuses the tested for-chars + push +
block-return paths. So the indexed solver now builds in its natural form; the streaming and
recursive styles never needed it.

**Probing the `String` API for this kata turned up three more gaps** (one fixed, two filed),
all visible through karac's own
[`valid_palindrome.kara`](../../../../kara/examples/leetcode/valid_palindrome.kara), which
documents the very char-iteration idioms #38 exercises yet did not build:

- **`for c in <String>` mistyped the loop variable** as `String` / `ref String` instead of
  `char` ([`B-2026-06-18-2`](../../../../kara/docs/bug-ledger.jsonl), typecheck, **fixed
  [`a658f238`](../../../../kara/docs/bug-ledger.jsonl)**) — a typechecker/codegen mismatch
  (codegen already binds the decoded codepoint as `char`), so `for c in s { c.is_alphabetic() }`
  ran but did not build. The fix maps a String iterable's element type to `char` in
  `element_type_of`; `for c in s` now binds `char` and the existing char predicates dispatch.
- **`s.char_at(i)` / `s.char_count()` are unimplemented** end-to-end
  ([`B-2026-06-18-3`](../../../../kara/docs/bug-ledger.jsonl), **open**) — the typechecker
  rejects them and they do not function under the interpreter, so the O(n) Unicode-aware
  access pair `design.md` documents (and `valid_palindrome.kara` centers on) is unavailable.
- **`char.is_uppercase()` / `is_lowercase()` have no codegen handler**
  ([`B-2026-06-18-4`](../../../../kara/docs/bug-ledger.jsonl), **open**) — the sibling
  predicates `is_alphabetic` / `is_numeric` / `is_alphanumeric` / `is_whitespace` are wired,
  these two are not. (Plus [`B-2026-06-18-5`](../../../../kara/docs/bug-ledger.jsonl) — a
  bound `let it = s.chars()` value still isn't materializable in codegen, the narrower
  sibling of the fixed collect lowering.)

#38 itself builds and runs in all three styles regardless — it reaches char access through
`.chars().collect()` + indexing (fixed above) and `for c in s.chars()`, none of which depend
on the open items.

## Benchmarks

Workload: count-and-say generalized to an arbitrary digit seed (the say-transform is
well-defined on any digit string). **`TOTAL = 12000`** times, seed the sequence with the
decimal digits of `k + 1` (a per-iteration seed, so nothing hoists), apply **`STEPS = 14`**
streaming run-length steps, and fold a **position-weighted** digit signature of the final
term — `sum digit_value*(i+1)` — into a rolling checksum (sink `994339104`). The seed varies
with the loop index (no comparator can hoist the work out), and the checksum carries a
loop-borne dependency, so this is a single-lane (seq) bench by construction. Run lengths in
this workload never exceed 9 (the seeds are ≤ 5 digits and count-and-say keeps runs short —
verified max 5), so every mirror appends the count as a **single digit in place** — the hot
path is allocation-free across all five languages, isolating the run-length-encode +
String-growth codegen from each stdlib's integer-formatting path. Unlike #36/#37 this is a
**heap-allocating** workload (each term is a fresh growing `String`). Apple M5 Pro;
`bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded streaming run-length say)

| | Go | C | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 18.8 ms | 25.0 ms | 32.0 ms | 32.7 ms | **39.4 ms** | 589 ms |
| vs Kāra | 2.10× faster | 1.58× faster | 1.23× faster | **1.21× faster (= safety)** | — | 14.9× slower |

**Kāra trails the C-class here — but the gap is runtime/codegen overhead, not the algorithm
or anything fundamental, and profiling it drove *two* karac fixes that closed most of it
(65.0 → 39.4 ms).** Where #36/#37 (stack integer compute) put Kāra *ahead* of C and Rust, #38
is pure `String` work — a UTF-8-correct heap buffer where C/Go/Rust drive a raw byte buffer.
Profiling the binary (leaf-time samples) found the gap was several overheads C structurally
avoids, two of them straight-line fixes:

- **`String.push(char)` did a runtime encode CALL + a variable-length `memcpy`** — which LLVM
  lowers to a libc `memmove` call even to copy one byte (the profile: `memmove`/`memcpy` ~40%,
  encode ~20% of the hot time). karac now takes an **ASCII fast-path** — a codepoint `< 0x80`
  is its own single byte, stored directly, no call, no copy
  ([`B-2026-06-18-6`](../../../../kara/docs/bug-ledger.jsonl), **fixed
  [`1bb11108`](../../../../kara/docs/bug-ledger.jsonl)**): #38 65.0 → 46.3 ms (`memmove` 324 →
  36 samples, encode gone).
- **`for c in s.chars()` called `karac_string_decode_char` per character.** With the build
  side fixed, that read-side decode became the top non-allocation cost — so it got the
  **symmetric read-side fast-path**: a leading byte `< 0x80` is decoded inline (peek the byte,
  advance one), the slow runtime call only for multibyte
  ([`B-2026-06-18-7`](../../../../kara/docs/bug-ledger.jsonl), **fixed
  [`89760340`](../../../../kara/docs/bug-ledger.jsonl)**): 46.3 → 39.4 ms, and decode drops
  out of the profile entirely. Both fixes speed *all* String code, not just this kata.
- **The residual 1.58× to C is now purely allocation.** Re-profiled, the hot non-loop time is
  almost entirely `malloc`/`realloc`/`free`/`bzero` — a fresh `String` allocated and grown per
  `say` step, where C reuses one buffer. Closing it means **builder-buffer reuse across
  steps**, a deeper change (String value semantics) left as identified headroom — not claimed
  until implemented and measured.
- **The overflow tax is ~zero here.** `rustc -O` (32.0 ms) and `-C overflow-checks=on`
  (32.7 ms) are within ~2% — character compares and byte appends, no arithmetic — so
  equal-safety Rust is 1.21× ahead, the same as unchecked. Go leads (18.8 ms) on a tight
  `[]byte` loop; C (25.0 ms) and Rust (32.0 ms) follow on the same byte-buffer footing. (And
  the gap was never the char *iteration* itself: an isolated `chars()` micro-bench runs at C
  speed — the costs were the per-char encode/decode *calls* and the allocation, now two-thirds
  addressed.)

**No par lane — by construction.** The per-iteration say is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not fire: the
default and `KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.13 MiB** | 1.13 MiB | 1.17 MiB | 8.70 MiB |
| binary size (seq) | 33.5 KiB | 456.0 KiB | **32.9 KiB** | 2434.1 KiB |
| compile elapsed | 74.8 ms | 93.0 ms | **47.0 ms** |
| compile peak RSS | 13.8 MiB | 28.2 MiB | **2.5 MiB** |

Each term is a heap `String`, so runtime RSS is allocator-bound; Kāra (1.13 MiB), Rust
(1.13 MiB), and C (1.17 MiB) tie to within rounding, while Go's runtime pays 8.70 MiB and
Python's interpreter 7.08 MiB. The seq compute binary references no par-scheduler runtime, so
LTO + `-dead_strip` carve it to **33.5 KiB** — 13.6× under Rust and within a rounding of C's
32.9 KiB (Go's static runtime is 2.4 MiB). Compile favours Kāra over `rustc -O` on both
elapsed (74.8 vs 93.0 ms) and peak compiler RSS (13.8 vs 28.2 MiB); clang's 47.0 ms / 2.5 MiB
is the toolchain floor.

## Kāra features exercised

- **`s.chars().collect()` into a `Vec[char]`** — the indexed two-pointer style materializes
  each term for O(1) random access, the idiomatic form surfaced (and fixed) as
  [`B-2026-06-18-1`](../../../../kara/docs/bug-ledger.jsonl); now builds, with `chars[i]` /
  `chars[j]` indexing and `chars.len()`.
- **Per-`char` String iteration** — `for c in s.chars()` binds each Unicode scalar as a
  `char`, with `char` equality (`c == run_digit`) driving the run state machine and
  `(c as i64) - ('0' as i64)` recovering a digit's value for the checksum.
- **Growing `String` via `push` / `push_str`** — each term is built incrementally
  (`out.push(digit_char)`, `out.push(run_digit)`), the heap-allocating counterpart to
  #36/#37's stack scratch — so this kata isolates string-building codegen.
- **`char.try_from((n + 48) as u32)`** — the checked int→`char` digit conversion (a bare
  `n as char` is rejected — not every integer is a valid scalar), used to emit a run's
  single-digit count.
- **Three factorings of one transform** — streaming state machine, recursive unfolding, and
  indexed two-pointer grouping, all agreeing across `countAndSay(1..12)` under both
  `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-18-1`](../../../../kara/docs/bug-ledger.jsonl) (`kata:38`,
codegen, **fixed `e272ed42`**) — `s.chars().collect()` into a `Vec[char]` (the idiomatic
O(1)-indexed-char form) failed codegen with *"no handler for method 'collect' on
non-identifier receiver"* though it ran fine under the interpreter; the fix lowers
`<string>.chars().collect()` to the already-supported `for c in s.chars() { v.push(c) }`
build. See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
