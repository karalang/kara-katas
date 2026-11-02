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
`bench/bench.sh` (`hyperfine`, 30 runs). Measured 2026-11-02 with karac `g96fca5370` (the
v2/MIR backend; [`bench/results.json`](bench/results.json) `measured_at`
2026-11-02T14:45Z UTC).

### Seq lane — runtime (single-threaded streaming run-length say)

| | Go | C | Rust (`-O`) | Rust (`overflow-checks=on`) | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 20.4 ms ± 0.5 | 27.4 ms ± 1.7 | 36.1 ms ± 1.5 | 36.2 ms ± 1.8 | **51.7 ms ± 3.5** | 589 ms (last measured 2026-06-18, not re-run) |
| vs Kāra | 2.53× faster | 1.89× faster | 1.43× faster | **1.43× faster (= safety)** | — | ~11.4× slower (cross-session) |

**Kāra trails the C-class here, and on the v2/MIR backend the gap widened and has stayed
wide: Kāra/Rust went 1.23× (June snapshot) → 1.10× (2026-09-07, legacy backend) → 1.44×
(2026-11-01, karac g6697158fa) → 1.43× now; Kāra/C 1.58× → 1.43× → 1.91× → 1.89×.** The
last step is flat. (Absolute times drift between sessions with machine state, so the
session-to-session story is told in ratios, not ms.) The gap is not mainly instruction
count: exact pmc counts against legacy dd86e3955 put the MIR binary at **1.06× legacy's
instructions**, close to legacy's level after
[`B-2026-10-28-43`](../../../../kara/docs/bugs-v2.md) (fixed, see the Bug ledger below). It
is **IPC**: cycles are **1.25× legacy's**. It is not the per-iteration
call-site stores: those are gone in the measured build
([`B-2026-10-31-2`](../../../../kara/docs/bugs-v2.md), fixed by kara a4ea53a5ee). The cause
is not yet attributed, and is tracked as
[`B-2026-10-31-37`](../../../../kara/docs/bugs-v2.md) (open).

