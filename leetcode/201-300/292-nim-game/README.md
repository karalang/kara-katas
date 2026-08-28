# 292. Nim Game

A heap of `n` stones. You and a friend alternate turns, you first, and each turn
removes 1, 2 or 3 stones. **Whoever takes the last stone wins.** Both play
optimally. Can you win?

```
n = 1, 2, 3   ->  true     take them all
n = 4         ->  false    whatever you leave (3, 2, 1) they take
n = 5, 6, 7   ->  true     leave exactly 4
n = 2147483647 -> true     the top of the constraint range
```

**Constraint:** `1 ≤ n ≤ 2³¹ − 1`. That bound is not decoration — it is what
makes two of the three approaches below unable to answer the question.

## Approaches

| file | mechanism | cost | reaches |
|---|---|---|---|
| `nim_game.kara` ★ | `n % 4 != 0` | O(1) | the whole range |
| `nim_game_dp.kara` | build the win/lose table | O(n) time, O(n) space | memory-bound |
| `nim_game_memo.kara` | memoized game-tree search | O(n), recursion depth `n` | **stack-bound, ~100k** |
| `differential.kara` | three bands, each honest about its reach | — | — |
| `bench/nimgame.kara` | the table to 20,000,000 | benchmark lane | — |

## A one-line answer is not the same as an obvious one

Written cold, `n % 4 != 0` looks like a magic constant. Derived, it is forced.

Call a heap **losing** if the player about to move cannot win against optimal
play. `n = 0` is losing — no stone to take, and whoever moved last already won.
A position is **winning** exactly when *some* move reaches a losing position
(the mover chooses); it is **losing** when *every* move reaches a winning one
(the opponent chooses next).

From `n = 0` losing, the moves reach 1, 2 and 3 — each can step back to 0, so
all three are winning. Then 4 must reach 3, 2 or 1, all winning, so 4 is losing.
And that is the whole induction: from a multiple of 4 every move lands on a
non-multiple, and from a non-multiple you can always take `n % 4` and hand back
a multiple.

So the answer is not a pattern spotted in a table — it is the statement that
**1, 2, 3 cannot span a gap of 4**. `nim_game_dp.kara` computes the table the
induction describes, and reading it is how anyone actually finds this:

```
i    0  1  2  3  4  5  6  7  8  9 10 11 12
win  F  T  T  T  F  T  T  T  F  T  T  T  F
```

## The differential says what it cannot check

The three arms do not reach the same distance, and the differential is built in
bands around that rather than hiding it:

- **Band 1** — all three arms, every `n` from 0 to 800. 801 cases, 0 mismatches.
- **Band 2** — closed form vs DP only, sampled out to 100,000. 12 cases, 0 mismatches.
- **Band 3** — the closed form alone near 2³¹, checked against the *property*
  the induction proves rather than an oracle. **This is not independent
  confirmation**, and the output says so on its own line.

Above the DP's reach there is no second implementation to disagree with. Testing
`n ≤ 1000` and implying the rest would be the exact dishonesty the repo's rules
call out, so the bands are reported separately and band 3 is labelled.

**Band 1's size is set by the interpreter, not by taste.** Both computational
arms are O(n) and are called once per `n`, so the band is quadratic in its
bound: under `--interp`, 200 → 11 s, 400 → 29 s, 800 → 120 s, and 4000 did not
finish in an hour. A differential the interpreter cannot run can never catch an
*interpreter-only* bug — kata [#289](../289-game-of-life/) found exactly one
that way (`B-2026-08-20-32`, a shallow nested clone that three compiled surfaces
got right). So the band is sized to keep all four surfaces checkable rather than
to maximise a number only the compiled legs would ever see.

Three planted mutations are each caught *and localized*: a wrong modulus breaks
both arms plus bands 2 and 3; a DP that can only take 1–2 stones breaks the DP
arm alone; a memo whose empty heap is a win breaks the memo arm alone.

## The recursion arm found a compiler bug

`nim_game_memo.kara` recurses once per stone, so its ceiling is the stack. Probed
directly: **depth 100,000 succeeds, depth 200,000 dies.** How it dies is the
finding — a bare `SIGSEGV`, exit 139, with **zero bytes on stderr**. No message,
no hint that recursion depth was the cause.

Measured against the mirrors on the same machine and the same recursion:

| | exit | stderr |
|---|---|---|
| **Kāra (AOT)** | 139 SIGSEGV | *(empty)* |
| C `-O0` | 139 SIGSEGV | *(empty)* |
| Rust `-O0` | 134 SIGABRT | `thread 'main' has overflowed its stack` |
| Go | 2 | `runtime: goroutine stack exceeds …` |

Kāra lands on the C side of that line, behind both comparators it otherwise
measures itself against — and BENCHMARKS.md frames those comparisons as an
*equal-safety* tie precisely because silent wrongness is what the language
refuses. Filed as `B-2026-08-20-34`.

One measurement worth flagging: at `-O` rustc turns that recursion into a loop
and exits 0, which would have made Rust look like it has no stack limit at all.
The honest comparison is `-O0`, where the recursion actually happens.

## Benchmarks
<!-- bench-staleness -->
> **Figures in this section are undated; the feed was last measured 2026-08-28.** Where the two disagree, [`bench/results.json`](bench/results.json) and the [charts](../../../BENCHMARKS.md) are current; the numbers below are kept because the analysis around them explains *why* the shape is what it is, and that reasoning outlives the milliseconds.

> **Host:** the tables below are a shared **x86-64 Linux cloud container**
> snapshot, kept as [`bench/results.container-x86.json`](bench/results.container-x86.json).
> The canonical Apple M5 Pro lane is [`bench/results.json`](bench/results.json) —
> that is the file `scripts/consolidate-bench.sh` feeds into the top-level chart,
> and it is current as of the date stamped above. Absolute milliseconds are NOT
> comparable between the two hosts; only the **within-file cross-language
> ratios** are.

The closed form is one modulo, so timing it would measure the loop around it.
The bench builds the **table** instead — a real O(n) workload with a branchy
inner loop over a `Vec[bool]`, and the shape a reader writes before spotting the
pattern. See [BENCHMARKS.md](../../../BENCHMARKS.md) for methodology. Sink is
`losing 5000001 checksum 107109439` across Kāra, C, Rust and Go.
