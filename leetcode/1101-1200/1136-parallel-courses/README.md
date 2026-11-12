# 1136. Parallel Courses

You are given an integer `n`, the number of courses, labeled from `1` to
`n`, and an array `relations` where `relations[i] = [prevCourse_i,
nextCourse_i]` means course `prevCourse_i` has to be taken before course
`nextCourse_i`.

In one semester you can take any number of courses as long as you have
taken all the prerequisites in the previous semester for the courses you
are taking.

Return the minimum number of semesters needed to take all courses. If
there is no way to take all the courses, return `-1`.

```
n = 3, relations = [[1,3],[2,3]]        ->  2
n = 3, relations = [[1,2],[2,3],[3,1]]  ->  -1
```

**Constraints:** `1 <= n <= 5000`; `1 <= relations.length <= 5000`;
`relations[i].length == 2`; `1 <= prevCourse_i, nextCourse_i <= n`;
`prevCourse_i != nextCourse_i`; all the pairs are unique.

The arms are `fn minimum_semesters(n: i64, relations: Vec[Vec[i64]]) -> i64`.

## Approaches

The answer is the number of courses on the longest chain of
prerequisites, or -1 when the relations close a cycle.

| file | mechanism |
|---|---|
| `minimum_semesters.kara` ★ | Kahn's algorithm a semester at a time: the courses with no prerequisite left are this semester's, taking them lowers the counts of the courses after them, and those that reach 0 are next semester's. A course never taken means a cycle. O(n + m) |
| `minimum_semesters_memo.kara` | depth-first search: a course needs one semester more than the most any course after it needs, remembered once found; a course met again while its own search is open closes a cycle. O(n + m) |
| `minimum_semesters_order.kara` | a topological order by an explicit stack, each course placed once every course after it is, then the longest chain read over that order: a course's semester is one more than the latest of its prerequisites'. O(n + m) |
| `minimum_semesters_sinks.kara` | Kahn's algorithm run backwards: the courses no other course needs are the last semester's, removing them frees the courses before them, and the semesters are counted from the end. O(n + m) |
| `minimum_semesters_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, `relations: Vec<Vec<i32>>`, `vec![vec![]; n + 1]` and `vec![0; n + 1]` indexed through `as usize`, a `VecDeque` emptied a level at a time with `for _ in 0..queue.len()`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 12 lines: the answers for LeetCode's two
examples and six more (one course and no relation, a chain, a ring, four
courses before one, a diamond with a tail, and a cycle beside a pair),
then over 2000 random plans of 2 to 12 courses and 1 to 15 relations,
every other one without a cycle, the semesters summed, how many have a
cycle, and a checksum (`2000 random plans: semesters total 4842, 446 with
a cycle, checksum 877490300`), and three of LeetCode's largest: 5000
courses in one chain (`5000`), 5000 courses and 5000 random relations
without a cycle (`10`), and the chain closed into a ring (`-1`).
`minimum_semesters.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the fewest semesters `k` for which some plan gives every
course a semester from 1 to `k` and takes each relation's first course
in an earlier semester than its second, every plan for each `k` tried,
or -1. No plan needs more semesters than there are courses, since a
semester with no course can be dropped, so `k` stops at `n`. It checks
2000 problems of 2 to 6 courses in five kinds of 400: 1 to 8 relations
between any two courses; 1 to 8 relations along a drawn order, so no
cycle; a chain through a drawn order and up to 2 relations more along
it; relations along a drawn order and one against it; and courses in 2
to `n` layers, each course after the first layer needing one course of
the layer before. Every random choice, the renaming for P3 among them,
is drawn before any arm answers. 509 of the 2000 have a cycle.

| | property |
|---|---|
| P1 | the answer is the literal one |
| P2 | the relations listed in reverse give the same answer |
| P3 | the courses renamed by a drawn order give the same answer |
| P4 | every relation turned around gives the same answer |
| P5 | a new course before every course takes one semester more, and -1 stays -1 |
| P6 | a new course with no relation changes nothing |

All 60,000 checks pass on every arm: `2000 problems: checksum 29914207,
60000 checks over 5 arms: 0 failures`. A Python reading of the same
problems, every plan tried with `itertools.product`, gives the same
checksum.

