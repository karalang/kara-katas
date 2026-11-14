# 2139. Minimum Moves to Reach Target Score

You are playing a game with integers. You start with the integer `1` and
you want to reach the integer `target`.

In one move, you can either:

- **Increment** the current integer by one (i.e., `x = x + 1`).
- **Double** the current integer (i.e., `x = 2 * x`).

You can use the **increment** operation **any** number of times,
however, you can only use the **double** operation **at most**
`maxDoubles` times.

Given the two integers `target` and `maxDoubles`, return *the minimum
number of moves needed to reach* `target` *starting with* `1`.

```
target = 5, maxDoubles = 0     ->  4
target = 19, maxDoubles = 2    ->  7
target = 10, maxDoubles = 4    ->  4
```

**Constraints:** `1 <= target <= 10^9`; `0 <= maxDoubles <= 100`.

A double is worth most when the number is largest, so going forward the
doubles come last, and going back from the target they come first:
while doubles are left, an odd target is one more than an even one and
an even one is half of itself doubled. Once they run out, what is left
is climbed one at a time. O(min(log target, maxDoubles)).

## Approaches

| file | mechanism |
|---|---|
| `moves.kara` ★ | from the target back to 1 by a loop over a rebound `let mut target = target`, an odd target stepped down and an even one halved while doubles last, then the rest climbed |
| `moves_rec.kara` | the same walk as a recursion: none at 1, all climbs once the doubles are gone, else one more than the odd step or the halving |
| `moves_bits.kara` | no loop: with h halvings, the lesser of the doubles and the target's width less 1 by `leading_zeros`, the low h bits cost h halvings and one step per 1 among them by `count_ones`, and the rest, the target shifted right by h, is climbed |
| `moves_struct.kara` | a `struct Climb` of the number still to reach, the doubles left and the moves made, taken back one move at a time by `back` (`mut ref self`) while `can_halve` (`ref self`) says a double still helps |
| `moves_forward.kara` | forward from 1: climb to the target's top part, then for each low bit, highest first, double and step once more for a 1, the moves counted by a `fold` over the bits carrying the pair (number reached, moves), its closure taking a tuple pattern |
| `moves_solution.kara` | LeetCode's Rust template: the backward walk over `mut` parameters in `i32`; carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and five
more (already there, already there with doubles to spare, no doubles at
the largest target, every double the largest target could use, and a
power of two), each with its answer; then the total and a checksum over
2000 random targets of 1 to 100, 1 to 10^4 or 1 to 10^9 in turn, with 0
to 10 doubles or 0 to 100. `moves.py` mirrors the ★ arm and its output
is byte-identical.

No compiler gap was met. `karac fix` carries the template in two rounds
of 6 and 2 edits: Rust's spellings (each `mut` parameter to `own`, with
a `let mut` of it at the top of the body, which keeps Rust's meaning,
`&&` to `and`, `struct Solution;` to `struct Solution {}`,
`Solution::` to `.`); then `moves` typed `i32`, since a bare `0` takes
`i64` and the method returns it as its `i32`, and the adapter's `as i64`
dropped, since an `i32` widens on return.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a search, breadth first, from 1 with no double spent, each
move adding 1 or, while doubles are left, doubling, until the target is
reached; numbers past the target are never needed, since neither move
makes a number smaller. No order of the moves is assumed. It checks 300
random targets of 1 to 200 with 0 to 8 doubles; then 30 powers of two
up to 2^9 with 0 to 10; then 30 of one less than a power of two. All
360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the moves are the statement read literally |
| P2 | one double more: no more moves |
| P3 | no doubles: the target less 1 |
| P4 | the target doubled, with one double more: one move more |
| P5 | the target doubled and 1 added, with one double more: two more |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 targets: checksum 484921821, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
targets by the same search. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Thirty-five edits to the differential, four to seven to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a double never spent | P1 159, P4 30, P5 30, P6 159 |
| M3 | ★: the climb left uncounted | P1 225, P2 225, P3 352, P6 225 |
| M5 | ★: a halving counted twice | P1 321, P2 36, P4 360, P5 360, P6 321 |
| M6 | rec: at 1, one move | P1 135, P2 36, P3 8, P6 135 |
| M7 | rec: no doubles costing the target | P1 225, P3 352, P6 225 |
| M34 | rec: a halving spending two doubles | P1 223, P2 139, P4 311, P5 311, P6 223 |
| M11 | bits: the width one more | P1 94, P2 41, P6 94 |
| M12 | bits: the halvings all the doubles | P1 94, P2 135, P6 94 |
| M13 | bits: the low bits one too many | P1 235, P2 24, P3 167, P6 235 |
| M16 | climb: halving while one double is left over | P1 194, P4 31, P5 31, P6 194 |
| M18 | climb: the climb counted from 0 | P1 360, P3 360, P6 360 |
| M19 | climb: the moves never counted | P1 321, P4 360, P5 360, P6 321 |
| M21 | forward: the bits walked lowest first | P1 152, P2 22, P4 241, P5 264, P6 152 |
| M22 | forward: a 1 bit's step uncounted | P1 241, P5 360, P6 241 |
| M29 | forward: a 0 bit costing the step a 1 bit does | P1 275, P2 24, P4 360, P5 360, P6 275 |
| M32 | solution: the adapter's doubles one more | P1 189, P3 342, P6 189 |
| M33 | solution: the template's even and odd swapped | P1 143, P4 143, P5 360, P6 143 |

