# 1041. Robot Bounded In Circle

On an infinite plane, a robot initially stands at `(0, 0)` and faces
north. Note that:

- The **north direction** is the positive direction of the y-axis.
- The **south direction** is the negative direction of the y-axis.
- The **east direction** is the positive direction of the x-axis.
- The **west direction** is the negative direction of the x-axis.

The robot can receive one of three instructions:

- `"G"`: go straight 1 unit.
- `"L"`: turn 90 degrees to the left (i.e., anti-clockwise direction).
- `"R"`: turn 90 degrees to the right (i.e., clockwise direction).

The robot performs the `instructions` given in order, and repeats them
forever.

Return `true` if and only if there exists a circle in the plane such
that the robot never leaves the circle.

```
instructions = "GGLLGG"  ->  true
instructions = "GG"      ->  false
instructions = "GL"      ->  true
```

**Constraints:** `1 <= instructions.length <= 100`; `instructions[i]`
is `'G'`, `'L'` or `'R'`.

## Approaches

Every arm rests on one fact. After a pass of the instructions the robot
has moved by some offset and turned by some multiple of a quarter turn.
If it faces north again, every pass adds the same offset, so it stays
near the origin only if that offset is zero. If it faces any other way,
the offsets of four passes (two, for a half turn) cancel, so its path
repeats and stays inside a circle.

| file | mechanism |
|---|---|
| `robot_bounded.kara` ★ | one pass: the position and a heading from 0 to 3 kept as integers, `if` chains for the step; bounded when the robot is home or does not face north. O(n) |
| `robot_bounded_four.kara` | four passes: four times one pass's turn is a whole number of turns, so after four passes the robot faces north and is bounded exactly when it is home. The steps come from an `Array` of four `(dx, dy)` pairs. O(n) |
| `robot_bounded_rotate.kara` | the heading as a vector: `L` rotates `(dx, dy)` to `(-dy, dx)` and `R` to `(dy, -dx)`, each a multi-assign in a `match` arm. O(n) |
| `robot_bounded_enum.kara` | the heading as an enum: `Heading` knows its turns and its step, and a `Robot` struct obeys one instruction at a time through a `mut ref self` method. O(n) |
| `robot_bounded_fold.kara` | one `fold` over the characters with `(x, y, facing)` as the state, each step written arithmetically from the heading. O(n) |
| `differential.kara` | the five arms against the robot walked step by step, five properties |

