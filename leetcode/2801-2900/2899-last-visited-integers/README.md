# 2899. Last Visited Integers

Given an integer array `nums` where `nums[i]` is either a positive
integer or `-1`. We need to find for each `-1` the respective positive
integer, which we call the last visited integer.

To achieve this goal, let's define two empty arrays: `seen` and `ans`.

Start iterating from the beginning of the array `nums`.

- If a positive integer is encountered, prepend it to the **front** of
  `seen`.
- If `-1` is encountered, let `k` be the number of **consecutive** `-1`s
  seen so far (including the current `-1`),
  - If `k` is less than or equal to the length of `seen`, append the
    `k`-th element of `seen` to `ans`.
  - If `k` is strictly greater than the length of `seen`, append `-1`
    to `ans`.

Return *the array* `ans`.

```
nums = [1, 2, -1, -1, -1]  ->  [2, 1, -1]
nums = [1, -1, 2, -1, -1]  ->  [1, 2, 1]
```

**Constraints:** `1 <= nums.length <= 100`; `nums[i] == -1` or
`1 <= nums[i] <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `last.kara` ★ | the integers seen kept in a `Vec` in the order they come, so the front of the statement's `seen` is the end of this one, and the run of -1s counted; the k-th of a run reads the k-th integer back from the end, or -1 when there are fewer |
| `last_front.kara` | the statement as written: each integer prepended to `seen`, a `VecDeque` through `push_front`, and the k-th of a run read with `get(k - 1)` from the front, matched on its `Option` |
| `last_insert.kara` | the statement's prepend on a plain `Vec`, through `insert(0, ..)`, every integer shifting the rest, and the k-th read through `get(k - 1).unwrap_or(-1)` |
| `last_back.kara` | no `seen` at all: for each -1, the length of its run so far is the -1s just before it, and the answer is found by walking back from the run's start, counting the integers passed |
| `last_solution.kara` | a Rust solution as LeetCode's Rust users write it: `seen` as a `Vec<i32>` pushed at the end, the run counted in a `usize`, the k-th read as `seen[seen.len() - k]`, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Reading `seen` back from the end was checked first against the
statement's prepend in Python, over 3000 random arrays of up to 12
entries, before any arm was written.

Every arm prints the same 6 lines: LeetCode's two examples; 100
entries, LeetCode's most, all -1, 50 integers then 50 -1s, and integers
and -1s in turn, each as its count of answers and its first and last;
then 3000 random arrays of 1 to 10 entries, -1 one time in two and
otherwise 1 to 5, and 1000 of 100 entries, -1 one time in three and
otherwise 1 to 100, as a total and a checksum of the answers.
`last.py` mirrors the ★ arm and its output is byte-identical.

```
[2, 1, -1] [1, 2, 1]
100 answers: first -1, last -1
50 answers: first 50, last 1
50 answers: first 1, last 99
3000 small arrays: answers total 8982, checksum 612328030
1000 arrays of 100: answers total 1641604, checksum 167000809
```

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: each integer prepended to `seen` with `insert(0, ..)`,
and for each -1 the run ending at it counted afresh by walking back,
its k-th entry of `seen` taken, or -1. It draws 2000 random arrays of 1
to 10 entries, -1 one time in two and otherwise 1 to 5, then 50 of up
to 3000, past LeetCode's 100, -1 one time in three, all before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one answer for each -1 |
| P3 | every integer raised by 1000: every answer but -1 raised by 1000 |
| P4 | an integer and then a -1 added at the end: that integer added to the answer |
| P5 | a -1 put in front: a -1 put in front of the answer |
| P6 | each arm agrees with at least three of the other four |

The differential prints `2050 cases, answers total 1124939: checksum
49871344, 61500 checks over 5 arms: 0 failures` under every lane in
Verification, and the statement's prepend in Python over the same cases
gives the same checksum. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Ten edits to the differential, three to the walk back, two each to the
★ arm, the `VecDeque` and the `insert` arms, and one to the solution,
each run under `karac __mir-run` and `karac __mir-llvm-run`. All ten
are killed, each the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a run never ended by an integer | P1 1036, P4 1829, P5 1005, P6 1036 |
| M2 | ★: the k-th read from the oldest | P1 939, P4 1828, P6 939 |
| M3 | front: each integer put at the back | P1 939, P4 1828, P6 939 |
| M4 | front: the k-th read one further on | P1 1413, P4 2034, P6 1413 |
| M5 | insert: every -1 reading the latest | P1 778, P6 778 |
| M6 | insert: each integer appended, not prepended | P1 939, P4 1828, P6 939 |
| M7 | back: the run's start not walked back | P1 778, P6 778 |
| M8 | back: the -1s passed counted as integers | P1 274, P6 274 |
| M9 | back: the run's length one short | P1 1452, P4 2050, P6 1452 |
| M10 | solution: the k-th never the oldest | P1 1026, P4 201, P6 1026 |

## Benchmarks

The bench draws 10000 arrays of 100 entries, LeetCode's most, -1 one
time in three and otherwise 1 to 100, all first, then answers each 20
times by the ★ arm in all five languages, every call building its own
`seen` and answer. Every implementation prints `10000 arrays of 100, 20
rounds: answers total 328751060, checksum 703054417`.

BENCHTAB

## Verification

All five arms print the same output as `last.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as written, and so did the
differential's `let mut fronted: Vec[i64] = [-1];`, a list literal
taken as the `Vec` its binding asks for.

LeetCode's Rust template took one `karac fix` run, the wrapper
included, and the diff shows these: `struct Solution {}` came for the
`impl`; `Vec<..>` became `Vec[..]`, `Vec::new()` `Vec.new()`; the run's
`k: usize` became `k: i64`; `for &x` and `|&x|` lost their `&`;
`Solution::` took `.`. The wrapper's `.into_iter().map(|x| x as i64)`
back to `i64` stayed as written.
