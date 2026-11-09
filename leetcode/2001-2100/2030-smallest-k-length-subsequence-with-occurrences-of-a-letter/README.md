# 2030. Smallest K-Length Subsequence With Occurrences of a Letter

Given a string `s`, an integer `k`, a letter `letter` and an integer
`repetition`, return the lexicographically smallest subsequence of `s` of
length `k` that holds `letter` at least `repetition` times. The test cases
guarantee that `letter` appears in `s` at least `repetition` times.

```
s = "leet",      k = 3, letter = "e", repetition = 1  ->  "eet"
s = "leetcode",  k = 4, letter = "e", repetition = 2  ->  "ecde"
s = "bb",        k = 2, letter = "b", repetition = 2  ->  "bb"
```

**Constraints:** `1 <= repetition <= k <= s.length <= 5 * 10^4`; `s` is
lowercase English letters; `letter` is a lowercase English letter that
appears in `s` at least `repetition` times.

The answer is built from the left: a place takes the smallest character
that still leaves room for the places after it and enough copies of
`letter` for the ones still owed. A stack does that in one pass, popping a
larger character when a smaller one comes and the pop can still be made
good; the other arms choose each place directly.

## Approaches

| file | mechanism |
|---|---|
| `subseq.kara` ★ | a stack of bytes: a character pops the larger ones above it while the rest of `s` can refill the stack to `k` and enough copies of `letter` are left; it is pushed while there is room the copies still owed do not need. O(n) |
| `subseq_table.kara` | each place chosen in turn from a table of where each of the 26 characters next occurs, with a suffix count of `letter`. O(26 n) |
| `subseq_lists.kara` | each place chosen in turn from per-character lists of positions, each with a cursor that only moves forward, and a prefix count of `letter`. O(n + 26 k) |
| `subseq_string.kara` | the ★ arm's stack kept as the answer `String` itself, read with `chars().last()` and shortened with `pop`. O(n) once `last` is O(1) (see Verification) |
| `subseq_scan.kara` | each place found by scanning the window it can come from for the smallest character that leaves enough copies of `letter`, the first of equals. O(k (n - k)) |
| `subseq_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<char>`, `while let Some(&top) = stack.last()`, `as usize`, `as i32`, `&&`, `||`, `into_iter().collect()`, a `&String` wrapper), carried by `karac fix` to a clean check |
| `differential.kara` | all six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: the answers for LeetCode's three
examples and five more; then the copies of `letter` kept and a checksum of
the answers for 3000 problems of 1 to 20 letters from the first 1 to 6 of
the alphabet, and for 6 problems of 2000 to 50000 letters, with `k` near
the ends of its range where the scan arm stays fast. `subseq.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of `k` positions tried, by a bitmask, the ones holding
at least `repetition` copies of `letter` kept, the smallest string they
spell taken. It checks 1500 problems of 1 to 10 letters from the first 1
to 5 of the alphabet. Every random choice of a problem is drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | with `repetition` one lower (when it is at least 2), the answer is no larger |
| P3 | with `k` the whole length and `repetition` at most the copies there are, the answer is `s` itself |
| P4 | every character moved one up the alphabet, `letter` too, moves the answer one up |
| P5 | the answer is a valid problem of its own (`k` letters, at least `repetition` copies), and asked for again from itself is the answer |
| P6 | each arm agrees with at least three of the other five |

P2 holds because a looser demand admits every subsequence the tighter one
does. P3 because the only subsequence of the whole length is `s`. P4
because moving every character up keeps their order. P5 because the answer
is a subsequence of itself and every rival from it is one of `s`; an answer
that is not itself a valid problem fails P5 without being asked, since the
arms assume the guarantee and the scan arm stops with no place to take.

The differential prints `1500 problems: checksum 863121362, 54000 checks
over 6 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run under
`karac __mir-run` and `karac __mir-llvm-run`. Seventeen are kept, three to
each of the five Kāra arms and two to the Rust arm. All thirty are killed,
each fails the same way under both backends, none by a crash, and no two
kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: an equal character popped | P1 132, P2 46, P6 132 |
| M2 | ★: the room to refill counted one high | P1 321, P3 835, P5 321, P6 321 |
| M3 | ★: a popped letter's copy not given up | P1 237, P2 28, P5 237, P6 237 |
| M4 | table: the last place that leaves room refused | P1 815, P2 101, P3 1500, P5 1500, P6 815 |
| M5 | table: a character's next occurrence only at the index itself | P1 637, P2 172, P5 341, P6 637 |
| M6 | table: no copies of the letter counted ahead | P1 801, P2 334, P3 929, P5 702, P6 801 |
| M7 | lists: a position at the start passed over | P1 1060, P2 264, P3 1500, P5 1500, P6 1060 |
| M8 | lists: every character counted as the letter | P1 74, P2 43, P5 74, P6 74 |
| M9 | lists: the search stopped at the first character with no position left | P1 732, P2 22, P3 980, P4 1164, P5 896, P6 732 |
| M10 | string: the length not shortened on a pop | P1 473, P2 4, P5 473, P6 473 |
| M11 | string: a letter pushed only into spare room | P1 853, P2 263, P3 341, P5 853, P6 853 |
| M12 | string: the letters left never counted down | P1 237, P2 47, P5 237, P6 237 |
| M13 | scan: the largest character taken | P1 471, P2 137, P6 471 |
| M14 | scan: the window not moved past the place taken | P1 445, P3 880, P6 445 |
| M15 | scan: a letter taken counted twice | P1 118, P5 118, P6 118 |
| M16 | Rust: any popped character counted against the letters | P1 152, P6 152 |
| M17 | Rust: one copy of the letter fewer counted | P1 82, P6 82 |

