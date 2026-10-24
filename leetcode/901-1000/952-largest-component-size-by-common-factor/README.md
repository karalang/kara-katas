# 952. Largest Component Size by Common Factor

You are given an integer array of unique positive integers `nums`.
Consider the following graph: there are `nums.length` nodes, labeled
`nums[0]` to `nums[nums.length - 1]`, and there is an undirected edge
between `nums[i]` and `nums[j]` if `nums[i]` and `nums[j]` share a common
factor greater than 1. Return *the size of the largest connected
component in the graph.*

```
nums = [4,6,15,35]               ->  4
nums = [20,50,9,63]              ->  2
nums = [2,3,6,7,4,12,21,39]      ->  8
```

**Constraints:** `1 <= nums.length <= 2 * 10^4`; `1 <= nums[i] <= 10^5`;
all the values of `nums` are unique.

## Approaches

| file | mechanism |
|---|---|
| `largest_component_size.kara` ★ | union by prime: two numbers share a factor above 1 exactly when they share a prime. Each number is factored by trial division and joined to the first number seen with each of its primes, in a disjoint-set forest over the numbers' places, union by size; a `Map` holds each prime's first place. The largest set is the answer. O(n sqrt(m)) for numbers up to m |
| `largest_component_size_sieve.kara` | the same union by prime, with each number factored by a table of smallest prime factors, built once by a sieve up to the largest number; each prime's first place is kept in an array the sieve's size. O(m log log m + n log m) |
| `largest_component_size_values.kara` | a disjoint-set forest over the values 0 to the largest number, not the places: each number is joined to every factor f above 1 it has, found in pairs f and number / f up to its square root. Two numbers sharing a factor are joined through it; the largest set counts only the numbers in it. O(n sqrt(m)) |
| `largest_component_size_bfs.kara` | the graph walked as given, with the primes standing in for the edges: each number lists its primes, each prime the numbers it divides, and a breadth-first search from each number not yet reached crosses from numbers to primes and back, every prime expanded once. O(n sqrt(m)) to factor, then linear in the lists |
| `largest_component_size_multiples.kara` | no number is factored: the numbers are marked in an array up to the largest, and for each prime p, found by a sieve on the way, the marked multiples of p are all joined to the first of them. O(m log log m) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and five
more (one number, 1 with primes only, three numbers each sharing a prime
with the other two, four where only 77 and 35 share one, and two primes
near the top with 2); for 300 random cases of 1 to 12 numbers up to 60,
1,924 numbers in all, the largest components' total and a checksum; and
four cases of LeetCode's largest size: 20,000 random numbers up to
100,000 (one component of 18,596), the odd numbers 1 to 39,999 (17,379),
the 9,592 primes below 100,000 (1), and the even numbers 2 to 40,000
(20,000). `largest_component_size.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: an edge between two numbers when some factor from 2 up to the
smaller of them divides both, tried one by one, and the largest set of
nodes reached from one node along the edges by a depth-first search. It
checks 3,200 random cases, 3,000 of 1 to 12 numbers up to 100 against
the statement and 200 of up to 400 numbers up to 2,500 against the other
properties, 59,999 numbers in all. Every number the properties make is
at most twice the largest a case can have, so the arms that size an
array by the largest number stay quick.

| | property |
|---|---|
| P1 | the statement's answer, on the small cases |
| P2 | the numbers in another order give the same answer |
| P3 | one prime renamed, in every number, to a prime no number has (the largest prime used goes to the smallest unused prime, or to the first unused prime above it) gives the same graph and the same answer |
| P4 | followed by a second case of one to eight numbers made only of primes the first case lacks, sometimes with 1 when it lacks 1, the answer is the larger of the two cases' answers |
| P5 | each number times its smallest prime, where the product is new and stays in range, has the same primes, and gives the same answer |
| P6 | each arm agrees with at least two of the other four |

P3 cannot rename anything in 12 cases (such as `[1]`) and P5 changes no
number in 123; those checks pass as they stand.

It prints `3200 cases of 59999 numbers: largest components adding to
50348, checksum 274146429, 95000 checks over 5 arms: 0 failures` under
`karac __mir-run` (38 s) and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Forty-eight edits to the differential, each run under
`karac __mir-llvm-run`; fifteen are kept, three to each arm, and all
fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a square taken as its own prime (the trial bound `p * p >= x`) | P1 593, P5 881, P6 700 |
| M2 | ★: one power of each prime divided out | P1 374, P3 2, P5 1021, P6 465 |
| M3 | ★: the larger set never grown | P1 2473, P6 2672 |
| M4 | sieve: a first place of 0 taken as none | P1 1836, P2 1001, P4 5, P6 2010 |
| M5 | sieve: the place joined, not its set | P1 882, P2 1098, P6 1074 |
| M6 | sieve: counted under the parent, not the root | P1 833, P2 1163, P6 1018 |
| M7 | values: no factor at the square root | P1 243, P5 536, P6 340 |
| M8 | values: never joined to the cofactor | P1 768, P3 28, P5 355, P6 953 |
| M9 | values: never joined to the factor | P1 2389, P3 35, P5 869, P6 2588 |
| M10 | bfs: the last prime dropped | P1 1401, P3 18, P5 424, P6 1595 |
| M11 | bfs: the start not marked | P1 2997, P6 3197 |
| M12 | bfs: a number queued more than once | P1 2413, P2 991, P6 2612 |
| M13 | multiples: the walk from twice the prime | P1 824, P5 748, P6 1001 |
| M14 | multiples: the largest number never walked to | P1 1950, P3 403, P4 1949, P5 653, P6 2140 |
| M15 | multiples: the number joined, not its set | P1 1005, P3 67, P5 743, P6 1198 |

P1 and P6 kill all fifteen, P5 nine, P3 six, P2 four and P4 two.

P2 kills M4, M5, M6 and M12, whose mistakes depend on which place
comes first or on the order of the joins. P3 kills M2, M8, M9, M10, M14
and M15. P5 misses M3, M4, M5, M6, M11 and M12. P4 kills only M4 and
M14.

Thirty-three other edits were tried and set aside. Nine failed exactly
the same checks as others, in four groups: six answer 1 for every case,
failing P1 on the 2,473 small cases whose answer is larger (M3, ★ never
keeping a prime's first place, sieve counting by place, values resetting
each count to 1, bfs never queuing a reached number, and multiples
counting by value), and three mistakes were made the same way in ★ and
bfs, which factor alike (a square taken as its own prime, one power
divided out, and trial division from 3), so M1 and M2 are kept and the
third pair dropped. Twelve were sound but beyond three an arm: ★ growing
the smaller set and finding one step up, sieve putting every prime's
first place at 0 and stopping its factoring at 2, values taking factors
from 1, joining the value rather than its set and counting under the
parent, bfs counting sizes from 1, and multiples walking every other
multiple, counting under the parent, anchoring the walk at the prime and
stopping at the first composite. One crashed: ★ joining a set to itself
doubles its size each time, until the size overflows.

Eleven were equivalent. ★ reading the best from every place, not only
the roots: a place joined under another never grows again, and its root
counts it. ★ joining the larger set under the smaller: only the depth
changes. Sieve keeping the largest prime in the table: the entry is
still a prime of the number, divided out before the table is read again.
Sieve dividing out one power of a prime: the table gives the same prime
again, whose first place is now this one. Values joining a set to
itself, which changes nothing, and joining the factor to the cofactor:
the number is joined to the factor too, so it still reaches the
cofactor. Bfs expanding a prime again: every holder is marked already.
Multiples marking the prime itself composite, which the walk reads only
before it starts; walking composites too, whose multiples were joined
through each of their primes; never walking the largest prime, which has
no other multiple in range; and never marking 1, which no prime walks.

## Verification

Every arm prints the same output as `largest_component_size.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `46c2e7477d`, the runtime
archives rebuilt at the same commit. Under `karac __mir-run` the arms
take 1.2 to 1.9 s each, bfs 3.0 s and values 4.4 s, and the differential
38 s, all measured beside a test run.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The legacy compiler was removed from kara at M3, so there is no legacy
lane.

