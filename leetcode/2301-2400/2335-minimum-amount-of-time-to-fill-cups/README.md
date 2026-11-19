# 2335. Minimum Amount of Time to Fill Cups

You have a water dispenser that can dispense cold, warm, and hot water.
Every second, you can either fill up `2` cups with **different** types
of water, or `1` cup of any type of water.

You are given a **0-indexed** integer array `amount` of length `3`
where `amount[0]`, `amount[1]`, and `amount[2]` denote the number of
cold, warm, and hot water cups you need to fill respectively. Return
*the **minimum** number of seconds needed to fill up all the cups*.

```
amount = [1,4,2]   ->  4
amount = [5,4,4]   ->  7
amount = [5,0,0]   ->  5
```

**Constraints:** `amount.length == 3`; `0 <= amount[i] <= 100`.

A second fills at most two cups and at most one of a kind, so filling
them takes at least half of all the cups, rounded up, and at least the
most cups of one kind. The larger of the two is always enough: each
second, fill a cup of each of the two kinds with the most left. If one
kind outnumbers the other two together, it is filled one a second with
a cup of another beside it while they last; otherwise the two largest
stay within one of each other and every second but perhaps the last
fills two.

## Approaches

| file | mechanism |
|---|---|
| `cups.kara` ★ | the larger of the most cups of one kind and half of all the cups, rounded up. O(1) |
| `cups_greedy.kara` | second by second: the counts sorted, and a cup filled of each of the two kinds with the most left, or of the one kind left |
| `cups_heap.kara` | a `PriorityQueue.max_first()` of the kinds still wanting cups: each second pops the two with the most, fills one cup of each, and pushes back those not done |
| `cups_search.kara` | a binary search on the time: `t` seconds suffice when no kind wants more than `t` cups and all of them fit two to a second, found by halving between 0 and all the cups |
| `cups_iter.kara` | iterators: the seconds counted up from 0, and the first that `find` sees with every kind within it by `all` and the `sum` of the cups within twice it |
| `cups_solution.kara` | LeetCode's Rust template: a `mut` parameter sorted with `sort_unstable`, the three counts destructured from a tuple, and the most plentiful kind against the other two; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples; no cups;
100 of each; 100 of one kind; one kind just short of the other two
together; then 2000 random cases of 0 to 100 cups of each kind, a kind
left empty one time in 5, with a checksum and the seconds in all.
`cups.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 13 edits.
`check` first reports seven errors and offers 11 edits for them: the
parameter written `mut amount`, which the method sorts, to
`amount: own Vec[i32]` with a `let mut amount = amount;` in the body,
two edits, since a bare parameter borrows and cannot be sorted in
place; the six brackets of the three `Vec<..>`; `struct Solution;` to
`struct Solution {}`; the `&` of `|&x|` dropped; and `Solution::` to
`Solution.` in the harness's wrapper. The other two follow from those:
`sort_unstable` to `sort`, and the wrapper's `as i64` on the `i32`
answer dropped, since it widens on its own.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: from the cups still wanted, every second may fill two cups
of different kinds or one cup of any kind, every such choice is tried,
and the fewest seconds to fill them all kept, memoized in a
`Map[Vec[i64], i64]` by the cups left. No formula and no greed. It
checks 300 random cases of 0 to 8 cups of each kind; then 30 with one
kind of up to 100 cups and the others up to 10; then 30 of up to 100
of each; every hundredth case has no cups at all. All 360 are drawn
before any arm answers.

| | property |
|---|---|
| P1 | up to 8 cups of each kind, the answer is the literal reading's |
| P2 | the answer is at least the most cups of one kind and half of all the cups, and at most all the cups |
| P3 | the kinds in any of the six orders: the same answer |
| P4 | one cup more of any one kind: no fewer seconds, and at most one more |
| P5 | every kind with as many cups as the most of them: half of all those cups, rounded up |
| P6 | each arm agrees with at least three of the other five |

P4 holds because the extra cup can always be filled in a second of its
own. P5 is the answer for three equal kinds, where no kind outnumbers
the other two.

The differential prints `360 cases: checksum 509146664, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and tries every choice under `lru_cache`. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the most of the first two kinds alone | P1 30, P2 45, P3 147, P6 45 |
| M2 | ★: half of all the cups rounded down | P1 60, P2 65, P5 140, P6 65 |
| M6 | ★: half of all the cups and one more | P1 78, P2 4, P5 220, P6 88 |
| M7 | greedy: one cup a second | P1 282, P5 356, P6 341 |
| M8 | greedy: the most plentiful kind paired with the least | P1 282, P5 352, P6 341 |
| M9 | greedy: stopped once the second kind runs out | P1 222, P2 272, P5 140, P6 272 |
| M12 | heap: the kind with the fewest taken first | P1 207, P5 352, P6 257 |
| M13 | heap: the second kind never put back | P1 100, P2 111, P5 346, P6 111 |
| M14 | heap: a kind put back with no cups left | P1 297, P2 15, P4 4, P5 356, P6 356 |
| M17 | search: a kind with exactly `t` cups refused | P1 182, P6 230 |
| M19 | search: the search started at 1 | P1 3, P2 4, P5 4, P6 4 |
| M21 | search: a time that suffices stepped past | P1 106, P2 128, P4 246, P5 216, P6 128 |
| M22 | iter: all the cups held to three a second | P1 100, P2 111, P5 356, P6 111 |
| M23 | iter: each kind allowed one cup over the time | P1 104, P2 147, P6 147 |
| M25 | iter: all the cups held to one a second and one | P1 264, P5 352, P6 323 |
| M28 | solution: the counts never sorted | P1 74, P2 102, P3 147, P6 102 |
| M30 | solution: a dominant kind answered with all the cups | P1 182, P4 66, P6 230 |

