# 294. Flip Game II

Same board as [#293](../293-flip-game/): a string of `+` and `-`, and a move
flips two **consecutive** `+` to `--`. Two players alternate, and **a player who
cannot move loses**. Can the player to move force a win?

```
"++++"    ->  true     flip the middle pair; every reply loses
"+++++"   ->  false    every opening move hands back a winning position
"+"       ->  false    no move exists
"+-+-+"   ->  false    no two adjacent
"++-++"   ->  false    two runs of two, and they cancel
```

## Approaches

| file | mechanism | cost |
|---|---|---|
| `flip_game_ii.kara` ★ | memoized search over board strings | distinct boards |
| `flip_game_ii_naive.kara` | the same search, memo deleted | distinct move sequences |
| `flip_game_ii_grundy.kara` | Sprague–Grundy over the `+` runs | one O(n²) table, then O(n) |
| `differential.kara` | 8,191 exhaustive boards, three arms, five properties | — |
| `bench/flipgame2.kara` | 900 boards × memoized search | benchmark lane |

## The recursion is the definition

A position is winning exactly when **some** move leads to a position that is
losing for the opponent. That is not a heuristic or a search strategy — it is
what "winning" means for a finite impartial game, and the ★ file writes it
literally:

```kara
while i < states.len() {
    if not can_win(states[i], memo) {
        let _ = memo.insert(s.clone(), true);
        return true;
    }
    i = i + 1;
}
```

Note the asymmetry, which is easy to write by accident and hard to spot: a
**win** is provable the moment one losing reply is found, but a **loss** is only
established after every move has been refuted. The early `return` is the
existential quantifier, not an optimisation bolted onto the loop.

This is also where #293 pays off. `next_states` is called on every node of the
tree, and #293's version tests the pair before touching the heap — most nodes
here are move-poor, so a version that copies first and checks after would pay
for the whole tree.

## What the memo is worth, counted

Both searches prune, so the gap is narrower than the raw tree size suggests and
opens up only as `n` grows. On a single run of `n`:

| n | 14 | 16 | 18 | 20 |
|---|---:|---:|---:|---:|
| memoized | 516 | 1,492 | 2,856 | 11,488 |
| unmemoized | 1,530 | 7,426 | 13,396 | 180,022 |
| ratio | 3.0× | 5.0× | 4.7× | 15.7× |

The memoized count tracks the number of distinct **boards**; the unmemoized one
tracks distinct move **sequences**. The ratio is not monotone, and the reason is
worth knowing: `n = 15` is a *losing* run, so proving it requires refuting every
branch rather than finding one lucky reply, and its neighbours inherit that cost.

## The board is not one game

The searching arms treat the board as a single monolithic state. It isn't. A
move needs two adjacent `+`, so it lives entirely inside one maximal **run** of
`+` and can never touch two runs at once. The board is a **sum of independent
games**, one per run, and the `-` characters are not part of the game at all —
only separators.

Sprague–Grundy says every finite impartial game under normal play is equivalent
to a Nim heap, and the value of a sum is the XOR of the parts. So:

```
g(run₁) ^ g(run₂) ^ … ^ g(runₖ)  ≠ 0
```

and the search disappears entirely. A move inside a run of length `n` splits it
into runs of `i` and `n-2-i`, which gives the whole table:

```
g(0) = g(1) = 0
g(n) = mex { g(i) ^ g(n-2-i) : 0 ≤ i ≤ n-2 }
```

That recurrence is the octal game **0.07**, Dawson's Kayles. The first values,
computed by `flip_game_ii_grundy.kara`:

```
n  0  1  2  3  4  5  6  7  8  9 10 11 12 13 14
g  0  0  1  1  2  0  3  1  1  0  3  3  2  2  4
```

Read off the zeros — 0, 1, 5, 9, and (past this table) 15 and 21. A single run of
**five** is a loss for the mover. From inside the search, `"+++++" -> false`
looks like an accident of one particular tree; from here it is a table entry.

## Three arms, five properties

Arms A (memo) and B (no memo) share a shape, so their agreement is weak
evidence: a misreading of the rules would sit in both and the diff would stay
silent. **C is why this differential is worth running.** It never enumerates a
move, never builds a successor and never recurses — it reads run lengths and
XORs a table. It shares nothing with A and B but the problem statement.

The properties follow from the statement rather than from any implementation:

| | property |
|---|---|
| **P1** | a board and its reverse have the same answer |
| **P2** | a board with no `++` is a loss for the player to move |
| **P3** | **C satisfies the defining recursion** — winning iff some successor is losing |
| **P4** | the answer depends only on the **multiset of run lengths** |
| **P5** | A and C agree on a bare run of `n`, out to `n = 18` |

P3 is the strong one. C computes nothing resembling a successor internally, so
checking it against `next_states` is a test of the Sprague–Grundy theorem *on
this game*, not a restatement of C's own code.

P4 catches a bug none of the arms could catch alone: an implementation that let
a move straddle a `-`, or that treated the whole board as one run, still gets
every easy board right and fails here. And P5's output is an external oracle —
the losing runs it finds are `0 1 5 9 15`, the published zeros of Dawson's
Kayles below 19, which no arm in this repo had any way to know.

**Bands are sized by the tree-walk interpreter**, the slowest of the four
surfaces every kata must agree on: 8,191 boards for A and C, 2,047 for B,
≈3 minutes under `karac run --interp` against 1.4 seconds compiled. A compiled
build could afford length 14 and a spine to 22; the interpreter is the binding
constraint, and saying so beats quietly shipping a differential that nobody
re-runs on all four surfaces.

## Benchmarks

900 boards of length 22 across three `+` densities, each solved by memoized
backtracking with a fresh map — roughly 1.4M lookups on 22-byte string keys.
Container, x86-64, 4 cores; full numbers and environment in
[`bench/results.container-x86.json`](bench/results.container-x86.json). See
[BENCHMARKS.md](../../../BENCHMARKS.md) for methodology and caveats.

| lang | mean | vs C | notes |
|---|---:|---:|---|
| C | 326.5 ms ± 3.7 | 1.00× | hand-rolled open-addressing table |
| **Kāra** | **527.7 ms ± 9.8** | **1.62×** | `Map[String, bool]`, SipHash-1-3 |
| Go | 714.4 ms ± 29.5 | 2.19× | `map[string]bool` |
| Rust (`-O`, overflow-checks=on) | 873.6 ms ± 15.0 | 2.68× | `HashMap<String, bool>` |
| Rust (`-O`) | 870.6 ms ± 15.3 | 2.67× | |

Kāra is **1.66× faster than equal-safety Rust** here and comfortably ahead of
Go. That is the opposite of [#293](../293-flip-game/), where the same three
languages ran string-building and Kāra sat *behind* Rust — the workload moved
from allocating strings to hashing them, and the ordering changed with it.

> **Re-measured 2026-08-22**, after `B-2026-08-21-6` replaced Kāra's FxHash
> `Map` default with keyed SipHash-1-3 (below). The first cut of this table was
> taken on the FxHash compiler and read `1.48×`; the section that follows is
> what changed and what it cost. Read the **ratios**, not the absolutes: C
> reproduced to within 1.4% across the two runs but Rust and Go did not
> (Rust `-O` moved 705 → 871 ms on a nominally identical container image), so
> the two runs are not one machine and only the within-run column is safe.

### The hasher is the obvious explanation, and it is *still* mostly wrong

Rust's `HashMap` defaults to SipHash-1-3, seeded per process and DoS-resistant.
When this kata was written Kāra's `Map` emitted FxHash — rotate/XOR/multiply,
compile-time-constant seed, no flooding resistance — so the head-to-head priced
a **safety difference** as if it were code generation, the mistake
BENCHMARKS.md forbids on integer overflow. That was `B-2026-08-21-6`, and
**fixing it removed the asymmetry**: the default is now keyed SipHash-1-3 on
both sides, so the table above is already an equal-hash comparison.

That makes the cost of the keyed default directly measurable, because
`Map[K, V, FxBuildHasher]` now resolves and opts back out:

| | mean |
|---|---:|
| Kāra, `Map[String, bool]` (SipHash-1-3, keyed) | 522.1 ms ± 6.0 |
| Kāra, `Map[String, bool, FxBuildHasher]` | 471.6 ms ± 5.8 |

**Hash-flooding resistance costs 1.11× here** — and note where the second row
lands: 471.6 ms against the 476.2 ms this kata first recorded, confirming that
the original `1.48×` was the FxHash number and that the whole of the regression
to `1.62×` is the new default, not a codegen change.

But 1.11× is not the gap to C. Even unkeyed, Kāra is 1.44× C on this workload,
so **the hasher explains about a fifth of the distance and the rest is
unattributed** — which is what the original probe concluded, and it survives
its own premise being replaced. The Rust-side transplant
([`bench/flipgame2_fx.rs`](bench/flipgame2_fx.rs)) still agrees from the other
direction: Rust with SipHash-1-3 and Rust carrying Kāra's old FxHash byte-loop
measure 870.6 ms and 849.7 ms, indistinguishable next to a 2.7× gap. It is now
a historical control rather than a fairness correction — it models the
`FxBuildHasher` opt-in, not the default — and it stays byte-at-a-time, so it
prices *that* hash function and not the best available fast hash.

The probe is a side file, not a `bench.sh` lane, and must be built by hand:

```
rustc -O flipgame2_fx.rs -o target/flipgame2_fx && ./target/flipgame2_fx
```

### Two gaps this kata found — both now fixed

Writing the probe meant reading how `Map` actually hashes, and the answer did
not match the spec. Both were filed in the compiler repo rather than worked
around here, and both have since landed:

- **`B-2026-08-21-6`** — design.md said twice that `Map`/`Set` use
  `SipHash13BuildHasher` seeded per process, and that iteration order therefore
  "differ[s] from one run to the next". None of it held: the same binary gave
  byte-identical iteration order across runs, `karac run --interp` ordered
  differently from `karac build` (each deterministically), and
  `Map[K, V, FxBuildHasher]` — design.md's own spelling — did not resolve, so
  there was no opt-in either way. **Fixed**: the hash now lives in one shared
  `karac-hash` crate that both backends bottom out in, it is SipHash-1-3 under
  a per-process random key (`KARAC_HASH_SEED=<n>` pins it for reproducible
  runs), and the `FxBuildHasher` opt-in resolves. The benchmark section above
  is the price.
- **`B-2026-08-21-8`** — the interpreter's `Map` was an association list
  (`Vec<(Value, Value)>`, looked up with `iter().find`), so every operation was a
  linear scan. Insert-then-lookup of *n* keys measured 0.65 / 2.02 / 7.16 /
  27.51 s for n = 1000 / 2000 / 4000 / 8000 — 4× per doubling, quadratic —
  against 0.00 s compiled. **Fixed the same day**; the same probe now runs in
  0.62 s at n = 8000.

### The bands are not waiting on that fix — I checked, and I was wrong

When the quadratic `Map` was filed, this kata's differential bands were cut to
12/10/18/16 and the cut was attributed to it. With the fix landed, the obvious
follow-up was to put them back. **The measurement says no:**

| | interpreter |
|---|---:|
| band 12/10/18/16, before the `Map` fix | 191.60 s |
| band 12/10/18/16, after the `Map` fix | 215.28 s |
| band 13/10/18/16, after the `Map` fix | 440.92 s |

Not one second faster. (The two 12-band runs are from different container
instances, so read them as *unchanged* rather than as a regression.) The cost is
building a fresh successor `String` per node inside `next_states` — which no map
change touches — and one more band step costs **7.3 minutes** on a file that has
to agree on four surfaces.

So 12 is the right band, and it was the right band for a reason nobody had
checked. The lesson is the same one the `String.push` episode taught two katas
earlier: a plausible attribution is not a measurement, and the way to tell them
apart is to fix the suspected cause and see whether anything moves.
