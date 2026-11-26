# 1792. Maximum Average Pass Ratio

A school has classes, each with a final exam. `classes[i] = [pass_i,
total_i]` says the `i`th class has `total_i` students and `pass_i` of
them will pass. There are `extraStudents` more students, each sure to
pass in any class they join. A class's pass ratio is its passing
students over its students, and the average pass ratio is the sum of the
classes' ratios over the number of classes. Assign every extra student
to a class so the average pass ratio is as large as it can be, and
return it. Answers within `10^-5` of the true one are accepted.

```
classes = [[1,2],[3,5],[2,2]],         extraStudents = 2  ->  0.78333
classes = [[2,4],[3,9],[4,5],[2,10]],  extraStudents = 4  ->  0.53485
```

**Constraints:** `1 <= classes.length <= 10^5`, `classes[i].length ==
2`, `1 <= pass_i <= total_i <= 10^5`, and `1 <= extraStudents <= 10^5`.

The arms are `fn max_average_ratio(classes: Vec[Vec[i32]],
extra_students: i32) -> f64`, and every answer is printed to five
places.

## Approaches

| file | mechanism |
|---|---|
| `max_average_ratio.kara` ★ | greedy: a student added to a class of `p` passing out of `t` raises its ratio by `(p + 1) / (t + 1) - p / t`, and that gain only shrinks as the class grows, so each student goes where the gain is largest now. A largest-first `PriorityQueue` of `(F64, i64)`, gain and class (`F64`, since `f64` has no order). O((n + extra) log n) |
| `max_average_ratio_cross.kara` | the same greedy with the gains compared exactly: a gain is `(t - p) / (t * (t + 1))`, so two classes compare by cross-multiplying in `i64`, through a `Class` struct's own `Ord`. O((n + extra) log n) |
| `max_average_ratio_tree.kara` | the same greedy over a `SortedSet` of `(F64, i64)`, the largest gain taken from its end with `pop_last`. O((n + extra) log n) |
| `max_average_ratio_closed.kara` | the same greedy, each queue entry carrying its class, `(gain, pass, total)`, the gain in closed form, and the average summed as the queue is emptied. O((n + extra) log n) |
| `max_average_ratio_solution.kara` | a Rust solution as LeetCode's Rust users write it (a tuple struct with a hand-written `Ord` in a `BinaryHeap`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's two examples (`0.78333
0.53485`); four edges, one class all passing with four students, one
class of two with one passing and one student, two classes alike, and a
full class beside one with a single student passing (`1.00000 0.66667
0.55000 0.86667`); the constraints' most, 100000 classes and 100000
students, every class of 100000 with one passing, and then classes at
random (`the most: 0.00002 0.46333`); and 2000 random cases of 1 to 12
classes of up to 20 students with 1 to 30 more students (`2000 random
cases: checksum 456261628`). `max_average_ratio.py` mirrors the ★ arm,
and its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, cross and closed arms check clean as first
written. The tree arm was first written with Rust's
`ratios.iter().sum::<f64>()`; check said Kāra has no turbofish, and
`karac fix` removed it, 1 fix. The harness builds its 100000 classes
with `one.push([1, 100000].to_vec())` in a loop, and check refuses it,
`expected 'Vec[i32]', found 'Vec[i64]'`, with no fix: B-2026-11-26-6, a
literal reaching `Vec.push` through `.to_vec()` does not take the
element type from the receiver. The first literal is suffixed by hand,
`[1i32, 100000]`. The Rust solution takes one round of 40 fixes by
`karac fix`'s count, and its diff is: the `use` lines dropped, `struct
Item(f64, i32, i32)` to `struct Item { f0: f64, f1: i32, f2: i32 }` with
every construction, pattern and `.0` following, `&self, other: &Self` to
`self, other: ref Self`, `struct Solution;` to `struct Solution {}`,
`Vec<Vec<i32>>` to `Vec[Vec[i32]]`, `BinaryHeap::new()` to
`PriorityQueue.max_first()`, `for c in &classes` to `for c in ref
classes`, `.sum::<f64>()` to `.sum()`, and `Solution::` to `Solution.`.
Every arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every way to share the extra students among the classes
tried, and the largest average kept, while there are at most 4 classes
and 6 more students. LeetCode's examples, the four edges, four lists of
300 classes of up to 1000 students with 1 to 1000 more, and 1990 random
cases of 1 to 4 classes of up to 8 students with 1 to 6 more. Two
answers agree when they are within `10^-9`. Each arm meets six
properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, while there are at most 4 classes and 6 more students |
| P2 | the classes in reverse order give the same answer |
| P3 | one more student never lowers the answer |
| P4 | a class of 7 all passing, appended, takes no student, and the average becomes `(n * answer + 1) / (n + 1)` |
| P5 | every class twice over, and twice the students, give the same answer |
| P6 | the ★ arm's answer |

The differential was first written with the cases pushed as
`cases.push(([[1, 2], [3, 5], [2, 2]].to_vec(), 2))` and P4's class as
`grown.push([7, 7].to_vec())`, and check refused all 7 with no fix, the
same B-2026-11-26-6, there for a literal inside a tuple too; the first
literal of each is suffixed by hand. All 59,975 checks pass on every
arm: `2000 cases: checksum 341700209, 59975 checks over 5 arms: 0
failures`, under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`. Python, running the ★ arm's mirror over the same
cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the gain worked out without the new student in the class's size | P1 1208, P2 227, P4 296, P5 220, P6 4852 |
| M2 | ★: the smallest gain taken first | P1 1404, P2 2, P4 747, P5 747, P6 5636 |
| M3 | cross: the comparison the wrong way round | P1 1404, P2 6, P4 747, P5 747, P6 1409 |
| M4 | cross: one side of the cross-multiplication missing its + 1 | P1 161, P2 70, P4 9, P5 198, P6 165 |
| M5 | tree: the smallest gain taken from the set | P1 1404, P2 2, P4 747, P5 747, P6 1409 |
| M6 | tree: a student added who never passes | P1 1995, P2 71, P3 2000, P4 257, P5 741, P6 2000 |
| M7 | closed: the new gain worked out for the class before it grew | P1 360, P4 205, P5 256, P6 364 |
| M8 | closed: each ratio summed over one student too many | P1 1995, P4 2000, P5 266, P6 2000 |
| M9 | solution: a student added who never passes | P1 1995, P2 59, P3 2000, P4 209, P5 861, P6 2000 |
| M10 | solution: the comparison the wrong way round | P1 1404, P2 2, P4 747, P5 747, P6 1409 |

## Benchmarks

The bench builds 200 random lists of 1000 classes of up to 1000 students
once, and makes 4000 calls of the ★ arm, each list and its 1 to 1000
more students drawn from the checksum so far. The Rust, C and Go mirrors
break a tie in the gain toward the larger class, as the ★ arm's `(F64,
i64)` does. It checks clean as first written. Every implementation
prints `4000 calls over 200 lists of 1000 classes: checksum 373151666`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 0.50 s against Rust's 0.30 s (0.31 s with overflow checks
on), C's 0.33 s and Go's 0.80 s; Python takes 2.5 s.
