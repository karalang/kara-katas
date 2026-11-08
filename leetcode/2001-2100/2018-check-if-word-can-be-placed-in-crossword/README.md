# 2018. Check if Word Can Be Placed In Crossword

You are given an `m x n` board of a crossword puzzle: each cell is a
lowercase letter (already filled), `' '` (empty), or `'#'` (blocked), and a
string `word`. The word can be placed horizontally, left to right or right
to left, or vertically, top to bottom or bottom to top, when it does not
occupy a `'#'` cell, each cell it occupies is `' '` or already holds the
word's letter there, the cells just left and right of a horizontal word are
not `' '` or a letter, and the cells just above and below a vertical word
are not `' '` or a letter. Return whether it can be placed.

```
board = [["#"," ","#"],[" "," ","#"],["#","c"," "]], word = "abc"  ->  true
board = [[" ","#","a"],[" ","#","c"],[" ","#","a"]], word = "ac"  ->  false
board = [["#"," ","#"],[" "," ","#"],["#"," ","c"]], word = "ca"  ->  true
```

**Constraints:** `1 <= m * n <= 2 * 10^5`; `board[i][j]` is `' '`, `'#'`
or a lowercase letter; `1 <= word.length <= max(m, n)`; `word` is
lowercase letters.

The cells beside a placed word must be walls or off the board, so a word
fits only a whole run between walls, of exactly its length, read one way or
the other.

## Approaches

| file | mechanism |
|---|---|
| `crossword.kara` ★ | every row and every column cut at its walls into runs, each copied into a `Vec`; a run fits when it is as long as the word and every cell is empty or holds the word's letter, read forwards or backwards. O(m n) |
| `crossword_brute.kara` | every start cell and every direction: the cell behind the start a wall or off the board, the word's cells open and matching, the cell past its end a wall or off the board. O(m n k) |
| `crossword_lines.kara` | the board read in all four directions, each line a `String` split at `"#"`; a piece fits when it is as long as the word and matches it by `zip`, read forwards only. O(m n) |
| `crossword_transpose.kara` | a check of the rows alone, walking each row by index and comparing a run in place, both ways, with no copy; run on the board and then on its transpose. O(m n) |
| `crossword_fold.kara` | each line read once by a `fold`, a wall chained on at its end, the state the run's length and whether it still matches forwards and backwards. O(m n) |
| `crossword_solution.kara` | LeetCode's Rust template (a unit struct, `impl Solution`, `Vec<Vec<char>>`, `for line in &lines`, `line.split(\|&ch\| ch == '#')`, `zip` with `\|(&a, &b)\|`, a `&Vec` wrapper), carried by `karac fix` to one remaining error: blocked by B-2026-11-08-47 |
| `differential.kara` | the five arms that check against the statement read literally, six properties |

