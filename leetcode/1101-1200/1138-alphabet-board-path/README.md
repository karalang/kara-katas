# 1138. Alphabet Board Path

On an alphabet board, we start at position `(0, 0)`, corresponding to
character `board[0][0]`.

Here, `board = ["abcde", "fghij", "klmno", "pqrst", "uvwxy", "z"]`.

We may make the following moves:

- `'U'` moves our position up one row, if the position exists on the board;
- `'D'` moves our position down one row, if the position exists on the board;
- `'L'` moves our position left one column, if the position exists on the board;
- `'R'` moves our position right one column, if the position exists on the board;
- `'!'` adds the character `board[r][c]` at our current position `(r, c)`
  to the answer.

(Here, the only positions that exist on the board are positions with
letters on them.)

Return a sequence of moves that makes our answer equal to `target` in the
minimum number of moves. You may return any path that does so.

```
target = "leet"  ->  "DDR!UURRR!!DDD!"
target = "code"  ->  "RR!DDRR!UUL!R!"
```

**Constraints:** `1 <= target.length <= 100`; `target` consists only of
English lowercase letters.

The arms are `fn alphabet_board_path(target: String) -> String`.

## Approaches

The only trap is the lone `z` at the start of the last row: a path to it
must reach column 0 before stepping down onto it, and a path from it must
climb out of the last row before stepping right. Any order of moves that
does both is a shortest path, so the arms answer differently and are
compared on what their paths type and how long they are, not on the
moves themselves.

| file | mechanism |
|---|---|
| `alphabet_board_path.kara` ★ | coordinates: letter `c` sits at row `(c - 'a') / 5` and column `(c - 'a') % 5`, so the moves between two letters are the differences of their rows and columns, written up, left, down, right with `"U".repeat(..)` and `push_str`. O(answer) |
| `alphabet_board_path_bfs.kara` | breadth-first search over the board's 26 cells from each letter to the next, the path read back through the move that first reached each cell. O(target.len() * 26) |
| `alphabet_board_path_find.kara` | each letter looked up on the board as LeetCode draws it, six rows of text, and the moves written left, up, right, down. O(answer + target.len() * 26) |
| `alphabet_board_path_step.kara` | one move at a time: up while the letter is above, then left or right to its column, then down. O(answer) |
| `alphabet_board_path_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `target.bytes()`, `(b - b'a') as i32`, a tuple of `i32` coordinates walked one `while` loop per direction), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five properties |

Every arm prints the same 20 lines. For LeetCode's two examples and
thirteen more (the corners, `z` alone, twice, and on either side of
other letters, and the whole alphabet both ways), each line gives the
answer's length, whether walking it on the board from `a` types the
target, and its form: each letter's moves put in the order U, L, D, R,
then the `!`. Every shortest path between two cells makes the same
moves in some order, so two shortest answers have the same form, and
the ★ arm's answers are their own form. Then over 2000 random targets
of 1 to 100 letters, the lengths summed, how many fail to type their
target, and a checksum over every form (`2000 random targets: lengths
total 437268, 0 wrong, checksum 869572194`), and four of LeetCode's
longest, 100 letters: `z` 100 times (length 105), and `az`, `ez` and
`ya` 50 times each (595, 995 and 900). `alphabet_board_path.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the fewest moves that, starting at `a`, type the target, by
breadth-first search over every place on the board paired with how many
letters are typed so far. A move is U, D, L or R onto a cell of the
board, or `!` where the cell's letter is the next one to type. It checks
2000 targets of 1 to 10 letters in four kinds of 500: any letters;
letters from the corners and the cells around `z` (`a`, `e`, `u`, `v`,
`y`, `z`, `t`); `z` half the time; and runs of 1 to 3 of one letter.
Every random choice, the prefix length for P4 among them, is drawn
before any arm answers. 880 of the 2000 hold a `z`.

| | property |
|---|---|
| P1 | walking the answer on the board types the target, never leaving the board, in the literal fewest moves |
| P2 | each letter of the target doubled is typed, in one `!` more per letter |
| P3 | an `a` put first is typed, in one move more |
| P4 | a prefix of the target takes as many moves as the answer up to that prefix's last `!` |
| P5 | no letter's moves go both up and down, or both left and right |
| P6 | between two `a`s, the target and the target backwards are both typed, in as many moves |