Where #36/#37 (stack integer compute) put Kāra *ahead* of C and Rust, #38 is pure `String`
work — a UTF-8-correct heap buffer where C/Go/Rust drive a raw byte buffer. The June
profiling history below (legacy backend; its ms are that session's) drove two karac fixes
that speed *all* String code:

- **`String.push(char)` did a runtime encode CALL + a variable-length `memcpy`** — which LLVM
  lowers to a libc `memmove` call even to copy one byte (the profile: `memmove`/`memcpy` ~40%,
  encode ~20% of the hot time). karac now takes an **ASCII fast-path** — a codepoint `< 0x80`
  is its own single byte, stored directly, no call, no copy
  ([`B-2026-06-18-6`](../../../../kara/docs/bug-ledger.jsonl), **fixed
  [`1bb11108`](../../../../kara/docs/bug-ledger.jsonl)**): #38 65.0 → 46.3 ms at the time
  (`memmove` 324 → 36 samples, encode gone).
- **`for c in s.chars()` called `karac_string_decode_char` per character.** With the build
  side fixed, that read-side decode became the top non-allocation cost — so it got the
  **symmetric read-side fast-path**: a leading byte `< 0x80` is decoded inline (peek the byte,
  advance one), the slow runtime call only for multibyte
  ([`B-2026-06-18-7`](../../../../kara/docs/bug-ledger.jsonl), **fixed
  [`89760340`](../../../../kara/docs/bug-ledger.jsonl)**): 46.3 → 39.4 ms at the time, and
  decode dropped out of the profile entirely.
- **In June the residual to C was allocation.** Re-profiled then, the hot non-loop time was
  almost entirely `malloc`/`realloc`/`free`/`bzero` — a fresh `String` allocated and grown per
  `say` step, where C reuses one buffer. Closing it means **builder-buffer reuse across
  steps**, a deeper change (String value semantics) left as identified headroom — not claimed
  until implemented and measured. The MIR-era widening on top of that is the IPC gap above.
- **The overflow tax is small here.** `rustc -O` (36.1 ms) and `-C overflow-checks=on`
  (36.2 ms) are within 1% — character compares and byte appends, no arithmetic — so
  equal-safety Rust is 1.43× ahead of Kāra, the same as unchecked's 1.43×. Go leads (20.4 ms) on a
  tight `[]byte` loop; C (27.4 ms) and Rust (36.1 ms) follow on the same byte-buffer footing.
  (And the gap was never the char *iteration* itself: an isolated `chars()` micro-bench ran at
  C speed in June — the costs were the per-char encode/decode *calls* and the allocation.)

**No par lane — by construction.** The per-iteration say is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par-on-reduction pass does not fire. On the v2
backend neither build dispatches tasks (no call of `karac_mir_task_spawn` in either one's
`KARAC_MIR_LL` IR, checked 31 Oct 2026); the timed binary here is the `KARAC_AUTO_PAR=0` seq build, and it runs single-threaded (50.3 ms user over
51.7 ms wall).

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.16 MiB** | 1.16 MiB | 1.19 MiB | 9.52 MiB |
| binary size (seq) | 312.3 KiB | 456.0 KiB | **32.9 KiB** | 2434.1 KiB |
| compile elapsed | 125.8 ms | 98.1 ms | **52.0 ms** |
| compile peak RSS | 62.1 MiB | 28.2 MiB | **2.6 MiB** |

Each term is a heap `String`, so runtime RSS is allocator-bound; Kāra (1.16 MiB), Rust
(1.16 MiB), and C (1.19 MiB) tie to within rounding, while Go's runtime pays 9.52 MiB
(Python's interpreter measured 7.08 MiB on 2026-06-18, not re-run). Binary size: v2/MIR Kāra
binaries run well over legacy's ~34 KB (tracked as kara ledger `B-2026-10-28-36`); this one
is **312.3 KiB**, level with g6697158fa, 1.46× under Rust's 456.0 KiB and 9.5× over C's
32.9 KiB (Go's static runtime is 2.4 MiB). Compile now favours `rustc -O` over Kāra on both
elapsed (98.1 vs 125.8 ms) and peak compiler RSS (28.2 vs 62.1 MiB); clang's 52.0 ms / 2.6 MiB
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

## Bug ledger

**Surfaced [`B-2026-10-28-43`](../../../../kara/docs/bugs-v2.md)** (perf, open). On the v2/MIR backend `bench/count_and_say.kara` executes 1.67× legacy's instructions: MIR stores the panic location into a global on every loop iteration, and since the globals became `thread_local` (for auto-par correctness, `B-2026-10-26-7`) each store is a TLV-getter call. Removing the `thread_local` alone recovers ~76% of the gap. **Fixed** by kara `e1bd415c72`: each block now takes the thread-locals' address once, so the loop no longer calls the TLV getter (1.80G → 1.26G instructions, 1.18× legacy).

**Surfaced [`B-2026-10-31-2`](../../../../kara/docs/bugs-v2.md)** (perf, **fixed** by kara a4ea53a5ee). The two stores of the call site per loop trip: a library body that can abort now takes its caller's place as arguments, as legacy passed it statically, and instructions are back at legacy's count.

**Surfaced [`B-2026-10-31-37`](../../../../kara/docs/bugs-v2.md)** (perf, open). The binary runs 1.06× legacy dd86e3955's instructions but 1.25× its cycles (1.43× `rustc -O` on wall time); the cause is not yet attributed. Measured 2026-11-02 with karac g96fca5370.

**Surfaced [`B-2026-11-02-24`](../../../../kara/docs/bugs-v2.md)** (perf, low, open). This kata's seq binary stays at 312.3 KiB on g96fca5370, where 12 other kata seq binaries measured the same day are 52–69 KB.
