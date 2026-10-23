# 886. Possible Bipartition

We want to split a group of `n` people (labeled from `1` to `n`) into
two groups of any size. Each person may dislike some other people, and
they should not go into the same group. Given the integer `n` and the
array `dislikes` where `dislikes[i] = [ai, bi]` indicates that the
person labeled `ai` does not like the person labeled `bi`, return `true`
if it is possible to split everyone into two groups in this way.

```
n = 4, dislikes = [[1,2],[1,3],[2,4]]  ->  true
n = 3, dislikes = [[1,2],[1,3],[2,3]]  ->  false
```

**Constraints:** `1 <= n <= 2000`, `0 <= dislikes.length <= 10^4`,
`dislikes[i].length == 2`, `1 <= ai < bi <= n`, all the pairs of
`dislikes` are unique.

## Approaches

| file | mechanism |
|---|---|
| `possible_bipartition.kara` ★ | two colours by breadth-first search: the split exists exactly when the graph of dislikes can be coloured with two colours, no dislike joining one colour; a search from each person not yet coloured gives each neighbour the other colour, and a neighbour already holding the same colour means no split. O(n + E) |
| `possible_bipartition_recursive.kara` | two colours by recursion: the same colouring as a recursive depth-first search, `paint(u, c)` failing when a neighbour already holds c. O(n + E), recursion up to n deep |
| `possible_bipartition_enemies.kara` | union-find over each person's dislikes: everyone a person dislikes must share one group, so a union-find joins them; the split fails exactly when someone ends up in the set of a person they dislike. O((n + E) * alpha(n)) |
| `possible_bipartition_parity.kara` | union-find with parity: each person keeps whether they sit with their parent or apart from it; a dislike across two sets joins them with the parity that puts the two apart, and one within a set fails when the two already sit together. O(E * alpha(n)) |
| `possible_bipartition_doubled.kara` | union-find over two copies of everyone: x stands for "x in group A" and x + n for "x in group B"; a dislike joins a with b + n and b with a + n, and the split fails when some person's two copies end up joined. O((n + E) * alpha(n)) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (a cycle of five; one person; two who dislike each other; 2,000
people with no dislikes; a path of 2,000; cycles of 2,000 and 1,999; and
one person disliking the 1,999 others); how many of 3,000 groups of up
to 8 people can be split, 2,499; and of 100 groups of 1,000 to 2,000
people with 10^4 dislikes, with a checksum. The random groups' dislikes
are drawn across two random sides, and up to five (or two, in the large
groups) more are drawn between any two people, so that some groups can
be split and some cannot. `possible_bipartition.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way of splitting the people into two groups, as the
bits of a number below 2^n, tried until one puts every pair who dislike
each other apart. It checks 3,100 cases: 3,000 groups of up to 10
people against the statement, and 100 of 100 to 500 people with up to
2,000 dislikes against the other properties. The ★ arm finds a split for
2,434.

| | property |
|---|---|
| P1 | the statement's answer, on up to 10 people |
| P2 | dislikes all drawn across two sides can always be split |
| P3 | the people relabelled, the pairs in another order and each written either way round, give the same answer |
| P4 | one pair fewer never stops a split, and one more pair never makes one |
| P5 | a copy of the group beside it, people n + 1 to 2n, changes nothing, and three new people who all dislike one another rule out any split |
| P6 | each arm agrees with at least two of the other four |

P3 to P6 are checked on every case, and P2 on every case drawn with no
pairs between any two people. It prints `3100 cases, 2434 can be split,
79750 checks over 5 arms: 0 failures` under `karac __mir-run` and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a neighbour given the same colour | P1 1925, P2 401, P6 1988 |
| M2 | ★: a clash ignored | P1 629, P5 3100, P6 666 |
| M3 | ★: only person 1's part of the graph searched | P1 59, P3 92, P5 2493, P6 59 |
| M4 | recursive: a clash found deeper in the search ignored | P1 193, P3 244, P4 53, P6 227 |
| M5 | recursive: a clash taken to be a neighbour of the other colour | P1 1925, P2 401, P6 1988 |
| M6 | recursive: everyone painted the first colour | P1 1211, P2 252, P3 246, P6 1274 |
| M7 | enemies: a person's second dislike never joined to the first | P1 292, P3 130, P4 1, P5 2726, P6 292 |
| M8 | enemies: a person joined to their own dislikes | P1 1380, P2 284, P6 1443 |
| M9 | enemies: the joins never made | P1 629, P5 3100, P6 666 |
| M10 | parity: sets joined with the two together | P1 201, P2 63, P6 264 |
| M11 | parity: a path's parity dropped as it is compressed | P1 193, P2 46, P3 305, P4 12, P5 2404, P6 256 |
| M12 | parity: a clash taken when two of one set sit apart | P1 632, P2 63, P3 85, P4 12, P5 2601, P6 695 |
| M13 | doubled: only a joined to the other copy of b | P1 14, P3 153, P6 14 |
| M14 | doubled: each person compared with the copy of the one before | P1 1889, P2 358, P3 365, P5 316, P6 1952 |
| M15 | doubled: the second join putting the two together | P1 1925, P2 401, P6 1988 |

P1 and P6 kill all fifteen. M1, M5 and M15 are one fault in three arms,
every pair who dislike each other taken as a clash, so any dislike rules
out a split, and they fail the same cases; M2 and M9 are its opposite,
no clash ever found, and fail the same cases, every one of them on P5's
three people who all dislike one another. M13 is the closest to
surviving, and fails P3 ten times as often as the statement: with only a
joined to b's other copy, the answer depends on which way round each
pair is written, which P3 changes. One mutant was replaced: skipping the
last person's joins in the enemies arm, tried first for M9, survived,
and is most likely equivalent, as the joins of the others still close
any odd cycle through that person (worked by hand on cycles of three and
five, not proved).

## Verification

Every arm prints the same output as `possible_bipartition.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `fe44986b7e`. Under `karac __mir-run` the arms take 3.9 to 6.3 s
each (the enemies arm, joining every person's dislikes and then checking
every pair, the slowest) and the differential 17 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

