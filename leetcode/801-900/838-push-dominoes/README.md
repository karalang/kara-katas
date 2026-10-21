# 838. Push Dominoes

There are `n` dominoes standing in a line, and some of them are pushed
at the same moment, each to the left or to the right. After each second,
each domino falling to the left pushes the domino next to it on the
left, and each domino falling to the right pushes the one next to it on
the right. A standing domino pushed from both sides at once stays up,
balanced between the two forces, and a falling domino gives no extra
force to one that is already falling or fallen. The line is given as a
string `dominoes`: `'L'` for a domino pushed left, `'R'` for one pushed
right and `'.'` for one not pushed. Return the string of the final
state.

```
dominoes = "RR.L"            ->  "RR.L"
dominoes = ".L.R...LR..L.."  ->  "LL.RR.LLRRLL.."
```

**Constraints:** `1 <= n <= 10^5`, and every character is `'L'`, `'R'`
or `'.'`.

## Approaches

Every arm turns the string into a list of `char`s and builds the answer
with `String.push`.

| file | mechanism |
|---|---|
| `push_dominoes.kara` ★ | the stretches between pushes: a walk from push to push, with an `L` imagined before the line and an `R` after it; between like pushes every domino falls that way, between an `R` and an `L` the halves fall inward and an odd middle stays up, and between an `L` and an `R` nothing moves. O(n) |
| `push_dominoes_forces.kara` | forces from both sides: a pass from the left gives each domino the force of the nearest `R` with only standing dominoes between, `n` at the `R` and one less each step, a pass from the right the same for `L`s, and each domino falls toward the stronger. O(n) |
| `push_dominoes_waves.kara` | second by second: the dominoes that fell in the last second push their neighbours, a domino pushed from both sides at once settles standing, and each second's falls are the next second's pushers. O(n) in all |
| `push_dominoes_nearest.kara` | the nearest push on each side: two passes find the distance back to the nearest `R` and ahead to the nearest `L` with only standing dominoes between, and each domino falls toward the nearer, standing at a tie. O(n) |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 17 lines: LeetCode's two examples; eleven more
(single dominoes of each kind, an `R` and an `L` with one and with two
dominoes between, an `R` falling to the end and an `L` from the start,
an `L` and an `R` facing away, a fall stopped by an `R` facing a
balanced middle, pushes away from each other in the middle of a line,
and an `R` whose stretch an `L` cuts in half); three lines of LeetCode's
greatest length, 10^5, with each domino pushed each way with chance 1,
10 and 60 in 200, shown by their counts and a checksum; and 300 random
lines of 1 to 60 dominoes, with the number left standing and a checksum.
`push_dominoes.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: second by second, each standing domino with an `R` on its
left or an `L` on its right falls that way unless it has both, the new
state worked out whole from the old, until a second changes nothing. Its
1,600 cases come in four kinds of 400: lines of 1 to 8 dominoes of any
mix; lines up to 60 with few pushes; lines up to 60 with many; and lines
of up to 8 pieces, each an `L` or an `R` followed by 0 to 6 standing
dominoes, so that every length of stretch between every pair of pushes
comes up.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the line mirrored, read right to left with each push turned round, gives the answer mirrored |
| P3 | the answer is settled: given as a line, it comes back unchanged |
| P4 | every pushed domino keeps its push |
| P5 | an `L` added before the line and an `R` after it change nothing between them |

It prints `1600 cases, 32000 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first domino of a stretch between like pushes left up | P1 1076, P2 843 |
| M2 | ★: the middle domino between an `R` and an `L` falling | P1 449, P2 449 |
| M3 | ★: an `R` imagined before the line, not an `L` | P1 711, P2 1209, P5 711 |
| M4 | forces: an `L`'s force not fading | P1 612, P2 612 |
| M5 | forces: an `L` not stopping an `R`'s force | P1 797, P2 828, P3 710, P4 496 |
| M6 | forces: a tie falling right | P1 1268, P2 1268 |
| M7 | waves: a second push from the other side winning, not balancing | P1 449, P2 449 |
| M8 | waves: a domino that fell not marked as settled | P1 296 |
| M9 | waves: each domino pushing the wrong neighbour | P1 1110, P5 1169 |
| M10 | nearest: an `L` not cutting off the `R` before it | P1 616, P2 696, P3 46 |
| M11 | nearest: a tie falling right | P1 449, P2 449 |
| M12 | nearest: the distance back to an `R` one too long | P1 612, P2 612, P3 296 |

P1 kills all twelve and P2, the mirror, all but two: most edits favour
one direction, and the mirror turns that round. The two it misses act
alike in both directions: M8 lets two dominoes that fell toward each
other in one second knock each other back in the next, and M9 makes
every domino push the wrong way. P5 sees only the edits that change how
the line's ends are read (M3) or that push past them (M9). P3 and P4 see
only the edits that let a fall run through a push: M5 even overwrites
pushed dominoes, which P4 alone checks. M2, M7 and M11 kill alike, 449
failures each: all three topple the balanced middle of an `R` and `L`
pair with an odd stretch between.

## Verification

Every arm prints the same output as `push_dominoes.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release and debug
builds are both at kara `d4ba0a00ad`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes 1.3 to 2.2 s
and the differential 2.8 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run every arm and the differential right:
`karac run --interp`, `karac run` and `karac build` all print the same
output. Built with `KARAC_AUTO_PAR=1`, the second-by-second arm returns
every line unchanged, so that no domino falls, on every run; the other
three arms are right under it. Legacy refuses the bench program as
moving a `String` out of an index, which v2's borrowing parameters do
not do. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 16
lines once, each of LeetCode's greatest length, 10^5 dominoes, line `g`
pushing each domino left with chance `1 + 4g` in 200 and right with the
same chance. Each of 1,300 rounds settles the next line and reads 16
dominoes of the result. Every implementation prints `1300 rounds of 16
lines: 16666 of the dominoes read fallen, checksum 459566967`, the Kāra
program under `karac __mir-run` included, in 167 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.93 to 1.23 s |
| Rust (`rustc -O`) | 1.06 to 1.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.97 to 1.10 s |
| Go | 1.98 to 2.26 s |
| Python | 12.4 to 12.6 s |
| Kāra (`karac build --mir`) | 1.34 to 1.56 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.45 s, against Rust's
1.11 (1.05 under overflow checks), C's 0.98 and Go's 2.20: 1.4 times
Rust's time under overflow checks, 1.5 times C's, and 0.66 times Go's.
Under valgrind's cachegrind C runs 3.2 billion instructions and 0.94
billion branches, Rust 6.2 and 1.54 billion and v2 7.6 and 1.82 billion;
the three mispredict about alike, 81, 92 and 97 million branches. Most
likely the gap to C is the answer built one `char` at a time with
`String.push`, a call that may grow the buffer and encodes the `char`,
where C stores a byte (not traced). Built for `x86-64-v3`, the target
`karac build` uses, C takes 0.94 to 1.08 s and Rust with overflow checks
0.97 to 1.09 s, against v2's 1.36 to 1.40 s in the same five interleaved
runs. Python takes 12.5 s, about 13 times C's time. The comparison with
C and Rust waits until after M4.

## Compiler findings

None on v2: every arm, the differential and the bench program pass
`karac check` and run on both v2 backends as written.