Every arm prints the same 21 lines: the answers for ten strings,
LeetCode's three examples among them, with a lone `L`, `R` and `G`, a
square walked back to its start (facing west, then north) and two that
end facing north away from it; for every
string of 1 to 8 instructions (3^n of each length), the number that are
bounded and a checksum; the same for 500 random strings of 1 to 100
instructions, half drawn evenly and half mostly `G`; and the two
longest, 100 `G` (`false`) and `GL` 50 times (`true`).
`robot_bounded.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: it walks the robot step by step and asks whether it
stays within `4n` of the origin, in both coordinates, over `4(4n + 1)`
passes of `n` instructions. A bounded robot repeats its path every four
passes, none of which takes it more than `4n` steps out. An unbounded
one is moved by the same nonzero whole offset every four passes, so
after `4(4n + 1)` passes it is more than `4n` out in one coordinate. It
checks 3879 strings: every string of 1 to 7 instructions (3279), 400
random ones of 8 to 20 and 200 of 21 to 100. The 3679 of at most 20
instructions are walked.

| | property |
|---|---|
| P1 | the robot walked step by step, on at most 20 instructions |
| P2 | the same loop started at another instruction (the string turned by a random number of places) changes nothing |
| P3 | `L` and `R` swapped, the mirror image of the path, changes nothing |
| P4 | the string repeated 2 to 4 times changes nothing |
| P5 | a turn that undoes itself (`LR`, `RL`, `LLLL` or `RRRR`) put in anywhere changes nothing |
| P6 | each arm agrees with at least two of the other four |

The differential prints `3879 strings (3679 walked): checksum 90584348,
115370 checks over 5 arms: 0 failures` under `karac __mir-run` (12.6 s),
`karac __mir-llvm-run` and `karac __mir-llvm-asan` with no error, and
the same line under `karac run` and from a `karac build` binary. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with a 120 s limit.
Fifteen are kept, three to each arm. All fifteen are killed, each fails
the same way under both backends, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: `L` turns right | P1 877, P5 878, P6 934 |
| M2 | ★: a step west taken east | P1 6, P2 5, P4 944, P6 6 |
| M3 | ★: `R` turns around | P1 1403, P3 1365, P5 798, P6 1477 |
| M4 | four: two passes | P1 1519, P2 134, P4 1062, P6 1604 |
| M5 | four: `L` taken modulo 3 | P1 2100, P2 318, P3 1282, P4 60, P5 577, P6 2246 |
| M6 | four: east and south swapped in the table | P1 841, P2 39, P3 76, P6 893 |
| M7 | rotate: `L` a reflection, `(dy, dx)` | P1 877, P2 448, P3 858, P4 537, P5 415, P6 931 |
| M8 | rotate: `L` one coordinate at a time, `dx = -dy; dy = dx;` | P1 837, P3 107, P5 39, P6 891 |
| M9 | rotate: `y` moved by `dx` | P1 363, P2 255, P6 364 |
| M10 | enum: left from west is north | P1 667, P2 353, P3 936, P4 739, P5 127, P6 725 |
| M11 | enum: right from south is east | P1 479, P2 536, P3 803, P4 438, P5 257, P6 536 |
| M12 | enum: `and` for `or` | P1 2411, P2 170, P4 146, P6 2554 |
| M13 | fold: a step south taken north | P1 9, P2 5, P4 1052, P6 9 |
| M14 | fold: `L` taken modulo 2 | P1 868, P2 754, P3 1488, P4 613, P5 177, P6 916 |
| M15 | fold: north and east taken as vertical | P1 168, P2 203, P3 212, P4 1170, P6 168 |

P1 and P6 kill all fifteen, P2 twelve, P4 ten, P3 nine and P5 eight. M2
and M13 break only the steps taken facing one way, and a pass that ends
facing north with those steps out of balance is rare among short
strings: P1 sees 6 and 9. P4 sees about a thousand of each. A pass that
ends facing south, repeated twice, walks back to the start facing north,
which is where a lopsided step shows. P3 misses six (M1, M2, M4, M9,
M12, M13): for each, the mirrored string comes out exactly as wrong as
the original. Under M1, for instance, every turn is a right turn in
both. P5 sees the edits that break a turn (M1, M3, M5, M7, M8, M10, M11,
M14), since only a turn can fail to undo itself. M8 is the classic
sequential-swap slip: `dy = dx` reads the `dx` just written, so a left
turn from north gives `(-1, -1)`.

Fifteen other edits were set aside. One is equivalent: the fold arm's
east and west swapped, which reflects the whole path across the y-axis
and leaves the answer alone. The other fourteen were killed too, beyond
three per arm. Eight fail exactly as a kept one does: the ★ arm
counting only a half turn (as M4) or checking only `x` (as M9) or taking
a step south north (as M13); the rotate arm's `R` turning left (as M1);
the enum arm's `L` turning right (as M1) or its south step going north
(as M13); and the rotate and fold arms starting east, which fail alike.
Six fail in ways of their own: the four arm's west step drifting north,
`or` for `and` in its home test, and one pass for four; the rotate arm
comparing with east as the start; the enum arm taking south as the
start; and the fold arm's `==` for `!=`.

## Verification

Every arm prints the same output as `robot_bounded.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and
under `karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with
no error. `karac run` and a `karac build` binary print the same output
for every arm and the differential. `karac check --output=json` reports
nothing on any file. The runs used a release build of kara `8876b6f720`;
the checks and fixes below used a build with the three fixes, which
landed at `1a547cb615`. Under `karac __mir-run` the arms take 0.52 s (★)
to 0.60 s (enum, rotate, fold) and 1.0 s (four, which walks the string
four times).

Writing the arms through the Mend loop turned up three gaps in `karac
check` and `karac fix`, fixed in kara (B-2026-11-03-21, B-2026-11-03-22
and B-2026-11-03-23):

- `s.push(t.char_at(i))`, with `char_at` giving an `Option[char]`, said
  only "'push' expects a Char argument, found 'Option[char]'". A
  mismatch whose found
  type wraps the expected one now says to unwrap it, at a `let`, an
  argument, `push` and the branches of an `if` or `match`.
- `'L' => (dx, dy) = (-dy, dx),` drew a fix that drops the parentheses,
  `'L' => dx, dy = -dy, dx,`, which does not parse in a braceless arm,
  so `karac fix` refused to write the file. The fix now braces it,
  `'L' => { dx, dy = -dy, dx; }`.
- `let undo = vec!["LR", "RL", "LLLL", "RRRR"][k];` drew the borrow fix
  `ref vec![..][k]`, and the temporary drops at the end of the `let`, so
  the result was an E0516 with no fix. An element of a temporary now
  takes the `.clone()` fix.

## Benchmarks

The bench builds 2000 strings of 100 instructions (the problem's most)
once in all five languages, half drawn evenly from `G`, `L` and `R` and
half mostly `G`. Then it solves every string 500 times with the ★ arm,
one pass over the characters, counting the bounded ones and folding
each answer into a checksum. Every implementation prints `2000 strings
of 100 instructions, 500 rounds: 743000 bounded, checksum 349069671`.
Doubling the rounds doubles C's time (0.98 s against 0.49 s), so no
compiler hoists the solving out of the round loop.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.486 to 0.511 s | 0.499 s |
| Rust (`rustc -O`) | 0.507 to 0.576 s | 0.535 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.508 to 0.608 s | 0.542 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.536 to 0.632 s | 0.569 s |
| Kāra (`karac build`) | 0.552 to 0.629 s | 0.575 s |
| Go | 0.638 to 0.667 s | 0.649 s |
| Python | 8.0 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here
(0.56 s real, 0.54 s user on one run) and runs as fast as the
sequential one.

Kāra took 1.05 times Rust's median time under overflow checks. Rust,
Go and Kāra walk the string as `char`s, decoding UTF-8; C reads bytes
(inferred from the sources, not profiled).
