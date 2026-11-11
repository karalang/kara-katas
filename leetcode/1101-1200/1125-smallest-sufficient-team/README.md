# 1125. Smallest Sufficient Team

In a project, you have a list of required skills `req_skills`, and a
list of people. The `i`th person `people[i]` contains a list of skills
that the person has.

Consider a sufficient team: a set of people such that for every required
skill in `req_skills`, there is at least one person in the team who has
that skill. We can represent these teams by the index of each person.

Return any sufficient team of the smallest possible size, represented by
the index of each person. You may return the answer in any order.

It is guaranteed an answer exists.

```
req_skills = ["java","nodejs","reactjs"],
people = [["java"],["nodejs"],["nodejs","reactjs"]]                      ->  [0,2]
req_skills = ["algorithms","math","java","reactjs","csharp","aws"],
people = [["algorithms","math","java"],["algorithms","math","reactjs"],
          ["java","csharp","aws"],["reactjs","csharp"],["csharp","math"],
          ["aws","java"]]                                                ->  [1,2]
```

**Constraints:** `1 <= req_skills.length <= 16`; `1 <= people.length <=
60`; each skill is 1 to 16 lowercase letters; the skills of
`req_skills` are unique, and every skill of a person is one of them;
each person's skills are unique (a person may have none); an answer
exists.

The arms are `fn smallest_sufficient_team(req_skills: Vec[String],
people: Vec[Vec[String]]) -> Vec[i64]`. Any smallest team is accepted,
and the arms may find different ones, so the output gives each team's
size and whether it is sufficient, never the team itself.

## Approaches

Each arm but the search gives skill `i` the bit `1 << i`, so a person is
a mask of their skills and a team covers the mask its members' masks
make together.

