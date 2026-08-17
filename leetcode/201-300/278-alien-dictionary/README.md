# 278. Alien Dictionary

Words from an alien language, given in that language's lexicographic order.
Recover the order of its letters. Return `""` if the input is inconsistent.

```
["wrt","wrf","er","ett","rftt"]  ->  "wertf"
["z","x"]                        ->  "zx"
["z","x","z"]                    ->  ""      z<x and x<z — a cycle
["abc","ab"]                     ->  ""      a word before its own prefix
["ab","abc"]                     ->  "abc"   legal; no constraint at all
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `alien_order.kara` ★ | Kahn, smallest-available tie-break | O(26² + total length) |
| `alien_order_dfs.kara` | DFS reverse postorder, three colours | same |
| `alien_order_brute.kara` | permutations, first that satisfies the words | O(k!·length) |
| `differential.kara` | 1200 cases, two oracles | — |
| `bench/alien.kara` | one 250k-word dictionary, recovered 48 times | benchmark lane |

## Two things happen before any sorting

**One edge per adjacent pair.** `wxqkj` before `wxjki` says `q < j` and nothing
else — everything after the first difference is unconstrained, because
lexicographic order already stopped caring. Taking more than one edge per pair is
the classic over-read.

**The prefix rule.** If a word comes before its own prefix — `["abc","ab"]` — the
input is invalid, and *no edge is involved*. A shorter word must come first under
any alphabet. This case yields no constraint at all, which is exactly why a
solver that only looks for differing characters sails past it and returns a
confident wrong answer.

Then the sort, and a cycle means `""`.

## The answer is not unique, so there are two oracles

Letters the words never relate may appear in any order: `["ab","abc"]` admits
every permutation of `{a,b,c}` and the problem accepts any of them. **Comparing
solver output as strings is therefore wrong in general** — it would fail correct
solvers. Which oracle applies is forced by the solver, not chosen:

**Kahn vs brute — string equality.** Both commit to the lexicographically
smallest valid order: Kahn by always taking the smallest available letter, brute
by enumerating permutations in order. Two independent routes to the same
canonical form is the strongest check here, and it's the only reason the ★ solver
bothers with a tie-break.

**DFS — validation.** Reverse postorder yields *a* valid order, and no visit
order makes it the lex-smallest in general — that greedy property belongs to the
repeated-minimum formulation. So it's checked against the *problem*: whatever it
emits must be a permutation of exactly the present letters and must order every
adjacent word pair correctly.

**All three — agreement on existence.** Empty vs non-empty is the sharp binary
the problem is really about, and it's comparable regardless of tie-break.

```
cases 1200
satisfiable 776
unsatisfiable by CYCLE 263, by the PREFIX RULE 161
DFS answers that differed from the lex-smallest 365
DFS answers that failed VALIDATION 0
digest 275239060
kahn vs brute, as strings 0
existence disagreements 0
```

**365 DFS answers differed from the lex-smallest and all 365 validated.** A pure
equality harness would have reported 365 false failures — that's the size of the
mistake the two-oracle split avoids.

The validator is not a third solver. It never constructs an order, only checks
one, which is what lets it adjudicate between solvers that legitimately disagree.

## What the injected bugs did

| injection | kahn ≠ brute | DFS invalid | existence |
|---|---:|---:|---:|
| kahn: drop the prefix rule | 120 | 0 | 120 |
| kahn: take every differing position | 192 | 0 | 129 |
| kahn: forget isolated letters | 815 | 0 | 96 |
| kahn: skip edge dedup | 79 | 0 | 79 |
| **dfs: treat grey as finished (no cycle detection)** | **0** | **263** | 263 |
| **both graph solvers drop the prefix rule** | 120 | **120** | 120 |
| brute force: let the prefix case slip | 120 | 0 | 120 |

The fifth row is why the validator exists: removing DFS's cycle detection is
**completely invisible** to the equality oracle — which never involves DFS — and
the validator catches all 263. That count is exactly the number of cyclic inputs,
since DFS then returns an order for every one of them.

The sixth is the [#276](../276-paint-fence/)/[#277](../277-find-the-celebrity/)
lesson again: Kahn and DFS build their graph the same way and share both
pre-conditions, so breaking the prefix rule in *both* leaves them agreeing. The
brute force never builds a graph — it checks candidate orders against the words,
so the prefix case needs no special handling and falls out for free.

The last row runs it backwards: break the *oracle* and the graph solvers catch it.

## Generator notes

Random word lists are unsatisfiable far more often than not, so a third of the
cases are made satisfiable by sorting the words under a planted (reversed)
alphabet — the same manufacturing [#277](../277-find-the-celebrity/) needed for
its celebrity. And the two ways to be unsatisfiable are counted separately
because different bugs miss them: 263 cycles against 161 prefix violations, so a
harness that stopped producing either would be visible.

## Three compiler bugs this kata found

`B-2026-08-17-10` — **indexing an iterator typechecks, then every backend
improvises differently.** Found by asking the first question anyone asks about
strings: can I subscript the characters.

```
karac check       All checks passed.
karac run --interp   panicked at eval_expr.rs:747: internal error:
                     entered unreachable code ... obj=Value::Iterator