## Benchmarks

The bench program builds 20 sets of 2,000 distinct random numbers up to
100,000 once. In each of 40 rounds it runs the ★ arm on every set, each
round starting from a different one, and folds the answers into a
checksum. Every implementation prints `40 rounds over 20 sets of 2000
numbers up to 100000: largest components adding to 1456400, checksum
959356810`. Each call builds a new forest and a new map from prime to
first place: a `Map` in Kāra, a `HashMap` in Rust, a map in Go, a dict
in Python, and in C an open-addressing table with linear probing sized
for six primes a number.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.44 to 0.48 s | 0.46 s |
| Rust (`rustc -O`) | 0.35 to 0.41 s | 0.36 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.35 to 0.41 s | 0.37 s |
| Go | 0.59 to 0.66 s | 0.61 s |
| Python | 9.75 s | |
| Kāra (`karac build --mir`) | 0.42 to 0.47 s | 0.44 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Python's run is about 21 times
C's.

v2 takes 1.17 times Rust's median time under overflow checks and 0.95
times C's. Under valgrind's cachegrind v2 runs 3.48 billion
instructions and 0.80 billion branches with 13.6 million mispredicted,
Rust with overflow checks 3.54 billion, 0.75 billion and 12.5 million,
and C 2.28 billion, 0.60 billion and 9.8 million. C runs the fewest
instructions and still takes the longest of the three; that was not
looked into further.
