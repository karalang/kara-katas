# 1733. Minimum Number of People to Teach

On a social network consisting of `m` users and some friendships between
users, two users can communicate with each other if they know a common
language.

You are given an integer `n`, an array `languages`, and an array
`friendships` where:

- There are `n` languages numbered `1` through `n`,
- `languages[i]` is the set of languages the `i`th user knows, and
- `friendships[i] = [ui, vi]` denotes a friendship between the users
  `ui` and `vi`.

You can choose **one** language and teach it to some users so that all
friends can communicate with each other. Return *the* ***minimum***
*number of users you need to teach.*

Note that friendships are not transitive, meaning if `x` is a friend of
`y` and `y` is a friend of `z`, this doesn't guarantee that `x` is a
friend of `z`.

```
n = 2, languages = [[1],[2],[1,2]], friendships = [[1,2],[1,3],[2,3]]                 ->  1
n = 3, languages = [[2],[1,3],[1,2],[3]], friendships = [[1,4],[1,2],[3,4],[2,3]]     ->  2
```

**Constraints:** `2 <= n <= 500`; `languages.length == m`;
`1 <= m <= 500`; `1 <= languages[i].length <= n`;
`1 <= languages[i][j] <= n`; `1 <= ui < vi <= languages.length`;
`1 <= friendships.length <= 500`; all the tuples `(ui, vi)` are unique;
`languages[i]` contains only unique values.

## Approaches

| file | mechanism |
|---|---|
| `teach.kara` ★ | only one language is taught, so a friendship whose users share one needs nothing and one that shares none needs both its users to know the taught language. Each user's languages go in a `Set`, `is_disjoint` finds the stuck friendships, their users are gathered in a `Set`, and the language most of them already know is taught to the rest. O(f k + u k) for f friendships, u users and k languages a user knows |
| `teach_grid.kara` | a table of flags, `knows[u][l]`; a friendship is stuck when no language has both its users' flags, and each language's count of stuck users who know it is read down its column. O(f n + u n) |
| `teach_sorted.kara` | each user's languages sorted, two users sharing one when a merge of their lists finds an equal pair; the stuck users' languages gathered into one sorted list, whose longest run of one language is the most of them that know it. O(f k + s k log(s k)) for s stuck users |
| `teach_solution.kara` | a Rust solution as LeetCode's Rust users write it, a `HashSet<i32>` of languages per user, `langs[a].is_disjoint(&langs[b])`, the stuck users in a `HashSet<usize>` and a `vec![0; n as usize + 1]` of counts, carried to Kāra by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 7 lines: LeetCode's two examples, friends who
all share a language, and a ring of four who share none; then the users
taught summed and a checksum for 3000 random problems of up to 5
languages and 6 users, 300 of up to 50 languages and 100 users, and 5
of up to 500 languages and 500 users, LeetCode's limits, each user
knowing 1 to 3 languages and the friendships distinct. `teach.py`
mirrors the ★ arm and its output is byte-identical.

