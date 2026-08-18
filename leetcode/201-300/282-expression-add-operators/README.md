# 282. Expression Add Operators

Insert `+`, `-` or `*` between the digits of `num` — or nothing, joining them
into a multi-digit operand — so the expression evaluates to `target`. Return
every such expression.

```
"123", 6   ->  ["1+2+3", "1*2*3"]
"232", 8   ->  ["2*3+2", "2+3*2"]
"105", 5   ->  ["1*0+5", "10-5"]     — never "1*05"
"00",  0   ->  ["0*0", "0+0", "0-0"]
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `add_operators.kara` ★ | backtracking, carrying the last operand | O(4ⁿ) |
| `add_operators_enumerate.kara` | all 4ⁿ⁻¹ patterns, evaluated properly | O(4ⁿ·n) |
| `differential.kara` | 1092 cases, four checks | — |
| `bench/exprops.kara` | 220 nine-digit inputs searched exhaustively | benchmark lane |

## The difficulty is precedence, not search

A running total works for `+` and `-`: each new term is added or subtracted. It
breaks for `*`, because the new factor binds to the **previous term**, not the
total — after `2+3`, a `*4` must give `2+12`, not `(2+3)*4`.

So the search carries its last term and undoes it:

```kara
cur = cur - last + (last * n)      // and the new last is last * n
```

Subtract what the previous term contributed, then re-add it multiplied. That one
line is the whole kata, and it's why the state is `(pos, expr, cur, last)` rather
than `(pos, expr, cur)`. A solver tracking only the total is right on every
`+`/`-` case and silently wrong the moment a `*` follows anything.

The sign matters too: after `-`, `last` must go **negative**, or `1-2*3` comes
out as `1-2*3 = -3` computed the wrong way. That's the second injection below.

## Leading zeros produce right answers to the wrong question

A multi-digit operand may not start with `0`, so from a position holding `0` the
only operand is the single digit `0`. `"105"` admits `"1*0+5"` and `"10-5"` but
never `"1*05"`.

**Forgetting this does not produce a wrong value.** Every expression it emits
still evaluates to the target — `1*05` really is 5. It produces expressions that
are *not legal*, so a harness checking only arithmetic sees nothing wrong. The
injection table measures exactly that: 32415 illegal expressions, **0** of them
with a wrong value.

## Four checks, three of them per-expression

The answer is a set of strings, so the first check is set equality after sorting.
The other three hold of every returned expression on its own, without reference
to either solver:

1. **The sets match** after sorting.
2. **Every expression evaluates to the target** — re-evaluated independently.
3. **Every expression is legal** — no multi-digit operand starting with `0`.
4. **Every expression preserves the input digits, in order** — strip the
   operators and what remains must be `num` exactly.

**Check 4 looks redundant and isn't.** This is a *construction* problem, and
checks 2 and 3 are both satisfied by expressions built from the wrong digits:
`"1+1"` evaluates to 2 and has no leading zero, and would sail past both while
having nothing to do with an input of `"123"`. It's [#280](../280-wiggle-sort/)'s
multiset lesson in a different costume — when the answer is built from the input,
something has to verify the input is what it was built from.

```
cases 1092, of which have at least one solution 371
expressions returned 618
digest 507046168
expressions whose value is wrong 0
expressions with an illegal leading zero 0
expressions not preserving the input digits 0
set mismatches between the two solvers 0
```

## What the injected bugs did

| injection | set mismatch | wrong value | illegal zero | digits lost |
|---|---:|---:|---:|---:|
| backtrack: track only the total, no `last` | 84 | 58 | 0 | 0 |
| backtrack: `last` stays positive after `-` | 62 | 34 | 0 | 0 |
| enumerate: evaluate left to right, no precedence | 328 | 300 | 0 | 0 |
| backtrack: drop the leading-zero rule | 76 | 0 | 102 | 0 |
| enumerate: drop its leading-zero check | 76 | 0 | 102 | 0 |
| **both drop the leading-zero rule** | **0** | **0** | **204** | 0 |
| backtrack: emit a digit-losing expression | 371 | 391 | 0 | **618** |

The sixth row is why check 3 exists as a *property* rather than a comparison:
both solvers agree perfectly — **0 set mismatches** — and every one of the 204
expressions they agree on evaluates correctly. Only the independent legality
check sees anything. The leading-zero rule is exactly the kind of rule two
independent implementations can share a misreading of, because it comes from the
problem statement rather than from the arithmetic.

Rows four and five show the same bug caught from either side when only one solver
has it; row seven exists to prove check 4 fires at all, since no other injection
reaches it.

## A harness bug this table found

The first version of this differential ran checks 2–4 over the **backtracker's**
output only. Row five then read `illegal-zero 0` — a broken enumerator was
visible solely as a set mismatch, which says *that* something differs but nothing
about *what*. Making the per-expression checks symmetric took that row from `0`
to `102`. Worth recording because the asymmetry was invisible until an
injection landed on the unchecked side.

## Kāra features exercised

- **Recursive backtracking** with a `mut ref Vec[String]` accumulator threaded
  through every call.
- **String building by `+`** along the recursion, and `substring` for operands.
- **`bytes()` with `as i64` casts** for digit and operator classification.
- **A two-pass expression evaluator** over parallel `Vec[i64]` operand/operator
  stacks.

## Running

```bash
karac run add_operators.kara
karac run add_operators_enumerate.kara     # same sets, different enumeration order

diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in add_operators add_operators_enumerate differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```

### How the differential's range was chosen

Digit strings of length 1–3 over `{0,1,2,3}`, against targets −4…8. Lengths 4 and
5 were dropped, and the size was picked by **measurement rather than feel**: at
length 3 every injection above is still caught with every qualitative signature
intact — including the row where both solvers agree and only the legality check
fires. Longer inputs add depth but no new *shape*, while the `--interp` leg goes
35 s → ~9 min → ~2 h. The range is set by the slowest surface, as in
[#279](../279-perfect-squares/).

Both solvers sort before reporting, since the answer is a set and they enumerate
it in different orders — DFS against mask order. The demo inputs are capped at
seven digits so the enumerating solver stays practical under `--interp`; the
10-digit LeetCode case `"3456237490"` with target 9191 returns `[]`, and
`"2147483647"` with target 2147483647 returns itself.

## Benchmarks

The search *is* the workload, and it is allocation-heavy in a way the algorithm
can't avoid: every branch builds a new expression string, so a nine-digit input
walks tens of thousands of partial strings. 220 inputs; the sink is each input's
solution count and length-hash folded as `i·1000003 + found·31 + hash`, summed.
All lanes print `60478588`.

### SEQ lane — single-threaded against single-threaded

| lane | time | vs C |
|---|---:|---:|
| `clang -O3` | 385.0 ms ± 16.1 | 1.00× |
| `go build` | 758.5 ms ± 39.8 | 1.97× |
| **`karac build`, `KARAC_AUTO_PAR=0`** | **1176 ms ± 42** | **3.05×** |
| **`rustc -O -C overflow-checks=on`** (equal safety) | **1384 ms ± 41** | **3.59×** |
| `rustc -O` | 1402 ms ± 43 | 3.64× |

**0.85× against the equal-safety comparator** — Kāra ahead of Rust, stated
precisely rather than claimed as a codegen win: Rust's mirror uses `format!` per
branch, which does more work than a plain concatenation. Fair as "the same
algorithm" — it's how a Rust programmer writes it — but the gap is a string-API
difference as much as a compiler one.

### PAR lane — against mirrors that also reached for threads

| lane | time | vs pthreads |
|---|---:|---:|
| `clang -O3` + pthreads (metal floor) | 98.8 ms ± 7.3 | 1.00× |
| Go, one goroutine per input | 270.8 ms ± 14.2 | 2.74× |
| **`karac build`, `#[par_order_free]`** | **303.9 ms ± 13.2** | **3.08×** |

**3.9× over its own sequential twin** on 4 cores, and level with hand-written
goroutines. The 220 searches are over *different* inputs and share nothing, so
this is parallelism the problem contains rather than manufactured.

### The sink had to be redesigned for that lane to exist

The first version of this bench folded every solution into one running
`hash·31 + len` across all inputs, in DFS order — a fold that depends on which
search finished first. **I then cited that sink as the reason there could be no
par lane**, which was backwards: the sink was mine to choose. Each input now
computes its own local `(count, hash)` and contributes an `i`-weighted term to a
sum, which is the same change [#270](../270-closest-binary-search-tree-value/)
made and for the same reason. The `i` factor still catches two inputs swapping
results, which a plain sum of counts would not.

This is why [#279](../279-perfect-squares/), [#280](../280-wiggle-sort/) and
[#281](../281-zigzag-iterator/) genuinely have no par lane and this one does: in
those the sequential dependency is *in the algorithm* — `least[i]` reads earlier
entries, a wiggle scan depends on what the previous step left, a drain depends on
which cursors advanced. Here nothing was dependent except my own accumulator.

### The C mirror was wrong the first time

C initially measured **211 ms** on the sequential lane, 4.6× faster than
everything else, because I'd written the natural C thing: a `char buf[64]` on the
stack, reused per branch. Kāra, Rust and Go all allocate a fresh string per
branch, so the stack-buffer lane wasn't running the same algorithm — it measured
a memory strategy and called it a compiler comparison. Switching to
`malloc`/`free` per branch moved it to **385 ms**, and that 174 ms gap is the
price of parity.
