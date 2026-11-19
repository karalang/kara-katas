# 1640. Check Array Formation Through Concatenation

You are given an array of **distinct** integers `arr` and an array of
integer arrays `pieces`, where the integers in `pieces` are **distinct**.
Your goal is to form `arr` by concatenating the arrays in `pieces` **in
any order**. However, you are **not** allowed to reorder the integers in
each array `pieces[i]`.

Return `true` *if it is possible to form the array* `arr` *from*
`pieces`. Otherwise, return `false`.

```
arr = [15,88], pieces = [[88],[15]]                    ->  true
arr = [49,18,16], pieces = [[16,18,49]]                ->  false
arr = [91,4,64,78], pieces = [[78],[4,64],[91]]        ->  true
```

**Constraints:** `1 <= pieces.length <= arr.length <= 100`;
`sum(pieces[i].length) == arr.length`; `1 <= pieces[i].length <=
arr.length`; `1 <= arr[i], pieces[i][j] <= 100`; the integers in `arr`
are distinct, and the integers in `pieces` are distinct.

## Approaches

| file | mechanism |
|---|---|
| `formation.kara` ★ | the values are distinct, so at each point of the array at most one piece can start there: a `Map` from each piece's first value to the piece finds it, `let .. else` fails at a value no piece starts with, and each piece found is matched value by value. O(n) |
| `formation_scan.kara` | no index: at each point, `find` the piece that starts there and compare it with the slice of the array it would cover, in a `match` with a guard. O(np) for p pieces |
| `formation_places.kara` | each distinct value has one place in the array, collected into a `Map`; the array can be formed when every piece's values sit at consecutive places in order, and the pieces cover as many values as the array has. O(n) |
| `formation_solution.kara` | LeetCode's Rust template: a `HashMap` collected from `enumerate().map(..)`, then one walk comparing `&arr[i..i + p.len()]` with `p.as_slice()`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 8 lines: LeetCode's three examples, one value,
and a piece in the wrong order inside; then the cases that can be formed
counted and a checksum for 3000 random cases of up to 6 values, 300 of
up to 100 and 20 of up to 5000, each array cut into pieces of 1 to 3 and
the pieces shuffled, a third left so, a third with two values of the
array swapped and a third with one replaced. `formation.py` mirrors the
★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: try every order of the pieces, and see whether any of them,
joined end to end, is the array. It checks 3000 random cases of 1 to 6
distinct values from 1 to 12, cut and shuffled as the arms' batches are,
a third left so, a third with two values swapped, a third with one
replaced. Every case is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the pieces in reverse order give the same answer |
| P3 | every value negated gives the same answer |
| P4 | the array reversed, and every piece reversed, gives the same answer |
| P5 | an array that can be formed holds exactly the pieces' values |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 481622127, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. The first M6 tried, the places arm
accepting pieces that cover no more than the array rather than exactly
as much, survived and is equivalent within the constraints, which give
the pieces exactly `arr.length` values. It was replaced.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a piece matched by its length alone | P1 444, P4 648, P5 366, P6 444 |
| M2 | ★: a value no piece starts with ends the walk as a success | P1 934, P4 636, P5 634, P6 934 |
| M3 | ★: pieces found by their last value | P1 966, P6 966 |
| M4 | scan: a piece matched by its first value alone | P1 444, P4 648, P5 366, P6 444 |
| M5 | scan: a failed match past the start counts as a success | P1 564, P4 805, P5 410, P6 564 |
| M6 | places: a piece's values expected to fall, not rise | P1 1099, P6 1099 |
| M7 | places: a piece's values only required to be in the array | P1 531, P6 531 |
| M8 | places: the values covered never counted | P1 1469, P6 1469 |
| M9 | template: a piece compared by its length alone | P1 444, P4 648, P5 366, P6 444 |
| M10 | template: the walk moves on one value per piece | P1 966, P6 966 |

## Benchmarks

The bench draws 50000 random cases at LeetCode's largest size, the
values 1 to 100 shuffled, cut into pieces of 1 to 3 and the pieces
shuffled, every third case with two values of the array swapped, all of
them first; then it checks each by the ★ arm in all five languages,
each building its own hash map of first values per case: Kāra's `Map`,
Rust's `HashMap`, Go's `map`, Python's `dict`, and an open-addressing
table written out in C. Every implementation prints `50000 cases of 100
values: 34006 can be formed, checksum 278977467`. The C build also runs
clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `formation.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★ arm checked clean as first written, its `let Some(k) = .. else {
return false; };` included.

The scan arm first matched each piece as Rust does,
`Some(piece) if arr[i..].starts_with(piece) => ..`, and the check
refused it: "no method 'starts_with' on type 'Slice'". Kāra's
sequences have no `starts_with` or `ends_with`; only `String`'s exist,
and `karac fix` has nothing to offer. That is ROWID. The arm compares the
slice the piece would cover instead,
`i + piece.len() <= arr.len() and arr[i..i + piece.len()] == piece`.

The places arm compared `place.get(value) != Some(first + k)`, an
`Option[ref i64]` against an `Option[i64]`, which the check refused:
`get` views its item. `karac fix` wrote `.cloned()`, which copies it
out (library/core-types.md).

LeetCode's Rust template takes one `karac fix` of 21 edits, among them
`HashMap<i32, usize>` to `Map[i32, i64]` with the `use` line dropped,
`map.get(&arr[i])` to `map.get(arr[i])`, `Some(&k)` to `Some(k)`,
`let p = &pieces[k]` to `let p = ref pieces[k]`, `&arr[i..i + p.len()]`
to the bare slice, and `||` to `or`; `p.as_slice()` stays as it is. The
arm then checks and agrees with no hand edit.
