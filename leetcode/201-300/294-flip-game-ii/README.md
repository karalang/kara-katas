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
    i = i + 1i64;
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
| C | 322.0 ms ± 8.0 | 1.00× | hand-rolled open-addressing table |
| **Kāra** | **476.2 ms ± 13.2** | **1.48×** | `Map[String, bool]` |
| Go | 634.1 ms ± 24.9 | 1.97× | `map[string]bool` |
| Rust (`-O`, overflow-checks=on) | 688.1 ms ± 18.8 | 2.14× | `HashMap<String, bool>` |
| Rust (`-O`) | 705.4 ms ± 45.3 | 2.19× | |

Kāra is **1.44× faster than equal-safety Rust** here and comfortably ahead of
Go. That is the opposite of [#293](../293-flip-game/), where the same three
languages ran string-building and Kāra sat *behind* Rust — the workload moved
from allocating strings to hashing them, and the ordering changed with it.

### The hasher is the obvious explanation, and it is wrong

Rust's `HashMap` defaults to SipHash-1-3, seeded per process and DoS-resistant.
Kāra's `Map` emits FxHash — rotate/XOR/multiply — with a compile-time-constant
seed and no flooding resistance. Comparing them head to head prices a **safety
difference** as if it were code generation, which is the mistake BENCHMARKS.md
forbids on integer overflow.

So [`bench/flipgame2_fx.rs`](bench/flipgame2_fx.rs) transplants Kāra's exact
hash function into the Rust twin — same rotate-left-5, same seed, same
per-byte loop — and changes nothing else:

| | mean |
|---|---:|
| Rust, SipHash-1-3 | 669.7 ms ± 14.1 |
| Rust, Kāra's hash | 675.4 ms ± 31.4 |

**Indistinguishable.** On 22-byte keys the hasher is not where the difference
lives, and Kāra's 1.44× lead is not bought with the weaker default. One caveat
that cuts against the measurement: the transplant is byte-at-a-time to stay
faithful to Kāra's emitted loop, where `rustc-hash` processes 8-byte chunks — so
this prices *Kāra's hash function*, not the best available fast hash. Where the
1.44× actually comes from is unattributed; ruling the hasher out is what this
probe establishes, not what replaces it.

The probe is a side file, not a `bench.sh` lane, and must be built by hand:

```
rustc -O flipgame2_fx.rs -o target/flipgame2_fx && ./target/flipgame2_fx
```

### Two gaps this kata found

Writing the probe meant reading how `Map` actually hashes, and the answer did
not match the spec. Both are filed in the compiler repo rather than worked
around here:

- **`B-2026-08-21-6`** — design.md says twice that `Map`/`Set` use
  `SipHash13BuildHasher` seeded per process, and that iteration order therefore
  "differ[s] from one run to the next". Neither holds: the same binary gives
  byte-identical iteration order across runs, `karac run --interp` orders
  differently from `karac build` (each deterministically), and
  `Map[K, V, FxBuildHasher]` — design.md's own spelling — does not resolve, so
  there is no opt-in either way.
- **`B-2026-08-21-8`** — the interpreter's `Map` is an association list
  (`Vec<(Value, Value)>`, looked up with `iter().find`), so every operation is a
  linear scan. Insert-then-lookup of *n* keys measures 0.65 / 2.02 / 7.16 /
  27.51 s for n = 1000 / 2000 / 4000 / 8000 — 4× per doubling, quadratic —
  against 0.00 s compiled. That is why this kata's differential bands are 12 and
  18 rather than 14 and 22: not caution, a complexity class.
