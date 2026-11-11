# 2105. Watering Plants II

Alice and Bob want to water `n` plants in their garden. The plants are
arranged in a row and are labeled from `0` to `n - 1` from left to
right, where the `i`th plant is located at `x = i`.

Each plant needs a specific amount of water. Alice and Bob each have a
watering can, initially full. They water the plants in the following
way:

- Alice waters the plants in order from left to right, starting from the
  `0`th plant. Bob waters the plants in order from right to left,
  starting from the `(n - 1)`th plant. They begin watering the plants
  simultaneously.
- It takes the same amount of time to water each plant regardless of how
  much water it needs.
- Alice/Bob must water the plant if they have enough in their can to
  fully water it. Otherwise, they first refill their can (instantaneously)
  then water the plant.
- In case both Alice and Bob reach the same plant, the one with more
  water currently in his/her watering can should water this plant. If
  they have the same amount of water, then Alice should water this plant.

Given a 0-indexed integer array `plants` of `n` integers, where
`plants[i]` is the amount of water the `i`th plant needs, and two
integers `capacityA` and `capacityB` representing the capacities of
Alice's and Bob's watering cans respectively, return the number of times
they have to refill to water all the plants.

```
plants = [2,2,3,3], capacityA = 5, capacityB = 5   ->  1
plants = [2,2,3,3], capacityA = 3, capacityB = 4   ->  2
plants = [5], capacityA = 10, capacityB = 8        ->  0
```

**Constraints:** `n == plants.length`; `1 <= n <= 10^5`;
`1 <= plants[i] <= 10^6`; `max(plants[i]) <= capacityA, capacityB <= 10^9`.

The two walks are independent until they meet, so each gardener's
refills are a greedy walk over their own half. Only a middle plant, in a
row of odd length, depends on both: it goes to the fuller can, and it
costs a refill only when neither can holds enough. Which of the two
waters it never changes the count.

## Approaches

| file | mechanism |
|---|---|
| `watering.kara` ★ | two indices walking in from the ends, each can refilled first when short, and the middle plant, if any, settled with `a.max(b)`. O(n) |
| `watering_struct.kara` | a `struct Can` (capacity, water left, refills) per gardener with a `water` method (`mut ref self`) that refills when short and a `holds` method; the pairs `k` and `n - 1 - k` in a `for` loop, a middle plant to the fuller can |
| `watering_fold.kara` | each gardener's half folded with `fold`, (water left, refills) as the state: Alice's `plants[..n / 2]`, Bob's other half reversed with `rev()`; a middle plant settled from the two states left |
| `watering_rec.kara` | one call per pair, `step(plants, i, j, a, b, ..)`, returning the refills from there on, the meeting rules as its base cases and a `pour` helper returning (water left, refill) as a tuple; n / 2 calls deep, 5 * 10^4 at the constraints' largest |
| `watering_zip.kara` | the two ends at once: `zip` of `plants.iter()` and `plants.iter().rev()`, `take(n / 2)`, with the two cans and their capacities as `[i64; 2]` arrays and one inner loop over the gardeners |
| `watering_solution.kara` | LeetCode's Rust template (`plants: Vec<i32>`, `i32` capacities, `let (mut i, mut j) = (0usize, plants.len() - 1)`), carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 13 lines: LeetCode's three examples and five
more (a middle plant neither can water; a middle plant only Bob, holding
more, can; a refill at every plant; two plants each a full can; and no
refill at all), each row with its answer; then the total for 3000 random
rows of 1 to 50 plants needing 1 to 10, the cans holding the largest
need to 5 more, and a checksum of the answers; then the constraints'
largest, 10^5 plants: every one needing 10^6 with cans of 10^6, and
needs rising from 1 with cans of 10^9. `watering.py` mirrors the ★ arm
and its output is byte-identical.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: time steps, Alice at plant `t` and Bob at plant `n - 1 - t`
at step `t`, each refilling first when short, both stopping once they
have passed; at the same plant the one holding more waters it, Alice on
a tie. It checks 300 random rows of 1 to 12 plants needing 1 to 6, the
cans holding the largest need to 4 more; then 20 rows of 1 to 30 plants
needing up to 10^6 with cans up to 10^9; then 20 rows where every plant
needs exactly a full can. All 340 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer is 0 to n - 2 (0 for one plant): each gardener's first plant needs no refill |
| P3 | the row reversed and the cans swapped: the same answer |
| P4 | every need and both cans doubled: the same answer |
| P5 | both cans as large as the whole row's needs: no refill |
| P6 | each arm agrees with at least three of the other five |

Doubled, a wide row's cans reach 2 * 10^9, past the constraints but
within `i32`, so the Rust arm's adapter still passes them exactly. The
differential prints `340 rows: checksum 650170359, 12240 checks over 6
arms: 0 failures` under every lane in Verification; the checksum of the
literal answers was checked against a Python reading of the same rows
with the two-index walk. On a failure it prints the first ten and then
the count by property.

## Mutation testing

