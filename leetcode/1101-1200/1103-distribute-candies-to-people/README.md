# 1103. Distribute Candies to People

We distribute some number of `candies` to a row of `n = num_people`
people in the following way: we give 1 candy to the first person, 2
candies to the second person, and so on until we give `n` candies to
the last person. Then we go back to the start of the row, giving `n +
1` candies to the first person, `n + 2` to the second, and so on until
we give `2 * n` candies to the last person.

This repeats, one more candy each time and back to the start of the
row after its end, until we run out of candies. The last person
receives all of the remaining candies, not necessarily one more than
the previous gift.

Return an array of length `num_people` and sum `candies` that
represents the final distribution of candies.

```
candies = 7,  num_people = 4  ->  [1,2,3,1]
candies = 10, num_people = 3  ->  [5,2,3]
```

**Constraints:** `1 <= candies <= 10^9`; `1 <= num_people <= 1000`.

The arms are `fn distribute_candies(candies: i64, num_people: i64) ->
Vec[i64]`. Gift `g` goes to person `(g - 1) mod n`, and 10^9 candies
make 44,721 whole gifts and a short one, so handing them out one gift
at a time is fast enough.

## Approaches

| file | mechanism |
|---|---|
| `distribute_candies.kara` ★ | the handing out as the statement tells it: gifts of 1, 2, 3, ... to each person in turn, round and round, the last whatever is left. O(sqrt candies) |
| `distribute_candies_formula.kara` | in closed form: the number of whole gifts `k` from a square root, corrected by a step either way; person `i`'s gifts `i + 1`, `i + 1 + n`, ... up to `k` an arithmetic series, and the rest to the person after gift `k`. O(n) |
| `distribute_candies_rounds.kara` | a whole round at a time: round `j` gives person `i` exactly `jn + i + 1`, `n^2 j + n(n + 1)/2` in all, added with `iter_mut().enumerate()` while the candies cover a round, then the last round gift by gift |
| `distribute_candies_search.kara` | the number of whole gifts `k` by binary search, the largest with `k(k + 1)/2` at most the candies; then `k / n` whole rounds for everyone and one more gift for the first `k % n`, built by `map` and `collect`, and the rest to the next |
| `distribute_candies_scan.kara` | iterator chains: the gifts as a `scan` over `1..` carrying the candies left, which ends with `return None` when they run out, then `enumerate` and `fold` into the people by place |
| `distribute_candies_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `mut candies: i32`, `vec![0; n]`, `ans[i % n]` over a `usize`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 16 lines: the answers for LeetCode's two
examples and nine more (one candy to one person and to five, 6 and 7
candies to three, 21 and 22 to six, 100 to one, 55 and 60 to ten),
then over 2000 random problems of up to 10^6 candies among 1 to 1000
people a checksum of the answers (`checksum 444405626`), and 10^9
candies, LeetCode's most, among 1, 2, 999 and 1000 people.
`distribute_candies.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the candies handed out one at a time, each to the person
whose turn it is, a turn ending when that person has had one more than
the turn before or the candies run out. It checks 2000 problems in four
kinds of 500: up to 200 candies among 1 to 10 people; up to 5000 among
1 to 100; the candies of exactly `k` whole gifts, one more or one
fewer, among 1 to 20; and up to 100 candies among at least as many
people as gifts. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | `n` counts, none negative, summing to the candies, and by a second reading each the person's own gifts `i + 1`, `i + 1 + n`, ... peeled off in turn, with something left over at one person at most |
| P3 | one candy more is one more for exactly one person |
| P4 | two to four times as many people, folded back onto `n` by place, give the same answer |
| P5 | as many people as there are gifts, and one to five more, differ only by the people with none |
| P6 | from the candies of `k` whole gifts to those of `k + n`, person `(k + j) mod n` gains gift `k + j + 1` and nothing else |

All 72,000 checks pass on every arm: `2000 problems: checksum
72537642, 72000 checks over 6 arms: 0 failures`. A Python reading of
the same problems, one candy at a time, gives the same checksum.

