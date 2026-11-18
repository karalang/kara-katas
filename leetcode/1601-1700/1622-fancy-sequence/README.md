# 1622. Fancy Sequence

Write an API that generates fancy sequences using the `append`,
`addAll`, and `multAll` operations.

Implement the `Fancy` class:

- `Fancy()` Initializes the object with an empty sequence.
- `void append(val)` Appends an integer `val` to the end of the sequence.
- `void addAll(inc)` Increments all existing values in the sequence by
  an integer `inc`.
- `void multAll(m)` Multiplies all existing values in the sequence by an
  integer `m`.
- `int getIndex(idx)` Gets the current value at index `idx` (0-indexed)
  of the sequence **modulo** `10^9 + 7`. If the index is greater or equal
  than the length of the sequence, return `-1`.

```
["Fancy", "append", "addAll", "append", "multAll", "getIndex", "addAll",
 "append", "multAll", "getIndex", "getIndex", "getIndex"]
[[], [2], [3], [7], [2], [0], [3], [10], [2], [0], [1], [2]]
->  [null, null, null, null, null, 10, null, null, null, 26, 34, 20]
```

**Constraints:** `1 <= val, inc, m <= 100`; `0 <= idx <= 10^5`; at most
`10^5` calls in total to `append`, `addAll`, `multAll`, and `getIndex`.

## Approaches

| file | mechanism |
|---|---|
| `fancy.kara` ★ | the whole sequence lies under one map `x -> mul x + add`, kept mod `10^9 + 7`; a value appended under it is stored as `(val - add) / mul`, the division a Fermat inverse. addAll and multAll change only the map. O(log p) per append, O(1) otherwise |
| `fancy_tree.kara` | no inverse: a segment tree whose internal nodes hold maps not yet handed to their children. addAll and multAll compose onto the root; a leaf is written or read after the maps on its path are pushed down to it. The tree doubles when it fills. O(log n) per call, amortized |
| `fancy_blocks.kara` | no inverse: blocks of 64 values, each with one pending map. addAll and multAll compose onto every block; a value joins the last block after that block's map is written into its values. O(n / 64) per addAll or multAll, O(64) per append |
| `fancy_solution.kara` | LeetCode's Rust template: every value kept as given with the number of operations before it, and every prefix of the operations composed; a read undoes the first `t` of them by a Fermat inverse. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's example, a read of an empty
sequence, and one value multiplied by 100 eleven times, past the modulus;
then the reads past the end and a checksum of every read for 3000 random
sequences of 20 calls, 300 of 300, and one of 100000. `fancy.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: the values themselves, each addAll and multAll applied to
every one of them as it comes. It checks 3000 random call sequences: one
in three of up to 8 calls, one in three of up to 60 with arguments of 1
or 2 only, the rest of up to 400 with arguments up to 100, past the
tree's first 16 leaves and the first block of 64. Reads go up to one
past the end. Every random choice is drawn before any arm answers. The
interpreter takes about 19 s.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | a multAll(1) after every call leaves the answers |
| P3 | every addAll(inc) split as addAll(1), addAll(inc - 1) leaves them |
| P4 | every even multAll(m) split as multAll(2), multAll(m / 2) leaves them |
| P5 | a read past the end is -1, and every other read is in `0..10^9 + 7` |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 494382937, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends, and each only by P1 and P6: every
mutant is still a consistent sequence, so splitting or padding the calls
(P2 to P4) leaves its wrong answers as they were, and none reads out of
range (P5). M6 shows only in a sequence of more than 16 appends.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a value stored as given, not under the inverse | P1 1654, P6 1654 |
| M2 | ★: multAll leaves `add` unscaled | P1 1631, P6 1631 |
| M3 | ★: a value stored as `val + add` | P1 1759, P6 1759 |
| M4 | tree: a node's map not pushed when either part is the identity | P1 1778, P6 1778 |
| M5 | tree: the root left out of the path pushed to a leaf | P1 1828, P6 1828 |
| M6 | tree: the maps not pushed down before the tree doubles | P1 823, P6 823 |
| M7 | blocks: a value joins the last block without its map written in | P1 1652, P6 1652 |
| M8 | blocks: multAll leaves a block's `add` unscaled | P1 1444, P6 1444 |
| M9 | template: the first `t` additions undone without the ratio | P1 1552, P6 1552 |
| M10 | template: addAll records no increment | P1 1757, P6 1757 |

## Benchmarks

The bench draws 50 sequences of 100000 calls, all of them first, in the
mix the harness uses, then plays each on a fresh `Fancy` by the ★ arm in
all five languages. Every implementation prints `50 sequences of 100000
calls: 199979 reads past the end, checksum 529238121`. The C build also
runs clean under gcc's AddressSanitizer and UndefinedBehaviorSanitizer.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `9691a6290e` on LLVM 22:

| | median |
|---|---|
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.386 s |
| Kāra (`karac build`) | 0.390 s |
| C (`clang -O3`) | 0.392 s |
| Rust (`rustc -O`) | 0.394 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.398 s |
| Go | 0.512 s |
| Python | 6.6 s |

Kāra, C and both Rust builds are level: the work is a Fermat power per
append, about 30 multiplies and `%` each, the same in every language.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.344 s and 0.396 s on one run).

## Verification

All four arms print the same output as `fancy.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`9691a6290e`.

## Writing it

The harness's example was first written in Rust's way, a list of
`(&str, i32)` pairs mapped to `String`s:
`[("append", 2), ..].iter().map(|(n, a)| (n.to_string(), *a)).collect()`
into a `Vec[(String, i32)]`. It was refused as
`C: FromIterator[(String, i64)]`, with no machine fix. A string literal is
already a `String` in Kāra, so the natural spelling is the list itself,
`let example: Vec[(String, i32)] = [("append", 2), ..]`, which checks.
Probing the refusal found that a list literal read through `iter()` and
an adapter (`[1, 2].iter().map(|x| *x)`), or a closure that builds a
tuple from a bound literal list's items (`q.iter().map(|a| (*a, *a))`),
did not take the annotation's width either; nor did one that wraps the
item in `Some`. The kara fix for B-2026-11-18-71 makes all three check. A
closure that destructures a `(String, number)` item, `|(n, a)|`, is still
refused (B-2026-11-18-72).

`fancy_blocks.kara` first wrote the last block through
`self.blocks.last_mut().unwrap()`. Kāra has no `last_mut`, and the
diagnostic says to write through an index, `self.blocks[last].mul = ..`,
which the arm does. `karac fix` added the `and` for `&&`, an `own` on the
tree's `with_size` parameter, `self = ..` for `*self = ..`, `ref` on a
block read, and dropped the widening `as i64` casts every arm had.

LeetCode's Rust template takes one `karac fix` of 26 edits: the `<..>`
types to `[..]`, `usize` to `i64`, `Vec::new()` to `Vec.new()`,
`vec![1]` to `[1]`, `mut base: i64` parameters to `let mut` rebinds,
`&mut self` to `mut ref self` and `&self` to `self`, `Self::pow` to
`Fancy.pow`, and the widening `as i64` casts. It then checks and agrees
with no hand edit.
