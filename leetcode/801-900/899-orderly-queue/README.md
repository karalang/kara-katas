# 899. Orderly Queue

You are given a string `s` and an integer `k`. You can choose one of the
first `k` letters of `s` and append it at the end of the string.

Return the lexicographically smallest string you could have after
applying the mentioned step any number of moves.

```
s = "cba", k = 1    ->  "acb"
s = "baaca", k = 3  ->  "aaabc"
```

**Constraints:** `1 <= k <= s.length <= 1000`, and `s` consists of
lowercase English letters.

## Approaches

With `k = 1` the only move takes the first letter to the end, so the
strings reachable are the rotations of `s`, and the answer is the
smallest rotation. With `k >= 2` the first two letters can go to the end
in either order, which together with rotating swaps any two neighbours,
so every order of the letters is reachable and the answer is the letters
sorted. The arms differ in how they find the smallest rotation and in
how they sort.

| file | mechanism |
|---|---|
| `orderly_queue.kara` ★ | every rotation, or the letters sorted: each rotation built as a string and the smallest kept; for `k >= 2` the library sort. O(n^2) for `k = 1` |
| `orderly_queue_counts.kara` | rotations compared in place, letters counted: each rotation compared with the best so far letter by letter, reading round the end of `s`; for `k >= 2` a count of each letter. O(n^2) for `k = 1` |
| `orderly_queue_booth.kara` | Booth's least rotation: a Knuth-Morris-Pratt failure function over `s` written twice, kept for the best rotation so far and moved on when a smaller letter shows up; for `k >= 2` the letters counted. O(n) |
| `orderly_queue_duval.kara` | Duval's Lyndon factorization: `s` written twice split into Lyndon words that do not rise, the smallest rotation starting at the last factor that begins in the first copy; for `k >= 2` the library sort. O(n) for `k = 1` |
| `orderly_queue_pointers.kara` | two candidate starts, and neighbours swapped: at the first difference between the two candidates' rotations, the larger and every start just after it are ruled out; for `k >= 2` a sort by swapping neighbours, the move the queue itself allows. O(n) for `k = 1`, O(n^2) otherwise |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's two examples and eight
more (one letter, four equal letters, `bab` with `k` = 1 and 2, `abab`,
a reversed four with `k` = 4, and the alphabet reversed with `k` = 1
and 2); for 300 random cases of up to 300 letters from 1 to 26 letters,
half of them with `k = 1` and a quarter of them a short piece repeated,
a checksum of the answers; and two of LeetCode's largest, 1,000 letters
of `abb` repeated with one letter changed near the end, `k = 1`, and
1,000 random letters, `k = 2`. `orderly_queue.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every string the moves reach from `s`, a move taking one of
the first `k` letters out and writing it at the end, found breadth
first, and the smallest of them. It checks 3,200 random cases: 3,000 of
up to 6 letters from 1 to 3 against the statement, and 200 of up to 300
letters from 1 to 26 against the other properties, half of them with
`k = 1` and a quarter a short piece repeated; 41,309 letters in all.

| | property |
|---|---|
| P1 | the statement's smallest string, on the small cases |
| P2 | the letters of `s` rearranged, and for `k = 1` one of its rotations |
| P3 | no larger than the smallest rotation of `s`, which the moves reach for any `k`; for `k >= 2`, letters that never go down |
| P4 | any `k >= 2` gives what `k = n` gives, and `k = 1` gives nothing smaller than `k = 2` |
| P5 | the same answer for `s` rotated by a random amount, and the answer given back as `s` gives itself |
| P6 | each arm agrees with at least two of the other four |

P2 to P6 are checked on every case. It prints `3200 cases, 41309
letters, 95000 checks over 5 arms: 0 failures` under `karac __mir-run`
and `karac __mir-llvm-run`, and the same under `karac __mir-llvm-asan`
with no error.

## Mutation testing

Fifteen edits to the differential, three to each arm, each run under
`karac __mir-llvm-run`. All fifteen are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the rotation by one never tried | P1 215, P3 223, P5 306, P6 223 |
| M2 | ★: the largest rotation kept | P1 772, P3 858, P6 858 |
| M3 | ★: `k = 2` taken as rotations only | P1 45, P3 47, P4 47, P6 47 |
| M4 | counts: the start before the better one kept | P1 384, P3 412, P5 391, P6 412 |
| M5 | counts: each letter counted once | P1 855, P2 954, P3 355, P4 381, P6 954 |
| M6 | counts: the rotation written one letter on | P1 772, P3 858, P6 858 |
| M7 | booth: the start one past the one found | P1 772, P3 858, P6 858 |
| M8 | booth: the failure links never followed | P1 305, P3 357, P5 429, P6 357 |
| M9 | booth: no `z` written out | P2 9, P6 9 |
| M10 | duval: `s` read once, not twice | P1 16, P3 26, P5 57, P6 26 |
| M11 | duval: the start never moved | P1 581, P3 660, P5 628, P6 660 |
| M12 | duval: the letters never sorted | P1 434, P3 531, P4 660, P5 509, P6 531 |
| M13 | pointers: the smaller candidate ruled out | P1 772, P3 858, P6 858 |
| M14 | pointers: the later candidate taken | P1 466, P3 525, P5 482, P6 525 |
| M15 | pointers: the first two letters never swapped | P1 293, P3 382, P4 495, P5 378, P6 382 |

P6 kills all fifteen, and P1 and P3 all but M9, which drops every `z`
when it counts the letters back out: the small cases use only `a` to
`c`, and a string missing its last letters is still no larger than the
smallest rotation, so only P2's letter count sees it, on the nine large
cases with `k >= 2` and a `z`. Four mutants in three arms fail exactly
the same cases (M2, M6, M7, M13): each answers with the wrong rotation
in the same way whatever rotation of `s` it is given, so P2 and P5
hold. P5 kills the mutants whose answer depends on where `s` starts
(M1, M4, M8, M10, M11, M12, M14, M15). P4 kills the ones that go wrong only for `k >= 2` (M3, M5,
M12, M15).

No mutant had to be replaced.

## Verification

Every arm prints the same output as `orderly_queue.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its line under all three. `karac check` passes all
five arms, the differential and the bench program. `karac run` and a
`karac build --mir` binary print the same output for every arm and the
differential. The release build and the runtime archives are both at
kara `5502146bed`. Under `karac __mir-run` the arms take 0.3 to 2.3 s
each (the ★ arm, which builds every rotation as a string, is the slow
one) and the differential 12 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all six print their output and report no leak.

