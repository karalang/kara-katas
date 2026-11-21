# 2413. Smallest Even Multiple

Given a **positive** integer `n`, return *the smallest positive integer
that is a multiple of **both*** `2` *and* `n`.

```
n = 5   ->  10
n = 6   ->  6
```

**Constraints:** `1 <= n <= 150`.

The least common multiple of 2 and `n` is `n` itself when `n` is even,
and `2 n` when it is odd.

## Approaches

| file | mechanism |
|---|---|
| `even.kara` ★ | parity: `n` when `n % 2 == 0`, and `2 * n` otherwise. O(1) |
| `even_gcd.kara` | the least common multiple by Euclid: `2 n / gcd(2, n)`, the gcd by recursive remainders. O(log n) |
| `even_count.kara` | counting up the multiples of `n` until one is even, at most two steps. O(1) |
| `even_shift.kara` | a shift: `n << (n & 1)`, by 1 exactly when `n` is odd. O(1) |
| `even_iter.kara` | iterators: the even numbers from 2 by `step_by(2)`, the first that `n` divides by `find`. O(n) |
| `even_solution.kara` | LeetCode's Rust template: `if n % 2 == 0 { n } else { n * 2 }` over `i32`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 4 lines: LeetCode's two examples; 1, 2, 149
and 150; the answers for 1 to 20; then a checksum and the total of the
answers for every `n` from 1 to 150. `even.py` mirrors the ★ arm and its
output is byte-identical; the differential's literal reading checks the
same answers for every `n` the constraints allow.

`check` first reports 1 error on the template, `struct Solution;`, and
`karac fix` carries it in one call, reporting 2 edits: `struct
Solution;` given its braces, and the wrapper's widening `as i64`
removed. The one-line `if` stands as Kāra, and `karac fmt` spreads it
over five lines.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: 1, 2, 3 and so on tried in turn, and the first that both 2
and `n` divide. No parity test and no gcd. It checks every `n` from 1 to
150, then 50 random `n` up to `10^5`, beyond the constraints, where the
arms' arithmetic is the same.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | 2 and `n` both divide the answer, and it is `n` or `2 n` |
| P3 | `2 n`: the answer `2 n`, which is `n`'s answer when `n` is odd |
| P4 | `3 n`: three times `n`'s answer |
| P5 | `n + 1`: of the answers' quotients by `n` and by `n + 1`, one is 1 and one is 2 |
| P6 | each arm agrees with at least three of the other five |

P3 holds because `2 n` is even, P4 because `3 n` has `n`'s parity, and
P5 because exactly one of `n` and `n + 1` is even.

The differential prints `200 cases: checksum 141979800, 7200 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that builds
the same cases and counts up the same way. On a failure it prints the
first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M4 | ★: only multiples of 4 kept | P1 49, P3 103, P5 100, P6 49 |
| M5 | ★: an even n doubled too | P1 97, P3 200, P5 200, P6 97 |
| M6 | ★: 1 kept as it is | P1 1, P2 1, P3 1, P4 1, P5 1, P6 1 |
| M8 | gcd: a quotient for the remainder | P1 199, P2 199, P3 200, P4 200, P5 200, P6 199 |
| M10 | gcd: the gcd with 4 | P1 48, P2 48, P3 97, P5 100, P6 48 |
| M11 | gcd: multiplied by the gcd | P1 200, P2 103, P3 200, P6 200 |
| M13 | count: a step of 1 | P1 102, P2 102, P3 102, P4 103, P5 199, P6 102 |
| M15 | count: the multiple before returned | P1 200, P2 200, P3 200, P5 200, P6 200 |
| M16 | count: the search stopping at 50 | P1 78, P2 78, P3 78, P4 17, P5 151, P6 78 |
| M17 | shift: shifted by the second bit | P1 152, P2 152, P3 103, P4 103, P5 200, P6 152 |
| M20 | shift: an odd n halved | P1 103, P2 103, P3 103, P4 103, P5 200, P6 103 |
| M21 | shift: the lowest bit set after | P1 200, P2 200, P3 200, P4 200, P5 200, P6 200 |
| M22 | iter: a multiple of 3 accepted | P1 195, P2 195, P3 197, P4 198, P5 197, P6 195 |
| M24 | iter: every number tried | P1 102, P2 102, P3 102, P4 1, P5 199, P6 102 |
| M26 | iter: the evens from 4 | P1 2, P2 1, P3 1, P4 2, P5 2, P6 2 |
| M29 | solution: the second bit tested | P1 100, P2 51, P3 103, P4 103, P5 97, P6 100 |
| M31 | solution: an odd n quadrupled | P1 103, P2 103, P3 103, P5 200, P6 103 |

P1, P3 and P6 kill all seventeen, P5 sixteen, P2 fifteen, and P4
eleven. P2 misses the two that answer `2 n` for an even `n` too, only
multiples of 4 kept (M4) and an even `n` doubled (M5), since `2 n` is
still divisible by 2 and by `n`; P5 misses the gcd arm's multiplied by
the gcd (M11). P4 misses six whose wrong answer is a fixed multiple of
`n` chosen by `n`'s parity or by whether 4 divides it, which `3 n`
shares with `n`, so the wrong answers still scale by three.

Of the thirty-one, fourteen were not kept, each failing the same checks
as a kept one or, for three, left over: the parity test or shift
inverted (M1, M19, M27) as multiplied by the gcd (M11); an odd `n`
returned as it is, tripled, or a remainder of 1 ending the search (M2,
M3, M9) as the template's odd `n` quadrupled (M31); the product never
doubled (M7) as the multiple before returned (M15); the count starting
at `2 n`, the last even multiple taken and a multiple of `2 n` sought
(M12, M23, M25) as an even `n` doubled too (M5); and the template's odd
`n` given 2 more (M28) as an odd `n` halved (M20). The count arm's
multiple of 4 sought (M14), the shift arm's shifted one further (M18)
and the template's even `n` halved (M30) fail apart from every kept
one, and were left out because those arms keep their share already.

## Verification

Every arm prints the same output as `even.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.16 to 0.21 s. The differential
takes 18 s there, most of it the literal reading counting up to `2 *
10^5`, 5.8 s under `karac __mir-llvm-asan` and 0.4 s under `karac run`.

## Benchmarks

The bench makes 200000 passes over every `n` from 1 to 150, folding each
answer plus the pass into the checksum, with the ★ arm in all five
languages. Every implementation prints `200000 passes over n from 1 to
150: checksum 843606458`. The answer is one test and at most one
doubling; the checksum's multiply and remainder dominate the time in
every language.

BENCHTAB
