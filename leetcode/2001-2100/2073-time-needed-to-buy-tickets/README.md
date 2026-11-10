# 2073. Time Needed to Buy Tickets

There are `n` people in a line queuing to buy tickets, where the `0`-th
person is at the front of the line and the `(n - 1)`-th person is at
the back of the line.

You are given a 0-indexed integer array `tickets` of length `n` where
the number of tickets that the `i`-th person would like to buy is
`tickets[i]`.

Each person takes exactly 1 second to buy a ticket. A person can only
buy 1 ticket at a time and has to go back to the end of the line (which
happens instantaneously) in order to buy more tickets. If a person does
not have any tickets left to buy, the person will leave the line.

Return the time taken for the person initially at position `k`
(0-indexed) to finish buying tickets.

```
tickets = [2,3,2], k = 2    ->  6
tickets = [5,1,1,1], k = 0  ->  8
```

**Constraints:** `n == tickets.length`; `1 <= n <= 100`;
`1 <= tickets[i] <= 100`; `0 <= k < n`.

Each second one person buys one ticket, so the time is the number of
tickets bought before person `k` has all theirs. Person `k` buys on
`tickets[k]` rounds of the line. Someone ahead of `k` buys on every one
of them, up to `tickets[k]` tickets; someone behind buys only on the
rounds before `k`'s last, up to `tickets[k] - 1`. O(n). The approaches
differ in whether they count or simulate, and in how they keep the line.

## Approaches

| file | mechanism |
|---|---|
| `tickets.kara` ★ | one pass over `iter().enumerate()`: each person's tickets capped at `tickets[k]` up to `k` and one fewer behind, summed. O(n) |
| `tickets_queue.kara` | the line itself: a `VecDeque` of (place, tickets still wanted) collected from `enumerate()`, the front buying one a second and pushed to the back while it wants more, until `k` leaves. O(sum of tickets) |
| `tickets_rounds.kara` | round by round over a copy of the wants: each round walks the line once, everyone still wanting buys one, and the walk stops when `k` has none left. O(n · tickets[k]) |
| `tickets_fold.kara` | the ★ count as iterator chains: the line split at `k` with `split_at(k + 1)`, the front half's `map` and `sum` capped at `tickets[k]`, the back half's at one fewer |
| `tickets_struct.kara` | the line as a value: a `struct Line` of the wants and a cursor, a method `serve(mut ref self)` that sells the front person a ticket and moves the cursor on to the next who still wants one, wrapping round |
| `tickets_solution.kara` | LeetCode's Rust template (`tickets: Vec<i32>`, `k: i32`, `let k = k as usize`, `iter().enumerate()` with `\|(i, &t)\|` and `.map(..).sum()`), carried by `karac fix` in two rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and five
more, each line, its `k` and the answer; then the sum of the answers
and a checksum for 2000 random lines of 1 to 100 people wanting up to 1,
10 or 100 tickets, each asked about a random place; then the answer for
the constraints' largest, 100 people of 100 tickets asked about the
last. `tickets.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the line kept as a list of (place, tickets still wanted),
each second the front person taken off, buying one and put back at the
end while they want more, until person `k` leaves with their last. It
checks 300 random lines of 1 to 12 people wanting up to 1, 3 or 10
tickets; then 20 where everyone wants the same, and 20 with `k` at the
back. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the people ahead of `k` reversed, and those behind reversed, leave the answer |
| P3 | one more person at the back wanting `t` adds the least of `t` and one fewer than `k` wants |
| P4 | `k` wanting one more ticket never lowers the answer and adds at most the line's length |
| P5 | the answer is at least what `k` wants plus the people ahead, and at most all the tickets |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 lines: checksum 452371383, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
lines. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run`, and the kept ones under `karac
__mir-run` too. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the places counted from the second person | P1 213, P2 87, P3 80, P5 70, P6 213 |
| M2 | ★: `k` wanting at least two | P1 117, P3 152, P6 117 |
| M3 | ★: each person behind one ticket short | P1 81, P3 63, P6 81 |
| M4 | queue: the last second counted twice | P1 340, P5 94, P6 340 |
| M5 | queue: the line built backwards | P1 257, P3 277, P5 54, P6 257 |
| M6 | queue: a person wanting two leaving after one | P1 188, P3 180, P5 76, P6 188 |
| M7 | rounds: a person with none left still taking a second | P1 124, P3 35, P5 66, P6 124 |
| M8 | rounds: `k` done a ticket early | P1 188, P3 153, P5 75, P6 188 |
| M9 | rounds: the first person's seconds not counted | P1 340, P2 55, P5 186, P6 340 |
| M10 | fold: `k` split into the back half | P1 340, P5 171, P6 340 |
| M11 | fold: everyone a round more | P1 246, P3 277, P6 246 |
| M12 | fold: the back half capped by the front | P1 44, P3 62, P6 44 |
| M13 | struct: a person with none left served once | P1 70, P2 18, P3 28, P5 39, P6 70 |
| M14 | struct: the front person kept at the front | P1 167, P3 188, P6 167 |
| M15 | struct: the line starting at the second person | P1 226, P2 36, P3 86, P5 101, P6 226 |
| M16 | solution: the adapter asking about the next place | P1 242, P2 96, P3 191, P5 9, P6 242 |
| M17 | solution: the adapter's line backwards | P1 156, P2 136, P3 235, P5 29, P6 156 |