karac build       ok -> "a"        (let-bound)   /   BUILD FAILS (inline)
```

`w.chars()[0]` let-bound compiles and returns the right character; written inline
it fails to build; `v.iter()[0]` fails to build; and all three panic the
interpreter with an internal error rather than a diagnostic. Three defects in one
— the typechecker admits the index, the interpreter panics instead of erroring,
and the backends disagree with each other and codegen with itself. Filed medium:
nothing silently miscompiles, but it's a crash on a natural first attempt.

This kata uses `.bytes()`, which is the corpus idiom and correct everywhere. That
isn't routing around the gap — the gap is that the *wrong* form isn't diagnosed.

`B-2026-08-17-11` — **E0200's suggested repair is the unsafe one.** `bytes()`
yields `u8`, so every letter index here is `b[i] - 97` and the compiler correctly
refuses to mix widths:

```
cannot mix integer types 'u8' and 'i64' in arithmetic — they must match;
cast explicitly with `as` (e.g. the operand as 'u8')
```

The only concrete type it names is `u8` — the *narrowing* direction. On `"Ab"`,
whose first byte is 65:

| repair | result |
|---|---|
| widen — `(b[0] as i64) - 97i64` | `-32`, correct |
| narrow — `b[0] - (97i64 as u8)` | **runtime error: integer overflow** |

Both compile. One converts a caught compile-time error into a trap that fires
only when the subtraction goes negative — which for `bytes()` work means any
letter below the one you're subtracting. This kata would have shipped a trap on
uppercase input had I followed the message instead of reasoning about direction.

It's also not machine-applicable: E0200 carries no `replacement` field, so
`karac fix` declines it while diagnostics like `!` → `not` carry
`replacement: {offset, length, text}` and apply cleanly. The order of fixes
matters — adding a `replacement` *first*, without changing the example, would
make `karac fix` auto-apply the trapping repair everywhere it sees one.

## Kāra features exercised

- **`String.bytes()`** with explicit `as i64` casts — the compiler rejects mixing
  `u8` and `i64`, which is the right call and the diagnostic says exactly what to
  write.
- **`String.substring`** for index→letter, and `+` string building.
- **A flat `Vec[bool]` of 676** as the adjacency matrix, indexed `u * 26 + v`.
- **An explicit stack DFS** with a parallel index stack, avoiding recursion.
- **Next-permutation in place** — swap, then reverse the suffix.

## Running

```bash
karac run alien_order.kara
karac run alien_order_dfs.kara       # a valid order, not the lex-smallest one
karac run alien_order_brute.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in alien_order alien_order_dfs alien_order_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

## Benchmarks

**The topological sort is not the workload.** It runs over 26 letters — O(26²)
however many words you feed it. All the time is in phase 1, walking adjacent word
pairs to find each first difference, which is O(total input length). So the
workload is a big *dictionary*, not a big alphabet.

Two generator decisions carry it. The words are **already in planted-alphabet
order**, because an unsorted list returns `""` after a handful of comparisons and
measures nothing. And consecutive words **share long prefixes** — they're the
base-6 numerals of 0..250000 — because words drawn independently at random differ
at position 0 almost every time, so the scan exits immediately and the bench
measures loop overhead instead of the comparison it exists to time.

**Build once, punch 48 times.** Constructing the dictionary is string work, not
the algorithm. Leaving it inside the loop was measurably wrong: hoisting it cut
the runtime from 0.69 s to 0.04 s, so the first version of this bench was **94%
dictionary construction** and only 6% the thing it claimed to measure.

250,000 words over a 6-letter alphabet, recovered 48 times. Every lane prints
`128003665`. 4-core x86 container, hyperfine.

| lane | time | vs C |
|---|---:|---:|
| `clang -O3` | 185.5 ms ± 6.8 | 1.00× |
| `go build` | 191.4 ms ± 8.3 | 1.03× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **258.9 ms ± 14.8** | **1.40×** |
| `rustc -O` | 277.2 ms ± 10.6 | 1.49× |
| **`karac build`, `KARAC_AUTO_PAR=0`** | **321.8 ms ± 30.6** | **1.73×** |

**1.24× against the equal-safety comparator** — Kāra is level with Rust here, and
both trail C and Go, which is unusual for this corpus and worth its own look
someday.

### The parallel lane

| | time | cpu |
|---|---:|---:|
| `alien_seq.kara` | 293.6 ms ± 15.5 | 99% |
| **`alien.kara`** (`#[par_order_free]`) | **165.6 ms ± 6.2** | **202%** |
| | **1.77× ± 0.11** | |

It shipped at **1.03× slower** and 101% CPU, which is how `B-2026-08-17-14` was
found — the second kata in this corpus to publish a broken par lane rather than
drop it.