Thirty edits to the differential, five to each arm, each run under
`karac __mir-llvm-run` and `karac __mir-run`. Seventeen are kept, three
to each Kāra arm and two to the Rust-template arm. Each kept one is
killed, fails the same way under both backends and not by a crash, and
no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a middle plant to the emptier can | P1 49, P6 49 |
| M2 | ★: Alice refilling when exactly enough | P1 79, P2 23, P3 94, P6 79 |
| M3 | ★: Bob never using water | P1 219, P3 136, P6 219 |
| M4 | struct: a refill taking the plant's need twice | P1 115, P6 115 |
| M6 | struct: the innermost pair skipped | P1 112, P6 112 |
| M20 | struct: only the busier gardener's refills | P1 183, P3 6, P6 183 |
| M7 | fold: a refill's plant left unwatered | P1 162, P6 162 |
| M8 | fold: Bob walking his half outward | P1 14, P3 27, P6 14 |
| M9 | fold: a middle plant looked for in even rows | P1 139, P2 19, P3 47, P6 139 |
| M10 | rec: water never taken from the can | P1 234, P6 234 |
| M11 | rec: a middle plant never refilled for | P1 61, P6 61 |
| M12 | rec: the cans' sizes swapped at every step | P1 38, P6 38 |
| M14 | zip: both cans refilled to Alice's size | P1 47, P3 73, P6 47 |
| M15 | zip: the middle plant watered by both | P1 130, P2 49, P5 32, P6 130 |
| M29 | zip: half of each need poured | P1 206, P4 90, P6 206 |
| M17 | solution: the adapter swapping the cans | P1 87, P6 87 |
| M18 | solution: a middle plant refilled for when exactly enough | P1 24, P2 3, P5 24, P6 24 |

P1 and P6 kill all seventeen, P3 six, P2 four, P5 two and P4 one. Most
of these edits keep the answer within its bounds and unmoved by
scaling, so P1 carries the weight. P3 sees the edits that treat Alice
and Bob differently: one refilling early (M2), one never pouring (M3),
one walking outward (M8), both refilled to Alice's size (M14), the
middle plant sought in rows with none (M9), and only the busier
gardener's refills counted (M20), which a swap can hand to the other. P2 sees the edits that can
count a refill at a gardener's first plant or two for one plant (M2,
M9, M15, M18). P5 sees the edits that refill for a middle plant a full
can could water: the middle watered by both (M15) and a refill when the
fuller can holds exactly enough (M18). P4 sees only the edit that does
not scale: half of each need poured, rounded down (M29).

M1 is the rule the statement spends most words on, the middle plant to
the fuller can. Giving it to the emptier one changes the answer only
when the emptier can is short and the fuller is not: 49 of the 340 rows.

Of the thirty, thirteen were not kept, and none survives. Three fail as
a kept one: the struct arm's middle plant to the emptier can as M1; the
recursive arm's middle plant never watered as M11; and the recursive
arm's Bob refilling to Alice's size as M14. Ten are killed with checks
of their own but were left out because their arm keeps its share: the ★
arm's last plant never reached and Alice pouring Bob's plant's need;
the struct arm's Bob watering Alice's plants; the fold arm's Alice given
Bob's can and its refill when exactly enough; the zip arm's gardeners
short of each other's need and its middle judged by Alice's can alone;
and the Rust arm's Alice refilling to Bob's size, Bob pouring Alice's
plant's need, and Bob stepping two plants at a time.

## Verification

Every arm prints the same output as `watering.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.7 s to 1.3 s, and the
differential 0.4 s (timed while other work shared the machine).

`karac fix` carries the template in four rounds of 15, 1, 1 and 1 edits:
Rust's spellings (`Vec<..>` to brackets, `let (mut i, mut j)` to `let
mut (i, j)`, `&&` to `and`, `struct Solution;` to `struct Solution {}`,
the adapter's `&Vec` to `ref`, `Solution::` to `.` and its `&x` pattern
dropped); then the `0usize` suffix dropped, as Kāra writes indices in
`i64`; then the adapter's `ref` parameter to a bare one; then the
adapter's closing `as i64` dropped, as a cast `i32` widens without.

That last round is new. Kata 2103's adapter, `Solution.count_points(..)
as i64`, drew `lossless_cast` for the same cast, and this one, whose
call also casts its arguments, `capacity_a as i32`, did not: the type a
function's return wants of its cast was kept in a single slot, and the
argument's own cast, checked inside the outer one's operand, took the
slot over. The slots are a stack now. Fixed in kara 81aca4606b, test
`tests/kata_2105_nested_cast_lint.rs`. The same lint now offers to drop
the closing cast in the adapters of earlier katas written the same way;
they are left as they were.

## Benchmarks

The bench builds 200 rows of 10^5 plants once, needs from 1 to 10^6 and
cans from the row's largest need to 2 * 10^6, then counts every row's
refills ten times over, with the ★ arm in all five languages: two
indices walking in from the ends. Every implementation prints
`2000 rows: 92073520 refills,
checksum 483579965`.

BENCHTAB
