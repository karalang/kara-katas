# 2092. Find All People With Secret

You are given an integer `n` indicating there are `n` people numbered
from `0` to `n - 1`. You are also given a 0-indexed 2D integer array
`meetings` where `meetings[i] = [xi, yi, timei]` indicates that person
`xi` and person `yi` have a meeting at `timei`. A person may attend
multiple meetings at the same time. Finally, you are given an integer
`firstPerson`.

Person `0` has a secret and initially shares the secret with a person
`firstPerson` at time `0`. This secret is then shared every time a
meeting takes place with a person that has the secret. More formally,
for every meeting, if a person `xi` has the secret at `timei`, then they
will share the secret with person `yi`, and vice versa.

The secrets are shared instantaneously. That is, a person may receive
the secret and share it with people in other meetings within the same
time frame.

Return a list of all the people that have the secret after all the
meetings have taken place. You may return the answer in any order.

```
n = 6, meetings = [[1,2,5],[2,3,8],[1,5,10]], firstPerson = 1  ->  [0,1,2,3,5]
n = 4, meetings = [[3,1,3],[1,2,2],[0,3,3]], firstPerson = 3   ->  [0,1,3]
n = 5, meetings = [[3,4,2],[1,2,1],[2,3,1]], firstPerson = 1   ->  [0,1,2,3,4]
```

**Constraints:** `2 <= n <= 10^5`; `1 <= meetings.length <= 10^5`;
`meetings[i].length == 3`; `0 <= xi, yi <= n - 1`; `xi != yi`; `1 <=
timei <= 10^5`; `1 <= firstPerson <= n - 1`.

Within one time the secret spreads through every chain of meetings, so
a time is a graph, and those who know after it are everyone joined to a
knower. Across times only who knows carries over, not who met. The
meetings sorted by time, each time's graph joined in a union-find whose
root of the secret is person 0, and everyone not joined to 0 cut loose
again after it, give the answer in O(m log m). The approaches differ in
how they spread the secret within a time. Every arm returns the people
in increasing order.

## Approaches

| file | mechanism |
|---|---|
| `secret.kara` ★ | the meetings sorted with `sort_by_key`, a union-find over a `Vec[i64]` with path halving whose unions keep the smaller root, so 0 stays one; after each time its people not joined to 0 are cut loose. O(m log m) |
| `secret_bfs.kara` | each time's meetings in a `Map[i64, Vec[i64]]` of who meets whom, and a `VecDeque` from the knowers among them, the secret passed on until it reaches no one new. O(m log m) |
| `secret_earliest.kara` | by the earliest time each person learns: a `PriorityQueue[(i64, i64)]` of `(time, person)`, smallest first, a meeting no earlier than its person learned passing the secret on at its time; Dijkstra's order makes each first pop the earliest. O(m log m) |
| `secret_relax.kara` | to a fixed point: each time's meetings passed over again and again, every meeting of a knower and one who does not know telling the other, until a pass tells no one. O(g²) for a time of `g` meetings |
| `secret_struct.kara` | the meetings grouped by time in a `SortedMap[i64, Vec[(i64, i64)]]`, each time a `struct Gathering` of a `Map` of who meets whom, with a recursive `spread` from each knower. O(m log m) |
| `secret_solution.kara` | LeetCode's Rust template (`meetings: Vec<Vec<i32>>` sorted in place by `sort_by_key(\|m\| m[2])`, a recursive `find` over a `Vec<usize>`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 10 lines: LeetCode's three examples and four
more, each gathering and who knows; then the count and a checksum of
who knows for 2000 random gatherings of 2 to 60 people and up to 80
meetings at times 1 to 10; then the constraints' largest, 100000 people
and 100000 meetings at random times, then a chain of meetings whose
times rise from the first person, and one whose times fall. `secret.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: 0 and the first person know at time 0; then for each time
from the earliest, every meeting at that time between one who knows and
one who does not tells the other, the meetings looked at again and again
until no one more is told. It checks 300 random gatherings of 2 to 10
people and up to 14 meetings at times 1 to 4; then 20 whose meetings
all share one time, and 20 whose meetings each have their own. All 340
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the people are the statement read literally |
| P2 | the meetings listed in reverse give the same people |
| P3 | every time doubled and moved on by 5 gives the same people |
| P4 | 0 and the first person are there, and the people are distinct, in increasing order, and below `n` |
| P5 | a meeting of 0 and person `p` after every other adds `p` and no one else |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 gatherings: checksum 654908757, 12240
checks over 6 arms: 0 failures` under every lane in Verification; the
checksum of the literal people was checked against a Python reading of
the same gatherings. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty edits to the differential, five to each of its arms, each run
under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept,
three to each Kāra arm and two to the Rust-template arm. Each kept one
is killed, fails the same way under both backends and not by a crash,
and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first person never told | P1 160, P4 143, P5 153, P6 160 |
| M2 | ★: the first of a meeting never cut loose | P1 28, P2 1, P5 42, P6 28 |
| M3 | ★: the meetings not sorted | P1 62, P2 91, P5 51, P6 62 |
| M4 | bfs: the queue from those who do not know | P1 223, P5 256, P6 223 |
| M5 | bfs: one told but not asked on | P1 60, P5 56, P6 60 |
| M6 | bfs: two times gathered as one | P1 24, P3 24, P5 14, P6 24 |
| M7 | earliest: the meetings one way only | P1 143, P5 135, P6 143 |
| M8 | earliest: the latest first | P1 54, P5 71, P6 54 |
| M9 | earliest: the time ignored | P1 47, P5 57, P6 47 |
| M10 | relax: one pass only | P1 33, P2 50, P5 29, P6 33 |
| M11 | relax: a time's first meeting skipped | P1 152, P2 132, P5 235, P6 152 |
| M12 | relax: 0 not told at the start | P1 171, P4 151, P5 158, P6 171 |
| M13 | struct: the latest time first | P1 73, P5 81, P6 73 |
| M14 | struct: 0 spreading nothing | P1 109, P5 222, P6 109 |
| M15 | struct: each meeting with oneself | P1 255, P5 311, P6 255 |
| M16 | solution: the larger root kept | P1 255, P2 12, P4 215, P5 311, P6 255 |
| M17 | solution: `find` giving the person, not the root | P1 340, P4 340, P5 340, P6 340 |

