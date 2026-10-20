# 810. Chalkboard XOR Game

Numbers are written on a chalkboard, and Alice and Bob take turns, Alice
first, each erasing one number. A player who erases a number and leaves
the remaining numbers with a bitwise XOR of 0 loses; the XOR of no
numbers is 0. A player whose turn starts with the board's XOR at 0 wins.
Return whether Alice wins, both players playing their best.

```
nums = [1, 1, 2]  ->  false
nums = [0, 1]     ->  true
nums = [1, 2, 3]  ->  true
```

**Constraints:** `1 <= nums.length <= 1000` and `0 <= nums[i] < 2^16`.

## Approaches

Alice wins exactly when the board's XOR is already 0 or it holds an even
number of numbers. On an even count with a XOR `x` that is not 0, some
number differs from `x`, since an even count of `x` would XOR to 0, so
the player to move can always erase without leaving 0; Alice always
moves on an even count, so she is never forced to leave 0. On an odd
count with a XOR that is not 0 it is Bob who always moves on an even
count. The four arms differ in how they find the XOR.

| file | mechanism |
|---|---|
| `xor_game.kara` ★ | the XOR in a loop over the board, then the XOR of 0 or an even count. O(n) |
| `xor_game_bits.kara` | an even count wins at once; otherwise the ones in each of the 16 bits counted, and the XOR is 0 when every bit's count is even. O(16 n) |
| `xor_game_recursive.kara` | the XOR of a slice as the XOR of its two halves, down to one number or none. O(n), O(log n) deep |
| `xor_game_iter.kara` | the XOR as one `fold` over the board's iterator |
| `differential.kara` | the four arms against the game played out, four properties |

Every arm prints the same 13 lines: LeetCode's three examples; `[5]`,
which Alice must erase to leave 0; `[0]`, which starts at 0; `[7, 7,
7]`, an odd count of one number; `[3, 3]`, even and at 0; `[1, 2, 4,
8]`, even and not at 0; `[1, 2, 3, 4, 5]`, odd with a XOR of 1, where
Alice has safe moves at first and loses all the same; LeetCode's
largest, 1000 numbers below 65536; the first 999 of them, whose XOR is
15281; 998 of them with their XOR added, so that the XOR of the 999 is
0; and 2000 random boards of 1 to 9 numbers below 8, with Alice's wins
counted and a checksum. `xor_game.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the game itself:
`wins(mask)` says whether the player to move wins with the numbers in
`mask` left, a turn that starts at XOR 0 being a win and otherwise a win
when some number can be erased without leaving 0 and leaving a board the
other player loses, memoized over the 2^n boards. Its 1,600 cases have 1
to 12 numbers and come in four kinds of 400: numbers below 8; numbers
below 4, so that the XOR is often 0; multiples of 16384, so that the top
bit of a number below 65536 decides; and one number repeated with one
other first, so that most moves leave 0. Every case is checked against
the game.

| | property |
|---|---|
| P1 | the game's answer |
| P2 | the board reversed, and rotated by one, gives the same answer |
| P3 | the board with two more of the same number gives the same answer |
| P4 | the board with one more number gives the game's answer for it, and an odd board made even is a win |

It prints `1600 cases (934 won by Alice), 4 arms, 25600 checks, 0
failures` under `karac __mir-run` and `karac __mir-llvm-run`, and the
same under `karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the count's parity left out | P1 666, P2 666, P3 666, P4 722 |
| M2 | ★: an odd count, not an even one, wins | P1 1332, P2 1332, P3 1332, P4 1444 |
| M3 | ★: the XOR of 0 left out | P1 129, P2 129, P3 129, P4 83 |
| M4 | ★: the last number left out of the XOR | P1 302, P2 400, P3 166, P4 186 |
| M5 | bits: only the low 15 bits counted | P1 51, P2 51, P3 51, P4 9 |
| M6 | bits: a bit counted once it is set anywhere | P1 100, P2 100, P3 126, P4 83 |
| M7 | bits: an even count not short-cut | P1 666, P2 666, P3 666, P4 722 |
| M8 | recursive: a single number taken as 0 | P1 666, P2 666, P3 666, P4 722 |
| M9 | recursive: the halves overlapping by one | the program stops: a slice of two recurses into itself until the stack runs out |
| M10 | iter: the fold started at 1 | P1 251, P2 251, P3 251, P4 159 |
| M11 | iter: OR in place of XOR | P1 100, P2 100, P3 126, P4 83 |
| M12 | iter: a count above 1, not an even one, wins | P1 556, P2 556, P3 666, P4 722 |

