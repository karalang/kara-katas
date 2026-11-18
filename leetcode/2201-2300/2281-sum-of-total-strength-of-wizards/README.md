# 2281. Sum of Total Strength of Wizards

As the ruler of a kingdom, you have an army of wizards at your command.

You are given a **0-indexed** integer array `strength`, where
`strength[i]` denotes the strength of the `i`th wizard. For a
**contiguous** group of wizards (i.e. the wizards' strengths form a
**subarray** of `strength`), the **total strength** is defined as the
**product** of the following two values:

- The strength of the **weakest** wizard in the group.
- The **total** of all the individual strengths of the wizards in the
  group.

Return *the **sum** of the total strengths of **all** contiguous groups
of wizards*. Since the answer may be very large, return it **modulo**
`10^9 + 7`.

A **subarray** is a contiguous **non-empty** sequence of elements
within an array.

```
strength = [1,3,1,2]  ->  44
strength = [5,4,6]    ->  213
```

**Constraints:** `1 <= strength.length <= 10^5`; `1 <= strength[i] <=
10^9`.

Count each group at its weakest wizard. Wizard `i` is the weakest of
every group from just past `L`, the nearest weaker wizard on its left,
to just before `R`, the nearest no stronger on its right; the asymmetry
counts a group whose weakest strength repeats once, at the rightmost.
Both are found by a monotonic stack. A group's total is a difference of
prefix sums `P`, and summed over every left and right end it is a
difference of the prefix sums' own prefix sums `PP`:

```
(i - L) * (PP[R + 1] - PP[i + 1]) - (R - i) * (PP[i + 1] - PP[L + 1])
```

O(n), modulo `10^9 + 7` throughout.

## Approaches

| file | mechanism |
|---|---|
| `wizards.kara` ★ | two monotonic-stack passes for `L` and `R`, the tables `P` and `PP`, and each wizard's strength times its groups' totals by the formula above |
| `wizards_onepass.kara` | one stack of rising strengths closed by a wizard of strength 0 past the end; a wizard popped has the arriving one as `R` and the new top as `L`, and is summed then |
| `wizards_dp.kara` | by right ends: for the groups ending at `r`, the sum of their weakest strengths and the same weighted by `P` at each start, each built from the nearest weaker wizard's by one stack pass; the groups' totals are `P[r + 1]` times the first less the second |
| `wizards_struct.kara` | `struct Army` of the strengths and both tables; `reach` sets each wizard's ends as it is popped, `span` reads a run of `P`, `groups` the totals and `total` the sum; a repeated weakest is counted at the leftmost |
| `wizards_iter.kara` | in chains: `P` and `PP` by `scan` after a leading 0 by `chain`, the two stack passes, then each wizard's share by `map` and the sum by `fold` |
| `wizards_solution.kara` | LeetCode's Rust template: `Vec<i32>` in, `i32` out; `while let Some(&t) = st.last()` for each pass, `map_or` for the ends, `pre` for `PP`, and the remainder made positive at the end; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more (one wizard, 49; the strongest alone, also 49, since 10^18 is 49
modulo 10^9 + 7; three alike, 40; rising and falling, 238 both), each
with its total; then 2000 random armies of 1 to 40 wizards of strength
up to 3, 100 or 10^9, with a checksum; then three of the constraints'
largest, 10^5 wizards: random up to 10^9 (634088063), all of strength
10^9 (611131623), and rising from 1 (342969129). `wizards.py` mirrors
the ★ arm and its output is byte-identical; it was also checked against
the sum over every slice by `min` and `sum` on 3000 random armies.

The iter arm first chained `[0].iter()` onto the `scan` of the prefix
sums. `karac check` refuses it as Rust would: `[0].iter()` yields a
`ref i64` and the `scan` an `i64`, so the two cannot `chain`, and
`karac fix` adds `.cloned()` to the first.

`karac fix` carries the template in one round, reporting 38 edits.
Among them: `Vec<i32>` and `Vec<i64>` to brackets, `vec![-1i64; n]` to
`Vec.filled(n, -1)` and `vec![n as i64; n]` to `Vec.filled(n, n)`,
`Vec<usize>` to `Vec[i64]`, `while let Some(&t) = st.last()` to `while
let Some(t) = st.last().cloned()`, `map_or(-1, |&t| t as i64)` to
`map_or(-1, |t| t)`, the `i64` suffixes and the `as usize` and `as i64`
casts dropped, `struct Solution;` to `struct Solution {}`, and in the
adapter `&Vec<i64>` to a bare `Vec[i64]`, `|&x|` to `|x|`, `Solution::`
to `Solution.` and the `as i64` dropped. `1_000_000_007` is kept as
written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every group from every left end to every right end, its
weakest strength and its total found by walking it, their product added
up. No stacks and no prefix sums. It checks 300 random armies of 1 to
12 wizards of strength up to 2, 5 or 1000; then 30 of wizards all
alike; then 30 rising or falling. All 360 are drawn before any arm
answers. No total there reaches 10^9 + 7, so the bounds in P4 are read
without the modulus.

