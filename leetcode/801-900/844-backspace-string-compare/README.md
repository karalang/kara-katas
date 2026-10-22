# 844. Backspace String Compare

Given two strings `s` and `t`, return `true` if they are equal when both
are typed into empty text editors, where `'#'` is a backspace. A
backspace on an empty text leaves it empty.

```
s = "ab#c", t = "ad#c"   ->  true    (both become "ac")
s = "ab##", t = "c#d#"   ->  true    (both become "")
s = "a#c",  t = "b"      ->  false   ("c" and "b")
```

**Constraints:** `1 <= s.length, t.length <= 200`, and both hold only
lowercase letters and `'#'`. The follow-up asks for O(n) time and O(1)
space.

## Approaches

| file | mechanism |
|---|---|
| `backspace_compare.kara` ★ | two pointers from the back, the follow-up's O(1) space: reading each string's bytes from the back, a count of pending backspaces says how many of the next characters to skip; each step finds the next surviving character of both strings and compares them, and the strings are equal when they run out together. The bytes are read through `s.bytes()` without a copy. O(n + m) time |
| `backspace_compare_stack.kara` | typed out on a stack: a letter is pushed and a `'#'` pops the last letter if there is one; the two stacks are compared. O(n + m) time and space |
| `backspace_compare_fold.kara` | a fold into a string: `s.chars().fold(String.new(), ...)`, where a `'#'` pops the last character of the text so far and any other character is appended; the two texts are compared. O(n + m) time and space |
| `backspace_compare_reversed.kara` | the survivors read backwards: each string is walked once from the back with a count of pending backspaces, collecting the characters that survive in reverse order, and the two reversed lists are compared. O(n + m) time and space |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 16 lines: LeetCode's three examples; ten more
(a single letter, backspaces alone, backspaces before a letter, two
backspaces that cancel a letter in one string and are spent on nothing
in the other, a prefix, two letters undone and a different one typed,
and four pairs where several letters are undone at once); the first 20
characters of a pair of LeetCode's longest strings, 200 characters, one
undoing each letter just after it and the other undoing each just before
the next, and the whole pair; and 2,000 random pairs, every other one a
string and the same with letters put in and undone and, once in three,
one character changed, with how many are equal and a checksum.
`backspace_compare.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: while a `'#'` remains, the first one is deleted together with
the character just before it, if there is one, and the texts left are
compared. It shares no code with any arm: it neither scans from the back
nor types into a stack. Its 1,600 cases come in four kinds of 400: two
short random strings; a string and the same with up to four letters put
in and undone, one character then changed once in three; two strings
that are mostly backspaces; and a string of 100 to 180 characters and
the same with up to ten letters put in and undone, so that the second
reaches LeetCode's 200. In 935 of them the strings are equal.

| | property |
|---|---|
| P1 | the statement's answer |
| P2 | `t` against `s` gives the same answer |
| P3 | `s` with letters put in and undone equals `s`, and against `t` gives the same answer |
| P4 | one to three backspaces put before `s`, or before `t`, give the same answer |
| P5 | a letter added to both gives the same answer, and so does a letter added to `s` and undone |

It prints `1600 cases, 935 equal, 32000 checks over 4 arms: 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and the same under
`karac __mir-llvm-asan` with no error.

## Mutation testing

Twelve edits to the differential, three to each arm, each run under
`karac __mir-run`. All twelve are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a `'#'` cancels nothing | P1 791, P3 1600, P5 261 |
| M2 | ★: equal when either string runs out | P1 423 |
| M3 | ★: each `'#'` cancels two characters | P1 534, P3 843, P5 403 |
| M4 | stack: a `'#'` on an empty stack pushed | P1 91, P4 618 |
| M5 | stack: a `'#'` ignored | P1 791, P3 1600, P5 261 |
| M6 | stack: only the lengths compared | P1 42 |
| M7 | fold: the `'#'` kept after it deletes | P1 772, P3 1583, P4 131, P5 207 |
| M8 | fold: the first character dropped | P1 82, P3 142, P4 477 |
| M9 | fold: `'a'` taken for the backspace | P1 716, P3 1046, P4 200, P5 396 |
| M10 | reversed: a pending backspace never used up | P1 351, P3 501, P5 595 |
| M11 | reversed: read forwards | P1 514, P3 747, P4 660, P5 334 |
| M12 | reversed: each `'#'` cancels two characters | P1 534, P3 843, P5 403 |

