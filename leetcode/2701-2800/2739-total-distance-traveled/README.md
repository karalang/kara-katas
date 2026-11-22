# 2739. Total Distance Traveled

A truck has two fuel tanks. You are given two integers, `mainTank`
representing the fuel present in the main tank in liters and
`additionalTank` representing the fuel present in the additional tank in
liters.

The truck has a mileage of `10` km per liter. Whenever `5` liters of fuel
get used up in the main tank, if the additional tank has at least `1`
liters of fuel, `1` liters of fuel will be transferred from the
additional tank to the main tank.

Return *the maximum distance which can be traveled.*

**Note:** Injection from the additional tank is not continuous. It
happens suddenly and immediately for every 5 liters consumed.

```
mainTank = 5, additionalTank = 10  ->  60
mainTank = 1, additionalTank = 2   ->  10
```

**Constraints:** `1 <= mainTank, additionalTank <= 100`.

## Approaches

| file | mechanism |
|---|---|
| `distance.kara` ★ | each transfer needs 5 liters burnt from the main tank and gives 1 back, so after the first 5 every further transfer costs 4: with m liters, `(m - 1) / 4` transfers, as many as the additional tank holds, and 10 km for each liter the truck gets. O(1) |
| `distance_liters.kara` | the main tank burnt one liter at a time, 10 km each, and every fifth liter burnt a liter taken from the additional tank if it has one. O(m) |
| `distance_truck.kara` | a `struct Truck` with its two tanks, driven 50 km at a time by a `mut ref self` method that burns five liters and tops the main tank up, the last few liters driven by another. O(m) |
| `distance_recursive.kara` | under 5 liters the truck drives them out; otherwise 50 km and a call on what is left, one liter more if the additional tank gave one, by a `match` on a pair of bools. O(m) deep |
| `distance_solution.kara` | a Rust solution as LeetCode's Rust users write it, the parameters taken `mut` and driven down five liters at a time, carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's two examples; one liter in
each tank; four in the main tank, too few for any transfer; five, just
enough for one; nine and two, both transfers used; LeetCode's largest
tanks; and every pair of tanks LeetCode allows, 1 to 100 liters each,
with the sum of the distances and a checksum. `distance.py` mirrors the
★ arm and its output is byte-identical.

```
60
10
10
40
60
110
1240
10000 pairs of tanks: distances sum to 6158000, checksum 353368802
```

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the truck driven one kilometre at a time, a tenth of a liter
each, and the moment the fuel burnt from the main tank reaches another 5
liters, a liter moved over if the additional tank has one; no liters
counted whole and no formula. It takes every pair of tanks LeetCode
allows, then 300 random pairs of up to 2000 liters, all before any arm
answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | one liter more in the main tank: 10 or 20 km more |
| P3 | one liter more in the additional tank: the same distance or 10 km more |
| P4 | at least 10 km a liter of the main tank, at most 10 km a liter of both |
| P5 | an additional tank holding at least as much as the main tank: the same distance as one holding exactly as much |
| P6 | each arm agrees with at least three of the other four |

The differential prints `10300 cases: checksum 949872942, 309000 checks
over 5 arms: 0 failures` under every lane in Verification, and a Python
reading of the same cases, kilometre by kilometre, gives the same
checksum. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Ten edits to the differential, two to each arm, each run under `karac
__mir-run` and `karac __mir-llvm-run`. All ten are killed, each the same
way under both backends. M2, M4 and M7 fail the same checks: each lets
the truck take more transfers than the additional tank holds. So do M8
and M10, each driving out 5 liters with no transfer.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: m / 4 transfers, not (m - 1) / 4 | P1 2263, P6 2263 |
| M2 | ★: the additional tank's limit ignored | P1 1149, P4 1149, P6 1149 |
| M3 | liters: a transfer every fourth liter | P1 8459, P6 8459 |
| M4 | liters: the additional tank never emptied | P1 1149, P4 1149, P6 1149 |
| M5 | truck: the last liters never driven | P1 10060, P2 10300, P3 217, P4 1100, P6 10060 |
| M6 | truck: a transfer of two liters | P1 9900, P2 2844, P3 1538, P4 3168, P6 9900 |
| M7 | recursive: a transfer taken even from an empty tank | P1 1149, P4 1149, P6 1149 |
| M8 | recursive: 5 liters driven out, not over | P1 2190, P6 2190 |
| M9 | solution: 40 km for each five liters | P1 9900, P2 241, P4 1149, P6 9900 |
| M10 | solution: the loop stops at 5 liters left | P1 2190, P6 2190 |

## Benchmarks

The bench draws `10^6` pairs of tanks of 1 to 100 liters, LeetCode's
bounds, all of them first, then answers each 100 times by the ★ arm in
all five languages. Every implementation prints `1000000 pairs of tanks,
100 rounds: distances sum to 61497954000, checksum 167987401`.

BENCHTAB

## Verification

All five arms print the same output as `distance.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `684b860a5`; `karac check` re-run clean at `e514b7b29`.

## Writing it

The four own arms checked clean as first written.

LeetCode's Rust template took one `karac fix` of 7 edits, the wrapper
included: `struct Solution {}` added; `mut main_tank: i32` and `mut
additional_tank: i32` lost their `mut`, each copied into a `let mut` at
the body's start, since a parameter's mode is written in its type;
`let mut ans = 0` gained `: i32`; and `Solution::` became `Solution.`
with the `as i64` dropped.
