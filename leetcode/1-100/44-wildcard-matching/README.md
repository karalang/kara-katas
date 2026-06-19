# 44. Wildcard Matching

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** String, Dynamic Programming, Greedy, Two Pointers, Recursion &nbsp;·&nbsp; **Source:** [leetcode.com/problems/wildcard-matching](https://leetcode.com/problems/wildcard-matching/)

Match the **entire** string `s` against pattern `p`, where `?` matches any single character and
`*` matches any sequence of characters (including the empty one).

```
("aa",    "a")      →  false
("aa",    "*")      →  true
("cb",    "?a")     →  false
("adceb", "*a*b")   →  true
("acdcb", "a*c?b")  →  false
```

**Constraints:** `0 ≤ s.length, p.length ≤ 2000`; `s` is lowercase letters; `p` is lowercase
letters, `?`, and `*`. Note `*` is a **free-standing** wildcard — unlike
[#10](../10-regular-expression-matching/), where `*` is a quantifier bound to the *preceding*
element (`x*` = zero-or-more `x`) and `.` is the any-char. Here `.` is a literal and `*`
absorbs any run on its own, which is exactly what collapses #10's recursive two-branch
expansion down to a single greedy scan.

## Why this kata — one invariant, three ways to spend space

The match relation is `dp[i][j] = "does s[:i] match p[:j]?"`, and the three canonical solvers
are three *space* factorings of computing it — the same shape as
[#42](../42-trapping-rain-water/) (O(1) scalars / O(n) arrays / O(n) stack), here over a 2-D
recurrence:

| Lens | Idea |
|---|---|
| **Greedy two pointers** ★ | walk one cursor in each string; on a `*` record a backtrack point (its index + the s-position), and on a dead end let that `*` swallow one more char — O(1) space, each backtrack advances `matched` so it is O(m·n) worst case |
| **2D DP table** | fill `dp[i][j]` from its neighbours: `*` carries left (match empty) or up (absorb one char); `?`/literal carries the diagonal — O(m·n) time **and** space |
| **1D rolling DP** | the table only reads row `i-1` while filling row `i`, so two length-(m+1) rows suffice — O(n) space |

The greedy file is the one that exploits the free-standing `*`: you never need to try every
split, only remember the *last* `*` and extend it one char at a time on failure. The table
makes the recurrence literal; the rolling row is its standard space optimization.

## Approaches

Three styles, all agreeing with the Python oracle for the LeetCode examples under `karac run`
**and** `karac build`.

| Approach | File | Shape |
|---|---|---|
| **Greedy two pointers** ★ | [`wildcard_matching.kara`](wildcard_matching.kara) | `Slice[u8]` over `s.bytes()`, four i64 cursors, no allocation |
| 2D DP table | [`wildcard_matching_dp2d.kara`](wildcard_matching_dp2d.kara) | flat `Vec[bool]` of `(n+1)·(m+1)`, indexed `i*(m+1)+j` |
| 1D rolling DP | [`wildcard_matching_dp1d.kara`](wildcard_matching_dp1d.kara) | two `Vec[bool]` rows rolled per s char |

The greedy form is allocation-free (a read-only `Slice[u8]` view + scalars); the 2-D table
allocates one flat `Vec[bool]`; the rolling form keeps two `Vec[bool]` rows — the same
O(1)/O(m·n)/O(n)-space trio as #42, the in-place-scan footing of
[#41](../41-first-missing-positive/) extended to a string-matching recurrence.

## What this kata surfaced

**A sub-word `Vec` element store wrote 8 bytes over a 1-byte slot — a heap overflow that
corrupted the adjacent allocation** ([`B-2026-06-19-5`](../../../../kara/docs/bug-ledger.jsonl),
`kata:44`, codegen, **fixed [`66a489ef`](../../../../kara/docs/bug-ledger.jsonl)**). The bench
terrain is a `Vec[u8]` built with *computed* pushes (`s.push(b'a' + (i as u8))`). A `u8`-typed
expression that involves arithmetic or a cast compiles to the default `i64`, and the element
`build_store` took its width from the **value**, not the element type: the GEP and the
allocation correctly used the 1-byte stride, but the store wrote 8 bytes. Consecutive
overlapping wide stores each preserve their own low byte, so **the values read back correct
and the interpreter agreed** — but the push that fills an exact-size-class buffer (cap
64/128/256…) smeared 7 bytes past the end, corrupting the next heap block. The result was an
**ASLR-intermittent `SIGSEGV`** on a later `realloc`/free, appearing only once the buffer grew
past ~64 elements: the small solver test cases passed, the length-240 bench crashed.

**ASAN never saw it** — the 7-byte spill lands in the allocator's realloc-rounding slack, not a
poisoned redzone, so the whole `memory_sanitizer` suite stayed green while `karac build`
binaries segfaulted. The diagnosis was build-and-run bisection (`-O0` still crashed → base
lowering, not the optimizer; instrumentation masked it → a wild store, not a tracked overflow;
size threshold ~64 → an exact-size-class boundary), ending at the element `build_store` in
`vec_method.rs`/`collections.rs`.

**The fix** coerces the value to the element type (`coerce_scalar_to_type`, truncating when
wider) immediately before each of the six element-store sites — `push`, `try_push`,
`push_front`, `try_push_front`, the `Vec` index-store, and the slice index-store. It is the
same bug class — and the same remedy — as `coerce_to_struct_field_ty`, which already cured
"8 bytes over a 1-byte field" for struct fields. Regression tests live in `tests/codegen.rs`
as **build+run** cases (ASAN can't guard this): a 240-element computed-`u8` push + index-store,
and a `Vec[bool]` variant — both reliably crashed pre-fix. Full codegen (1619) / par_codegen
(121) / memory_sanitizer (264) green; `fmt` + `clippy` clean.

**The kata ships the idiomatic forms,** all of which now build correctly: the greedy solver
reads `s.bytes()` as a `Slice[u8]`, and the DP solvers build and index `Vec[bool]` tables.

## Benchmarks

Workload: build `s` ("abc" repeated, length `N=240`) and a multi-star pattern `p`
(`*abc*abc*…*abc*`, eight groups) **once**, then **`TOTAL = 300000`** times punch a single s
slot (`s[k%n] = 'a' + k%4`, where a `'d'` breaks an "abc" group so the boolean answer flips),
run the ★ greedy match, and fold the result into a rolling checksum (sink `494778662`). The
per-iteration cost is the greedy **scan** over `s` (locating each group after a `*`), not an
O(n) refill — the hot loop allocates nothing, the answer varies with the loop index (no
hoisting), and the checksum carries a loop-borne dependency, so it is a single-lane (seq)
bench by construction. Apple M5 Pro; `bench/bench.sh` (`hyperfine`).

### Seq lane — runtime (single-threaded greedy matcher)

| | C | Rust (`-O`) | Rust (`overflow-checks=on`) | Go | **Kāra** | Python |
|---|---|---|---|---|---|---|
| time | 37.5 ms | 39.1 ms | 39.5 ms | 41.3 ms | **44.4 ms** | 1616 ms |
| vs Kāra | 1.18× faster | 1.14× faster | 1.12× faster | 1.08× faster | — | 36.4× slower |

**Kāra lands in the pack** — within ~1.1–1.2× of the C-class on a byte-comparison-heavy scan,
and 36× ahead of interpreted Python. This is a branchy `?`/`*`/literal dispatch over `u8`
loads with a backtrack rewind; there is no allocation or arithmetic-checking story to isolate,
so the equal-safety comparator (`rustc -C overflow-checks=on`, 39.5 ms) is within noise of
plain `rustc -O` (39.1 ms), and Kāra (44.4 ms) trails the group by a small, steady margin —
the modest codegen gap on a tight scalar loop, not an outlier in either direction.

### Runtime memory, binary size, compile

| | Kāra | Rust | C | Go |
|---|---|---|---|---|
| **runtime peak RSS** | **1.00 MiB** | 1.05 MiB | 1.00 MiB | 2.64 MiB |
| binary size (seq) | 33.3 KiB | 455.6 KiB | **32.7 KiB** | 2434.1 KiB |
| compile elapsed | 72.9 ms | 99.3 ms | **44.1 ms** |
| compile peak RSS | 13.5 MiB | 30.5 MiB | **2.5 MiB** |

Two small byte buffers mean runtime RSS is allocator-bound: Kāra and C tie at **1.00 MiB**
(byte-for-byte equal peak, 1 048 888 bytes), Rust within rounding at 1.05 MiB, while Go's
runtime pays 2.64 MiB and Python's interpreter 6.8 MiB. The seq binary references no
par-scheduler runtime, so LTO + `-dead_strip` carve it to **33.3 KiB** — 13.7× under Rust and
within a rounding of C's 32.7 KiB. Compile favours Kāra over `rustc -O` on both elapsed (72.9
vs 99.3 ms) and peak compiler RSS (13.5 vs 30.5 MiB); clang's 44.1 ms / 2.5 MiB is the floor.

**No par lane — by construction.** The per-iteration match is pure, but the checksum reduction
carries a loop-borne dependency, so karac's auto-par pass does not fire: the default and
`KARAC_AUTO_PAR=0` binaries are **byte-identical** and both run single-threaded.

## Kāra features exercised

- **Read-only `Slice[u8]` over `s.bytes()`** — the ★ greedy solver walks the byte view with
  four i64 cursors and `b'?'`/`b'*'` byte literals, no allocation, the in-place-scan footing of
  [#41](../41-first-missing-positive/) and the string-handling idiom of
  [#10](../10-regular-expression-matching/).
- **Flat `Vec[bool]` DP table** — the 2-D solver allocates one `Vec[bool]` of `(n+1)·(m+1)`
  cells and indexes it by computed offset `i*(m+1)+j`, the allocating contrast to the greedy
  scalars (and the surface that surfaced [`B-2026-06-19-5`](../../../../kara/docs/bug-ledger.jsonl)).
- **Two rolling `Vec[bool]` rows** — the 1-D solver keeps `prev`/`curr` rows and rolls them per
  s character, the O(n)-space middle point.
- **`break` out of an inner loop, computed-index reads/writes** — across the three factorings.
- **Three factorings of one O(m·n) idea** — greedy, full table, rolling row — all agreeing
  across the LeetCode examples under both `karac run` and `karac build`.

---

**Bug ledger:** [`B-2026-06-19-5`](../../../../kara/docs/bug-ledger.jsonl) (`kata:44`, codegen,
**fixed [`66a489ef`](../../../../kara/docs/bug-ledger.jsonl)**) — a sub-word `Vec`/slice element
store (`Vec[u8]`/`Vec[bool]`/`Vec[u16]`/`Vec[u32]`) wrote a computed value at full i64 width
over the 1/2/4-byte slot, overflowing the buffer by the trailing bytes on the push that fills
an exact-size-class allocation (heap corruption, ASLR-intermittent segfault); ASAN missed it,
so the guard is a build+run regression. The fix coerces the value to the element width before
every element store. See the [`karac` bug ledger](../../../../kara/docs/bug-ledger.jsonl).
