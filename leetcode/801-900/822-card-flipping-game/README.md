# 822. Card Flipping Game

There are `n` cards, with `fronts[i]` printed on the front of card `i`
and `backs[i]` on its back. All the cards lie face up, and any number of
them may be turned over. After turning, an integer is good if it faces
down on some card and faces up on no card. Return the smallest good
integer after turning the cards, or 0 if there is none.

```
fronts = [1,2,4,4,7], backs = [1,3,4,1,3]  ->  2     turn card 1: [1,3,4,4,7] up, [1,2,4,1,3] down
fronts = [1], backs = [1]                  ->  0
```

**Constraints:** `1 <= n <= 1000`, and `1 <= fronts[i], backs[i] <=
2000`.

## Approaches

A number on both sides of one card, a double, always faces up, so it is
never good. Any other number on a card can be: turn up the other side of
every card that has it, and it faces down on some card and up on none.
So the answer is the smallest number on any card that is not a double,
or 0.

| file | mechanism |
|---|---|
| `flipgame.kara` ★ | the doubles collected in a set, then the smallest number on any card that is not in it. O(n) |
| `flipgame_table.kara` | two tables of 2,001 marks indexed by the number, one for the doubles and one for the numbers on any card; the first number marked in the second and not the first answers. O(n + 2000) |
| `flipgame_brute.kara` | each number on any card tried against every card, failing on one that has it on both sides, the smallest passing kept. No set and no table. O(n^2) |
| `flipgame_iter.kara` | the doubles `collect`ed into a set from a `zip` of the two sides and a `filter`, and the answer the `min` of both sides `chain`ed together with the doubles filtered out |
| `differential.kara` | the four arms against every way of turning the cards played out, four properties |

Every arm prints the same 11 lines: LeetCode's two examples; six small
cases (one card with two numbers; two doubles of one number; two cards
that swap two numbers; a double whose number is also on another card;
the numbers 2,000 and 1,999 with a double of 2,000; and three doubles);
two hands of LeetCode's largest, 1,000 cards, one with the numbers 1 to
500 each doubled and 500 random cards up to 2,000, and one of numbers up
to 20; and 300 random hands of up to 12 cards of numbers up to 5, with a
total, the hands with no good number and a checksum. `flipgame.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement
played out: every one of the `2^n` ways of turning the cards, and in
each the backs that face up on no card; the answer is the smallest such
back over all of them, or 0. It knows nothing of doubles. Its 1,600
cases have up to 10 cards each and come in four kinds of 400: numbers up
to 4, where doubles are common; numbers up to 2,000, where they are
rare; half the cards doubles, of numbers up to 6; and numbers from 1,996
to 2,000, the top of the range. 110 cases have no good number.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the fronts and backs swapped give the same answer |
| P3 | the cards in reverse order give the same answer |
| P4 | with a double of the answer added, the answer is larger, or 0 |

It prints `1600 cases (110 with no good number), 25600 checks over 4
arms: 0 failures` under `karac __mir-run` and `karac __mir-llvm-run`,
and the same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the doubles never recorded | P1 461, P4 1600 |
| M2 | ★: the backs never tried | P1 566, P2 1142 |
| M3 | ★: the largest kept | P1 1343, P4 1343 |
| M4 | table: the backs never marked as on a card | P1 566, P2 1142 |
| M5 | table: the table read only to 1,999 | P1 5 |
| M6 | table: the cards with two numbers marked as doubles | P1 1095, P2 1356, P4 1461 |
| M7 | brute: a number fails on any front | P1 924, P2 1363 |
| M8 | brute: the first card never checked | P1 171, P3 207 |
| M9 | brute: the fronts never tried | P1 576, P2 1142 |
| M10 | iter: the cards with two numbers taken as doubles | P1 1095, P2 1356, P4 1461 |
| M11 | iter: the backs never tried | P1 566, P2 1142 |
| M12 | iter: the largest kept | P1 1343, P4 1343 |

P1 kills all twelve. M5 fails on only 5 cases, those whose answer is
2,000. The fourth kind of case first drew numbers from 1,990 to 2,000,
no case then answered 2,000, and M5 survived; narrowed to 1,996 to
2,000, five cases do. Mistakes made twice fail on the same numbers of
cases: the backs never tried in M2, M4 and M11; the largest kept in M3
and M12; and the cards with two numbers taken as doubles in M6 and M10.
P2 sees every edit that treats the two sides differently, and P3 only
M8, the one edit that treats one card differently. P4 sees the edits
that answer a double or the largest number: a double of the largest
number leaves it the largest of what is left, so the answer does not
grow.

## Verification

Every arm prints the same output as `flipgame.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` is at kara
`385539fdac`, with the runtime archives built from that tree; the
release build that runs `check` and `__mir-run` is at `d5daf8420c`, two
compiler changes ahead of it (`b2ead3a82f`, `8dd3fa3bd1`).

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★, table and brute-force arms. The legacy interpreter prints the
iterator arm's output, and the JIT and `karac build` refuse it and the
differential in codegen, finding no handler for `min` on the chained
iterator. Legacy refuses the bench program, as it takes `all_backs[g]`
passed to a function as a move out of an index. Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
hands once, each of 1,000 cards, LeetCode's largest, of numbers up to
2,000, half of the cards doubles. Each of 50,000 rounds answers the next
hand afresh: about 500 inserts into a hash set of integers and 2,000
lookups, so the work is hashing integers and probing the set. Every
implementation prints `50000 rounds of 64 hands: total 135145, checksum
279808087`, the Kāra program under `karac __mir-run` included, in 94 s
with the interpreter's step limit raised by `KARAC_MIR_MAX_STEPS`.

Spot timings on a shared 4-core container, six runs of each compiled
program and nine of v2's, five of them interleaved, and one of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.79 to 0.87 s |
| Rust (`rustc -O`) | 2.68 to 2.78 s |
| Rust (`rustc -O -C overflow-checks=on`) | 2.74 to 2.92 s |
| Go | 3.73 to 3.98 s |
| Python | 9.6 s |
| Kāra (`karac build --mir`) | 3.00 to 3.25 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 3.15 s, against C's
0.82, Rust's 2.74 (2.77 under overflow checks) and Go's 3.84. The hash
most likely decides the order (not traced): C hashes each integer with
one multiplication, while Rust and v2 both use SipHash-1-3, keyed afresh
per process in v2 and per set in Rust, and Go its own hash. Under
valgrind's cachegrind v2 runs 25.3 billion instructions, against Rust's
18.4 billion and C's 3.0 billion. Built for `x86-64-v3`, the target
`karac build` uses, C takes 0.75 to 0.82 s and Rust with overflow checks
2.67 to 2.88 s, against v2's 2.90 to 3.12 s in the same five interleaved
runs. Python takes 9.6 s, less than Go, as its sets of small integers
hash an integer to itself. The comparison with C and Rust waits until
after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