P1 and P6 kill all seventeen, P3 fourteen, P5 twelve, P2 six and P4 none.
`P1 340` is an arm wrong on every line: a second counted twice (M4), the
first person's seconds lost (M9), or `k` treated as one of those behind
it (M10), which P5's lower bound sees as too few seconds. P3 sees an
edit that gets wrong how much a newcomer at the back buys, and that is
most of them, since the person behind `k` is where the count turns.
P2, which reverses each side of `k`, sees an edit that ties a person's
part to their place and not only to which side of `k` they stand (M1,
M9, M13, M15, M16, M17). P4 kills nothing: every edit here still has
`k`'s extra ticket cost at most one more round, and no edit lowered the
answer for it.

Of the thirty-one, fourteen were not kept, and none survives. Seven fail
as a kept one: the ★ and Rust arms' `k` counted as one behind as M10;
the queue arm's buyer going back to the front as M14; the rounds arm's
round walked from the back as M5; the fold arm's front person left out
as M9; the struct arm's `k` done with one left as M8; the Rust arm's
each person behind one short as M3. Four fail in two pairs and none of
them is kept: the ★ and fold arms' people behind buying as many rounds
as `k` (P1 219, P3 277), and the ★ and Rust arms' everyone short a
round (P1 340, P3 305, P5 227). Three are killed with checks of their
own but were left out because their arm keeps three, or two: the queue
arm's last ticket taking no time (P1 340, P3 63, P5 194), the rounds
arm's no one wanting more than five (P1 55, P3 35, P5 8), and the Rust
arm's most taken in place of the sum (P1 272, P3 188, P5 241).

## Verification

Every arm prints the same output as `tickets.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them.

Under `karac __mir-run` the arms take 0.4 s to 0.8 s, except the rounds
and struct arms at 1.1 s and 1.6 s and the queue arm at 2.8 s, which
sell every ticket one at a time, and the differential 0.5 s (timed while
other work shared the machine).

No arm met a compiler gap. The Rust arm was written as LeetCode's Rust
template. `karac fix` carries it in two rounds of 8 and 1 edits: Rust's
spellings (`Vec<..>` to brackets, the `&` of `|(i, &t)|` and `|&t|`
dropped, `struct Solution;` to `struct Solution {}`, `Solution::` to
`Solution.`); then `k as usize` to `k as i64`, Kāra's type for places.
The fixed arm reads as the template does, `i32`s and all.

## Benchmarks

The bench answers every place in 20000 lines of 100 people wanting 1 to
100 tickets with the ★ arm in all five languages, 2000000 answers, the
lines built first. Every implementation prints `2000000 answers: sum
6741030742, checksum 83502949`.

BENCHTAB