P1 and P6 kill all seventeen, P2 nine, P5 nine, P4 eight and P3 six. P2
gives one double more, which a right answer never pays for; it sees an
edit whose answer can rise with the doubles: a halving counted twice or
spending two doubles (M5, M34), a climb or a move left uncounted where
a double replaces it (M3, M6), the width or the low bits wrong (M11,
M12, M13), and the forward plan's bits walked or costed wrongly (M21,
M29). P4 and P5 double the target, with a 1 added for P5, and give the
double that takes; they see an edit that mis-prices a double or a step
at the end of the walk: a double never spent or kept back (M2, M16,
M34), a halving counted twice or never (M5, M19), the forward plan's
bits (M21, M29), and the template's odd and even swapped (M33); P5 also
sees a 1 bit's step uncounted (M22). P3 takes the doubles away, so the
answer is the target less 1; it sees an edit to the climb or the end of
the walk: the climb uncounted or counted from 0 (M3, M7, M18), a first
move at 1 (M6), the low bits taken without a double (M13), and the
adapter's one double more (M32).

Of the thirty-five, eighteen were not kept. Four are equivalent: the ★
arm's walk and the template's stopping at 2, since from 2 a halving and
a step both cost one move; the forward arm's width one short, since
its top part is then 2 or 3, climbed in one or two moves, as a double
and a step would be; and the forward arm's check of the number reached
dropped, since the plan always reaches it. None fails by a crash.
Thirteen fail as a kept one does: five ways of dropping a 1 bit's step
or halving an odd number (the ★ arm's odd target halved down, the
recursion's odd step uncounted and its odd target halved too, the bits
arm's low 1 bits uncounted, the climb's odd number halved), as M22; the
recursion's halving spending no double and the template's double never
spent, as M2; the bits arm's top part not climbed and the forward arm's
top part counted by its 1 bits, as M3; the forward arm's double more
than the width, as M11; the adapter's doubles one fewer, as M16; the
forward arm's climb from 0, as M18; and the climb's doubles left counted
as moves, as M12. One is killed with checks of its own but was left out
because its arm keeps its share: the adapter passing no doubles (P1
312, P4 352, P5 352, P6 312).

## Verification

Every arm prints the same output as `moves.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.1 s to 0.2 s and the
differential 0.5 s.

## Benchmarks

The bench builds 1000 targets of 1 to 10^9 once; then runs 4000 rounds
over them, round r asking each target plus r with r % 40 doubles, so
that no solve repeats one before, 4000000 solves in all, with the ★ arm
in all five languages. Every implementation prints `4000000 solves:
93402650736174 moves in all, checksum 304810354`.

BENCHTAB
