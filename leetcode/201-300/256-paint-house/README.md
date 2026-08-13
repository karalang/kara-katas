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

### What the x86 corroboration run shows

| lang | mean (ms) | σ |
|---|---|---|
| Rust | 200.0 | 12.6% |
| C | 201.8 | 8.9% |
| Go | 208.2 | 10.7% |
| Kāra | 214.6 | 10.9% |
| Rust (checked) | 220.1 | 9.6% |

**This is a four-way tie and should not be read as a ranking.** The full spread
is 7.3% while every σ is 9–13%, so the intervals overlap almost entirely. Kāra
appearing below C and Rust here is not a result, and neither is it edging
equal-safety Rust.

Stated plainly because this lane resisted measurement harder than any other in
the corpus. This host's run-to-run σ for the *same binary* swings between 10% and
26%; that was confirmed by re-measuring one binary and watching σ move 25.8% →
13.7% with nothing changed. Three candidate causes were tested and refuted —
container load (still noisy at load 0.59), working-set size (the resize above did
not reduce σ), and auto-par thread startup (`KARAC_AUTO_PAR=0` measured the
same). The resize was kept on its own merits, not as a variance fix.

Published numbers await the Apple-silicon host —
`bench/results.container-x86.json` is corroboration only (BENCHMARKS.md § Hosts),
and on this lane that caveat is doing more work than usual.

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
