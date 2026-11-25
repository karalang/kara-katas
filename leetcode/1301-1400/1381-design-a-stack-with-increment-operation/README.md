# 1381. Design a Stack With Increment Operation

Design a stack that supports increment operations on its elements.
Implement the `CustomStack` class:

`CustomStack(int maxSize)` initializes the object with `maxSize`, the
maximum number of elements in the stack.

`void push(int x)` adds `x` to the top of the stack if the stack has not
reached the `maxSize`.

`int pop()` pops and returns the top of the stack, or `-1` if the stack
is empty.

`void inc(int k, int val)` increments the bottom `k` elements of the
stack by `val`. If there are less than `k` elements in the stack,
increment all the elements in the stack.

```
["CustomStack","push","push","pop","push","push","push","increment","increment","pop","pop","pop","pop"]
[[3],[1],[2],[],[2],[3],[4],[5,100],[2,100],[],[],[],[]]
->  [null,null,null,2,null,null,null,null,null,103,202,201,-1]
```

**Constraints:** `1 <= maxSize, x, k <= 1000`, `0 <= val <= 100`, and at
most `1000` calls will be made to each method of `increment`, `push` and
`pop` each separately.

Each arm is `struct CustomStack` with `fn new(max_size: i32) ->
CustomStack`, `fn push(mut ref self, x: i32)`, `fn pop(mut ref self) ->
i32` and `fn increment(mut ref self, k: i32, val: i32)`.

## Approaches

| file | mechanism |
|---|---|
| `custom_stack.kara` ★ | an increment owed to the element k places up and left there; a pop pays the top element what it is owed and hands the debt down to the one below, since every increment that reached the top reached it too. O(1) for each call |
| `custom_stack_naive.kara` | the stack kept as it is: an increment adds to each of the bottom k elements in turn. O(k) for an increment |
| `custom_stack_fenwick.kara` | what each place has been raised by, kept as differences in a Fenwick tree: an increment adds val from the bottom and takes it off past the k-th place, and a pop clears its place's raise for the next element pushed there. O(log maxSize) for each call |
| `custom_stack_log.kara` | every increment kept in a log, and each element with where the log stood when it was pushed: a pop adds up the increments logged since that reached its place, which it has held all that time. O(calls) for a pop |
| `custom_stack_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `Vec<i32>` of what each element is owed beside the stack, `if let Some(below) = self.inc.last_mut() { *below += extra; }` to hand a pop's debt down), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 4 lines: LeetCode's example (`2 103 202 201
-1`); a stack of one, with a push past it ignored, an increment past it
reaching the one there is, a pop of nothing, and an increment of nothing
that no later push takes up, then a stack of three with the bottom two
raised, the top popped and another pushed, and all three raised (`105 -1
4 3 12 17 16 -1`); the constraints' most, a stack of 1000 with 1000
pushes, 1000 increments of the bottom 1 to 1000 by 0 to 100, and 1000
pops (`3000 calls: checksum 190459472`); and 2000 random sessions, a
stack of 1 to 20 and 1 to 100 calls in four mixes of pushes, pops and
increments (`2000 random sessions: 30650 pops, 5335 of an empty stack,
checksum 862358755`). `custom_stack.py` mirrors the ★ arm, and its
output is byte-identical. Every arm gives the same output under `karac
__mir-run`, `karac run`, `karac build` and `karac __mir-llvm-run`.

The Mend loop: the naive and log arms check clean as first written. The
★ arm was written with `max_size as i64` in `new`, and `karac check`
warns that the cast is unnecessary, an `i32` widening to `i64`
implicitly (`lossless_cast`), as on two lines of the harness; `karac
fix` drops all three. The harness's first draft printed with Rust's
turbofish, `.collect::[Vec[String]]()`, which `karac check` refuses
(E0001) and `karac fix` writes as `Vec[String].from_iter(..)`; it now
prints through a `show` helper. The Fenwick arm's `let mut sum = 0;` is
an `i64` that its `i32` return refuses, and `karac fix` declares it
`sum: i32`. The Rust solution takes one round of 14 fixes by `karac
fix`'s count, from 7 errors: each `Vec<i32>` to `Vec[i32]`, `usize` to
`i64`, each `Vec::new()` to `Vec.new()`, `maxSize as usize` to
`maxSize`, each `&mut self` to `mut ref self`, `k as usize` to `k as
i64`, and the `last_mut` handing the debt down to `if self.inc.len() > 0
{ self.inc[self.inc.len() - 1] += extra; }`. Before kara 125f1e1b95 that
last fix spelled the element `r#self.inc[..]`, taking the `self` it
starts with for a keyword to escape, and `karac fix` refused to write a
file it would leave with more parse errors than it found
(B-2026-11-21-65, filed from this kata). Every arm matches on the first
run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the stack kept as a list, and each increment making a new one
with the bottom k raised. LeetCode's example and 2000 sessions in four
kinds, 500 each: a stack of 1 to 3 and 1 to 30 calls, mostly pushes; a
stack of 1 to 8 and 1 to 40 calls, mixed; the same with mostly
increments; and with mostly pops. Each push is of 1 to 1000 and each
increment of the bottom 1 to 10 by 0 to 100. Every session is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | every pushed value raised by 1000: every answer but -1 raised by 1000 |
| P3 | every pushed value and every increment doubled: every answer but -1 doubled |
| P4 | the pushes a full stack ignores taken out, and room for 1000: the same answers |
| P5 | after every call that leaves room, a push of 1000 and a pop: 1000 from each, the rest the same |
| P6 | the ★ arm's answers |

