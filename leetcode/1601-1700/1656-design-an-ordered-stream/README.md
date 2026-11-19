# 1656. Design an Ordered Stream

There is a stream of `n` `(idKey, value)` pairs arriving in an
**arbitrary** order, where `idKey` is an integer between `1` and `n` and
`value` is a string. No two pairs have the same `id`.

Design a stream that returns the values in **increasing order of their
IDs** by returning a **chunk** (list) of values after each insertion. The
concatenation of all the **chunks** should result in a list of the sorted
values.

Implement the `OrderedStream` class:

- `OrderedStream(int n)` Constructs the stream to take `n` values.
- `String[] insert(int idKey, String value)` Inserts the pair
  `(idKey, value)` into the stream, then returns the **largest possible
  chunk** of currently inserted values that appear next in the order.

```
OrderedStream(5)
insert(3, "ccccc")  ->  []
insert(1, "aaaaa")  ->  ["aaaaa"]
insert(2, "bbbbb")  ->  ["bbbbb", "ccccc"]
insert(5, "eeeee")  ->  []
insert(4, "ddddd")  ->  ["ddddd", "eeeee"]
```

**Constraints:** `1 <= n <= 1000`; `1 <= id <= n`;
`value.length == 5`; `value` consists only of lowercase letters; each
call to `insert` has a unique `id`; exactly `n` calls are made to
`insert`.

## Approaches

| file | mechanism |
|---|---|
| `stream.kara` ★ | a slot per id and a pointer to the first id not yet returned: an insert fills its slot, and when the pointer's slot is filled the run of filled slots from it is returned. O(1) amortised per insert |
| `stream_map.kara` | values not yet returned wait in a `Map` by id; an insert at the pointer removes the run of ids that follow it, so each value is held only until it is returned. O(1) amortised |
| `stream_heap.kara` | pending pairs in a min-heap by id, popped into the chunk while the smallest is the pointer's. O(log n) per insert |
| `stream_solution.kara` | LeetCode's Rust template: a `Vec<String>` of slots, empty meaning unfilled, and a `ptr`. Carried by `karac fix` |
| `differential.kara` | the four arms against the statement read literally, five properties |

Every arm prints the same 11 lines: LeetCode's example, a stream of one
pair, and three pairs in order, each its own chunk; then the chunks, the
values in them and a checksum over every value's letters in the order
returned, for 3000 random streams of up to 10 pairs and 100 of up to
1000. `stream.py` mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: after each insert, the values of ids 1 to k have been
returned, k being the most for which every one of them is inserted, and
the chunk is the values of the ids that insert brought into that run,
k recounted from 1 each time. It checks 3000 random streams of 1 to 8
pairs, each inserted in a random order. Every stream is drawn before any
arm runs.

| | property |
|---|---|
| P1 | every chunk is the statement read literally |
| P2 | the chunks together are every value, in id order |
| P3 | a chunk is empty exactly when the id inserted is not the first one not yet returned |
| P4 | the values written in capitals give the same chunks in capitals |
| P5 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 940331177, 60000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends. One first try was replaced: the heap
arm stopping at an id above the pointer, rather than any other id,
survived, and is equivalent, since every id below the pointer has
already left the heap.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the last slot never returned | P1 3000, P2 3000, P3 1070, P5 3000 |
| M2 | ★: an empty slot skipped, not stopped at | P1 2603, P2 2603, P3 2603, P5 2603 |
| M3 | ★: the pointer starting at slot 0, which is never filled | P1 3000, P2 3000, P3 3000, P5 3000 |
| M4 | map: the pointer moved two ids per value | P1 2603, P2 2603, P3 1676, P5 2603 |
| M5 | map: the pointer starting at id 2 | P1 3000, P2 3000, P3 3000, P5 3000 |
| M6 | heap: only the first value of a run returned | P1 2318, P2 2318, P3 1055, P5 2318 |
| M7 | heap: each run returned backwards | P1 2318, P2 2318, P5 2318 |
| M8 | template: each value stored twice over | P1 3000, P2 3000, P5 3000 |
| M9 | template: the last slot never returned | P1 3000, P2 3000, P3 1070, P5 3000 |
| M10 | template: one value per chunk at most | P1 2318, P2 2318, P3 1055, P5 2318 |

## Benchmarks

The bench draws 2000 random streams of 1000 pairs, LeetCode's largest,
each inserted in a random order with a value of five random letters, all
of them first, then runs each through the ★ arm in all five languages,
each insert taking its own copy of the value and each chunk its own
copies of the values returned. Every implementation prints `2000
streams of 1000 pairs: 15025 chunks, checksum 265853568`. The C build
also runs clean under gcc's AddressSanitizer and
UndefinedBehaviorSanitizer.

TIMINGS

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. PARNOTE

## Verification

All four arms print the same output as `stream.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for them,
the differential and the bench. `karac check` reports nothing on any of
them, and `karac fix` has nothing left to change. Checked at kara `SHA`.

## Writing it

The ★, map and heap arms each wrote Rust's `mut self` for `insert`, which
`karac fix` turned into `mut ref self`, and declared the `value` it
stores `own String`; the ★ arm's `id_key as i64` index lost its cast.
The heap arm was written with `BinaryHeap[Reverse[(i32, String)]]`, and
`karac fix` rewrote it to Kāra's min-first `PriorityQueue[(i32,
String)]`, dropping the `Reverse` from the push, the `peek` pattern and
the `pop`.

LeetCode's Rust template takes one `karac fix` of 16 edits: `Vec<String>`
to `Vec[String]`, `ptr: usize` to `ptr: i64`,
`vec![String::new(); n as usize]` to `Vec.filled(n, String.new())`,
`&mut self` to `mut ref self`, `value` declared `own String`,
`(id_key - 1) as usize` to `id_key - 1`, `Vec::new()` to `Vec.new()`,
`&&` to `and` and `!` to `not`. The template's comment about `&self`
stays as LeetCode wrote it. The arm then checks and agrees with no hand
edit.