All 60,000 checks pass on every arm: `2000 targets: checksum 790400288,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
targets, by the same search over (cell, letters typed), gives the same
checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. Twenty-seven are caught; three are
equivalent, each a change to the order moves are made in that keeps
every path on the board: the search arm trying its four moves in the
other order, the step arm moving left before up (left is never needed
from the `z` row, whose only cell is in column 0), and the search arm
never marking its start as reached (the start is reached again from a
neighbour, which changes only the start's own way back, and no path is
read back through the start). Fifteen are kept, no two failing the same
checks; one of them stops the run.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a step left and back for every letter | P1 2000, P2 2000, P3 2000, P5 2000, P6 2000 |
| M2 | ★: `z` taken for `y` | P1 880, P2 880, P3 880, P6 880 |
| M3 | ★: the first letter skipped | P1 2000, P2 2000, P3 2000, P4 2000, P6 2000 |
| M4 | bfs: the last row as long as the others | stops: index out of bounds |
| M5 | bfs: every search from `a` | P1 1765, P2 1992, P3 1765, P6 1992 |
| M6 | bfs: a sixth column | P1 889, P2 889, P3 889, P6 1300 |
| M7 | find: the first letter up to it in every row | P1 1910, P2 1992, P3 1839, P5 1617, P6 1839 |
| M8 | find: left by the column distance either way | P1 1839, P2 1839, P3 1839, P5 1839, P6 1839 |
| M9 | find: never down to the last row | P1 537, P2 537, P3 537, P6 734 |
| M10 | step: up written down | P1 1457, P2 1457, P3 1457, P6 1942 |
| M11 | step: a step back and forth with every left | P1 1427, P5 1427 |
| M12 | step: column 4 taken for column 0 | P1 1180, P2 1180, P3 1180, P6 1180 |
| M13 | solution: left after down | P1 547, P2 547, P3 547, P6 714 |
| M14 | solution: row and column swapped | P1 1946, P2 1946, P3 1946, P6 1946 |
| M15 | solution: one step down short | P1 1942, P2 1942, P3 1942, P6 1942 |

P1 catches all fourteen edits that let the run finish; P2, P3 and P6
thirteen each, P5 four, and P4 one. P2, P3 and P6 each walk the answer
to a related target, so they see every edit that types a wrong letter
or leaves the board, and P6, whose targets end at `a` and run the letters
both ways, sees more of the edits that go wrong only on the way to or
from `z` (M6, M9, M13) or only going up (M10). The one edit those three
miss is a step left and back with every move left (M11): its paths type
the right letters, and doubling a letter, putting an `a` first, or
reversing the target between `a`s adds or removes no move left, so
lengths keep their relations; P5 sees its back and forth, and P1 its
length. P5 sees the other three edits that move both ways along a row
(M1, M7, M8). P4 compares the moves up to a prefix's last `!` with the
prefix's own answer, which only an edit that answers a prefix and the
whole target inconsistently can fail: the first letter skipped (M3) does,
since the prefix's last `!` comes one letter late. The edit that stops
the run lets the search step onto cells past `z`, and reads past the end
of its 26-cell tables.

Of the twelve caught and not kept, five fail exactly as a kept one: down
before left in the ★ arm as M13; `z` taken for `y` in the step and
solution arms as M2; `?` for `!` in the solution arm as M3; and up
written down in the solution arm as M10. The other seven each fail in a
way of their own and were not needed: the row never moving on from the
first (the ★ and find arms), down and right first (the ★ arm), the path
read back to front (bfs), right and down first and the rows counted from
the bottom (find), and right before up (step).

## Verification

Every arm prints the same output as `alphabet_board_path.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, bfs, find and step arms were written as Kāra and checked clean
as written, once the harness's `"spells it".to_string()` was written
`"spells it"`, as `karac fix` rewrites it (a string literal is already
a `String`; `karac check` leaves that style lint off and `karac fix`
turns it on). `karac fix` carried the solution arm in two rounds:
`String::new` and `Solution::alphabet_board_path` to `.`, and `let (mut
x, mut y)` to `let mut (x, y)`; then `struct Solution {}` declared.
`b'a'`, `(b - b'a') as i32` and the `i32` coordinates are Kāra as they
stand. In the differential, `karac fix` turned `flat_map(|c| [c, c])`
into `flat_map(|c| [c, c].into_iter())`: Kāra's `flat_map` takes a
closure that returns an iterator, as its signature in
`docs/library/iterators.md` says, where Rust's takes anything that
iterates.

The kata found one gap, in its bench rather than its arms:

- **B-2026-11-12-15** (open): a one-byte `repeat` is a call into the
  runtime, an allocation through a wrapper, and a `memcpy` for each
  doubling, where Rust's is inlined; see Benchmarks.

## Benchmarks

The bench builds 1000 targets of 100 letters once, LeetCode's longest.
Each of 100 rounds draws one letter of every target again and answers
it with the ★ arm: 100,000 calls, each writing its moves with four
`repeat`s and a `push` per letter. Every implementation prints `100
rounds over 1000 targets of 100 letters: lengths total 43385746, checksum
879524265`. Kāra and Rust build each run of moves as its own string
(`"U".repeat(n)`) and append it; C writes the runs into the answer's
buffer in place, Go with `strings.Repeat` into a `strings.Builder`.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `87bec305bc`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.186 to 0.222 s | 0.200 s |
| C (`clang -O3`) | 0.192 to 0.238 s | 0.210 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.534 to 0.792 s | 0.575 s |
| Rust (`rustc -O`) | 0.525 to 0.722 s | 0.589 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.547 to 0.807 s | 0.615 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.740 to 1.019 s | 0.809 s |
| Kāra (`karac build`) | 0.736 to 0.965 s | 0.819 s |
| Go | 0.890 to 1.062 s | 0.948 s |
| Python | 3.800 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Most of each call is up to 400 short strings made, copied
in and freed. C, which makes none, takes about 0.25x to 0.26x Kāra's
median time.
Rust makes the same allocations and takes about 0.71x to 0.76x: under
callgrind both spend the same in `malloc` and `free`, but Kāra calls
into the runtime for every `repeat`, wraps its allocation, and copies a
run of four in three `memcpy` calls, 7.0G instructions to Rust's 4.6G
(B-2026-11-12-15). Go takes about 1.17x Kāra's time and Python about
4.7x.
