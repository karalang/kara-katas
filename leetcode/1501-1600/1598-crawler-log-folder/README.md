# 1598. Crawler Log Folder

The Leetcode file system keeps a log each time some user performs a
change folder operation. The operations are described below:

- `"../"`: Move to the parent folder of the current folder. (If you are
  already in the main folder, remain in the same folder.)
- `"./"`: Remain in the same folder.
- `"x/"`: Move to the child folder named `x` (this folder is guaranteed
  to always exist).

You are given a list of strings `logs` where `logs[i]` is the operation
performed by the user at the `i`th step.

The file system starts in the main folder, then the operations in `logs`
are performed. Return the minimum number of operations needed to go back
to the main folder after the change folder operations.

```
logs = ["d1/","d2/","../","d21/","./"]         ->  2
logs = ["d1/","d2/","./","d3/","../","d31/"]   ->  3
logs = ["d1/","../","../","../"]               ->  0
```

**Constraints:** `1 <= logs.length <= 10^3`; `2 <= logs[i].length <= 10`;
`logs[i]` holds lowercase English letters, digits, `.` and `/`; `logs[i]`
follows the format described in the statement; folder names are
lowercase English letters and digits.

## Approaches

| file | mechanism |
|---|---|
| `crawler.kara` ★ | only the depth matters: a `match` on `log.as_str()`, one deeper for a move, one shallower for `../` but never below zero, and the depth at the end. O(n) |
| `crawler_stack.kara` | the path kept: the folders entered on a `Vec[Str]` used as a stack, each a slice of its log by `strip_suffix`; `../` pops, and the answer is how many are left. O(n) |
| `crawler_fold.kara` | one `fold` over the logs carrying the depth, the three cases an `if` chain in the closure. O(n) |
| `crawler_solution.kara` | LeetCode's Rust template (a `for log in logs` loop matching `log.as_str()`, an `i32` depth kept from going below zero by an `if`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and three
more (`./` alone, `../` from the main folder, a thousand moves), then the
total and a checksum for 3000 random logs of up to 8 operations, 300 of
up to 100 and 30 of up to 1000, a quarter `../`, a quarter `./` and half
a move into one of five folders. `crawler.py` mirrors the ★ arm and its
output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the folder the file system is in, as the list of folders from
the main one, changed by each operation as the statement says, and then
the fewest `../` after them that bring it back to the main folder, found
by trying 0, 1, 2, ... of them. It checks 3000 logs of 1 to 10
operations, every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | a `./` put in anywhere leaves the answer |
| P3 | a move into a folder and a `../` added at the end leave the answer |
| P4 | the folders renamed leave the answer |
| P5 | a `../` put before every log leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 315584619, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `../` may go above the main folder | P1 1163, P5 3000, P6 1163 |
| M2 | ★: `./` taken as a move | P1 1960, P2 2697, P6 1960 |
| M3 | ★: `../` stops at depth 1 | P1 1616, P3 86, P5 1384, P6 1616 |
| M4 | stack: `../` goes back to the main folder | P1 820, P3 1952, P6 820 |
| M5 | stack: `./` pushed as a folder | P1 1960, P2 2697, P6 1960 |
| M6 | fold: `../` may go above the main folder | P1 1163, P5 3000, P6 1163 |
| M7 | fold: a move goes two deeper | P1 2650, P3 3000, P6 2650 |
| M8 | template: `../` at the main folder goes above it | P1 1163, P5 1837, P6 1163 |
| M9 | template: a move goes to depth 1 | P1 1709, P3 1952, P6 1709 |
| M10 | stack: the answer capped at 3 | P1 523, P6 523 |

## Benchmarks

The bench draws 2000 logs of 5000 operations first, each log its own
`String`, then answers each by the ★ arm, in all five languages. Every
implementation prints `2000 logs of 5000 operations: total 2501734,
checksum 154971987`. The C mirror `strdup`s every log, as Kāra makes
each one a `String`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5dc4418bbd` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.569 s |
| Kāra (`karac build`) | 0.585 s |
| Go | 0.770 s |
| C (`clang -O3`) | 0.923 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.981 s |
| Rust (`rustc -O`) | 1.018 s |
| Python | 4.5 s |

Nearly all of every program's time is making the ten million strings;
the answer is one pass of comparisons. Kāra's lead over C and Rust is in
that part and was not traced further. It is not C's final `free` loop:
the C program without it took about as long.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.407 s and 0.582 s on one run).

## Verification

All four arms print the same output as `crawler.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5dc4418bbd`.

## Writing it

The ★ arm wrote `let mut depth = 0` and `depth = (depth - 1).max(0)`, and
`karac fix` typed it `depth: i32`, as a method does not fix a literal's
type. The shared harness wrote `"../".to_string()` in a closure building
a `Vec[String]`, and `karac fix` dropped the `to_string()`. The
differential's literal reading had the same `let mut k = 0` returned as
`i32`, and `karac fix` typed it.

The stack arm first wrote `log.trim_end_matches("/")`; `karac check`
said Kāra strips a suffix with `strip_suffix`, which returns an
`Option[Str]`, and it was rewritten by hand as
`log.strip_suffix("/").unwrap()`.

The fold arm was first written as a `map` of each log to a step of -1, 0
or 1 and a `fold(0, |depth, step| (depth + step).max(0))`. It is refused
on the whole chain with advice to write a truncating `as i32` and no
fix, though the same literal in a `let` is named and typed by `karac
fix` (B-2026-11-17-129). The arm was rewritten by hand as the one `fold`
over the logs it is now.

The Rust template took one `karac fix`, of 6 edits: `struct Solution;`
to `struct Solution {}`, `Vec<String>` to `Vec[String]`, and
`Solution::` to `Solution.`. It then checks and agrees with no hand edit.
