# 2076. Process Restricted Friend Requests

You are given an integer `n` indicating the number of people in a
network. Each person is labeled from `0` to `n - 1`.

You are also given a 0-indexed 2D integer array `restrictions`, where
`restrictions[i] = [x_i, y_i]` means that person `x_i` and person `y_i`
cannot become friends, either directly or indirectly through other
people.

Initially, no one is friends with each other. You are given a list of
friend requests as a 0-indexed 2D integer array `requests`, where
`requests[j] = [u_j, v_j]` is a friend request between person `u_j` and
person `v_j`.

A friend request is successful if `u_j` and `v_j` can be friends. Each
friend request is processed in the given order (i.e., `requests[j]`
occurs before `requests[j + 1]`), and upon a successful request, `u_j`
and `v_j` become direct friends for all future friend requests.

Return a boolean array `result`, where each `result[j]` is `true` if the
`j`-th friend request is successful or `false` if it is not.

**Note:** If `u_j` and `v_j` are already direct friends, the request is
still successful.

```
n = 3, restrictions = [[0,1]], requests = [[0,2],[2,1]]                         ->  [true,false]
n = 3, restrictions = [[0,1]], requests = [[1,2],[0,2]]                         ->  [true,false]
n = 5, restrictions = [[0,1],[1,2],[2,3]], requests = [[0,4],[1,2],[3,1],[3,4]] ->  [true,false,true,false]
```

**Constraints:** `2 <= n <= 1000`; `0 <= restrictions.length <= 1000`;
`restrictions[i].length == 2`; `0 <= x_i, y_i <= n - 1`; `x_i != y_i`;
`1 <= requests.length <= 1000`; `requests[j].length == 2`;
`0 <= u_j, v_j <= n - 1`; `u_j != v_j`.

Friends of friends are friends, so the people fall into groups, and a
request between two groups is refused exactly when some restriction has
one person in each. A union-find keeps the groups; each request between
two groups tries every restriction's two roots, and joins the groups if
none is the pair: O(m · r) finds. The approaches differ in how they keep
the groups and test a request.

## Approaches

| file | mechanism |
|---|---|
| `friends.kara` ★ | a union-find of parents in a `Vec`, found with path halving; a request between two roots refused if a restriction's two roots are those two, else one root hung under the other. O(m · r) finds |
| `friends_label.kara` | quick-find: every person carries their group's label, a request's labels compared with each restriction's by `any`, and a join relabelling every person of one label through `iter_mut()`. O(m · (r + n)) |
| `friends_forbid.kara` | each group a `struct Group` of its members and a `Set` of the people they may never befriend; a request refused if the smaller group's members meet the larger's forbidden set, else the smaller moved into the larger with `mem.take` and `extend` |
| `friends_dsu.kara` | a `struct Dsu` with methods: a recursive `find` that points every person on the way at the root, and `union` by size |
| `friends_trial.kara` | by trial: the parents `clone()`d, the request's union made in the copy, and the copy kept only if no restriction's two people now share a root |
| `friends_solution.kara` | LeetCode's Rust template (`Vec<Vec<i32>>`, a nested `fn find(p: &mut Vec<usize>, x: usize)` with path compression, `as usize` casts, `&&` and `\|\|`), carried by `karac fix` in three rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's three examples and four
more, each problem and its answers; then the count of requests accepted
and a checksum of the answers for 300 random problems of 2 to 60 people,
0 to 40 restrictions and 1 to 80 requests; then the same for the
constraints' largest, 1000 people, 1000 restrictions and 1000 requests.
`friends.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the friendships made so far kept as a graph of edges, each
request tried by adding its edge and flooding the graph from every
person, and refused, the edge taken back, if a restriction's two people
are then in one component. It checks 300 random problems of 2 to 12
people, 0 to 10 restrictions and 1 to 16 requests; then 20 with 10 to 29
restrictions, and 20 of 2 to 4 people asking again and again. All 340
are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | every pair, restrictions and requests, written the other way round gives the same answers |
| P3 | every request made twice in a row is answered twice: a repeat changes nothing |
| P4 | a request between two restricted people is refused, and with no restrictions every request is accepted |
| P5 | the first half of the requests is answered with the first half of the answers |
| P6 | each arm agrees with at least three of the other five |

The differential prints `340 problems: checksum 729078690, 12240 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
problems. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-two edits to the differential, five to six to each of its arms,
each run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen
are kept, three to each Kāra arm and two to the Rust-template arm. Each
kept one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a restriction's first person's group alone checked | P1 226, P2 193, P6 226 |
| M2 | ★: find stopping a step short of the root | P1 157, P2 72, P3 79, P4 30, P6 157 |
| M3 | ★: a refused request joining all the same | P1 221, P3 265, P4 168, P6 221 |
| M4 | label: only the second person relabelled | P1 55, P2 70, P6 55 |
| M5 | label: a restriction tried one way round | P1 179, P4 143, P6 179 |
| M6 | label: a request within a group refused | P1 177, P3 274, P4 263, P6 177 |
| M7 | forbid: the forbidden people left behind | P1 133, P2 140, P4 77, P6 133 |
| M8 | forbid: the movers' owner left as it was | P1 171, P2 158, P4 101, P6 171 |
| M9 | forbid: a restriction forbidden one way round | P1 176, P2 156, P4 141, P6 176 |
| M10 | dsu: a request within a group refused | P1 161, P3 248, P6 161 |
| M11 | dsu: no union ever made | P1 157, P6 157 |
| M12 | dsu: find giving the parent, not the root | P1 17, P2 18, P3 2, P4 1, P6 17 |
| M13 | trial: the trial kept when it breaks a restriction | P1 177, P6 177 |
| M14 | trial: a restriction broken when its people are apart | P1 277, P4 46, P6 277 |
| M15 | trial: the restrictions tried in the old groups | P1 265, P3 265, P4 189, P6 265 |
| M16 | solution: the adapter's first request dropped | P1 340, P3 340, P4 134, P5 316, P6 340 |
| M17 | solution: find giving the parent, not the root | P1 67, P2 88, P3 1, P4 1, P6 67 |

