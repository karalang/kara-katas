# 851. Loud and Rich

There are `n` people, labelled `0` to `n - 1`, each with a different
amount of money and a different quietness. `richer[i] = [a, b]` says
person `a` has more money than person `b`, and `quiet[x]` is person
`x`'s quietness. Return `answer`, where `answer[x]` is the quietest
person among everyone who certainly has at least as much money as person
`x`: `x` themselves, and anyone the pairs show to be richer.

```
richer = [[1,0],[2,1],[3,1],[3,7],[4,3],[5,3],[6,3]], quiet = [3,2,5,4,6,1,7,0]
  ->  [5,5,2,5,4,5,6,7]
richer = [], quiet = [0]  ->  [0]
```

**Constraints:** `1 <= n <= 500`, `quiet` is a permutation of `0..n`, `0
<= richer.length <= n * (n - 1) / 2`, every pair is distinct, and the
pairs are logically consistent, so they never make a cycle.

## Approaches

| file | mechanism |
|---|---|
| `loud_and_rich.kara` ★ | memoised search up the richer-than graph: the quietest person at least as rich as `x` is `x` or the answer for someone directly richer than `x`, so a recursive search that remembers each answer settles every person once. O(n + e) time |
| `loud_and_rich_topo.kara` | Kahn's topological order down the graph: start from everyone nobody is richer than, and reach a person only once everyone directly richer is settled; each pair `a -> b` offers `b` the quietest person found for `a`. O(n + e) time |
| `loud_and_rich_quietest.kara` | the quietest people first: people taken in order of quietness, each the answer for everyone below them in the richer-than order who has none yet, found by a walk that stops at anyone already answered. O(n log n + e) time |
| `loud_and_rich_relax.kara` | relaxing every pair until nothing changes, as in Bellman-Ford: a pair `a -> b` lets `b` take `a`'s answer when it is quieter, and after `k` passes each person has seen everyone up to `k` pairs richer. O(n * e) time |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 16 lines: LeetCode's two examples; nine more
(one pair each way round, nobody comparable, a chain getting quieter and
one getting louder, three people above one, one above three, a diamond,
and a person between two above and two below); four cases of LeetCode's
most people, 500: a chain getting quieter going down, the same chain
with its pairs in reverse order and getting louder going down, which
leaves the richest person as everyone's answer, and random orders with
about half of the 124,750 possible pairs and about one in a hundred,
each printed as a digest; and 300 random cases of up to 12 people, with
the sum of the answers' quietness and a checksum. `loud_and_rich.py`
mirrors the ★ arm and its output is byte-identical.

The quietest-first arm writes its walk's first stack as `[*p]`. The
natural `[p]`, with `p` a person read from `order.iter()`, is refused by
`karac check` and `karac __mir-run` as a `Vec[ref i64]` where a
`Vec[i64]` is expected, against core-semantics §5.10, which reads a
`ref` to a `Copy` value as the value in an element of a literal; that is
kara `B-2026-10-22-6`, and `*p` comes out when it closes.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: `y` is at least as rich as `x` when `y` is `x` or a chain of
pairs leads from `y` down to `x`, worked out as the transitive closure
of the pairs, and the answer for `x` is the quietest such `y`. Its 1,600
cases of 1 to 10 people come in four kinds of 400: each consistent pair
kept with chance 15 in 100, 60 in 100, a chain with every other pair
left implied, and a chance drawn per case; the pairs are shuffled. The
answers' quietness sums to 12,898.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the pairs in reverse order give the same answers |
| P3 | the people renamed by a random permutation give the renamed answers |
| P4 | one more consistent pair never makes anyone's answer louder |
| P5 | everyone's answer is no louder than they are, and is their own answer |

