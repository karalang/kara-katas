# 2896. Apply Operations to Make Two Strings Equal

You are given two **0-indexed** binary strings `s1` and `s2`, both of
length `n`, and a positive integer `x`.

You can perform any of the following operations on the string `s1`
**any** number of times:

- Choose two indices `i` and `j`, and flip both `s1[i]` and `s1[j]`.
  The cost of this operation is `x`.
- Choose an index `i` such that `i < n - 1` and flip both `s1[i]` and
  `s1[i + 1]`. The cost of this operation is `1`.

Return *the **minimum** cost needed to make the strings* `s1` *and*
`s2` *equal, or return* `-1` *if it is impossible.*

```
s1 = "1100011000", s2 = "0101001010", x = 2  ->  4
s1 = "10110",      s2 = "00011",      x = 4  ->  -1
```

**Constraints:** `n == s1.length == s2.length`; `1 <= n, x <= 500`;
`s1` and `s2` consist only of `0` and `1`.

## Approaches

| file | mechanism |
|---|---|
| `flips.kara` ★ | only the places where the strings differ matter. Two of them can be fixed together by the x operation, x for the pair, or a difference and the next by the cost-1 operation run along the gap between them, the gap's length. So the differences are paired up in order: in costs doubled, each difference either takes x, half a pair, or pairs with the one before at twice its gap. An odd count cannot be paired |
| `flips_memo.kara` | the ★ arm's recurrence top down: the best for the differences from i on is the better of x for i alone and twice the gap to the next for i paired with it, each with the best after; memoised in a `Vec[i64]`, the differences found through `bytes().iter().zip(..)` |
| `flips_states.kara` | along the string, not the differences: at each place the state is whether a cost-1 operation from the place before flips this one too, and whether an odd number of places so far took the x operation, waiting for a partner; four states, rolled forward in an `Array` |
| `flips_rolling.kara` | the ★ arm's recurrence kept in two numbers, the best up to the difference before and up to this one, rolled forward as each difference is found, the string walked once |
| `flips_solution.kara` | a Rust solution as LeetCode's Rust users write it: the differing places gathered from `as_bytes()` as a `Vec<usize>`, then `f[i + 1] = (f[i] + x).min(f[i - 1] + (p[i] - p[i - 1]) as i32 * 2)` in doubled costs, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

The pairing was checked first against a Dijkstra search in Python over
3000 random pairs of up to 8 characters, before any arm was written.

Every arm prints the same 4 lines: LeetCode's two examples; 500
characters, LeetCode's most, every one different, with x 500 and with
x 1, and different at every third place; then 3000 random pairs of 1 to
10 characters with x 1 to 5, and 300 of 100 to 500 with x up to 500,
every other s2 a few flips from s1, as the count that cannot be made
equal, a total of the other costs and a checksum. `flips.py` mirrors the
★ arm and its output is byte-identical.

```
4 -1
250 250 -1
3000 short pairs: 1519 impossible, costs total 2845, checksum 350952481
300 long pairs: 155 impossible, costs total 17560, checksum 220911153
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: s1 as a bit mask, every operation an edge, x for any
two places and 1 for two neighbours, and the cheapest way to s2 found
by Dijkstra's search with a `PriorityQueue[(i64, i64)]`, -1 when s2 is
never reached. It draws 2000 random pairs of 1 to 7 characters with x 1
to 5, then 50 of up to 500, x up to 500, every other one with s2 a few
flips from s1, all before any arm answers; the literal reading is asked
only of the first 2000.

| | property |
|---|---|
| P1 | up to 7 characters, the answer is the literal reading's |
| P2 | s1 and s2 swapped: the same answer |
| P3 | both reversed: the same answer |
| P4 | x doubled: -1 still, or from the answer to twice it |
| P5 | -1 exactly when an odd number of places differ, else from half that number to x times it; and s1 against itself costs 0 |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, costs total 3235: checksum
827718518, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and a Python search over the same cases gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a neighbouring pair's gap not doubled | P1 695, P5 507, P6 720 |
| M2 | ★: x taken whole for each difference | P1 101, P6 106 |
| M3 | memo: x alone one dearer | P1 101, P6 106 |
| M4 | memo: a pair's second difference counted again | P1 526, P6 551 |
| M5 | states: a cost-1 operation counted at half | P1 695, P5 507, P6 720 |
| M6 | states: the x operation needing no partner | P1 989, P4 325, P5 1010, P6 1010 |
| M7 | rolling: a gap one short | P1 669, P5 507, P6 694 |
| M8 | rolling: the best before never moved on | P1 235, P3 92, P5 207, P6 257 |
| M9 | solution: the first difference free | P1 301, P3 7, P4 116, P5 146, P6 306 |
| M10 | solution: a gap taken three times | P1 277, P6 301 |

## Benchmarks

The bench draws 5000 pairs of 500 characters, LeetCode's most, x up to
500, every other s2 a few flips from s1, all first, then answers each
20 times by the ★ arm in all five languages. Kāra, Rust and Go turn each
string into characters per call, as the ★ arm does; C reads the bytes
where they lie. Every implementation prints `5000 pairs of 500, 20
rounds: costs total 10280920, checksum 403996864`.

BENCHTAB

## Verification

All five arms print the same output as `flips.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

Two of the four own arms needed `karac fix`. `flips_states` called
`s1.as_bytes()`, Rust's name; the check names Kāra's, `bytes()`, and the
fix writes it. `flips_memo` zipped `s1.bytes().zip(s2.bytes())`; a
`bytes()` is a `Slice[u8]`, which takes `.iter()` before an adaptor, and
the check says so and the fix writes both `.iter()`s in. Beside that
real error the check printed two cascading ones, `tuple pattern used
but type is ?T9` and `?T10`, naming the inference variables of the
unresolved zip; both went with the fix. That family is not in the kara ledger yet: the kata rows are at
their cap, so the row waits for a free slot.

LeetCode's Rust template took 12 `karac fix` edits over two runs, the
wrapper included: `struct Solution {}` came for the `impl`; `Vec<..>`
became `Vec[..]` and the places' `Vec<usize>` a `Vec[i64]`;
`as_bytes()` became `bytes()` twice; `|&i|` lost its `&`; `vec![0i32;
p.len() + 1]` became `Vec.filled(p.len() + 1, 0i32)`; the wrapper's two
`.clone()`s, redundant for borrowed `String` parameters, went, as did its
`as i64` on the result, and `Solution::` took `.`. The `as i32` on the
`usize` gap stays as a cast of an `i64` difference.