| file | mechanism |
|---|---|
| `smallest_sufficient_team.kara` ★ | `team[m]`, an `Option[Vec[i64]]` for every mask, the smallest team found whose skills make `m`, grown one person at a time over every mask already reached. O(people * 2^skills) steps, each copying a team of at most `skills` people |
| `smallest_sufficient_team_parent.kara` | the same growth without copying teams: `size[m]` and `from[m]`, the mask it grew from and the person who grew it, and the team read back from the full mask at the end. O(people * 2^skills) |
| `smallest_sufficient_team_bfs.kara` | a breadth-first search over masks from the empty one, each step adding a person, so the full mask is first reached by a smallest team; each mask queued once, with where it came from. O(people * 2^skills) |
| `smallest_sufficient_team_search.kara` | a search: the lowest skill still lacking must come from someone, so each person who has it is tried in turn, and a branch stops once it is as large as the best team found. People whose skills another's include are dropped first. Exponential at worst |
| `smallest_sufficient_team_sparse.kara` | the ★ arm's growth over a `Map` holding only the masks reached, each person tried with every team in a copy of the map taken before they join any. O(people * masks reached) |
| `smallest_sufficient_team_solution.kara` | a Rust solution as LeetCode's Rust users write it (`impl Solution`, a `HashMap<&str, usize>` from skill to bit, `vec![None; n]` of `Option<Vec<i32>>` teams, `1usize <<`, `map_or`), carried to Kāra by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 11 lines: the size of the team found and
whether it is sufficient for LeetCode's two examples and six more (one
skill, people with none, one person with every skill, two who overlap, a
pair that beats three, and many people alike), then over 500 random
problems of up to 10 skills and 20 people, each skill held at chance 10%
to 40%, the sizes summed and a checksum (`500 random problems: team
sizes total 1297, checksum 341201469`), and two of LeetCode's largest:
16 skills and 60 people, each skill held at chance 5% and 20%.
`smallest_sufficient_team.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every set of people, taken as a list of who is in it, and the
size of the smallest whose skills, looked up by name, include every
required one. It checks 2000 problems in four kinds of 500: up to 8
people over up to 6 skills, each held at 30%; up to 8 people over up to
8 skills at 15%, so teams are large; one to three people over up to 6
skills at 50%; and up to 8 people each holding a run of up to 4 of 8
skills next to each other, so that teams cover the skills as intervals
cover a line. Every random choice is drawn before any arm answers.

| | property |
|---|---|
| P1 | the team's size is the literal one |
| P2 | the team names each person once, every one of them real, and between them has every skill |
| P3 | the people listed last first give a team of the same size |
| P4 | the skills renamed and listed last first give a team of the same size |
| P5 | two people of the team made one person, the other's place left empty, give a team one smaller |
| P6 | a person not on the team left out gives a team of the same size |

P5 holds because a smaller team still would, with the merged person
split back into two, be a team smaller than the smallest. All 63,840
checks pass on every arm: `2000 problems: checksum 831956906, 63840
checks over 6 arms: 0 failures`. A Python reading of the same problems,
trying the sets of people from the smallest up, gives the same checksum.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run` with `KARAC_HASH_SEED=1`
(the sparse arm walks a `Map`), each failing the same way under both.
All thirty are caught. Fifteen are kept, no two failing the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a team replaced by a larger one | P1 566, P3 586, P5 128 |
| M2 | ★: every person taken to have the first skill | P1 427, P2 527, P4 452 |
| M3 | ★: the first team for a mask kept, never a smaller one | P1 47, P3 91 |
| M4 | parent: a person's mask from their first skill alone | P1 1255, P2 1243, P4 124, P5 116 |
| M5 | parent: a team of every person taken as unreachable | P1 401, P2 401, P6 285 |
| M6 | parent: a shared skill taken away, not kept | P1 553, P2 457, P5 84 |
| M7 | bfs: a stack in place of the queue | P1 291, P3 422, P5 130, P6 15 |
| M8 | bfs: a person's mask from their last skill alone | P1 1263, P2 1229, P5 140 |
| M9 | bfs: the search stopped once all but the last skill are had | P1 171, P2 273, P3 310, P4 335, P5 20 |
| M10 | search: only the first person with the lowest skill tried | P1 59, P3 93, P4 82, P5 15 |
| M11 | search: a person never taken back off the team | P1 76, P2 18, P3 106, P4 102, P5 33 |
| M12 | sparse: a reached mask never given a smaller team | P1 196, P3 322, P5 133, P6 43 |
| M13 | sparse: a team replaced only by one two smaller | P1 185, P3 296, P5 123, P6 42 |
| M14 | solution: a team replaced by a larger one | P1 2000, P2 2000, P3 612 |
| M15 | solution: every team starting with person 0 | P1 2000, P2 1408, P5 427 |

P1 catches all fifteen, P5 eleven, P2 and P3 nine each, P4 five and P6
four. P3 to P6 together catch all fifteen. P3 sees the edits that make a
team depend on the order the people come in: an arm that keeps the first
team it finds for a mask, or tries only the first person with a skill,
finds a different one when the order is reversed, and sometimes a larger
one. P4 sees the edits that treat one skill apart from the others, the
first or the last, since renaming and reordering the skills moves which
one that is. P5 sees an arm that cannot find a team as small as the
smallest, since the merged person makes a smaller team the right answer.
P6 sees the edits whose answer depends on people the team does not
use: leaving one out shortens the list and moves the people after it.

P2 alone catches five edits that are not kept, each putting the wrong
people on a team of the right size: the ★ arm adding the last person in
place of each, the bfs arm recording each person by their place from
the end, the search arm putting the next person on, the sparse arm
putting the mask on rather than the person, and the solution arm adding
person 0 in place of each. Of the ten others, four fail alike in pairs:
the parent arm recording every mask as grown from the empty one and the
bfs arm taking a person's mask as the team's both read back a team of
one person, and the parent arm stopping its read back a person early and
the sparse arm adding a person twice both miss by one on every problem.
The search arm keeping the first team it finds fails as M10. Three fail
nearly as kept edits: the sparse arm replacing a team by a larger one as
M1, the solution arm replacing a team only by one two smaller as M3, and
the solution arm taking every person to have the first skill as M2. The
★ arm never requiring the last skill stops: a person who has it makes a
mask beyond the table, and the index is out of bounds. The search arm
taking a team without the first skill fails in a way of its own but was
not needed.