P1 kills all twelve. P3 fails in all 1,600 cases under M1 and M5, which
make a backspace do nothing, since the letters it puts in are then never
undone. P4 sees the edits that get a backspace on an empty text wrong
(M4 pushes it, M7 and M8 keep or drop a character at the front, and M11,
reading forwards, spends the leading backspaces on what follows), and P5
the edits that miscount what a backspace removes. M2 and M6 only P1
sees: M2 calls a string equal to any string it is a suffix of, and M6
any of the same length. M3 and M12 are the same edit to two arms and
fail identically.

P2 kills nothing, and cannot here: every arm puts both strings through
the same code, so an edit changes `s` and `t` alike and the answer stays
symmetric.

## Verification

Every arm prints the same output as `backspace_compare.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer) with no error; the
differential prints its lines under all three. `karac check` passes all
four arms, the differential and the bench program, the fold arm and the
differential with the warning in Compiler findings. The release and
debug builds are both at kara `c8c0d4a166`, and the runtime archives are
current with them. Under `karac __mir-run` each arm takes about 0.3 s
and the differential 8.4 s.

The leak check copied each arm's and the differential's sanitizer lane
executable as it was linked and ran it with the preloaded shim from kata
708, which refuses the lane's hand-made stack so that LeakSanitizer sees
`main`: all five print their output and report no leak.

The frozen legacy backends run the ★ and stack arms right: `karac run
--interp`, `karac run`, `karac build` and a `KARAC_AUTO_PAR=1` build all
print the same output. Legacy's interpreter stops the fold arm and the
differential at `out.pop()` with `method 'pop' not found on type
'String'`, though its compiled lanes run the fold arm right; its
compiled lanes refuse the reversed arm's `s.chars().rev()` as a chain
shape codegen does not support, though its interpreter runs it right.
Legacy refuses the bench program at a `*c` read through `.iter()` over
characters. Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm in all five languages. It draws 64
pairs once, each string at most LeetCode's 200 characters: the first is
120 characters, a `'#'` with chance 3 in 10 and otherwise one of the
first 2, 3 or 4 letters; the second is the first with 40 letters each
followed by a `'#'` put in at random places, and in every other pair one
character then changed. Each of 3,500,000 rounds compares the next pair.
Every implementation prints `3500000 rounds of 64 pairs: 1750000 equal,
checksum 333054855`, the Kāra program under `karac __mir-run` included,
in 474 s.

Spot timings on a shared 4-core container, eight runs of each compiled
program, five of them interleaved, and three of Python (`bench.sh`
timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.87 to 1.17 s |
| Rust (`rustc -O`) | 0.90 to 1.27 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.94 to 2.12 s |
| Go | 1.34 to 1.64 s |
| Python | 54.7 to 57.3 s |
| Kāra (`karac build --mir`) | 0.94 to 1.05 s |

The legacy backend refuses the program (Verification), so there is no
legacy time. `bench.sh` builds the Kāra program with `karac build
--mir`, the v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output.

At the medians of the interleaved runs v2 takes 1.01 s, against Rust's
0.99 (2.06 under overflow checks), C's 1.03 and Go's 1.48: 0.49 times
Rust's time under overflow checks, 0.98 times C's and 0.68 times Go's.
Overflow checks double Rust's time, most likely on the skip counter and
the index arithmetic of the inner loop (not traced). Under valgrind's
cachegrind C runs 13.4 billion instructions and 2.29 billion branches,
Rust 13.2 billion and 2.78 billion and v2 12.3 billion and 3.64 billion;
v2 mispredicts 405 million branches against C's 192 and Rust's 189
million, yet its time is no worse, most likely because the loop is short
and the branches it adds are cheap to recover from (not traced). Built
for `x86-64-v3`, the target `karac build` uses, C takes 0.96 to 1.12 s
and Rust with overflow checks 0.93 to 1.08 s, against v2's 0.93 to 1.07
s in the same five interleaved runs. Python takes 56 s, about 54 times
C's time. The comparison with C and Rust waits until after M4.

## Compiler findings

B-2026-10-22-2: the fold arm's `out.pop();` on a `String` warns
`discarded Option value` under `karac check`, while the stack arm's
`stack.pop();` on a `Vec` does not. The lint follows design.md, whose
displaced-value exemption lists `Vec.pop` but not `String.pop`, so the
row asks the spec to decide. The arm keeps the natural `out.pop();`, and
`karac check` still passes it with the warning; the differential carries
the same warning from its copy of the arm.