## Mutation testing

Thirty edits to the differential, six to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`,
each failing the same way under both. All thirty are caught. Three edits
first tried were replaced. One course too few taken accepted, in the ★
and the sinks arms, is an equivalent edit: a cycle holds at least two
courses, so a plan with a cycle never leaves exactly one course untaken.
Both became two courses left untaken accepted. A course taken one
prerequisite early in the ★ arm hung both backends, the counts of a
cycle's courses falling below 0 and staying there; it was replaced by
only a semester's first course freeing the courses after it. Fifteen are
kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: two courses left untaken accepted | P1 250, P4 163, P6 113 |
| M2 | ★: a course's prerequisites counted as one | P1 662, P4 432, P5 2000 |
| M3 | ★: the last course never starts | P1 617, P3 638, P4 974, P5 874, P6 874 |
| M4 | memo: a course remembered one semester short | P1 954, P2 176, P3 837, P4 1110, P5 1491 |
| M5 | memo: the last course after it counts, not the most | P1 342, P2 427, P4 206, P5 974 |
| M6 | memo: the last course's chain taken | P1 1031, P3 905, P4 1204, P5 1031, P6 850 |
| M7 | order: a course met on the stack passed over | P1 509, P2 6, P3 81, P4 143 |
| M8 | order: the order read backwards | P1 1491, P5 1491 |
| M9 | order: the last prerequisite sets a semester, not the latest | P1 27, P3 39, P4 55 |
| M10 | sinks: each course's prerequisites read as its followers | P1 1491 |
| M11 | sinks: a semester counted as one course removed | P1 685, P6 806 |
| M12 | sinks: course 1 never among the last | P1 643, P3 631, P4 971 |
| M13 | solution: one course a semester | P1 685, P6 1491 |
| M14 | solution: the queue emptied from the back | P1 190, P2 24, P3 148, P4 121 |
| M15 | solution: a cycle answered with the semesters so far | P1 509, P4 224, P6 255 |

P1 catches all fifteen, P4 eleven, P3 seven, P5 and P6 six each, and P2
four. P4 turns every relation around, which keeps the longest chain and
every cycle, so it sees nearly every edit that is wrong only in one
direction: a course left out at one end (M3, M12), a count kept per
prerequisite or per follower (M1, M2), a chain read by its last link
rather than its longest (M5, M6, M9), and a search or queue order that
only some plans survive (M7, M14). P5 puts one course before all the
others, so every plan gains a semester, and it sees the edits that count
semesters wrong (M2, M4, M5, M6), read the order backwards (M8), or
leave out the last course, which the new course now is (M3). P6 adds a
course with no relation, which the count of courses taken must include,
and sees the edits that count courses or semesters loosely (M1, M11,
M13, M15), the last course left out (M3), and the answer read off the
last course rather than the longest chain (M6), since the new course is
last and its chain is one course. P2 and P3 change
only the order the relations and the course numbers arrive in: P2 sees
four edits that depend on that order (M4, M5, M7, M14), and P3 seven,
among them the two that leave a course out by its number (M3, M12). An
edit wrong the same way on every listing, every naming and every
direction, each course's prerequisites read as its followers (M10), is
seen by P1 alone, failing on every one of the 1491 plans without a
cycle.

Of the fifteen not kept, eight fail exactly as a kept one: a semester
counted as one course taken in the ★ arm as M11; the courses that follow
read backwards in the ★ and solution arms, a finished course left open
in the memo arm, semesters counted from 0 in the order arm, and each
prerequisite counted twice in the solution arm, as M10; course `n` never
in the first semester in the solution arm as M3; and a semester counted
once per course in it in the sinks arm as M13. The other seven fail each
in a way of their own and were not needed.

## Verification

Every arm prints the same output as `minimum_semesters.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The ★, memo, order and sinks arms were written as Kāra and checked clean
as written. `karac fix` carried the solution arm in five rounds: the
`use std::collections::VecDeque` dropped, `Vec<..>` to `Vec[..]`, `&` to
`ref`, `!` to `not`, `::` to `.`, and the `&v` patterns to `v`; then
`struct Solution {}` declared; then `vec![0; n + 1]` to `Vec.filled(n +
1, 0)`, `vec![]` to `Vec.new()`, and the `as i64` at the call dropped; then `usize` to `i64`,
`vec![Vec.new(); n + 1]` to `Vec.filled(n + 1, Vec.new())`, and the `as
usize` casts to `as i64`; then the casts that widen for nothing dropped.

