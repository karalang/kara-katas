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

## A compiler bug this kata found

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