P1 and P6 kill all seventeen, P5 twelve, P2 eleven, P4 three and P3
two. P5, three equal kinds, fails where an edit miscounts when no kind
outnumbers the others, and misses those that only go wrong when the
kinds differ: the kinds read by place, a kind refused at exactly the
time or allowed one cup over, and a dominant kind answered with all the
cups. P2's bounds miss the edits that answer too many seconds but no
more than all the cups: one cup a second and the other ways of pairing
the kinds badly, a kind refused at exactly the time, and the dominant
kind's answer. P4, one cup more, fails only where an edit's answer jumps by two or
falls as a cup is added: a kind put back with no cups left, a time
that suffices stepped past, and the dominant kind answered with all
the cups. P3, the kinds reordered, fails only where an edit reads the
kinds by place: the most of the first two alone, and the counts never
sorted. The search started at 1 fails only on the cases with no cups
at all, which every hundredth case is for.

Of the thirty-one, fourteen were not kept. The ★ arm's most of one
kind alone (M3) and all the cups without the third kind (M5), the
greedy arm's counts sorted only once (M10) and the search capped at the
most of one kind (M20) fail as the iter arm's all the cups held to
three a second (M22). One cup a second in the greedy (M7), heap (M16)
and search (M18) arms, the greedy arm's second counted twice for two
cups (M11) and the iter arm's most time that suffices (M26) fail alike,
and only M7 is kept. The ★ arm's half of all the cups alone (M4), the
iter arm's any kind within the time (M24) and the template's least kind
against the other two (M27) and middle kind taken as the most (M31)
fail as the iter arm's each kind allowed one cup over (M23), and the
template's half rounded down (M29) as the ★ arm's (M2). The heap arm's
empty kind put in at the start (M15) fails apart from every kept one,
and was left out to keep three to an arm.

M22 and M23 replace the cups summed without the last kind and each
kind held to half the time, which left the iter arm's range of times
with none that fits, and crashed on its `unwrap`.

## Verification

Every arm prints the same output as `cups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes 0.2 to 0.6 s but the heap arm,
which pushes and pops for every second, 1.7 s. The differential takes
1.5 s there and 0.4 s under `karac __mir-llvm-run`.

## Benchmarks

The bench makes 3 passes over every amount from 0 to 100 cups of each
kind, one `Vec` of three refilled in place for each call, pass `p`
folding each answer plus `p` into the checksum, with the ★ arm in all
five languages. Every implementation prints `3 passes over 101^3
amounts: checksum 30006752`. The work is the call itself and the
checksum's multiply and remainder; nothing is allocated in the loop.

BENCHTAB