P1 and P6 kill all seventeen, P4 twelve, P2 and P3 eight each, and P5
one. P4 sees an arm that lets a restricted pair befriend or turns a
request away with nothing to forbid it: a restriction tried one way
round (M5, M9), joins made regardless (M3), restrictions read wrongly
(M14, M15). P2, which writes every pair the other way round, sees an
edit whose answer depends on the order of a pair: a restriction's first
person alone (M1), one person relabelled (M4), a group's forbidden
people or members split from it (M7, M8). P3, which makes each request
twice, sees a repeat that changes something: a request within a group
refused (M6, M10), or a refused one joining anyway (M3). P5 holds for
any arm that answers the requests in order, as every arm does, and
sees only the adapter that drops a request (M16); it is kept for the
statement's "processed in the given order". The finds that give a
parent in place of a root (M12, M17) are wrong only when a tree grows
three deep, which the small problems seldom reach.

Of the thirty-two, fifteen were not kept. One survives, and it is
equivalent: the Rust arm's adapter writing every pair the other way
round, which P2 shows changes nothing. Five fail as a kept one: the ★
and dsu arms' restriction tried one way round as M5; the forbid and Rust
arms' request within a group refused as M6; the label arm's no group
ever joined as M11. Five fail alike and none is kept: the ★, label, dsu
and Rust arms' every request accepted, a restriction read as one person
or no restrictions at all (P1 265, P4 232). Four are killed with checks
of their own but were left out because their arm keeps three: the
forbid arm's members left behind (P1 123, P2 135, P3 41, P4 68) and
smaller group tried against its own forbidden set (P1 265, P2 15, P4
230); the trial arm's root a step up at most (P1 126, P2 139, P3 20, P4
67) and only the restrictions on the request's people tried (P1 187, P4
141).

## Verification

Every arm prints the same output as `friends.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them.

Under `karac __mir-run` the arms take 0.5 s to 2.1 s and the
differential 2.7 s (timed while other work shared the machine).

The forbid arm met one compiler gap. It moved a group's members out with
Rust's `std::mem::take`, written with Kāra's dots: `std.mem.take(mut
groups[small].members)`. The `::` form gets the edit that deletes its
module path; the dotted one parsed as field accesses on an undeclared
`std` and said only "undefined name 'std'". It now names the path and
deletes the module segments Kāra has no use for, keeping its own `mem`,
and `karac fix` made the arm's `mem.take(..)`. Fixed in kara 3c5e8c8dc5, test
`tests/kata_2076_std_dot_path.rs`.

The Rust arm was written as LeetCode's Rust template. `karac fix` carries
it in three rounds of 22, 2 and 1 edits: Rust's spellings (`Vec<..>` to
brackets, `&mut p` to `mut p`, `&mut Vec<usize>` to `mut ref`, `&&` and
`||` to `and` and `or`, `Vec::` to `.`, `struct Solution;` to `struct
Solution {}`); then the nested `fn find`, which Kāra does not have,
moved out of the method to the top level; then the `mut` of the
recursive call inside it, which the first round did not see. The fixed
arm reads as the template does, `usize`s and all.

## Benchmarks

The bench answers 400 problems of the constraints' largest size with the
★ arm in all five languages: 1000 people, 1000 restrictions and 1000
requests each, every pair drawn at random. Every implementation prints
`400 problems: 327454 accepted, checksum 147159523`.

BENCHTAB