The frozen legacy backends' interpreter, JIT and `karac build
--legacy`, with and without auto-par, print the same output for all five
arms and the same line for the differential.

## Benchmarks

The bench program uses the ★ arm, in all five languages: 4,000 groups of
1,000 to 2,000 people, each person disliking the people five distinct
offsets on, every offset below n / 2 so that no pair repeats, 5n pairs
and up to 10^4; the offsets are odd, but one of them is even in half the
groups, and 1,470 of the groups can be split. The pairs are a `Vec` of
two-element `Vec`s in Kāra and Rust, as LeetCode passes them, a slice of
slices in Go and a list of lists in Python, with a list per person for
the graph and a `VecDeque`, `VecDeque`, slice or `deque` for the queue.
C keeps the pairs in one flat array, the graph in one array indexed by
each person's offset into it and the queue in an array. Every
implementation prints `4000 groups of up to 2000 people: 1470 can be
split, checksum 599947962`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.21 to 0.24 s | 0.23 s |
| Rust (`rustc -O`) | 1.54 to 1.75 s | 1.59 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.59 to 1.78 s | 1.68 s |
| Go | 3.14 to 3.68 s | 3.30 s |
| Python | 8.4 s | |
| Kāra (`karac build --mir`) | 1.49 to 1.79 s | 1.55 s |
| Kāra legacy (`karac build --legacy`) | 1.47 to 1.60 s | 1.50 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 885's does.

v2 takes 0.92 times Rust's median time under overflow checks, 1.03
times legacy's and 6.85 times C's. Under valgrind's cachegrind C runs
1.35 billion instructions, Rust with overflow checks 23.25 billion,
legacy 22.17 billion and v2 22.78 billion. The others allocate a `Vec`
for every pair, up to 10^4 a group, and one for every person's list,
where C allocates five arrays a group; that most likely accounts for
nearly all of C's lead (inferred from the layouts and counts, not
profiled). The comparison with C and Rust waits until after M4.