**The cause was nested dispatch, and it was neither of the two things I
proposed.** An auto-parallelized loop *inside* `solve` called `karac_par_run`
once per invocation: 48 nested dispatches into a pool the outer collect had
already saturated, each blocking its worker in `dispatch_and_wait`. All four
chunks then ran sequentially on one pool thread. `karac_par_reduce` has had a
fork-depth cap since slice 3b; `karac_par_run` had none, and that asymmetry was
the whole bug.

My bisection table has a mechanical reading in hindsight: each simplification of
`solve` changed *which* loops auto-par recognized, so the 101 / 166 / 248 / 345
gradient tracks how much of each variant's runtime sat inside a nested-dispatching
region. Graded because the convoy is proportional — not, as I guessed, because of
payload contention.

**And the race I worried about doesn't exist.** I suspected non-atomic refcount
traffic on the shared `Vec[String]` and flagged that it would make this a
soundness bug rather than a perf one. Plain `Vec` elements carry no refcount at
all — RC is the `shared struct` tier — so a read-only `words[p]` is a load, not a
retain. The premise was wrong, which is why it was filed as a question rather
than as a soundness row.

**Residual, still open:** 2.04× on 4 cores is not 4×. The scan is
memory-bandwidth-shaped — 250k string headers per branch — and whether any of the
gap is Kāra-specific is a smaller, separate question than the one this row
answered.
## Kāra features exercised

- **`String.bytes()`** with explicit `as i64` casts — the compiler rejects mixing
  `u8` and `i64`, which is the right call and the diagnostic says exactly what to
  write.
- **`String.substring`** for index→letter, and `+` string building.
- **A flat `Vec[bool]` of 676** as the adjacency matrix, indexed `u * 26 + v`.
- **An explicit stack DFS** with a parallel index stack, avoiding recursion.
- **Next-permutation in place** — swap, then reverse the suffix.

## Running

```bash
karac run alien_order.kara
karac run alien_order_dfs.kara       # a valid order, not the lex-smallest one
karac run alien_order_brute.kara

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in alien_order alien_order_dfs alien_order_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

## Benchmarks

**The topological sort is not the workload.** It runs over 26 letters — O(26²)
however many words you feed it. All the time is in phase 1, walking adjacent word
pairs to find each first difference, which is O(total input length). So the
workload is a big *dictionary*, not a big alphabet.

Two generator decisions carry it. The words are **already in planted-alphabet
order**, because an unsorted list returns `""` after a handful of comparisons and
measures nothing. And consecutive words **share long prefixes** — they're the
base-6 numerals of 0..250000 — because words drawn independently at random differ
at position 0 almost every time, so the scan exits immediately and the bench
measures loop overhead instead of the comparison it exists to time.

**Build once, punch 48 times.** Constructing the dictionary is string work, not
the algorithm. Leaving it inside the loop was measurably wrong: hoisting it cut
the runtime from 0.69 s to 0.04 s, so the first version of this bench was **94%
dictionary construction** and only 6% the thing it claimed to measure.

250,000 words over a 6-letter alphabet, recovered 48 times. Every lane prints
`128003665`. 4-core x86 container, hyperfine.

| lane | time | vs C |
|---|---:|---:|
| `clang -O3` | 185.5 ms ± 6.8 | 1.00× |
| `go build` | 191.4 ms ± 8.3 | 1.03× |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **258.9 ms ± 14.8** | **1.40×** |
| `rustc -O` | 277.2 ms ± 10.6 | 1.49× |
| **`karac build`, `KARAC_AUTO_PAR=0`** | **321.8 ms ± 30.6** | **1.73×** |

**1.24× against the equal-safety comparator** — Kāra is level with Rust here, and
both trail C and Go, which is unusual for this corpus and worth its own look
someday.

### The parallel lane does not fan out

| | time | cpu |
|---|---:|---:|
| `alien_seq.kara` | 321.8 ms ± 30.6 | ~100% |
| `alien.kara` (`#[par_order_free]`) | 330.2 ms ± 12.6 | **101%** |

48 branches of ~6 ms each, and `karac query concurrency` reports
`lowering: parallel_fanout, fanned_out: true, "dispatched across the worker
pool"`. It costs 3% and buys nothing.

This is `B-2026-08-17-14`, and it is the **second** instance of that exact
signature — [#276](../276-paint-fence/) had it before `c04bc65`. It is *not* that
bug: the chunker fix is present and verified in the same binaries, since #276's
16-iteration lane measures 384% CPU in the same session.

Five isolations reproducing the body's individual features all parallelize
correctly — pure arithmetic (387%), a captured `Vec[i64]` (355%), a captured
`Vec[String]` (361%), per-call allocation (300%), a String-returning callee
(364%). So it is not the branch count, the captured collection, the heap element
type, allocation, or the return type. The most obvious untested difference is
that the real callee contains **nested loops that are themselves classified as
collect reductions** (`sequential_tabulate` on `adj`, `done`, `out`, `digits`) —
none of the isolations had one inside a parallel branch.

The lane ships at 1.03× *slower* with a pointer to the row, rather than being
dropped. That's the call #276 made while its bug was open, and it's what got that
one fixed.