P1 and P6 kill all seventeen, P2 and P5 twelve each, P3 seven and P4 one.
P2 lowers `repetition`, which frees a place the tighter demand held for a
copy of `letter`; an edit that holds the wrong places (an equal character
popped, M1; the largest taken, M13) is seen there as well as by P1. P3 asks
for the whole string, so it sees the edits that refuse a place the whole
length needs: the last place that leaves room refused (M4), a position at
the start passed over (M7), the window not moved past the place taken
(M14). P5 feeds the answer back, and an answer short of `letter` is not a
valid problem, so it sees the edits that keep too few copies (M2, M3, M8,
M12, M15 among them). P4 moves the alphabet up, which only an arm that
walks the characters in order can tell from the original: with no `a` left
in the moved string, the lists arm stopping at the first character with no
position (M9) stops before it takes anything.

The other thirteen fail as a kept one does, or with counts of their own.
An equal character popped (string), and the last of equals taken (scan)
fail as M1; the room counted one high (string, Rust) as M2; the letters
left never counted down (★) as M12; a letter counted twice (lists) as
M15. A non-letter pushed into the last free room fails alike in the ★ and
Rust arms and as the scan arm's place allowed to owe more copies than
places left; a letter taken owing as much as any character fails alike in
the table and lists arms. The table arm's one copy fewer owed and the Rust
arm's pushed letter not counted fail with counts of their own.

Several drafts were replaced. The scan arm stops with no place to take
("index out of bounds") when an earlier edit leaves it owing more copies
than are left, so a longer window and one copy too many counted ahead
were dropped, and P5 was changed to judge an answer that is not a valid
problem without asking for it, since the arms assume the guarantee. The
copies ahead counted from the position itself, in the lists and scan arms,
changed no answer on the 1500 problems and was replaced too.

## Verification

Every arm prints the same output as `subseq.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
of them. Under `karac __mir-run` the arms take 2.3 s to 4.7 s, and the
differential 5.9 s.

The string arm reads the top of its stack with `out.chars().last()`, as a
Rust programmer would. `StrChars` took `Iterator.last`'s default, which
walks every char, so each read was O(n) and the arm quadratic: its
`__mir-run` lane ran past twenty minutes on the 50000-letter problems and
its ASan lane took 200 s, where `__mir-llvm-run` took 3.5 s. That was
B-2026-11-08-81; kara 89d9feafb3 reads `last` from the back through
`next_back`, as Rust's `Chars::last` does, and the arm now takes 3.3 s under
`__mir-run`, 0.7 s under ASan and 0.3 s compiled.

The Rust arm was written as LeetCode's Rust template and reaches a clean
check through `karac fix` alone, in three rounds (14, 1 and 1 edits).
`while let Some(&top) = stack.last()` became `while let Some(top) =
stack.last().cloned()`, the fix for a pattern that copies out of a
borrowed element.

## Benchmarks

The bench builds 10 strings of 50000 letters once in all five languages,
string `a` from the first `2 + 3 a` letters of the alphabet, each letter a
step from the last, then runs 20 rounds asking each string for a
subsequence with a `k`, a letter and a repetition of the round's own: 200
calls of the ★ arm. Every implementation prints `200 calls: 4976400
letters kept, checksum 894814684`.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 0.080 to 0.112 s | 0.084 s |
| C (`clang -O3`) | 0.083 to 0.109 s | 0.090 s |
| Go | 0.089 to 0.104 s | 0.094 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.086 to 0.110 s | 0.094 s |
| Rust (`rustc -O`) | 0.089 to 0.123 s | 0.100 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.095 to 0.129 s | 0.100 s |
| Python | 2.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (0.083 s) is not above its real time (0.084 s).

The sequential Kāra program is 0.95x Rust under overflow checks and 1.05x
C.