It prints `1600 cases, the answers' quietness sums to 12898, 32000
checks over 4 arms: 0 failures` under `karac __mir-run` and `karac
__mir-llvm-run`, and the same under `karac __mir-llvm-asan` with no
error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first richer person's answer taken over the person | P1 918, P4 177, P5 918 |
| M2 | ★: the pairs read the wrong way round | P1 1263 |
| M3 | ★: only people directly richer looked at | P1 504, P5 288 |
| M4 | topo: a person offered rather than their answer | P1 367, P2 3, P3 7, P4 5 |
| M5 | topo: only each person's first pair followed | P1 523, P2 523, P4 172 |
| M6 | topo: a person released after their first richer person | P1 66, P2 54, P3 29, P4 26, P5 20 |
| M7 | quietest: the loudest people first | P1 1263, P4 262, P5 1106 |
| M8 | quietest: the walk taking over answered people | P1 1023, P4 238, P5 988 |
| M9 | quietest: the walk stopping one step down | P1 504, P4 13 |
| M10 | relax: one pass only | P1 341, P2 467, P5 176 |
| M11 | relax: a person compared rather than their answer | P1 431, P2 292, P5 160 |
| M12 | relax: the pairs taken backwards | P1 1263 |

P1 kills all twelve. M2 and M12 are the same mistake in two arms, the
pairs read with the poorer person first, and fail the same cases; M3 and
M9 both stop one pair from the person, and fail as many cases under P1.
P2 sees the edits whose result depends on the order of the pairs: the
topological arm's, where the order decides who is released first (M4 to
M6), and the relaxation arm's, where it decides how far a single pass
reaches (M10, M11). P3 sees only M4 and M6, whose results depend on the
labels through the order people are released. P5 sees seven, those that
can leave someone with an answer louder than themselves or an answer
that is not its own answer (M1, M3, M6, M7, M8, M10, M11).

## Verification

Every arm prints the same output as `loud_and_rich.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `b28f8bf975`, and the runtime archives are
current with them. Under `karac __mir-run` the arms take 0.8 to 1.9 s
and the differential 1.9 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the topological and relaxation arms
right: `karac run --interp`, `karac run`, `karac build` and a
`KARAC_AUTO_PAR=1` build all print the same output. They run the ★ arm
right too, except that `karac run --interp` passes the 60 s limit after
printing the first line. Legacy refuses the quietest-first arm and the
differential at the `*p` above, since its `iter()` hands out copies of
the people rather than references to them, so `*` finds an `i64`; and it
refuses the bench program at the case borrowed with `ref cases[round %
count]`, passed on where it wants values. Legacy is frozen, so these are
noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
cases once, each of LeetCode's most people, 500, ranked by a random
order: case `g` keeps each of the 124,750 consistent pairs with chance
`2 << (g % 8)` in 1000, from about 250 pairs to about 32,000, and its
quietness is a random order too. Each of 10,000 rounds asks the next
case. Every implementation prints `10000 rounds of 64 cases: quietness
sums to 387911136, checksum 18138124`, the Kāra program under `karac
__mir-run` included, in 327 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.52 to 1.79 s |
| Rust (`rustc -O`) | 1.67 to 2.17 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.63 to 2.09 s |
| Go | 1.94 to 2.15 s |
| Python | 13.0 to 15.2 s |
| Kāra (`karac build --mir`) | 1.91 to 2.19 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.98 s, against Rust's
1.80 (1.80 under overflow checks too), C's 1.59 and Go's 2.00: 1.10
times Rust's time under overflow checks, 1.25 times C's and 0.99 times
Go's. Under valgrind's cachegrind v2 runs the most instructions, 12.70
billion against C's 8.69 billion and Rust's 11.93 billion, and the most
branches, 2.33 billion against 1.52 and 1.80 billion, and it mispredicts
74 million against 64 and 67 million. Built for `x86-64-v3`, the target
`karac build` uses, C takes 1.45 to 1.74 s and Rust with overflow checks
1.66 to 1.77 s, against v2's 1.85 to 2.10 s in the same five interleaved
runs. Python takes 13.0 s, about 8 times C's time. The comparison with C
and Rust waits until after M4.