P1 hands out the answer and P2 judges it by another reading; P3 to P6
compare the arm only with itself.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`, each failing the same way
under both. All thirty are caught. Fifteen are kept, no two failing the
same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last gift given whole | P1 1699, P2 1699, P3 2000 |
| M2 | ★: the last candy kept | P1 294, P2 294, P3 565, P6 15 |
| M3 | ★: a person's count replaced by the gift | P1 1222, P2 1222, P3 185, P4 1222, P6 2000 |
| M4 | formula: the rest one person late | P1 1626, P3 250, P5 1699 |
| M5 | formula: the person with the last whole gift skipped | P1 803, P2 803, P3 107, P4 604, P6 778 |
| M6 | formula: the series one term long | P1 2000, P2 2000, P3 261, P4 2000, P5 2000, P6 2000 |
| M7 | rounds: the last round started at the wrong gift | stops: index out of bounds |
| M8 | rounds: the rounds never growing | P1 1130, P2 1111, P4 1130, P6 1913 |
| M9 | rounds: the last person left out of the last round | P1 287, P2 287, P3 335, P4 210, P5 1699 |
| M10 | search: the series one term long | P1 1231, P2 1231, P3 39, P4 1231, P5 286, P6 1958 |
| M11 | search: at most 50 whole gifts | P1 459, P6 655 |
| M12 | scan: the gifts from two | P1 1898, P2 1877, P6 1915 |
| M13 | scan: one candy short | P1 2000, P2 2000 |
| M14 | solution: each gift one smaller | P1 1909, P2 1894, P5 2000, P6 1915 |
| M15 | solution: every other person skipped | P1 1900, P2 634, P5 1977, P6 1915 |

Of the fourteen that run to the end, P1 catches all fourteen, P2
twelve, P6 ten, P3 eight, and P4 and P5 six each. P2 misses the two
edits whose counts still sum to the candies and leave something over
at one person only, which is all the peeling asks: M4 gives the rest to
the person after the right one, and M11, unable to count past 50 whole
gifts, gives everything over 1275 candies to one person as the rest.
M11 shows only above 1275 candies, in
the 500 problems of up to 5000 and in P6's next round. P3 to P6, which
compare the arm only with itself, catch all but M13: an arm one candy
short is one candy short at every count, so one candy more still moves
exactly one person by one. M7 starts the last round at the wrong gift,
takes more small gifts than there are people, and indexes past the
end.

One edit first written changed nothing: with the closed form's square
root never corrected up, the `f64` square root of `8c + 1` already
gives the number of whole gifts for every count of candies here, so the
correction never runs. It was replaced by the closed form's whole gifts
each one short.

Of the fifteen not kept, eight fail as a kept edit: the ★ arm's gifts
one person late and the scan and solution arms' alike fail as M14, the
★ arm's gifts growing by two as M15, the scan arm's last gift whole as
M1, the scan and solution arms keeping the last candy as M2, and the
solution arm one person short stops as M7 does. The other seven fail in
ways of their own but were not needed: the closed form's whole gifts
one short and one gift fewer for everyone, the rounds arm's gifts of a
whole round one short and a round's cost counted without its rounds,
and the search arm's extra gift for the person after the last whole
one, its extra gift one short and its rest replacing the count.

## Verification

Every arm prints the same output as `distribute_candies.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, filed in the kara ledger and fixed. The ★ arm
was written as Kāra, and the other five as Rust writes them; `karac fix`
carried every Rust spelling to a clean check, in two to four rounds
each: `Vec<i64>` to `Vec[i64]`, `vec![0i64; n as usize]` to
`Vec.filled(n, 0)`, every `as usize` index cast and `i as i64` dropped,
`let (mut lo, mut hi) = (0i64, 50000i64)` to `let mut (lo, hi) = (0,
50000)`, and in the Rust solution `struct Solution {}` declared and
`mut candies: i32` to `candies: own i32` with a `let mut candies =
candies;`. One leftover reads oddly but is what `karac fix` leaves: the
closed form's `people[(k % n)]`, once `people[(k % n) as usize]`.

The scan arm is Rust's `scan`, which lends its state to be written in
place: `(1..).scan(candies, |left, gift| { if *left <= 0 { return None;
} let given = gift.min(*left); *left -= given; Some(given) })`. Kāra's
`scan` takes the state by value and returns `Some((next_state, item))`,
and since kata 2012 `karac fix` rewrites such a closure to that shape,
but any `return` in the body withheld the rewrite and left advice
alone. `return None` ends the iteration and carries no state, so it now
stays as written and the rest is rewritten, `let left = left - given;
Some((left, given))`, the body kept at its indentation
(B-2026-11-10-32, fixed). The arm is the `karac fix` output verbatim.

## Benchmarks

The bench draws 64 problems once, up to 10^9 candies among 1 to 1000
people, LeetCode's most. Each of 200 rounds moves every problem's
candies and hands them out with the ★ arm: 12,800 calls of up to
44,721 gifts each. Every implementation prints `200 rounds over 64
problems of up to 10^9 candies: first and last people hold
467465801720, checksum 526113656`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `33ef2a7ad2`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.833 to 0.863 s | 0.846 s |
| C (`clang -O3`) | 0.833 to 0.867 s | 0.852 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.839 to 0.908 s | 0.856 s |
| Kāra (`karac build`) | 0.843 to 0.921 s | 0.857 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.831 to 0.916 s | 0.866 s |
| Rust (`rustc -O`) | 0.835 to 0.903 s | 0.866 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.842 to 1.016 s | 0.873 s |
| Go | 1.399 to 1.455 s | 1.417 s |
| Python | 51.2 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra, C and Rust tie; Go takes about 1.7x their time. Python
takes about 59x Kāra's time.
