# 921. Minimum Add to Make Parentheses Valid

A parentheses string is valid if and only if:

- it is the empty string,
- it can be written as `AB` (`A` concatenated with `B`), where `A` and
  `B` are valid strings, or
- it can be written as `(A)`, where `A` is a valid string.

You are given a parentheses string `s`. In one move, you can insert a
parenthesis at any position of the string. For example, if `s = "()))"`,
you can insert an opening parenthesis to be `"(()))"` or a closing
parenthesis to be `"())))"`.

Return the minimum number of moves required to make `s` valid.

```
s = "())"  ->  1
s = "((("  ->  3
```

**Constraints:** `1 <= s.length <= 1000`; `s[i]` is either `'('` or
`')'`.

## Approaches

Once every matched pair is taken out, what is left is a run of `)`
followed by a run of `(`, and each of those needs one added partner.

| file | mechanism |
|---|---|
| `min_add_to_make_valid.kara` ★ | one count of the `(` still open: a `)` closes one, or, with none open, needs a `(` added; at the end each open one needs a `)`. O(n), O(1) space |
| `min_add_to_make_valid_stack.kara` | a stack of the parentheses not yet matched: a `)` on top of a `(` takes it off, anything else goes on, and the stack's height is the answer. O(n) |
| `min_add_to_make_valid_pairs.kara` | adjacent `()` pairs taken out in sweeps until a sweep takes out nothing, and the length left is the answer. O(n) a sweep, as many sweeps as the parentheses nest deep |
| `min_add_to_make_valid_prefix.kara` | the running balance (`(` is +1, `)` is -1): if its lowest point is `-m`, then `m` opening parentheses at the front and `final + m` closing ones at the back are needed. O(n) |
| `min_add_to_make_valid_halves.kara` | divide and conquer: a `Unmatched` struct holds a stretch's unmatched `)` and `(`, two neighbours combine by matching the left one's `(` with the right one's `)`, and the string is split in halves down to single characters. O(n), O(log n) deep |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: LeetCode's two examples and eight
more (valid, closed before opened, nested and valid, closes then opens,
all closes, a mix that needs one of each, all opens, and a pair after
an unmatched close); for 500 random strings of 1 to 1,000 parentheses,
leaning from `)` to `(`, the answers' sum (54,833) and a checksum; and
five of LeetCode's largest, 1,000 characters: all `(`, all `)`, `()`
500 times, `)(` 500 times and 500 nested pairs.
`min_add_to_make_valid.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally. It lists every valid string of each even length up to 16 from
the statement's rules (each non-empty one is `(A)` followed by `B` for
exactly one split), and the answer is the least `d` such that some valid
string of length `n + d` holds `s` in order, with the `d` added
parentheses among it. It checks 3,200 random strings, each leaning
toward `(` or `)` by a random amount: 3,000 of 1 to 8 parentheses
against the statement, and 200 of 1 to 1,000 against the other
properties; 109,403 parentheses in all.

| | property |
|---|---|
| P1 | the statement's fewest additions, on the small strings |
| P2 | between 0 and `n`, and of the same parity as `n`, since a valid string has even length |
| P3 | the same answer for the string read backwards with each parenthesis turned round |
| P4 | the same answer with a matched `()` put in at a random position |
| P5 | for a second random string `t`, the answer for `s` followed by `t` is at most the two answers added and at least their difference |
| P6 | each arm agrees with at least two of the other four |

It prints `3200 strings, 109403 parentheses, answers summing to 37531,
95000 checks over 5 arms: 0 failures` under `karac __mir-run` (6 s) and
`karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan` with
no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the parentheses still open at the end forgotten | P1 1848, P2 1262, P3 2782, P5 669, P6 2000 |
| M2 | ★: a close always taken as matching | P1 1837, P2 314, P3 2102, P5 1294, P6 1998 |
| M3 | ★: the larger of the two counts, not their sum | P1 835, P2 748, P6 948 |
| M4 | stack: a close matching whatever is on top | P1 1097, P3 2058, P5 381, P6 1234 |
| M5 | stack: an unmatched close never pushed | P1 1837, P2 1203, P3 2782, P5 813, P6 1998 |
| M6 | stack: a close matched against the bottom of the stack | P1 769, P3 1154, P4 1481, P5 522, P6 929 |
| M7 | pairs: a single sweep | P1 276, P4 416, P6 472 |
| M8 | pairs: any two different neighbours taken as a pair | P1 835, P6 948 |
| M9 | pairs: the character after a pair dropped with it | P1 1259, P2 1196, P3 1114, P4 2519, P5 402, P6 1458 |
| M10 | prefix: the lowest point read before each step | P1 812, P2 240, P3 1669, P4 229, P5 1400, P6 845 |
| M11 | prefix: the lowest point taken one lower | P1 2206, P2 830, P3 1669, P4 230, P6 2376 |
| M12 | prefix: a negative final balance taken as zero | P1 1296, P2 1120, P3 2782, P5 344, P6 1400 |
| M13 | halves: the left closes matched with the right opens | P1 1319, P4 801, P6 1465 |
| M14 | halves: matched closes kept | P1 1451, P2 1147, P3 1158, P4 2678, P5 107, P6 1649 |
| M15 | halves: the left stretch's open parentheses lost | P1 1297, P2 948, P3 2361, P4 813, P5 299, P6 1493 |

P1 and P6 kill all fifteen; P3 eleven, P2 and P5 ten, and P4 eight. M8
reduces the answer to the difference between the counts of `(` and `)`,
which has the right parity, is the same backwards and turned round, is
unchanged by an added pair and keeps P5's bounds, so only the statement
and the other arms see it. P4 misses seven (M1 to M5, M8, M12): each of
those arms still matches an added `()` at once, so the pair leaves its
wrong answer as it was. P3 misses four (M3, M7, M8, M13) whose mistakes
come out the same on the string read backwards and turned round.

Two mutants were replaced because each failed exactly the same checks
as another: the first M10 (prefix: the closes at the back forgotten)
counts only the parentheses left open, as M5 does, and the first M12
(prefix: the final balance used for the lowest point) gives the
difference between the counts, as M8 does.

## Verification

Every arm prints the same output as `min_add_to_make_valid.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build is at kara `9913c68556` and the runtime
archives at `5502146bed`, with no change to the runtime between them.
Under `karac __mir-run` the arms take 0.4 to 1.5 s each (the pairs arm
the longest) and the differential 6 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every arm and the differential print the same output under the frozen
legacy interpreter, the legacy JIT and both legacy builds, with and
without auto-par; the builds of the halves arm and the differential
also warn that a vector is moved and then used again, which v2's
borrowing parameters make untrue. Legacy refuses the bench program,
which passes `strings[i]` straight to the function: "cannot move ... out
of an index", legacy's owned parameters, where v2's parameter borrows
it. An earlier draft of the differential passed `next_random(mut seed)`
as an argument beside `mut seed` itself; v2, the legacy JIT and the
legacy builds evaluate the arguments left to right, but the legacy
interpreter drew different strings from it (118,204 parentheses rather
than 109,403), so the differential now draws those values first, which
v2 prints the same for. Legacy is frozen, so none of this is filed.

## Benchmarks

The bench program builds 1,000 random strings of 1,000 parentheses
once, leaning from `)` to `(`, and runs the ★ arm on every string in
each of 100 rounds, each round starting from a different string so that
the order-sensitive checksum changes. Every implementation prints `100
rounds over 1000 strings of 1000: answers summing to 21403600, checksum
463063363`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.43 to 0.48 s | 0.46 s |
| Rust (`rustc -O`) | 0.46 to 0.53 s | 0.47 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.48 to 0.55 s | 0.50 s |
| Go | 0.46 to 0.52 s | 0.48 s |
| Python | 4.2 s | |
| Kāra (`karac build --mir`) | 0.46 to 0.52 s | 0.48 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 902's does. Legacy cannot build it (see
Verification). Python's run is about nine times C's.

v2 takes 0.97 times Rust's median time under overflow checks and 1.05
times C's. All four compiled programs are bound by the same thing: each
character is a branch on a random parenthesis, and under valgrind's
cachegrind every one of them mispredicts about 49 million branches.
Beside that, v2 runs 0.91 billion instructions and 0.31 billion
branches, Rust with overflow checks 0.83 billion and 0.31 billion, and
C 0.62 billion and 0.20 billion.
