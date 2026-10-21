# 830. Positions of Large Groups

In a string `s` of lowercase letters, a group is a maximal run of the
same letter: `"abbxxxxzyy"` has the groups `"a"`, `"bb"`, `"xxxx"`,
`"z"` and `"yy"`. A group is written as the interval `[start, end]` of
its first and last index, and is large when it holds 3 or more letters.
Return the intervals of every large group, in order of start.

```
s = "abbxxxxzzy"         ->  [[3,6]]
s = "abc"                ->  []
s = "abcdddeeeeaabbbcd"  ->  [[3,5],[6,9],[12,14]]
```

**Constraints:** `1 <= s.length <= 1000`, `s` holds lowercase English
letters only.

## Approaches

Each group is found by reading to where the letter changes; the arms
differ in how they mark that place.

| file | mechanism |
|---|---|
| `large_group_positions.kara` ★ | two pointers: from the start `i` of each group, `j` runs on while the letter stays the same, and the next group starts at `j`. O(n) |
| `large_group_positions_pass.kara` | one index, and a group closed where the letter differs from the one before it, or at the end, its start kept until then. O(n) |
| `large_group_positions_runs.kara` | the string encoded first as runs of a letter and a count, then the runs walked with the offset where each starts. O(n) |
| `large_group_positions_iter.kara` | the starts of the groups a `filter` over the indices, each paired by `map` with the next start to give its end, and the pairs of 3 or more `filter`ed and `collect`ed. O(n) |
| `differential.kara` | the four arms against the statement read interval by interval, four properties |

Every arm prints the same 15 lines: LeetCode's three examples; eight
small strings (no group of 3, one letter, two, three, a group of 3 at
either end, two groups of 3 side by side, and a group of 2 before two
large ones); three strings of LeetCode's greatest length, 1,000 letters
at random over two letters, over three, and one letter throughout, with
the number of groups and a checksum of their intervals; and the same
over 300 random strings of up to 30 letters over up to three.
`large_group_positions.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every interval `[i, j]` of 3 or more letters that are all the
same, kept when it cannot grow at either end. Its 1,600 cases are
strings of up to 24 letters and come in four kinds of 400: over one or
two letters, so that large groups are common; over up to 26, so that
they are rare; runs of 1 to 5 of one letter, each unlike the last; and
runs of exactly 2, 3 or 4, on either side of the boundary of large.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | the string reversed gives the same groups, each mirrored and their order turned round |
| P3 | the letters renamed, each moved the same distance round the alphabet, give the same groups |
| P4 | the last letter written three more times extends the last group, which is then large, by 3 |

It prints `1600 cases, 25600 checks over 4 arms: 0 failures` under
`karac __mir-run` and `karac __mir-llvm-run`, and the same under `karac
__mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a group of exactly 3 not large | P1 686 |
| M2 | ★: the end one past the group | P1 1110, P2 1110, P4 1600 |
| M3 | ★: the next search from `i + 1`, not from `j` | P1 879, P2 879, P4 1600 |
| M4 | pass: the group at the end never closed | P1 566, P2 615, P4 1600 |
| M5 | pass: the start never moved | P1 1209, P2 1170, P4 28 |
| M6 | pass: a group of 2 counted as large | P1 891 |
| M7 | runs: the offset moved by 1 a run | P1 725, P2 802, P4 1030 |
| M8 | runs: a new run counted from 0 | P1 1110, P2 879, P4 1600 |
| M9 | runs: the end one past the run | P1 1110, P2 1110, P4 1600 |
| M10 | iter: the last group ending one short | P1 566, P2 828, P4 1600 |
| M11 | iter: every group kept | P1 1284 |
| M12 | iter: index 0 not a start | P1 714, P2 615, P4 363 |

P1 kills all twelve. P3 sees none: every arm compares letters only for
equality, so a renaming cannot move any group, and no edit tried makes
an arm depend on which letter is which. M1, M6 and M11, which move the
boundary of large, are seen by P1 alone: they are wrong the same way
read in either direction, and a group the last letter makes 3 longer is
large under each of them. M4 and M10 lose or cut short the group at the
end, so P4, which grows exactly that group, fails on every case. M2 and
M9 are the same mistake in two arms and fail the same cases.

## Verification

Every arm prints the same output as `large_group_positions.py` under
`karac __mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`,
and under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
four arms, the differential and the bench program. The release build
that runs `check`, `__mir-run` and the mutation runs is at kara
`ceec478182`; the debug build that runs `__mir-llvm-run`,
`__mir-llvm-asan` and `build --mir` is at `90714715b1`, ten commits
earlier, none of them in the runtime; the runtime archives match both.
Under `karac __mir-run` each arm takes about 0.2 s and the differential
3 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy interpreter (`karac run --interp`) prints the same
output for all four arms and the differential, and the legacy JIT
(`karac run`), `karac build` and an auto-par build for the ★, one-pass
and iterator arms. Its compiled backends refuse the run-length arm and
the differential that copies it, which add to a run's count with
`runs[k - 1].1 += 1`: a tuple element assigned through an index is not
lowered there. Its checker refuses the bench program, which passes
`strings[round % count]` to a bare parameter and so, under legacy's
rules, moves it out of an index. Legacy is frozen, so this is noted, not
filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
strings of 1,000 letters, LeetCode's greatest length, once, the g-th
over `1 + g % 3` letters, so that most hold many groups. Each of 200,000
rounds answers the next string, building a fresh list of intervals, each
an array of two. Every implementation prints `200000 rounds of 64
strings: 13240625 groups, checksum 584765943`, the Kāra program under
`karac __mir-run` included, in 239 s with the interpreter's step limit
raised by `KARAC_MIR_MAX_STEPS`. The C program keeps the intervals as a
growable array of pointers to pairs allocated one by one, as the Kāra
program's `Vec[Vec[i64]]` is.

Spot timings on a shared 4-core container, eight runs of each compiled
program and 13 of v2's, five of them interleaved, and three of Python
(`bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.11 to 1.22 s |
| Rust (`rustc -O`) | 1.12 to 1.30 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.13 to 1.49 s |
| Go | 1.77 to 2.26 s |
| Python | 17.7 to 20.7 s |
| Kāra (`karac build --mir`) | 1.45 to 1.95 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.62 s, against Rust's
1.17 (1.25 under overflow checks), C's 1.16 and Go's 1.84: 1.3 times
Rust's time under overflow checks, and 1.4 times C's. Under valgrind's
cachegrind v2 runs 9.0 billion instructions and 2.1 billion branches,
against Rust's 5.7 and 1.3 billion and C's 5.2 and 1.1 billion, and
mispredicts 93 million branches to their 67 and 65 million, most likely
at the ends of groups (not traced). Where v2's extra instructions go was
not traced. Built for `x86-64-v3`, the target `karac build` uses, C
takes 1.01 to 1.33 s and Rust with overflow checks 1.16 to 1.29 s,
against v2's 1.45 to 1.78 s in the same five interleaved runs. Python
takes 21 s, about 18 times C's time. The comparison with C and Rust
waits until after M4.

## Compiler findings

Nothing new in v2: every arm, the differential and the bench program run
on every v2 lane as written, and in the first spelling tried.
