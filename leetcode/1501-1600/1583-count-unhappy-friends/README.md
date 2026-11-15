# 1583. Count Unhappy Friends

You are given a list of `preferences` for `n` friends, where `n` is
always even.

For each person `i`, `preferences[i]` contains a list of friends sorted
in the order of preference. In other words, a friend earlier in the list
is more preferred than a friend later in the list. Friends in each list
are denoted by integers from `0` to `n - 1`.

All the friends are divided into pairs. The pairings are given in a list
`pairs`, where `pairs[i] = [x_i, y_i]` denotes `x_i` is paired with `y_i`
and `y_i` is paired with `x_i`.

However, this pairing may cause some of the friends to be unhappy. A
friend `x` is unhappy if `x` is paired with `y` and there exists a friend
`u` who is paired with `v` but:

- `x` prefers `u` over `y`, and
- `u` prefers `x` over `v`.

Return the number of unhappy friends.

```
n = 4, preferences = [[1,2,3],[3,2,0],[3,1,0],[1,2,0]], pairs = [[0,1],[2,3]]  ->  2
n = 2, preferences = [[1],[0]],                         pairs = [[1,0]]        ->  0
n = 4, preferences = [[1,3,2],[2,3,0],[1,3,0],[0,2,1]], pairs = [[1,3],[0,2]]  ->  4
```

**Constraints:** `2 <= n <= 500`; `n` is even;
`preferences.length == n`; `preferences[i].length == n - 1`;
`0 <= preferences[i][j] <= n - 1`; `preferences[i]` does not contain
`i`; all values in `preferences[i]` are unique;
`pairs.length == n / 2`; `pairs[i].length == 2`; `x_i != y_i`;
`0 <= x_i, y_i <= n - 1`; each person is contained in exactly one pair.

## Approaches

| file | mechanism |
|---|---|
| `friends.kara` ★ | each friend's rank of every other in an `n x n` table, and each friend's partner; `x` with partner `y` is unhappy when some `u` among the first `rank[x][y]` of its list (by `take`) ranks `x` above its own partner. O(n^2) |
| `friends_pairs.kara` | every two pairs `(x, y)` and `(u, v)` tried in all four orientations, each preference found by `position` in the list each time, the unhappy friends marked in a `Vec[bool]`. O(n^3) |
| `friends_sets.kara` | each friend's `Set` of the friends it lists before its partner, by `take_while`; `x` is unhappy when some `u` in its set has `x` in its own. O(n^2) expected |
| `friends_solution.kara` | LeetCode's Rust template (an `n x n` `order` table and a `matched` list over `usize`), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples and two more
(one with no unhappy friend, one of 6), then the unhappy friends and a
checksum for 3000 random problems of up to 6 friends, 300 of up to 60 and
3 of up to 500, every list a random order of the others and the pairs a
random pairing. `friends.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: for each `x`, its partner `y` found in `pairs`, then every
pair tried both ways as `(u, v)` with each preference found by walking
the list. It checks 3000 problems of 2, 4, 6 or 8 friends, every random
choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the pairs listed in reverse order, each pair flipped, leave the answer |
| P3 | every friend renumbered `x` to `x + 1` (mod `n`) leaves the answer |
| P4 | a new pair who each list the other first, and come last in every other list, leaves the answer |
| P5 | each list reversed before the partner and reversed after it leaves the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 174118608, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

The first M1 let the ★ arm's `take` reach the partner too; it was
equivalent, since the partner never ranks `x` above itself, and was
replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the friend `x` likes best never tried | P1 1563, P5 1154, P6 1563 |
| M2 | ★: `u` ranks `x` below its partner in place of above | P1 1783, P6 1783 |
| M3 | ★: a friend counted once for every `u`, not once | P1 1419, P6 1419 |
| M4 | pairs: either preference enough, not both | P1 1967, P6 1967 |
| M5 | pairs: the second pair tried one way round only | P1 1432, P2 1413, P6 1432 |
| M6 | pairs: `prefers` true up to one place past | P1 1907, P4 1212, P5 659, P6 1907 |
| M7 | sets: each set skips the friend liked best | P1 1772, P5 1060, P6 1772 |
| M8 | sets: unhappy when every `u` in the set agrees, not some | P1 2617, P4 3000, P6 2617 |
| M9 | template: the scan starts at the second friend | P1 1563, P5 1154, P6 1563 |
| M10 | template: only the first of each pair given a partner | P1 1415, P2 1517, P3 1530, P5 1352, P6 1415 |

## Benchmarks

The bench draws 40 problems of 500 friends first, every list a shuffle
of the others and the pairs a shuffle cut in twos, then counts each by
the ★ arm, in all five languages. Every implementation prints `40
problems of 500 friends: unhappy 19923, checksum 343547086`. Every list,
rank row and pair is its own allocation in every language.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `76e5a13ad` on LLVM 22:

| | median |
|---|---|
| Kāra (`karac build`) | 0.105 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.112 s |
| C (`clang -O3`) | 0.120 s |
| Rust (`rustc -O`) | 0.137 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.137 s |
| Go | 0.263 s |
| Python | 4.6 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is below its real time (0.084 s and 0.132 s on one run).

Kāra is 0.82x Rust under overflow checks by median. Most of the time in
every lane is drawing the 20000 shuffled lists; the count itself walks a
500 x 500 table forty times.

## Verification

All four arms print the same output as `friends.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`76e5a13ad`.

## Writing it

The ★ and sets arms were written in Kāra and checked as written. The
pairs arm bound `let list = preferences[who];`, which is refused as a
move out of an index; `karac fix` made it `ref preferences[who]`. The
differential's literal reading wrote `list: ref Vec[i64]` on a helper,
and `karac fix` dropped the redundant `ref`.

The Rust template took four rounds of `karac fix`:

1. twenty-two edits: the `Vec<..>` types to `Vec[..]`, `for pair in
   &pairs` to `for pair in ref pairs`, the `|&x|` pattern to a plain
   name, and `Solution::` to `Solution.`;
2. the inner `vec![0; n]` of `vec![vec![0; n]; n]` and `vec![0; n]` to
   `Vec.filled(n, 0)`, and the wrapper's `as i64` dropped;
3. the outer `vec![..; n]` to `Vec.filled(n, ..)`, and each `as usize`
   to `as i64`;
4. the now redundant `as i64` on `preferences[i][j]` in an index dropped.

The nested `vec!` takes two rounds, inner then outer. It then checks and
agrees with no hand edit.