Every frozen legacy lane, the interpreter, the JIT and `karac build
--legacy` with and without auto-par, refuses all five arms, the
differential and the bench program: `*c` on an element of `.iter()` is
rejected, because legacy's iterator gives the value itself. Legacy is
frozen, so this is not filed.

## Benchmarks

The bench program uses the counts arm, which needs no library sort: 1,000
strings of 1,000 letters, LeetCode's largest, each a random piece of 1
to 4 letters written over and over with one letter changed at a random
place, so that rotations agree for long stretches before they differ.
Every string is asked with `k = 1`, comparing rotations in place, and
with `k = 2`, counting the letters. Every implementation prints `1000
strings of 1000 letters, k = 1 and 2: checksum 460342489`.

Timings on a quiet 4-core container, eight interleaved runs of each
compiled program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.25 to 0.35 s | 0.29 s |
| Rust (`rustc -O`) | 0.72 to 0.74 s | 0.72 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.71 to 0.78 s | 0.72 s |
| Go | 1.18 to 1.27 s | 1.21 s |
| Python | 20.6 s | |
| Kāra (`karac build --mir`) | 0.71 to 0.75 s | 0.72 s |

`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend, as kata 898's does. Legacy refuses the bench program
(above), so it has no row.

v2 takes the same median time as Rust under overflow checks, and 2.51
times C's. Under valgrind's cachegrind C runs 3.99 billion instructions
and 362 million branches, Rust with overflow checks 4.60 billion and
1.10 billion, and v2 5.30 billion and 1.45 billion; none of them
mispredicts more than a million. The inner loop reads two letters at
`(i + d) % n` and `(best + d) % n`. C's binary holds 4 division
instructions and Rust's and v2's 25 and 29, which suggests that clang
inlined `n = 1000` into the loop and turned `% n` into multiplications
while Rust and v2 divide on every letter; where each program spends its
time was not profiled, so that is an inference. The comparison with C
and Rust waits until after M4.
