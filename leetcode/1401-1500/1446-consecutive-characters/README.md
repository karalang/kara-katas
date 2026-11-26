# 1446. Consecutive Characters

The power of the string is the maximum length of a non-empty substring
that contains only one unique character. Given a string `s`, return the
power of `s`.

```
s = "leetcode"             ->  2
s = "abbcccddddeeeeedcba"  ->  5
```

**Constraints:** `1 <= s.length <= 500`, `s` consists of only lowercase
English letters.

Each arm is `fn max_power(s: String) -> i32`.

## Approaches

| file | mechanism |
|---|---|
| `max_power.kara` ★ | one walk over the letters, the length of the run the letter so far ends and the longest run kept as it goes. O(n) |
| `max_power_starts.kara` | the places where a run starts, collected by a `filter` over the bytes, with the end pushed after them, and the widest gap between two next to each other through `windows(2)`. O(n) |
| `max_power_brute.kara` | from every start, the run carried on while the letter holds, and the longest. O(n²) |
| `max_power_fold.kara` | one `fold` over the letters, the last letter, its run and the longest run carried as a tuple. O(n) |
| `max_power_solution.kara` | a Rust solution as LeetCode's Rust users write it (`let s = s.as_bytes()`, `ans` and `cnt` from 1, `ans = ans.max(cnt)` as each run grows), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 3 lines: LeetCode's two examples and five more
(`2 5 1 5 1 3 2`); the constraints' most, 500 a's, 500 letters a and b
by turns, and 500 drawn of two letters (`500 letters: 500 1 12`); and
2000 random strings of 1 to 60 letters of the first 1 to 26 of the
alphabet (`2000 random strings: 6371 in all, checksum 301707205`).
`max_power.py` mirrors the ★ arm, and its output is byte-identical.
Every arm gives the same output under `karac __mir-run`, `karac run`,
`karac build` and `karac __mir-llvm-run`.

The Mend loop: the starts and brute arms check clean as first written.
The ★ arm started `best` and `run` at a bare `0` and returned `best` as
the `i32` answer, which `karac check` refuses, saying `best` is an `i64`
because its literal kept the default, and `karac fix` declares them
`best: i32` and `run: i32`, 2 fixes. The fold arm seeded its fold with
`(' ', 0, 0)` and is refused the same way, and `karac fix` writes the
seed `(' ', 0i32, 0i32)`, 2 fixes. The Rust solution takes one round of
9 fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `s.as_bytes()` to `s.bytes()`, `let mut ans = 1` and `let mut cnt =
1` to `ans: i32` and `cnt: i32`, and `Solution::` to `Solution.`. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every substring, kept when it holds one letter only, and the
longest of those, while there are at most 60 letters. LeetCode's
examples, five edge cases (one letter, one run, two letters, two runs,
and a run inside), the constraints' most three ways (500 a's, 500
letters a and b by turns, and 500 drawn of two letters), and 1993 random
strings of 1 to 60 letters of the first 1 to 26 of the alphabet, a third
of them of the first 1 to 3.

P3 renames each letter to the next. Written `(b'a' + (c as u8 - b'a' +
1) % 26) as char`, it is refused, a `char` not cast to `u8` directly
since its range does not fit in 8 bits, and `karac fix` writes `c as u32
as u8`, 1 fix.

| | property |
|---|---|
| P1 | the statement read literally, while there are at most 60 letters |
| P2 | the letters in the other order give the same power |
| P3 | every letter renamed to the next, z to a, gives the same |
| P4 | every letter written twice gives twice the power |
| P5 | from 1 to the length, and the length exactly when the string is one letter only |
| P6 | the ★ arm's answer |

All 60,075 checks pass on every arm: `2003 cases: checksum 515776101,
60075 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by the longest
group of `itertools.groupby`, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a run grown by 2 a letter | P1 1693, P4 2003, P5 289, P6 6780 |
| M2 | ★: a new run counted from 0 | P1 2000, P4 2003, P5 569, P6 8012 |
| M3 | starts: a run taken to start where the letter stays the same | P1 1854, P4 2003, P5 523, P6 1857 |
| M4 | starts: the end placed one short | P1 376, P2 129, P4 377, P5 307, P6 377 |
| M5 | brute: no run carried on to the last letter | P1 376, P2 129, P4 377, P5 307, P6 377 |
| M6 | brute: every run counted one short | P1 2000, P4 2003, P5 569, P6 2003 |
| M7 | fold: a new run counted from 0 | P1 2000, P4 2003, P5 569, P6 2003 |
| M8 | fold: the last letter never carried on, so every letter starts a run | P1 1693, P4 2003, P5 261, P6 1695 |
| M9 | solution: the second letter never compared with the first | P1 318, P2 129, P4 366, P5 261, P6 320 |
| M10 | solution: a new run counted from 0 | P1 1285, P2 268, P4 1285, P6 1285 |

## Benchmarks

The bench draws 200 strings of 10^5 letters, each of the first 2 to 4
letters of the alphabet, and asks each string's power 10 times with the
★ arm, folding the powers to a checksum. Every implementation prints
`2000 strings of 10^5 letters: checksum 875223158`.

BENCHTAB

Measured by hand, Kāra takes 1.00 to 1.02 s against Rust's 0.26 s, C's
0.22 s and Go's 1.38 s; Python takes 14.5 s. With overflow checks on,
Rust takes 0.92 to 1.10 s, the same as Kāra. In Kāra's binary the loop
branches on `ch == last`, the branch holding `run += 1` and its overflow
test, and a drawn letter makes that branch hard to guess; `rustc -O`
without overflow checks picks the new run's length and the longest with
conditional moves, and has no branch to miss.
