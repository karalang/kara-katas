# 171. Excel Sheet Column Number

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Math, String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/excel-sheet-column-number](https://leetcode.com/problems/excel-sheet-column-number/)

Given an Excel column title (`"A"`, `"AB"`, `"ZY"`, …) return its 1-based column
number: `A → 1`, `B → 2`, …, `Z → 26`, `AA → 27`, `AB → 28`, …, `ZY → 701`.

```
"A"   →  1
"AB"  →  28
"ZY"  →  701
```

**Constraints:** `1 ≤ title.length ≤ 7`; uppercase `A`–`Z`; the result fits in a
signed 32-bit int (`"FXSHRXW" → 2147483647`).

## Why this kata — bijective base-26 *parse* (the lexer's `from_str_radix`)

This is the **parse** direction — char → value — exactly the self-hosted lexer's
`from_str_radix` accumulation, but over a **bijective base 26** (there is no zero
digit, so each digit subtracts a `'A'`-relative 1-offset):

```
n = n * 26 + (c - 'A' + 1)        most-significant char first (Horner fold)
```

It is the inverse of the **render** direction that its slice-partner
[#405 convert-to-hex](../../401-500/405-convert-a-number-to-hexadecimal/) covers
(value → glyph). Both kata files also carry a `to_title` round-trip render (the
LeetCode [#168](https://leetcode.com/problems/excel-sheet-column-title/)
direction) as a **second, self-checking oracle**: `to_title(to_number(t)) == t`.

| Lexer surface | This kata |
|---|---|
| **digit char → value** (`from_str_radix`, the int-literal arm) | `(b - b'A') as i64 + 1` over the title's `bytes()` |
| **base-N accumulation** | `n = n * 26 + digit` (Horner fold / recursion) |
| **value → digit glyph** (round-trip, the #168 render) | `LETTERS[d..d+1]` slice, bijective `n -= 1; n % 26; n /= 26` |

## Approaches

Two parse styles + a shared round-trip render, all byte-identical to the Python
oracle across all 11 titles, under `karac run` **and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Horner fold** ★ | [`column_number.kara`](column_number.kara) | left-to-right byte walk, `n = n*26 + (b - 'A' + 1)` |
| Recursive descent | [`column_number_recursive.kara`](column_number_recursive.kara) | `value_to(tb, i)` recurses on the prefix first, folds the current digit on the way out |
| Reference oracle | [`column_number.py`](column_number.py) | known-correct LeetCode answer + round-trip render |

## What this kata uncovered

**Flushed a HIGH auto-par miscompile — [`B-2026-06-13-18`](../../../../kara/docs/bug-ledger.md).**
The kata's `main` prints the 11 parse results, then a `"--- round-trip ---"`
separator, then 11 render lines. Under `karac build` the separator surfaced at
the **top** of the output instead of between the two loops — and, on closer
inspection, the ordering was **nondeterministic** run-to-run.

The IR placed every `println` in the right basic block, so it was not a
statement-ordering miscompile. The cause was **auto-parallelization**: the
analyzer grouped the consecutive `println` statements into a `parallel_group`
("no data or effect dependencies") and fanned them into `__par_branch` workers
that **raced on the one shared stdio stdout buffer**. Output is correct on a tty
(line-buffered, narrow race window) but reorders when stdout is a pipe/file
(fully buffered) — which is exactly the oracle-diff harness.

Root cause: the print builtins (`println` / `print` / `eprintln`) are
compiler-side I/O functions that carry **no resource effect** — making `println`
a `writes(Stdout)` effect would force every public fn that prints to *declare*
it, a surface break the language avoids. So to the effect-conflict gate two
`println`s look effect-free and independent. Console output, like a channel op,
is an ordering-sensitive side effect the resource-effect system doesn't model.

Fixed in karac `48145ad4`, mirroring the existing `stmt_has_channel_op` guard:

1. **`stmt_has_output_op`** — an AST guard that flags a statement directly
   containing a `println`/`print`/`eprintln` or a `Stdout`/`Stderr` write.
2. **`output_fns`** — a call-graph fixpoint of functions that *transitively*
   print. This kata's `to_number`-style helpers don't print, but the bug has a
   sharper transitive form: a value-returning helper that prints **and** carries
   a non-conflicting real effect (`writes(A)` vs `writes(B)`) escapes the
   `all_pure → trivial` cost gate and *would* be fanned out, reordering the
   prints buried inside it. The fixpoint serializes those call sites too.
3. **`find_parallel_groups`** excludes any output-emitting statement (direct or
   transitive) from both the seed and candidate positions of a group.

Pure compute with no output still parallelizes — the guard is precise, not a
blanket "any call serializes." Regression tests cover the direct, transitive,
and no-over-suppression cases.

The base-26 surface *itself* was a flat curve: the Horner fold, the recursive
prefix fold, the bijective `n -= 1` render, and the `LETTERS[d..d+1]` slice all
compiled first-try. The bug was in the **harness around** the algorithm — the
print sequence — which is exactly the kind of defect a multi-line-output kata is
positioned to flush.

## Benchmarks

Workload: parse a corpus of **50,000 distinct titles** (built once via `to_title`,
too many for an optimizer to tabulate) round-robin **10⁸ times**, reducing to the
summed column numbers (sink `2 500 050 000 000`). The parse is pure arithmetic —
**compute-bound**, a clean read on tight-loop codegen. Apple M5 Pro (6P+12E),
2026-11-01, karac g6697158fa (v2/MIR backend); `bench/bench.sh` (`hyperfine`,
30 runs seq / 50 runs par).

### Seq lane — runtime (single-threaded)

| | C | Rust (`-O`) | **Kāra** | Go | Rust (`-C overflow-checks=on`) |
|---|---|---|---|---|---|
| time | 150.5 ms | 156.4 ms | **292.1 ms** | 170.7 ms | 267.3 ms |
| vs Kāra | 1.94× faster | 1.87× faster | — | 1.71× faster | **1.09× faster** |

Against the previous M5 feed (karac 0.1.0, legacy backend, 2026-07-28) this is a
~1.1× slip relative to every comparator: Kāra/Rust 1.66× → 1.87×, Kāra/C 1.74× →
1.94×, Kāra/Go 1.54× → 1.71× (every comparator also ran ~15% slower in absolute
terms this session, so compare ratios, not milliseconds).

**Read the two Rust columns together — this is the whole story.** Kāra traps on
integer overflow *by default* (design.md § Arithmetic Overflow: "defined
behavior, never undefined"); `rustc -O` **silently wraps**. That safety is not
free: turning it on in Rust (`-C overflow-checks=on`) costs Rust **1.71×**
(156 → 267 ms) — most of the gap to Kāra. **At equal overflow safety, Kāra
trails Rust by 1.09×** (it was at parity on the July feed). Most of the 1.87×
against `rustc -O`'s default is the price of a silent-wraparound class of bugs
Kāra refuses to ship and Rust release opts out of. (C and Go also wrap; they are
the unsafe-but-fast floor, not safety peers.)

### Par lane — auto-par vs hand-tuned parallelism (multi-core)

The `sum += to_number(corpus[k % LEN])` reduction over independent iterations is
embarrassingly parallel. Every implementation parallelizes that *same* reduction
— the difference is what the programmer had to write:

| | parallel code written | time |
|---|---|---|
| C + pthreads *(metal floor)* | raw `pthread_create`/`join` + chunk + merge | 16.7 ms |
| Rust + rayon | `rayon` crate + `.into_par_iter()` rewrite | 17.2 ms |
| Go goroutines | manual chunking + `sync.WaitGroup` + merge | 21.0 ms |
| **Kāra (auto-par)** | **none** — the compiler recognized the reduction | **31.8 ms** |

The par lane is verified in the emitted IR (`KARAC_MIR_LL`): the default build
carries a call of `karac_mir_task_spawn`, the `KARAC_AUTO_PAR=0` twin does not.
Against the July feed Kāra/rayon moved 1.51× → 1.84× (Kāra/C 1.68× → 1.90×,
Kāra/Go 1.23× → 1.51×), the same ~1.1× seq slip plus some par-side loss.

**Kāra's auto-par turns its 292 ms seq run into 31.8 ms — a 9.2× self-speedup
across the machine's cores from the *same single-threaded source*, no parallel
code, no crate, no goroutine boilerplate.** The absolute number trails hand-tuned
rayon (1.84×) — partly the same overflow-safety tax (rayon wraps), partly
per-thread codegen — but the engineering delta is the point: rayon/goroutines/
pthreads each cost a dependency or a hand-rolled chunk-merge and a new class of
data-race bugs; Kāra delivers 9.2× from code that reads sequential.

### Compile, binary

| | Kāra | Rust | C |
|---|---|---|---|
| compile elapsed | **156 ms** | 112 ms | 50 ms |
| binary (seq) | **312 KiB** | 457 KiB | 33 KiB |

Kāra's cold compile (156 ms) is now 1.39× slower than `rustc -O` (112 ms); it
emits a **312 KiB** seq binary (377 KiB par) — **1.46× smaller than Rust**, **7.8×
smaller than Go** (2.4 MiB). Every MIR Kāra binary is ~300–390 KB (kara ledger
[`B-2026-10-28-36`](../../../../kara/docs/bugs-v2.md)). Runtime peak RSS is
3.0 MiB seq (Rust 3.0 MiB), 3.4 MiB par.

**Buyer reframe.** Kāra ships overflow-trap safety *by default* at near-Rust
codegen speed (1.09× behind at equal safety), and a 9.2× parallel speedup from
single-threaded source — the safety a Rust team would have to remember to enable,
and the parallelism they'd pay a crate + an API rewrite + a data-race audit for,
both arrive for free. The remaining single-thread gap to `rustc -O`'s default is
mostly the silent-overflow bug class Kāra declines to ship.

## Kāra features exercised

- **`bytes()` byte scan** — `(b - b'A') as i64` widening over the title.
- **Bijective base-26 parse** — Horner fold + recursive prefix fold.
- **Digit-table render (round-trip)** — `LETTERS[d..d+1]` slice + `push_str`,
  bijective decrement before the modulus (the #168 direction).
- **Round-trip self-oracle** — `to_title(to_number(t)) == t` across all titles.
- **Multi-line output** — the print sequence that surfaced B-2026-06-13-18.

---

**Bug ledger:** flushed **`B-2026-06-13-18`** (HIGH, `autopar`) — auto-par
parallelized the kata's console-output statements (the print builtins carry no
resource effect), and the workers raced on stdout, reordering output
nondeterministically. Fixed (`48145ad4`). See the
[`karac` bug ledger](../../../../kara/docs/bug-ledger.md).
