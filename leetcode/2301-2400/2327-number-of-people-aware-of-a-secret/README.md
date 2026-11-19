# 2327. Number of People Aware of a Secret

On day `1`, one person discovers a secret.

You are given an integer `delay`, which means that each person will
**share** the secret with a new person **every day**, starting from
`delay` days after discovering the secret. You are also given an
integer `forget`, which means that each person will **forget** the
secret `forget` days after discovering it. A person **cannot** share
the secret on the same day they forgot it, or on any day afterwards.

Given an integer `n`, return *the number of people who know the secret
at the end of day* `n`. Since the answer may be very large, return it
**modulo** `10^9 + 7`.

```
n = 6, delay = 2, forget = 4  ->  5
n = 4, delay = 1, forget = 3  ->  6
```

**Constraints:** `2 <= n <= 1000`; `1 <= delay < forget <= n`.

Everyone who learns the secret on the same day acts alike, so the
count learning it each day is all there is to keep. On a day `d` the
people sharing are those who learned it from `d - forget + 1` to
`d - delay`, a window that moves one day at a time, and at the end of
day `n` the people who know it are those who learned it in the last
`forget` days. O(n).

## Approaches

| file | mechanism |
|---|---|
| `secret.kara` ★ | `learned[d]`, the people learning on day `d`, from a running count of the sharers that gains the day `delay` back and loses the day `forget` back |
| `secret_naive.kara` | each day's newcomers the window of earlier days added up afresh. O(n forget) |
| `secret_prefix.kara` | prefix sums: `before[d]` everyone who learned by day `d`, the newcomers two of them subtracted, each index held at 0 from below, and the answer `before[n] - before[n - forget]` |
| `secret_ages.kara` | by age: a `VecDeque` of how many learned 0 to `forget - 1` days ago; each day the oldest drop off the back, a new front is pushed, and everyone of age `delay` or more tells one newcomer. O(n forget) |
| `secret_iter.kara` | iterators: the days `fold`ed into the list of newcomers, each day's the window that `skip` and `take` cut from it, summed, and the answer the last `forget` days `rev`ersed off its end |
| `secret_solution.kara` | LeetCode's Rust template: the `i32` arguments turned to `usize`, a `dp` of newcomers summed over each day's window by a nested loop, a `const MOD` in the body, and an `i32` answer; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's two examples; 2 days with
a delay of 1; 1000 days with a delay of 1 and nobody forgetting, which
is `2^999` modulo `10^9 + 7`; 1000 days where the first person shares
once, on the last; 1000 days with a delay of 3 and a forget of 7; then
2000 random cases of 2 to 300 days, with a checksum and the answers in
all. `secret.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 9 edits.
`check` first reports two errors, each with its edit: `struct
Solution;` to `struct Solution {}`, and `Solution::` to `Solution.` in
the harness's wrapper. The other seven follow from those: the three
`as usize` to `as i64`, the type of an index; `vec![0i64; n + 1]` to
`Vec.filled(n + 1, 0)`, and the suffixes of its `0i64` and the
answer's dropped; and the wrapper's `as i64` on the `i32` answer. The
`const MOD: i64 = 1_000_000_007;` inside the method stands as Kāra, and
so does `ans as i32`.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every person is kept as the day they learned the secret, and
each day every person whose age is from `delay` to `forget - 1` days
tells one newcomer, who joins the list; at the end of day `n` the
people younger than `forget` days are counted. No counts by day and no
window. That walk is run up to 16 days, up to 32768 people. It checks
300 random cases of 2 to 16 days; then 30 of 17 to 30; then 30 of 31 to
1000, each with `forget` from 2 to `n` and `delay` from 1 to
`forget - 1`. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | up to 16 days, the answer is the literal reading's |
| P2 | the answer is below `10^9 + 7`, and up to 30 days, where nothing has been reduced, from 1 to `2^(n - 1)` |
| P3 | up to 30 days, forget one day later, where that is not past `n`: no fewer people |
| P4 | up to 30 days, delay one day shorter, where that is not below 1: no fewer people |
| P5 | delay 1 and forget `n`: `2^(n - 1)` modulo `10^9 + 7`; and forget `delay + 1`: 2 when `delay` divides `n - 1`, and 1 otherwise |
| P6 | each arm agrees with at least three of the other five |

P2's bounds hold because whoever learns the secret tells someone
`delay` days later, so the newest person learned it fewer than `delay`
days before the end, and still knows it; and at most everyone shares
every day, doubling the people. P5's first form is that doubling: with
a delay of 1 and nobody forgetting by day `n`, everyone tells one
newcomer every day. In its second, everyone shares exactly once, on
the day `delay` after learning, and forgets the next day, so one
person learns it on each day `1 + k delay`, and the last `delay + 1`
days hold two of them when `delay` divides `n - 1`.

The differential prints `360 cases: checksum 549842044, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and counts the people by the day they learned
it, in a `dict`. On a failure it prints the first ten and then the
count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the first person never sharing | P1 300, P2 261, P3 96, P4 96, P5 360, P6 360 |
| M3 | ★: sharers lost a day early | P1 186, P5 219, P6 245 |
| M5 | ★: two people knowing on day 1 | P1 300, P2 65, P5 360, P6 360 |
| M7 | naive: sharers starting a day early | P1 177, P5 229, P6 229 |
| M10 | naive: the first person never sharing | P1 300, P2 261, P5 360, P6 360 |
| M11 | naive: the sharers carried from day to day | P1 267, P2 70, P5 337, P6 327 |
| M14 | prefix: each day's total its own newcomers alone | P1 297, P2 212, P3 112, P4 41, P5 360, P6 357 |
| M15 | prefix: the aware counted over one day fewer | P1 216, P5 360, P6 256 |
| M16 | prefix: one more person counted before day 1 | P1 300, P2 330, P5 360, P6 360 |
| M17 | ages: a newcomer more each day | P1 300, P2 82, P5 360, P6 360 |
| M18 | ages: everyone forgetting a day early | P1 300, P2 131, P5 360, P6 360 |
| M20 | ages: the newest not counted | P1 238, P5 360, P6 284 |
| M22 | iter: the newest sharers a day late | P1 300, P2 98, P5 360, P6 360 |
| M23 | iter: each sharer telling two | P1 300, P2 130, P3 3, P5 360, P6 360 |
| M25 | iter: the aware counted over the first days | P1 179, P5 173, P6 236 |
| M27 | solution: the last day alone counted | P1 300, P2 71, P5 360, P6 360 |
| M30 | solution: the modulus one less | P5 30, P6 16 |