```
1
2
0
3
3000 problems of up to 5 languages and 6 users: teachings sum to 1424, checksum 353423794
300 problems of up to 50 languages and 100 users: teachings sum to 11239, checksum 130027896
5 problems of up to 500 languages and 500 users: teachings sum to 524, checksum 50722911
```

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for every language and every set of users, those users are
taught that language, and the smallest set after which every pair of
friends shares a language is the answer. It checks 3000 random problems
of 1 to 4 languages and 2 to 6 users, each knowing 1 or 2 of them, each
pair of users friends with a chance of 1 in 2. Every case is drawn
before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the users numbered from the other end give the same answer |
| P3 | the languages numbered from the other end give the same answer |
| P4 | a new user who knows every language, a friend of everyone, changes nothing |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 789748241, 60000 checks
over 4 arms: 0 failures` under every lane in Verification, and a Python
reading of the statement, every `itertools.combinations` of the users
taught each language, gives the same checksum. On a failure it prints
the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. M7, M9 and M10 each fail the same
1254 problems, every one whose answer is not 0.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a friendship stuck when its users share a language, not when they share none | P1 1076, P4 1034, P5 1076 |
| M2 | ★: only the first user of a stuck friendship gathered | P1 1133, P5 1133 |
| M3 | ★: language 1 always the one taught | P1 454, P3 618, P5 454 |
| M4 | grid: the last language left out of the shared check | P1 37, P3 59, P4 13, P5 37 |
| M5 | grid: every user who knows a language counted, stuck or not | P1 2590, P4 3000, P5 2590 |
| M6 | sorted: the merge steps on the larger head, not the smaller | P1 115, P3 106, P4 116, P5 115 |
| M7 | sorted: a new run of one language counted from 0, not 1 | P1 1254, P5 1254 |
| M8 | sorted: each user's languages left unsorted | P1 55, P3 83, P5 55 |
| M9 | solution: the language fewest stuck users know taught | P1 1254, P5 1254 |
| M10 | solution: each friendship read as its first user with itself | P1 1254, P5 1254 |

## Benchmarks

The bench draws 50 random problems of LeetCode's largest size, 500
users each knowing 1 to 10 of 500 languages and 500 distinct
friendships, all of them first, then answers each 200 times by the ★
arm in all five languages; each answer builds its sets anew. Every
implementation prints `50 problems of 500 users, 500 languages and 500
friendships, 200 rounds: teachings sum to 4130200, checksum 456761257`.
C has no set: its mirror keeps each user's languages in a table of 32
slots and the stuck users in one of 1024, probed linearly with the key
hashed by one multiply, which is less work than Kāra's SipHash `Set`,
Rust's SipHash `HashSet` or Go's `map`. The C build also runs clean
under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9b0b5eb92c` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.795 s |
| Rust (`rustc -O`) | 1.061 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.097 s |
| Kāra (`karac build`) | 1.811 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 1.882 s |
| Go | 2.217 s |
| Python | 4.1 s |

The sequential Kāra build takes 1.77x Rust's time and 1.72x that of Rust
with overflow checks on, the equal-safety comparison (BENCHMARKS.md). C
is the fastest here at 0.795 s.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here:
its user time is not above its real time (1.732 s and 1.741 s on one
run).

## Verification

All four arms print the same output as `teach.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `9b0b5eb92c`.

## Writing it

The ★ arm asks whether two users share a language with
`known[u].is_disjoint(known[v])`, as Rust's `HashSet` and Python's
`set.isdisjoint` do. Kāra's `Set` had no such method, only `union`,
`intersection` and `difference`, and `karac check` refused the call.
Since kara `93fd9b2078` (B-2026-11-20-50) `Set` and `SortedSet` have `is_disjoint`,
`is_subset` and `is_superset`, each reading the other set without
taking it, and the arm checked clean as written. The grid arm checked
clean as first written.

The sorted arm took one `karac fix` of 6 edits: its merge started from
`let (mut i, mut j) = (0, 0)`, Rust's pattern, which E0001 names and the
fix writes `let mut (i, j) = (0, 0)`; and `total`, `best` and `run`,
plain `0`s that meet the `i32` answer only through `+=` and `max`, were
declared `: i32`.

LeetCode's Rust template took one `karac fix` of 38 edits:
`struct Solution {}` added, `use std::collections::HashSet;` deleted,
`Vec<..>` and `HashSet<..>` written `Vec[..]` and `Set[..]`, `usize`
written `i64`, `vec![0; n as usize + 1]` written `Vec.filled(n as i64 +
1, 0i32)`, `&friendships`, `&need` and `&langs[u]` walked as `ref`,
the `for &u` and `for &l` patterns written plain, `&langs[b]` passed as
`langs[b]`, and `languages.into_iter()` written
`languages.clone().into_iter()`, since the parameter borrows.
`is_disjoint`, `collect()` into a `Vec[Set[i32]]` and `*cnt.iter().max().unwrap()`
carried over as written.

The differential checked clean as first written. `arm_name` in it
indexes a list of string literals for a `Str`, as #1662's does
(B-2026-11-19-131).
