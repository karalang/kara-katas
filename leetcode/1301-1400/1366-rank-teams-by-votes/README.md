# 1366. Rank Teams by Votes

In a special ranking system, each voter gives a rank from highest to
lowest to all teams participating in the competition.

The ordering of teams is decided by who received the most position-one
votes. If two or more teams tie in the first position, we consider the
second position to resolve the conflict, if they tie again, we continue
this process until the ties are resolved. If two or more teams are
still tied after considering all positions, we rank them alphabetically
based on their team letter.

You are given an array of strings `votes` which is the votes of all
voters in the ranking systems. Sort all teams according to the ranking
system described above.

Return a string of all teams sorted by the ranking system.

```
votes = ["ABC","ACB","ABC","ACB","ACB"]  ->  "ACB"
votes = ["WXYZ","XYZW"]                  ->  "XWYZ"
votes = ["ZMNAGUEDSJYLBOPHRQICWFXTVK"]   ->  "ZMNAGUEDSJYLBOPHRQICWFXTVK"
```

**Constraints:** `1 <= votes.length <= 1000`, `1 <= votes[i].length <=
26`, `votes[i].length == votes[j].length`, `votes[i][j]` is an English
uppercase letter, all characters of `votes[i]` are unique, and all the
characters that occur in `votes[0]` also occur in `votes[j]`.

Each arm is `fn rank_teams(votes: Vec[String]) -> String`.

## Approaches

| file | mechanism |
|---|---|
| `rank_teams.kara` ★ | how many votes put each team in each place counted, then the teams sorted by those rows of counts, compared as vectors with more first, and by letter where every count ties. O(V T + T² log T) for V votes of T teams |
| `rank_teams_keys.kara` | each team given a key string that sorts as the ranking does: for each place, how many votes it did not get there in four digits, and its letter last; the keys sorted as strings |
| `rank_teams_insertion.kara` | the counts as in the ★ arm, then the teams put in order by insertion sort, one team ahead of another at the first place where their counts differ. O(V T + T³) |
| `rank_teams_beaten.kara` | the counts kept in a `Map` from team to row; every pair of teams compared once and each team's rank the number of teams ahead of it, then each written straight into its place |
| `rank_teams_solution.kara` | a Rust solution as LeetCode's Rust users write it (`teams.sort_by(\|a, b\| cnt[y].cmp(&cnt[x]).then(a.cmp(b)))` over a `vec![vec![0; n]; 26]`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 2 lines: LeetCode's three examples, every
order of three teams once, all tied, and one team (`ACB XWYZ
ZMNAGUEDSJYLBOPHRQICWFXTVK ABC M`); and 2000 random elections of up to
26 teams and 40 votes folded into a checksum (`2000 random elections: 75
won by A, checksum 425450293`). `rank_teams.py` mirrors the ★ arm, and
its output is byte-identical. Every arm gives the same output under
`karac __mir-run`, `karac run` and `karac __mir-llvm-run`.

The Mend loop: the keys arm checks clean. The ★ arm takes 2 fixes:
`vote.bytes()` is a slice, so `.enumerate()` and `.collect()` on it
become `.iter().enumerate()` and `.iter().collect()`. The insertion and
beaten arms take 2 each: `let (x, y) = (counts[a], counts[b])` would
move two rows out of the table (E0515), and the fix borrows them as
`(ref counts[a], ref counts[b])`. The Rust solution takes 14: `struct
Solution;` becomes `struct Solution {}`, `Vec<..>` becomes `Vec[..]`,
`vec![vec![0; n]; 26]` becomes `Vec.filled(26, Vec.filled(n, 0))`, `for
v in &votes` becomes `for v in ref votes`, `c as u8` on a char becomes
`c as u32 as u8`, and the closure's `*a` and `&cnt[x]` lose their
dereference and borrow. Every arm matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement
read literally: the teams split by how many first places each got, most
first, each part split again by the next place, and a part still whole
after the last place put in letter order. It checks the examples, 1500
random elections of up to 4 teams, where ties are common, and 500 of up
to 26, each with up to 40 votes.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | the votes taken in the opposite order, the same ranking |
| P3 | the teams renamed to the alphabet's last letters, in the same letter order, the ranking renamed |
| P4 | every vote cast twice, the same ranking |
| P5 | one more vote cast in the ranking's own order, the same ranking |
| P6 | the ★ arm's ranking |

All 60,150 checks pass on every arm: `2005 cases: checksum 213541138,
60150 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run` and `karac __mir-llvm-run`. Python, splitting by place counts the
same way, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash, and no two
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: full ties left in the first vote's order | P1 40, P2 59, P6 160 |
| M2 | ★: fewer votes ranked first | P1 1574, P5 829, P6 6296 |
| M3 | keys: the counts written without padding | P1 219, P4 375, P5 162, P6 219 |
| M4 | keys: only first places counted | P1 599, P6 599 |
| M5 | insertion: full ties in reverse letter order | P1 85, P6 85 |
| M6 | insertion: a team moved up one place at most | P1 729, P2 864, P6 729 |
| M7 | beaten: each comparison credited to the winner | P1 1611, P5 830, P6 1611 |
| M8 | beaten: first places skipped | P1 1527, P5 720, P6 1527 |
| M9 | solution: the first vote not counted | P1 683, P2 733, P4 510, P6 683 |
| M10 | solution: each vote counted one place later | P1 1531, P5 827, P6 1531 |

P1 and P6 kill all ten, P5 five, P2 three, P4 two, and P3 none. Every
arm compares letters only by their order, so renaming them in the same
order (P3) changes nothing for any edit; it stands for an arm that
would. Taking the votes in the opposite order (P2) catches the edits
that read the first vote specially: full ties left in its order (M1),
the insertion that moves a team one place at most from where the first
vote put it (M6), and the first vote not counted (M9). Casting every
vote twice (P4) catches the unpadded keys (M3), whose counts gain a
digit and sort as strings differently, and the first vote not counted
(M9), which the doubling counts once. One more vote in the ranking's
own order (P5) must leave the ranking as it is, and catches the edits
that rank by the wrong counts: fewer first places ahead (M2), a
comparison credited the wrong way (M7), first places skipped (M8),
votes counted a place late (M10), and unpadded keys (M3). Ties broken in
reverse letter order (M5) and only first places counted (M4) are caught
only by the literal reading and the ★ arm.

## Benchmarks

The bench builds 20 elections of 1000 votes over all 26 teams, the
constraints' most, once; then makes 3000 rounds, each swapping two
places of one vote, all drawn from the checksum so far, and ranking that
election with the ★ arm. Every implementation prints `3000 rounds over
20 elections of 1000 votes: checksum 265578368`. The work is counting
26,000 places and sorting 26 teams by rows of 26 counts, the same in
every language; each round also copies the changed vote into a new
string, as the Kāra does.

BENCHTAB