The kata found four gaps: one in the last round, and three more in
checking that round's fix over every kara-katas file it touches:

- **B-2026-11-12-5** (fixed): `karac fix` left `graph[r[0] as
  i64].push(r[1] as i64)` and `indegree[r[1] as i64] += 1` with `r:
  Vec[i32]`. A list position takes any integer, and an element pushed
  into a list whose element type is known widens as an argument does,
  but `lossless_cast` said so only for an argument, a field, a typed
  `let` and a return. It now flags both, and the fifth round drops
  them. The one cast left, `push(r[1] as i64)`, is the one that makes
  `graph` a list of `i64` lists: `Vec.filled(n + 1, Vec.new())` leaves
  its element type open until that push.
- **B-2026-11-12-6** (fixed): checking that the new lint keeps every
  program's output, over the 431 kara-katas files it newly flags, found
  `if c < 128 { c } else { 0xFFFD }` with `c: u8` passed to an `i64`
  parameter printing 253. The `0xFFFD` took its sibling's `u8` and
  wrapped, after an older fix had deleted the `c as i64` there. The
  branches now widen to the parameter's `i64`, and a literal that does
  not fit its sibling with nothing to widen to is refused.
- **B-2026-11-12-7** (fixed): the same check found `y = if c { a } else
  { y }` with `a: u8` refused, where `let y2: i64 = if c { a } else { y
  }` was accepted, so deleting a flagged `a as i64` there left a program
  that did not check. An assignment's branches now widen to the place
  they are stored in.
- **B-2026-11-12-8** (fixed): the same check found kata 664's
  differential refused after `karac fix`. `letter = b[j] as i64` after
  `let mut letter = -1`, with `b` a byte list, is what makes `letter` an
  `i64`, but `lossless_cast` called the cast unnecessary, and without it
  `letter` became a `u8` that `-1` cannot initialize. A cast that fixes
  an open binding is no longer flagged.

## Benchmarks

The bench builds 8 plans of 5000 courses once, LeetCode's largest, each
course from 2 on needing one earlier course drawn at random: 4999
relations and no cycle. Each of 300 rounds draws one course's
prerequisite again in every plan and answers the plan with the ★ arm:
2400 calls. Every implementation prints `300 rounds over 8 plans of 5000
courses and 4999 relations: semesters total 45386, checksum 559113177`.
Each keeps every relation as its own allocation of two values
(`Vec[i64]`, `Vec<i64>`, `[]int64`, a Python list, and C's `int64_t *`),
and builds in every call a growable list of the courses after each
course, a count per course, and a list per semester, with the language's
own growable list: Kāra's `Vec`, Rust's `Vec`, Go's slices and `append`,
and C's `realloc` doubling from 4.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `3436c6649a`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.464 to 0.712 s | 0.579 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.532 to 0.813 s | 0.615 s |
| C (`clang -O3`) | 0.502 to 0.809 s | 0.627 s |
| Kāra (`karac build`) | 0.576 to 0.833 s | 0.641 s |
| Rust (`rustc -O`) | 0.473 to 0.840 s | 0.641 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.495 to 0.855 s | 0.685 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.618 to 0.861 s | 0.688 s |
| Go | 1.023 to 1.243 s | 1.092 s |
| Python | 3.250 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Each call allocates 5001 lists of the courses after each course,
grows them one push at a time and frees them again; this README has not
measured how much of the time that takes. Kāra, C and Rust land within
each other's spread, which runs 0.24 to 0.37 s wide:
C at `-march=x86-64-v3` takes about 0.94x Kāra's median time, C at `-O3`
1.02x, Rust 1.04x, and Rust under overflow checks 1.11x. Go takes about
1.8x Kāra's time and Python about 5.3x.
