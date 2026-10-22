# 860. Lemonade Change

At a lemonade stand, each lemonade costs `$5`. Customers stand in a
queue and buy one at a time, in the order given by `bills`. Each
customer buys one lemonade and pays with a `$5`, `$10` or `$20` bill,
and must get the correct change back, so that the net transaction is
that the customer pays `$5`. The stand has no change at first. Return
`true` if every customer can be given the correct change, and `false`
otherwise.

```
bills = [5, 5, 5, 10, 20]  ->  true
bills = [5, 5, 10, 10, 20] ->  false
```

**Constraints:** `1 <= bills.length <= 10^5`; `bills[i]` is `5`, `10`
or `20`.

## Approaches

| file | mechanism |
|---|---|
| `lemonade_change.kara` ★ | a twenty is never given as change, so only the counts of fives and tens matter. A 10 takes a five; a 20 takes a ten and a five when there are both, or else three fives. The ten goes first because a ten can only ever pay part of a 20, while a five also pays for a 10, so keeping the fives never leaves fewer choices later. One pass, O(n) time, O(1) space |
| `lemonade_change_states.kara` | no choice made: every till (fives, tens) that some sequence of choices can reach is kept in a `Set`, each bill mapping the set to the next one. The queue is served if a till is left at the end. O(n^2) |
| `lemonade_change_cashier.kara` | a drawer, a `SortedMap` from denomination to the number of bills held. Each bill goes in, then the change is counted out from the largest denomination down, as many of each as fit. O(n) |
| `lemonade_change_brute.kara` | both ways of paying each twenty, by recursion over the queue with the till. O(2^t) for t twenties |
| `lemonade_change_all.kara` | the ★ rule as one `bills.iter().all(...)`: the closure updates the counts it captures and a `match` on the bill says whether that customer is served |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 16 lines: LeetCode's two examples; twelve
more (a first bill that is not a five, a 20 paid each of the two ways,
a 20 that must take the ten, a 20 with too little change left); the
number of queues served among all 3,279 queues of one to seven bills,
which is 162; and 2,000 random queues of up to 40 bills (a 5 half the
time, a 10 three times in ten, a 20 one time in five), with the number
served and a checksum. `lemonade_change.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the till keeps every bill taken, twenties included, and each
customer's change, the bill less 5, may be made from any of the bills
held, every way of making it tried in turn. Its 2,500 queues are all
1,092 queues of one to six bills and 1,408 random queues of up to 14
bills (a 5 six times in ten, a 10 three, a 20 one); 647 of them are
served.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | a 5 handed over first never turns a served queue away |
| P3 | every prefix of a served queue is served |
| P4 | a queue that does not start with a 5 is turned away |
| P5 | a 5 moved one place earlier never turns a served queue away |
| P6 | a 5 handed over last changes nothing |

It prints `2500 queues, 647 served, 56540 checks over 5 arms: 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a 20 paid with three fives before a ten | P1 12, P2 16, P3 39, P5 29, P6 12 |
| M2 | ★: a 10 taken with no five to give | P1 290, P4 215, P6 290 |
| M3 | ★: a 20 paid with a ten alone | P1 56, P6 56 |
| M4 | states: three fives never tried | P1 50, P2 50, P3 149, P5 61, P6 50 |
| M5 | states: a 10 keeps the five | P1 217, P6 217 |
| M6 | states: a queue with no till left not refused | P1 1853, P4 1261, P6 1853 |
| M7 | cashier: change counted out smallest first | P1 52, P2 54, P3 149, P5 117, P6 52 |
| M8 | cashier: the bill paid not put in the drawer | P1 488, P2 488, P3 2142, P5 718, P6 488 |
| M9 | cashier: at most one bill of each denomination | P1 50, P2 50, P3 149, P5 61, P6 50 |
| M10 | brute: a 20 only paid with three fives | P1 88, P2 58, P3 221, P5 163, P6 88 |
| M11 | brute: a 20 needs both ways to work | P1 132, P2 104, P3 366, P5 215, P6 132 |
| M12 | brute: a 10 needs no five | P1 467, P4 343, P6 467 |
| M13 | all: a 10 with no five accepted | P1 500, P4 357, P6 500 |
| M14 | all: a 5 not counted | P1 488, P2 488, P3 2142, P5 718, P6 488 |
| M15 | all: three fives taken when there are two | P1 33, P6 33 |

P1 and P6 kill all fifteen. M4 and M9 are the same fault, a 20 never
paid with three fives, and fail the same cases; so are M8 and M14, which
never count a five. M1 is the one that tests the greedy rule itself:
paying with three fives first is right on most queues, and fails only
on 12 of the 2,500.

## Verification

Every arm prints the same output as `lemonade_change.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and under
`karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `cacd39ad9b`. Under `karac
__mir-run` the arms take under a second and the differential 0.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends run the ★, cashier, brute-force and `all`
arms through `karac run --legacy --interp`, `karac run --legacy`,
`karac build` and a `KARAC_AUTO_PAR=1` build with the same output. They
refuse the states arm, the differential and the bench program at a `*`
on a `for` element (`*t` over the tills in a `Set`, `*b` over the
bills), saying the element is copied, where v2 yields a reference to
each element. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm, in all five languages: a queue of
100,000 bills, LeetCode's longest, built once so that every customer is
served, and 1,000 rounds that each change one bill (a 5 to a 10, a 10 to
a 20, a 20 to a 5), ask whether the queue is still served, and change it
back. A queue stops at its first customer without change, so a round
reads up to that customer or to the end. Every implementation prints
`1000 rounds on 100000 bills: 798 served, checksum 540467465`, the Kāra
program under `karac __mir-run` included, in 36 s.

Spot timings on a shared 4-core container, eight interleaved runs of
each compiled program and one of Python (`bench.sh` timings need a quiet
machine):

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.51 to 0.61 s | 0.54 s |
| Rust (`rustc -O`) | 0.45 to 0.57 s | 0.49 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.43 to 0.52 s | 0.47 s |
| Go | 0.54 to 0.73 s | 0.57 s |
| Python | 5.1 s | |
| Kāra (`karac build --mir`) | 0.57 to 0.68 s | 0.60 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 859's does.

v2 takes 1.28 times Rust's median time under overflow checks, 1.12 times
C's and 1.06 times Go's. The loop is bound by branch mispredictions: the
bill at each step is random. Under valgrind's cachegrind C runs 1.14
billion instructions and 263 million branches with 49.5 million
mispredicted, Rust with overflow checks 0.96 billion and 354 million with
49.5 million mispredicted, and v2 1.10 billion and 337 million with 60
million mispredicted. v2's extra fifth of mispredictions is most likely
the shape of its branch chain, which tests the bill in an order the
predictor does worse on (not traced). The comparison with C and Rust
waits until after M4.