P5 and P6 kill all seventeen, P1 sixteen, P2 eleven, P3 three and P4
two. P5's closed forms hold for every case, so nearly any miscount
shows in one of them; P1 misses only the wrong modulus, which differs
only once a count passes `10^9 + 7`, past the 16 days the literal
reading reaches, and which P5's doubling over up to 1000 days catches.
P2 fails where an edit counts more than everyone sharing every day
could reach, or nobody: a person too many at the start, a newcomer too
many, each sharer telling two, and those that lose the newest people.
P3 and P4, forgetting later and sharing sooner, fail only where an
edit makes the count fall as the window grows: the first person never
sharing, so that the count at the end is 0 or 1 whatever the window,
each day's total its own newcomers alone, and, on three cases, each
sharer telling two.

Of the thirty-one, fourteen were not kept. Nobody forgetting while
sharing in the ★ arm (M2), sharers lost a day late in the prefix arm
(M13), nobody forgetting in the ages arm (M19) and a person sharing on
the day they forget in the template (M28) all fail alike, and none is
kept. The newest sharers a day late in the naive (M8) and prefix (M12)
arms fail as the iter arm's (M22); the aware counted over one day fewer
in the naive arm (M9) and iter arm (M24) as the prefix arm's (M15); the
iter arm's day 0 put in front (M26) and the template's last day not
counted (M29) as the ages arm's newest not counted (M20); the ages
arm's newcomers put in the oldest place (M21) and the template's oldest
sharer left out (M31) as the naive arm's first person never sharing
(M10). The ★ arm's aware counted over one day more (M4) and aware never
reduced (M6) fail apart from every kept one, and were left out to keep
three to an arm.

M7, M17, M23 and M27 replace edits that failed as others did: a person
sharing on the day they forget in the naive arm, a person sharing from
a day after the delay in the ages arm, sharers lost a day early in the
iter arm and the first sharing a day late in the template. Five more
replacements were tried and failed as kept ones or each other did: the
aware counted from day 1 in the naive arm, sharers starting a day early
in the ages arm, sharers kept a day longer and the aware counted over
one day more in the iter arm, and each sharer telling two in the
template.

## Verification

Every arm prints the same output as `secret.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★ arm takes 0.5 s, the prefix arm 0.9 s,
the naive arm 2.9 s and the template 4.1 s, each summing a window for
every day; the iter arm, which rebuilds its `Vec` at every fold step,
12 s; and the ages arm 63 s, as walking a `VecDeque` with `enumerate`
is slow in the interpreter, while its compiled build runs at twice the
naive arm's time. The differential takes 55 s there and 0.8 s under
`karac __mir-llvm-run`.

## Benchmarks

The bench draws 3000 pairs of `forget` from 2 to 990 and `delay` below
it once, then makes 10 passes, case `k` in pass `p` asked for
`990 + (k + p) % 11` days, with the ★ arm in all five languages. Every
implementation prints `10 passes over 3000 cases of up to 1000 days:
checksum 899869202`. Each keeps the counts as 64-bit integers in a
fresh array of `n + 1` for every call.

BENCHTAB