## Verification

Every arm prints the same output as `smallest_sufficient_team.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
every arm and the differential. `karac check --output=json` reports
nothing on any file, and `karac fix` has nothing to apply.

The kata found one gap, now fixed. The ★, parent, bfs, search and
sparse arms were written as Kāra, the solution arm as Rust writes it.
`karac fix` carried the solution arm to a clean check in three rounds:
the `use` line dropped, `<..>` to `[..]`, `HashMap<&str, usize>` to
`HashMap[Str, usize]` and `::` to `.`; then `struct Solution {}`
declared and `HashMap` to `Map`; then `usize` to `i64`, `1usize` and
`0usize` to `1` and `0`, `vec![None; full + 1]` to `Vec.filled(full + 1,
None)` and `vec![]` to `Vec.new()`. The gap was in the sparse arm, which
grows each team with `for (m, team) in best.clone() { let mut next =
team; next.push(p); best[grown] = next; }`, Rust's way to change a copy
of an element it owns. A bare `for` borrows the collection (§4.6), so
`next` is a `ref` to the element. The fix put a `.clone()` at the move,
`best[grown] = next.clone()`, which left `next.push(p)` writing through
the `ref`: an error nothing fixed. A move of such a `let mut` copy now
takes the loop's `.into_iter()` when nothing uses the collection after
the loop, as a move of the element itself does, and otherwise a
`.clone()` where `next` is bound, which the write through `next` asks
for too (B-2026-11-11-84). The sparse arm took the first, in one
round.

## Benchmarks

The bench builds 8 random problems of LeetCode's largest once, 16
skills and 60 people, each skill held at chance 20%. Each of 8 rounds
gives one person in every problem a skill they lack or takes one they
have, hands any skill nobody has to the next person, and solves the
problem with the ★ arm: 64 solves over 2^16 masks. Every implementation
prints `8 rounds over 8 problems of 16 skills and 60 people: team sizes
total 248, checksum 939597609`, the checksum over each team's members in
order, which the ★ arm fixes. Kāra keeps each mask's team as an
`Option[Vec[i64]]`, Rust as an `Option<Vec<i64>>`, Go as a slice, nil
until reached, and Python as a list or `None`; each makes a new one for
every smaller team found. C keeps every team in a row of a fixed table
of 2^16 rows of 16 with its length, copied with `memcpy`, and finds a
skill's bit by comparing its name with each required one.

Timings on a 4-core container (Intel Xeon, 2.1 GHz), twelve interleaved
runs of each compiled program and one of Python, with karac `afb930a6c1`
on LLVM 22. karac builds for the x86-64-v3 baseline, so the C and
overflow-checked Rust programs are also built at `-march=x86-64-v3`:

| | time | median |
|---|---|---|
| C (`clang -O3 -march=x86-64-v3`) | 0.230 to 0.311 s | 0.276 s |
| C (`clang -O3`) | 0.230 to 0.308 s | 0.283 s |
| Go | 0.388 to 0.470 s | 0.428 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.448 to 0.581 s | 0.530 s |
| Rust (`rustc -O`) | 0.467 to 0.582 s | 0.545 s |
| Rust (`rustc -O -C overflow-checks=on -C target-cpu=x86-64-v3`) | 0.482 to 0.626 s | 0.569 s |
| Kāra (`karac build`) | 0.465 to 0.614 s | 0.574 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.456 to 0.698 s | 0.587 s |
| Python | 8.68 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here and
gives the same binary, byte for byte, so its two rows differ by noise
alone. Kāra takes about 1.1x Rust's time, 1.4x Go's and 2.1x C's. C
allocates nothing while it solves; Kāra and Rust allocate each new team
and free the one it replaces, where Go leaves the old one to its
collector. The gaps to Go and C were not traced further. Python takes
about 15x Kāra's time.