| | property |
|---|---|
| P1 | the total is the literal reading's |
| P2 | the army reversed: the same total |
| P3 | every strength times 3: the total times 9 |
| P4 | between the least strength and the greatest, times the sum of every group's strengths |
| P5 | a wizard of the least strength added at the front: the total grown by that strength times the sums of the groups the wizard starts |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 867625551, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that takes
`min` and `sum` of every slice. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a repeated weakest counted twice | P1 187, P4 156, P5 360, P6 187 |
| M4 | ★: the starts never taken off | P1 331, P2 247, P4 106, P5 360, P6 331 |
| M5 | ★: the groups not weighed by strength | P1 348, P3 360, P4 203, P5 203, P6 348 |
| M7 | onepass: the closing wizard of strength 2 | P1 157, P2 96, P3 157, P4 123, P5 157, P6 157 |
| M8 | onepass: with nothing weaker, the reach stopping at wizard 0 | P1 360, P2 275, P4 244, P5 355, P6 360 |
| M10 | onepass: the ends weighed by the right ends' count | P1 319, P2 272, P4 205, P5 360, P6 319 |
| M12 | dp: the weighted sums never grown | P1 257, P2 273, P4 20, P5 290, P6 257 |
| M13 | dp: the weaker wizard's groups dropped | P1 257, P2 272, P4 216, P5 290, P6 257 |
| M16 | dp: one start more weighted | P1 232, P2 235, P4 116, P5 257, P6 232 |
| M17 | struct: a repeated weakest counted twice | P1 187, P4 101, P5 360, P6 187 |
| M18 | struct: every wizard reaching the right end | P1 252, P2 277, P4 107, P6 252 |
| M19 | struct: a span one short at its start | P1 357, P2 274, P4 249, P5 331, P6 357 |
| M22 | iter: the strengths for the prefix sums | P1 331, P2 277, P4 298, P5 360, P6 331 |
| M23 | iter: the second table from 1 | P1 360, P2 254, P3 360, P4 70, P5 328, P6 360 |
| M24 | iter: the largest share for the sum | P1 331, P2 111, P4 285, P5 360, P6 331 |
| M28 | solution: each prefix sum from two back | P1 331, P2 277, P4 246, P5 359, P6 331 |
| M29 | solution: the right end one short | P1 360, P2 276, P4 327, P5 360, P6 360 |

P1, P4 and P6 kill all seventeen, P5 sixteen, P2 fourteen, and P3
three. P4's bounds catch every edit here: a group counted twice or
dropped, or a total short or long, moves the sum past the least
strength's or the greatest's share of the groups' sums. P5 misses only
the struct arm's every wizard reaching the right end: the added wizard,
the weakest, rightly reaches it anyway, and every other wizard's error
is the same with it as without. P2 misses the three edits that stay
symmetric under reversal: a repeated weakest counted twice, in either
arm, and the groups not weighed by strength. P3 catches only the edits that add or weigh by something that
does not grow with the strengths: the groups unweighted, the closing
wizard of a fixed strength, and a table started at 1.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Four fail as a kept one does: the ★ arm's and the
template's repeated weakest counted nowhere (M1, M27) fail the same
checks as the struct arm's counted twice (M17); and
the dp arm's group from wizard 0 left out and the template's reach
stopping at wizard 1 (M14, M31) as the onepass arm's reach stopping at
wizard 0 (M8). Ten fail in ways of their own and are left out because
their arms keep enough: the ★ arm's last right end left out and first
wizard left out of the sums (M3, M6), the onepass arm's ends from the
wizard itself and first start's sum left out (M9, M11), the dp arm's
totals read from the prefix before (M15), the struct arm's starts added
and each prefix sum counted twice (M20, M21), the iter arm's two edits
of the reach with nothing weaker (M25, M26), and the template's one
left end fewer (M30).

The iter arm's M22 first returned the strength itself from the `scan`,
`Some((sum, x))`, which `karac check` refuses as it should: `x` is a
`ref i64` where the item is an `i64`. It returns `x % MOD`.

## Verification

Every arm prints the same output as `wizards.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the differential takes 0.8 s, the dp arm 1.6 s,
the onepass arm 1.7 s, the ★ and struct arms 2.3 s and 2.4 s, the
template 3.3 s, and the iter arm 4.3 s.

## Benchmarks

The bench answers 30 armies of the constraints' largest, 10^5 wizards
of strength 1 to 10^9, with the ★ arm in all five languages. Every
implementation prints `30 armies of 10^5: checksum 16349188`. Each
builds its army a wizard at a time from the same generator, two draws
to a wizard.

BENCHTAB