P1 kills all twelve, and P2, P3 and P4 see every edit that returns an
answer too, since each edit gets the verdict wrong on some boards and
those properties keep the verdict. M9 never finishes a case: a slice of
two numbers splits into one number and the same two again, and `karac
__mir-run` stops with a stack overflow. M1, M7 and M8 fail the same
counts by a coincidence of these cases: M1 and M7 call the 666 even
boards whose XOR is not 0 lost, M8 calls the 666 odd boards whose XOR is
not 0 won, and the two sets are the same size. M6 and M11 fail the same
cases, as counting a bit once it is set anywhere and taking OR in place
of XOR both find a XOR of 0 only when every number is 0. M5 is seen only
on the multiples of 16384, the one kind where the top bit decides: a
first version of the differential drew numbers below 65536 at random
there, an odd board almost never had a XOR of exactly 32768, and M5
survived.

## Verification

Every arm prints the same output as `xor_game.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The debug build that
runs `__mir-llvm-run`, `__mir-llvm-asan` and `build --mir` and the
release build that runs `check` and `__mir-run` are both at kara
`491112bd56`, whose last compiler change is `51f0e57b3a`. The runtime
archives were built after the last runtime change, `7e85d320d5`.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`), the legacy JIT
(`karac run`), `karac build` and an auto-par build print the same output
for the ★ and recursive arms; the legacy build warns that `big` is used
after a move, legacy taking a bare parameter as owned rather than
borrowed, and prints the right output all the same. Legacy refuses the
bit-count arm, the iterator arm and the differential, as it types the
item of `nums.iter()` as an `i64` rather than a reference and so refuses
its `*`, and the bench program, reading `xor_game(boards[k])` as moving
a `Vec` out of an index (`E_INDEX_MOVE_NON_COPY`). Legacy is frozen, so
this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. 64 boards of 999
numbers below 32768 are made once. Each of 10,000,000 rounds writes a
new number into one place of the next board and asks who wins it, so
every round reads a whole board whose XOR has just changed. Every
implementation prints `10000000 rounds of 999 numbers: 298 won by Alice,
checksum 637565308`, the Kāra program under `karac __mir-run` included,
in 1,118 s with `KARAC_MIR_MAX_STEPS` raised past its default of 40
billion steps.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and two of Python (`bench.sh` timings
need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.47 to 1.68 s |
| Rust (`rustc -O`) | 3.46 to 3.64 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.52 to 3.61 s |
| Go | 4.01 to 4.52 s |
| Python | 266.47 to 274.34 s |
| Kāra (`karac build --mir`) | 1.04 to 1.14 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. Under `karac __mir-llvm-run` the program
prints the same line in 26.2 s, compile included; that JITs the MIR's IR
without optimization passes, so it is not a benchmark.

At the medians of the interleaved runs the v2 build takes 1.08 s,
against C's 1.51, Rust's 3.54 (3.57 under overflow checks) and Go's
4.14. The lead over C is the instruction set, not the language: `karac
build` targets `x86-64-v3` (see BENCHMARKS.md), and its XOR loop is four
AVX2 `vpxor`s of four numbers each, where `clang -O3` on the baseline
`x86-64` XORs two at a time. Under valgrind's cachegrind v2 runs 5.36
billion instructions, C 13.0 billion and Rust 19.9 billion. Built for
the same target, `clang -O3 -march=x86-64-v3` runs 4.09 billion and 1.10
to 1.21 s, a median of 1.15 s against v2's 1.05 s in five more
interleaved runs, so the two are level. Rust's loop is not vectorized at
either target: `rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`
runs the same 19.9 billion instructions, in 3.46 to 3.67 s. Legacy
refuses the bench program (see Verification), so there is no legacy
timing to set v2 against. The comparison with C and Rust waits until
after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench passed
`karac check` and every v2 lane as first written.
