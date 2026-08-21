# 293. Flip Game

A string of `+` and `-`. A move picks any two **consecutive** `+` and flips both
to `-`. Return every state reachable in one move.

```
"++++"   ->  ["--++", "+--+", "++--"]
"+"      ->  []          nothing to flip
"----"   ->  []          no "++" anywhere
"+-+-+"  ->  []          no two adjacent
"-++-"   ->  ["----"]    only the middle pair qualifies
```

## Approaches

| file | mechanism | work on a move-free string |
|---|---|---|
| `flip_game.kara` ★ | test the pair, then allocate | O(n) comparisons, no allocation |
| `flip_game_rebuild.kara` | allocate a copy per position, then test | O(n²) copying, discarded |
| `differential.kara` | 8191 exhaustive inputs, two arms, four properties | — |
| `bench/flipgame.kara` | 40,000 boards × 3 densities | benchmark lane |

## The string decision comes before the logic

Kāra's `String` is UTF-8 with no O(1) indexing, so the shape of the answer is
settled before any flipping happens:

```kara
let cs: Vec[char] = s.chars().collect();
```

design.md § Character access sanctions exactly this — *"when repeated indexed
access is genuinely needed, convert first … then `chars[i]` is O(1) on a type
where that is honest"* — and warns in the same breath that repeated `char_at(i)`
is O(n²). This is worth stating plainly because
[#288](../288-unique-word-abbreviation/) filed a bug claiming the idiom was
forced by a *missing* feature. It wasn't; `char_at` exists, the row was closed
as invalid, and the collect is the recommended spelling rather than a
workaround.

## Test first, then allocate

The ★ file checks `cs[i] == '+' && cs[i+1] == '+'` before touching the heap.
`flip_game_rebuild.kara` inverts that — copy the whole string, then check — so a
board with no legal move still does `n` copies of `n` characters and returns
nothing.

That ordering is not a micro-optimisation. It is the difference between a search
that finishes and one that doesn't in **#294 Flip Game II**, where this function
is called on every node of a game tree and most nodes are move-poor. The bench
sweeps three `+` densities for exactly that reason: at 15% most boards have no
move at all and the ordering dominates; at 85% nearly every position is a move,
both arms allocate anyway, and what's left is raw string-building throughput.

## Properties, not just agreement

Two arms that share a shape will duplicate a misreading of the problem, and the
diff stays silent. So the differential checks the arms against each other **and**
against four facts that follow from the statement rather than from any code:

1. **Count** — results equal the number of `++` positions, counted separately.
2. **Length** — a flip replaces two characters; it never inserts or drops one.
3. **Edit distance** — every result differs in exactly two adjacent positions,
   both `+` → `-`.
4. **Plus count** — every result has exactly two fewer `+`.

Exhaustive over `{+,-}ⁿ` for n = 0…12: **8191 inputs, 20481 states, zero
violations.** Binary alphabet and a small relevant length make exhaustive
cheaper than sampling and strictly better.

**Why property 1 exists.** Four planted mutations are all caught, but they are
not caught by the same things. Flipping only the first character, or the wrong
pair, or accepting `--`, all break the per-state properties. But a scan that
**misses the last pair** passes every per-state check with a clean zero — length,
edit distance and plus count are all fine, because every state it *does* produce
is perfectly valid. Only the count property and the long-string cases catch it.

Per-item validity cannot detect missing items. A suite made only of "is each
answer well-formed?" would have reported green on that one.

## Benchmarks

40,000 boards × 64 chars × three `+` densities. Container x86_64, sink
`states 2510273 checksum 320468494` across Kāra, C, Rust and Go.

| implementation | mean |
|---|---|
| c | 162.4 ms |
| c (`-march=x86-64-v3`) | 109.7 ms |
| rust (`overflow-checks=on`, equal-safety) | 406.1 ms |
| rust | 493.3 ms |
| **kāra** | **528.2 ms** |
| go | 555.5 ms |

The workload is allocation-dominated — one owned string per result — so everyone
lands in the same order of magnitude except C. Kāra is 3.25× off C and within
7% of plain Rust.

### Where the 3.25× to C actually goes

Worth decomposing rather than shrugging at, since the workload is simple enough
to account for completely. Two of the three candidates turn out to be fine:

**Allocation is not it.** An `LD_PRELOAD` counter gives Kāra 2,739,223 malloc /
255,809 realloc against C's 2,510,274 / 0 — about **1.09 malloc and 0.10 realloc
per state**. The presize pass is working. Rewriting `String.new()` as
`String.with_capacity(n)` produces *byte-identical* allocation counts and
identical timing (264.0 vs 266.0 ms), so the idiom leaves nothing on the table.

**The read side is not it.** A probe doing only the 160M `Vec[char]` indexed
reads, building no string, runs in 55.9 ms — about **0.35 ns per read**, so
bounds-check elision is doing its job.

**`String.push` is all of it.** Adding the pushes takes that probe to 264.9 ms,
so 160M pushes cost 209 ms — **~1.3 ns each**, roughly 4 cycles against a C byte
store at well under one. `objdump` shows why: `karac_string_encode_char` is an
**out-of-line call in the hot loop**, one per character. The runtime function
already opens with `if cp < 0x80`, so the ASCII path itself is a compare and a
store; what the program pays on top is the call boundary. Filed as
`B-2026-08-21-1` — inlining the ASCII test at the push site is what Rust's
`String::push` does, and is likely most of why the Rust mirror lands at 493 ms
building strings the same way.

So: expected in that nothing is broken, but ~40% of this kata's runtime sits
behind one un-inlined call.

### The first run of this bench was wrong, and the sink did not notice

C measured **29.4 ms** against Kāra's 514.7 — a 17.5× gap. That spread is too
wide for a language difference on a workload this simple, which is the only
reason it got a second look.

The mirrors had drifted into three different algorithms: the C twin used a
**static buffer and `memcpy`** and never touched the heap; Go did heap-alloc +
bulk copy; Rust and Kāra did heap-alloc + a per-character branch. Kāra's
`String` is append-only, so the per-character build is its natural form and the
mirrors have to match *that*. Rewritten to malloc-per-state with one branch per
character, C lands at 162.4 ms — **5.5× slower purely from allocating**, which
was the entire "gap".

**The sink agreed the whole time.** All four printed
`states 2510273 checksum 320468494` before and after, because they compute the
same answer by different means and a sink cannot see the difference. Cross-
language parity is a property of the *work*, not of the output — which is
exactly why [BENCHMARKS.md](../../../BENCHMARKS.md) makes it a rule rather than
a suggestion. The parity requirement is now stated in each mirror's header so
the next person doesn't optimise them back apart.