All 60,030 checks pass on every arm: `2001 sessions: checksum 603513125,
60030 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, replaying the
sessions on a list, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a pop's debt not handed down | P1 508, P2 508, P3 508, P5 508, P6 2032 |
| M2 | ★: an increment owed to the bottom element, not the k-th | P1 836, P2 836, P3 836, P5 836, P6 3344 |
| M3 | naive: a push taken while the stack is exactly full | P1 740, P2 740, P3 740, P4 740, P5 740, P6 740 |
| M4 | naive: a pop of nothing answers 0 | P1 1300, P2 1300, P3 1300, P5 1300, P6 1300 |
| M5 | Fenwick: a pop leaves its place's raise for the next push | P1 826, P2 826, P3 826, P5 1298, P6 826 |
| M6 | Fenwick: an increment taken off at the k-th place, not past it | P1 1298, P2 1298, P3 1298, P5 1298, P6 1298 |
| M7 | log: only the increments reaching past a place counted | P1 485, P2 485, P3 485, P5 485, P6 485 |
| M8 | log: every element counted from the start of the log | P1 1352, P2 1352, P3 1352, P5 1731, P6 1352 |
| M9 | solution: a pop answers without its debt | P1 1298, P2 1298, P3 1298, P5 1298, P6 1298 |
| M10 | solution: the debt handed down replaces what the one below is owed | P1 517, P2 517, P3 517, P5 958, P6 517 |

P1, P2, P3, P5 and P6 kill all ten, P4 one. Raising (P2) and doubling
(P3) never change which pops answer -1, so they fail exactly where the
literal reading does. The push and pop of 1000 (P5) catch more than P1
where an edit leaves something behind on a place: the raise a pop does
not clear (M5), increments logged before a push (M8), a debt written
over (M10). P4 catches only the edit that lets a full stack take one
more push (M3): taking out the pushes a full stack ignores leaves
nothing for the edit to take. M6 and M9 fail the same counts in
different arms: M9 fails wherever some pop answers a raised value, and
in these sessions so does M6, which loses the raise of the highest
element each increment reaches.

## Benchmarks

2000 rounds, each a new stack of 1000 and 3000 calls on it: four in ten
a push of 1 to 1000, three an increment of the bottom 1 to 1000 by 0 to
100, three a pop; each round's draws start from the checksum so far.
Every implementation prints `2000 rounds of 3000 calls on a stack of
1000: checksum 941618790`. The Rust function is the ★ arm with
`last_mut` handing the debt down; Go slices its two slices; C keeps two
fixed arrays of the stack's size and a top count.

BENCHTAB
