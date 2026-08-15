# 256. Paint House

`n` houses in a row, three colours, `costs[i][c]` to paint house `i` colour `c`.
No two adjacent houses may share a colour. Minimise the total.

```
[[17,2,17],[16,16,5],[14,3,19]]  ->  10      (2 + 5 + 3)
[[7,6,2]]                        ->   2
[]                               ->   0
```

**Constraints:** `0 ≤ n ≤ 100`; `1 ≤ costs[i][j] ≤ 20`.

## Approaches

| file | direction | state | space |
|---|---|---|---|
| `paint_house.kara` ★ | bottom-up, rolling | three scalars | O(1) |
| `paint_house_table.kara` | bottom-up, retained | `Vec` of triples | O(n) |
| `paint_house_memo.kara` | top-down, memoised | flat `Vec[i64]` + `seen` | O(n) |
| `differential.kara` | 6,000 randomized cost tables, all three agree | — | — |

## The mechanism

The constraint reaches back **exactly one house**, so the cheapest way to reach
house `i` in colour `c` is `costs[i][c]` plus the cheaper of the two ways to
reach `i-1` in either other colour. Nothing older than `i-1` is ever consulted —
which is the entire justification for the ★ file keeping three scalars and no
table.

The three files are not three spellings of one loop. The table file **retains**
what the rolling one discards, which is what makes "row `i-1` is all you need" a
testable claim rather than an assumption — and it is the only one of the three
that could reconstruct *which* colour each house took. The memo file recurses in
the opposite direction and answers a different question at each step — "given
this choice, what does the **rest** cost" rather than "what is the best way to
have **arrived** here" — so agreement on the total cross-checks the recurrence
itself, not merely the arithmetic.

## The trap: all three must be computed before any is assigned

```kara
r = costs[i].0 + min2(b, g);
b = costs[i].1 + min2(r, g);   // reads the NEW r — wrong
```

The second line consults house `i`'s own freshly-written red total instead of
house `i-1`'s, folding a house's cost into its own predecessor. The result is too
large and entirely plausible-looking.

**Which inputs expose it was measured, not guessed.** My first guess —
`[[1,2,3],[1,2,3]]` — does not expose it at all; it yields 3 either way, and is
kept in the tests as a *control* precisely for that. The inputs that do separate
them:

| input | correct | in-place |
|---|---|---|
| `[[17,2,17],[16,16,5],[14,3,19]]` | 10 | **26** |
| `[[1,100,100] ×3]` | 102 | **201** |
| `[[5,5,5] ×4]` | 20 | **25** |

The LeetCode example itself is the sharpest witness, which is a useful accident:
the bug cannot survive even the sample input.

## Generator design

A uniform draw exercises one regime, where the cheapest colour usually differs
between neighbours and the adjacency constraint rarely binds at all. Four
families instead:

- **uniform** — the baseline.
- **one-cheap-colour** — the same colour is cheapest at *every* house, so the
  constraint binds at every step and the optimum must alternate. This is the
  family that separates a real solver from one that just takes each house's
  minimum.
- **ties** — costs drawn from `{0,1}`, so equal alternatives are everywhere and
  any tie-break asymmetry between the three surfaces.
- **large** — values near 10⁹, where an n-house total approaches i64 range. Kāra
  traps on overflow rather than wrapping, so a solver accumulating differently
  would abort loudly rather than disagree quietly.

Over 6,000 cases: **32,698 houses, 494 empty inputs**, three solvers agreeing on
every one.

**The harness was tested against the bug it exists to find.** Reintroducing the
in-place update into `solve_rolling` makes it report **4,572 mismatches of
6,000**; restored, `0`.

## Benchmark

`bench/` builds one **150,000-house cost table once**, then sweeps it **800
times** with the rolling three-scalar DP. Sink `913249956`, reproduced by all
four mirrors.

Two design points:

- **Costs are drawn so the constraint binds.** One colour is cheap over *runs* of
  consecutive houses (run length itself varies), so the optimum must repeatedly
  leave the locally-cheapest colour and neither `min2` predicts away. A uniform
  draw would let the answer degenerate towards "take each house's minimum".