Every arm prints the same 11 lines: the answers for LeetCode's three
examples and six more; then the number placed and a checksum of the answers
for 3000 boards of up to 6 by 6, with walls, letters from the first 1 to 3
and words of 1 to 5 letters drawn per board, and for 6 boards of up to
100000 cells (300 by 300, 1 by 1000, 400 by 250, 30 by 3000, 600 by 150 and
2 by 500, the last with a word of 500 letters). `crossword.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms that check and the
statement read literally: every cell and each of the four directions, the
word's cells on the board and open, each empty or holding the word's
letter, and the cells just before and just after it walls or off the board.
It checks 1500 problems of boards of 1 to 5 by 1 to 5 drawn as the
harness's small boards are. Every random choice of a problem (the board,
the word, a letter to empty) is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the board transposed leaves the answer |
| P3 | every row reversed leaves the answer |
| P4 | the word reversed leaves the answer |
| P5 | a letter on the board emptied never turns a true answer false |
| P6 | each arm agrees with at least two of the other four |

The differential prints `1500 problems: checksum 563835693, 45000 checks
over 5 arms: 0 failures` under every lane in Verification. On a failure it
prints the first ten and then the count by property. The Rust-template arm
joins it, as a sixth, once it checks.

## Mutation testing

Twenty-five edits to the differential, five to each of its arms, each run
under `karac __mir-run` and `karac __mir-llvm-run`. Fifteen are kept, three
to each arm. All twenty-five are killed, each fails the same way under both
backends, none by a crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run longer than the word accepted | P1 233, P3 15, P6 233 |
| M2 | ★: the word read forwards only | P1 22, P3 22, P4 47, P6 22 |
| M3 | ★: a blank cell not matching forwards | P1 24, P3 23, P4 46, P6 24 |
| M4 | brute: the cell behind the start never checked | P1 240, P4 12, P6 240 |
| M5 | brute: the cell past the end never checked | P1 238, P4 12, P6 238 |
| M6 | brute: the last letter never checked | P1 345, P4 31, P6 345 |
| M7 | lines: the reversed rows left out | P1 7, P2 21, P3 21, P4 21, P6 7 |
| M8 | lines: the reversed columns left out | P1 14, P2 21, P4 24, P6 14 |
| M9 | lines: a blank matching only the letter `a` | P1 274, P5 33, P6 274 |
| M10 | transpose: the transpose never checked | P1 216, P2 414, P6 216 |
| M11 | transpose: the run's start not moved past the wall | P1 83, P3 91, P6 83 |
| M12 | transpose: a blank cell spoiling both readings | P1 558, P5 61, P6 558 |
| M13 | fold: a mismatch carried past the wall | P1 7, P3 9, P6 7 |
| M14 | fold: the wall left off the line's end | P1 399, P3 98, P6 399 |
| M15 | fold: a run that fit forgotten at the next wall | P1 75, P3 83, P6 75 |

P1 and P6 kill all fifteen, P3 eight, P4 seven, P2 three and P5 two. P3
reverses every row, which turns a word read left to right into one read
right to left and moves each run to the other end of its row, so it sees
the edits that treat the two ends of a run or of a line unevenly: a longer
run read from its first cell (M1), one reading of the word lost or spoiled
(M2, M3, M7), a run's start or its last run mishandled (M11, M14), and a
fold whose state leaks from one run to the next or is lost there (M13,
M15). P4 reverses the word, which swaps the forwards reading with the
backwards one, so it sees the same uneven readings (M2, M3, M7, M8) and the
brute arm's edits, which check one end of a placement and not the other
(M4, M5) or its letters but the last (M6). P2 transposes the board, which
swaps the rows and the columns; it sees only the edits that drop a whole
class of lines: the reversed rows or columns (M7, M8) and the transpose
(M10). It misses every edit that treats rows and columns alike, which is
all the others. P5 empties one letter on the board, which can only help a
word that fits, so it sees only the edits under which a blank matches less
than a letter does: a blank that matches only `a` (M9), and a blank that
spoils both readings (M12).

The other ten fail as a kept one does, or with counts of their own. The
word read forwards only fails alike four ways: M2, the brute arm trying
only right and down, the transpose arm's backward check reading the word
forwards, and the fold arm's backward check reading from the front. The
★ arm never reading the columns fails as M10; the lines arm accepting a
piece longer than the word as M5. The ★ arm's run never cleared at a wall,
the brute arm letting a filled cell take any letter, the lines arm
splitting at blanks too, the transpose arm reading only its first row and
the fold arm never reading the rows fail with counts of their own. Two
drafts were replaced. The ★ arm never trying a line's last run (`i <
line.len() and line[i] == '#'`) pushes the cell past the end and stops on
an index out of bounds, a crash; and the fold arm keeping a run that is
already longer than the word matching never fails, since a run that long
is turned down at its wall by its length alone.

## Verification

Every arm but the Rust template prints the same output as `crossword.py`
under `karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`,
and `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports nothing
on any of them. Under `karac __mir-run` the arms take 0.87 s (transpose) to
3.9 s (lines) and the differential 6.5 s.

The five arms were written in Kāra. Four checked clean with no fix. The
fold arm's `line.iter().chain(['#'].into_iter())` joins an iterator of
`ref char` to one of `char`, which `chain`'s bound refuses; the message
named `.cloned()` but offered no edit. Since kara 83dda78246 `karac fix`
appends `.cloned()` to the side that yields `ref T`, here the receiver.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in one round of 24 edits (the `Vec<..>` types, the `&` patterns in the
closures and on `&lines`, `||` to `or`, the `&Vec` and `&String`
parameters, the `::` path, and `struct Solution;`) to one error it has no
fix for: `line.split(|ch| ch == '#')`, Rust's split of a slice at the
elements a predicate picks, is "no method 'split' on type 'Vec'". Kāra's
sequences have `windows`, `chunks` and `split_at`, and `Str` has
`split(sep)`, but nothing splits a `Vec` by a predicate, and the refusal
names no other spelling (B-2026-11-08-47). It also draws two cascade
errors, "tuple pattern used but type is `?T5`", on the `zip` closures that
read the unknown pieces. With the split written by hand as a loop that
starts a new piece at each wall, the arm checks clean and prints the
mirror's output.

## Benchmarks

The bench builds 120 boards of 200 by 200 once in all five languages, with
walls at odds 1 or 2 in 10, letters from the first three at odds 4 in 10
and words of 10 to 19 letters, and runs the ★ arm on each for 40 rounds:
4800 calls, each reading up to 80000 cells. Every implementation prints
`4800 calls: 3800 placed, checksum 690068152`. Every language copies each
line and each run into its own growable array per call, as the Kāra program
does.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `64bba595f2` on LLVM 22:

| | time | median |
|---|---|---|
| Kāra (`karac build`) | 1.079 to 1.199 s | 1.109 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.079 to 1.187 s | 1.118 s |
| C (`clang -O3`) | 1.285 to 1.356 s | 1.306 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.310 to 1.412 s | 1.364 s |
| Rust (`rustc -O`) | 1.367 to 1.546 s | 1.421 s |
| Go | 1.767 to 1.916 s | 1.827 s |
| Python | 22.5 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`, the
sequential lane. A plain `karac build` parallelizes nothing here: its user
time (1.089 s) is not above its real time (1.109 s).

The sequential Kāra program is 0.82x Rust under overflow checks and 0.86x
C.