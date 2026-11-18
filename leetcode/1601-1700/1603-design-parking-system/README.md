# 1603. Design Parking System

Design a parking system for a parking lot. The parking lot has three
kinds of parking spaces: big, medium, and small, with a fixed number of
slots for each size.

Implement the `ParkingSystem` class:

- `ParkingSystem(int big, int medium, int small)` Initializes object of
  the `ParkingSystem` class. The number of slots for each parking space
  are given as part of the constructor.
- `bool addCar(int carType)` Checks whether there is a parking space of
  `carType` for the car that wants to get into the parking lot.
  `carType` can be of three kinds: big, medium, or small, which are
  represented by `1`, `2`, and `3` respectively. **A car can only park in
  a parking space of its** `carType`. If there is no space available,
  return `false`, else park the car in that size space and return `true`.

```
["ParkingSystem", "addCar", "addCar", "addCar", "addCar"]
[[1, 1, 0], [1], [2], [3], [1]]  ->  [null, true, true, false, false]
```

**Constraints:** `0 <= big, medium, small <= 1000`; `carType` is `1`,
`2`, or `3`; at most `1000` calls will be made to `addCar`.

## Approaches

| file | mechanism |
|---|---|
| `parking.kara` ★ | the spaces left of each size in a `Vec[i32]` indexed by the car's type less one; a car parks while its count is above zero, and takes one. O(1) a car |
| `parking_fields.kara` | a field for each size, the car's type picking one by `match` as a `mut ref` (`1 => mut ref self.big`), read and written through `*count`. O(1) a car |
| `parking_map.kara` | a `Map[i32, i32]` from car type to count, read with `get(..).unwrap()` and written back with `self.spaces[car_type] = ..`. O(1) expected a car |
| `parking_solution.kara` | LeetCode's Rust template (a `[i32; 3]` field, `&mut self`, `(car_type - 1) as usize` to index), carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's example and two more (a
lot with no space at all, and one of two spaces a size filled to the
brim), then the cars parked and a checksum of every answer for 3000 lots
of up to 3 spaces a size met by 10 cars, 300 of up to 1000 met by 3000,
and 3 of up to 1000 met by 1000000. `parking.py` mirrors the ★ arm and
its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every car parked so far kept in a list, and a car parked when
the cars of its size in the list are fewer than the spaces of its size.
It checks 3000 lots of 0 to 3 spaces a size, each met by 1 to 10 cars,
every random choice drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | the sizes renamed (big, medium, small made medium, small, big, the cars' types with them) leave the answers |
| P3 | one more space of each size never turns away a car that parked |
| P4 | the cars of each size parked are the fewer of its spaces and its cars |
| P5 | the cars in reverse order park as many |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 551620728, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a full size taken as having room | P1 2364, P4 2364, P6 2364 |
| M2 | ★: the medium and small counts swapped | P1 1802, P2 2375, P4 1802, P6 1802 |
| M3 | ★: the last small space taken lends a big one | P1 319, P2 606, P3 98, P4 319, P5 246, P6 319 |
| M4 | fields: a count of zero taken as room | P1 2364, P4 2364, P6 2364 |
| M5 | fields: a medium car parked in the big count | P1 1841, P2 2318, P4 1841, P6 1841 |
| M6 | map: every car taking a big space | P1 1700, P2 1729, P3 352, P4 1693, P5 792, P6 1700 |
| M7 | map: no more than two small spaces | P1 236, P2 441, P4 236, P6 236 |
| M8 | template: every car taking a big space | P1 1614, P2 1781, P3 131, P4 1614, P5 830, P6 1614 |
| M9 | template: the last space of a size never taken | P1 2292, P4 2292, P6 2292 |
| M10 | fields: a car taking as many spaces as its type | P1 1259, P2 1459, P4 1259, P6 1259 |

## Benchmarks

The bench makes 20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each, all of it first. Then: three counts in a list. Every implementation prints `20 rounds of 1000 lots of up to 3000 spaces a size, 10000 cars each: 89041000 parked, checksum 18051427`.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `5bb1708545` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.504 s |
| Rust (`rustc -O`) | 0.556 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.569 s |
| Kāra (`karac build`) | 0.571 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.600 s |
| Go | 0.607 s |
| Python | 13 s |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its user time is not above its real time (0.475 s and 0.492 s on one run).

## Verification

All four arms print the same output as `parking.py` under
`karac __mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`5bb1708545`.

## Writing it

The three Kāra arms were written in Kāra and checked as written. The
differential first wrote `(0..cars.len()).filter(|i| cars[*i] == t ..)`,
and `karac fix` dropped the `*`s, as a range hands the closure each
number by value. Its `of_t.min(sizes[t - 1])`, a count against an `i32`
widened to `i64`, ran under the interpreter and was refused by the LLVM
backend, ``native `i64.min` is not lowered yet`` (B-2026-11-18-6): it lowered a
number's method only when every argument was already the receiver's
width, or a literal.

The Rust template took one `karac fix` of 3 edits: the `[i32; 3]` field
to `Array[i32, 3]`, `&mut self` to `mut ref self`, and the comment
LeetCode puts above the `impl` kept as it is. It then checks and agrees
with no hand edit; its `as usize` is a Kāra cast too.