P1, P5 and P6 kill all seventeen, P2 five, P4 four and P3 one. P5 adds a
last meeting of 0 and someone, which every edit to how the secret
travels gets wrong for some gathering, as the new person must learn it
and no one else. P2, the meetings listed in reverse, sees an arm whose
answer depends on the order it meets them in: unsorted (M3), one pass
only (M10), a time's first meeting skipped (M11), a person left joined
to a root that is no longer 0 (M2, M16). P4 sees 0 or the first person
missing (M1, M12, M16, M17). P3 sees only an arm that reads the times as
numbers rather than an order, two times gathered as one when they are a
unit apart (M6), which doubling the times parts.

Of the thirty, thirteen were not kept, and one survives. Ten fail as a
kept one: the ★ arm's larger root kept as M16; the bfs, relax and Rust
arms' meetings not sorted as M3; the earliest arm's meeting at the time
learned passing nothing and the struct arm's spread one step only as M5;
the earliest arm's first person never queued and the struct arm's first
person never told as M1; the relax arm's telling only one way as M7;
the Rust adapter's times all 0 as M9. One is killed with checks of its
own but was left out because its arm keeps two: the Rust adapter's
first person one before (P1 155, P4 115, P5 140). One crashes and is not
kept: the bfs arm's meetings recorded one way only, which then reads
`met[p]` for a person with no entry. The survivor is equivalent: the ★
arm reading a person's parent in place of their root at the end, since
the cut-loose pass after each time calls `find` on everyone it met,
which leaves each of them pointing straight at their root.

## Verification

Every arm prints the same output as `secret.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 3.1 s to 6.9 s, but for the struct
arm's 22 s, and the differential 1.2 s (timed while other work shared
the machine). The struct arm is also about 10 times slower than the
others compiled, 5.8 s against 0.4 s to 0.6 s, 4.7 s of it in the falling
chain: its 99998 meetings come in falling times, so each is inserted at
the front of the `SortedMap`, which is kept as one sorted array and
moves every entry after it. 100000 inserts of falling keys take 1.8 s
compiled, where rising keys take 0.03 s; collections.md calls the map a
B-tree. Filed as SORTEDROW.

No arm met any other compiler gap. The Rust arm was written as
LeetCode's Rust template. `karac fix` carries it in three rounds of 29,
3 and 1 edits: Rust's spellings (`Vec<Vec<i32>>` and `Vec<usize>` to
brackets, `&mut Vec` to `mut ref` and `&mut parent` to `mut parent`, `mut
meetings` to `own` with `let mut meetings = meetings;`, `&&` to `and`,
`struct Solution;` to `struct Solution {}`, `Solution::` to `.`, the
`&` of the adapter's patterns dropped); then `find(parent, ..)` inside
`find` to `find(mut parent, ..)`, and `vec![]` and `vec![..]` to
`Vec.new()` and a list; then the adapter's `ref` parameter to a bare
one, which borrows already. The fixed arm reads as the template does.

## Benchmarks

The bench draws 10 gatherings of 100000 people and 100000 meetings, the
constraints' limit, at 1000 times, and answers each 4 times for a
different first person with the ★ arm in all five languages: each answer
sorts a copy of the meetings by time (a stable sort in each, a
hand-written merge sort in C) and runs the union-find over growable
arrays (a `Vec`, a `Vec`, a slice, a `list`, a `malloc`'d buffer).
Every implementation prints `40 answers: 586 people, checksum
864758904`.

BENCHTAB