- **The table is sized to stay cache-resident** (150k × 24 B = 3.6 MB; measured
  RSS 6.4 MiB). An earlier version used 4M houses, whose 93 MiB working set made
  the lane memory-bandwidth-bound — the wrong thing for a kata whose subject is a
  loop-carried recurrence. Rounds were raised to hold total work constant.

This is a pure **dependent-arithmetic** lane: no allocation in the punch loop at
all, each house reading the previous house's three totals. That complements
[#254](../254-factor-combinations/) (allocation-heavy) and
[#255](../255-verify-preorder-sequence-in-bst/) (`Vec` push/pop).

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 94.7 ± 1.6 ms | 0.91× |
| Rust `-O` | 96.3 ± 1.4 ms | 0.92× |
| Go | 98.1 ± 4.2 ms | 0.94× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 102.7 ± 1.8 ms | 0.99× |
| **Kāra (codegen)** | **104.2 ± 3.4 ms** | 1.00× |

**This lane is finally measurable, and the answer is a tie against equal-safety
Rust** — 104.2 against 102.7 ms, 1.5%, well inside σ. The container could not
resolve it at all: every σ there was 9–13% against a 7.3% total spread, so the
ordering was noise by construction. Here σ is 1.5–4.3% against a 1.10× spread,
which is tight enough to say something.

What it says is modest and worth stating exactly. Kāra is **last of five**, 1.10×
behind C and 1.08× behind wrapping Rust — but the entire deficit is the safety
contract, because against the build that makes the same guarantee it is level.
A three-way DP over a fixed table is arithmetic-dense with a loop-carried
dependency, so overflow checks have nowhere to hide, and they cost Rust 6.6%
(96.3 → 102.7 ms) and Kāra a statistically identical amount.

The container-era caveat about this lane resisting measurement is retained below
because it explains why no ranking was published from that host; it does not
apply to the run above.

### The x86 corroboration run

Container x86-64, `bench/results.container-x86.json` — corroboration only
(BENCHMARKS.md § Hosts), and on that lane the caveat did more work than usual.

| lang | mean (ms) | σ |
|---|---|---|
| Rust | 200.0 | 12.6% |
| C | 201.8 | 8.9% |
| Go | 208.2 | 10.7% |
| Kāra | 214.6 | 10.9% |
| Rust (checked) | 220.1 | 9.6% |

**That table is a four-way tie and was never a ranking.** That host's run-to-run
σ for the *same binary* swings between 10% and 26%; confirmed by re-measuring one
binary and watching σ move 25.8% → 13.7% with nothing changed. Three candidate
causes were tested and refuted — container load (still noisy at load 0.59),
working-set size (the resize above did not reduce σ), and auto-par thread startup
(`KARAC_AUTO_PAR=0` measured the same). The resize was kept on its own merits,
not as a variance fix.

## Kāra features exercised

- **`Slice[(i64, i64, i64)]`** — a 3-tuple element type, saying "exactly three
  colours" in the type rather than in a comment. ([#265](https://leetcode.com/problems/paint-house-ii/)
  generalises to k colours and is where a nested `Vec` belongs.)
- **Tuple construction in an expression position** — `dp.push((a, b, c))` with
  each component a computed sum.
- **A flat `Vec[i64]` memo with a parallel `Vec[bool]` seen-table**, indexed
  `i * 3 + c` — a different ownership surface from the `Vec` of triples.
- **`mut ref` memo and seen threaded through a recursion**, forwarded unmarked
  at the recursive call and `mut`-marked at the owning caller.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the two with
mirrors match Python.

No compiler bugs found. Every construct here — tuple elements, `mut ref`
accumulators, flat memo tables — is one earlier katas have already driven bugs
out of, so this is a clean run over known ground rather than new.

## Running

```bash
karac run paint_house.kara
karac run paint_house_table.kara
karac run paint_house_memo.kara

diff <(karac run paint_house.kara) <(python3 paint_house.py) && echo OK
diff <(karac run paint_house.kara) <(karac run paint_house_table.kara) && echo OK
diff <(karac run paint_house.kara) <(karac run paint_house_memo.kara) && echo OK

# 6,000 randomized cost tables, three solvers cross-checked, mirrored in Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

# run == build, on every program
for f in paint_house paint_house_table paint_house_memo differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
