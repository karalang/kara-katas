# 2296. Design a Text Editor

Design a text editor with a cursor that can do the following:

- **Add** text to where the cursor is.
- **Delete** text from where the cursor is (just like the backspace
  key).
- **Move** the cursor either left or right.

When deleting text, only characters to the left of the cursor will be
deleted. The cursor will also remain within the actual text and cannot
be moved beyond it. More formally, we have that `0 <= cursor.position
<= currentText.length` always holds.

Implement the `TextEditor` class:

- `TextEditor()` Initializes the object with empty text.
- `void addText(string text)` Appends `text` to where the cursor is.
  The cursor ends to the right of `text`.
- `int deleteText(int k)` Deletes `k` characters to the left of the
  cursor. Returns the number of characters actually deleted.
- `string cursorLeft(int k)` Moves the cursor to the left `k` times.
  Returns the last `min(10, len)` characters to the left of the cursor,
  where `len` is the number of characters to the left of the cursor.
- `string cursorRight(int k)` Moves the cursor to the right `k` times.
  Returns the last `min(10, len)` characters to the left of the cursor,
  where `len` is the number of characters to the left of the cursor.

```
["TextEditor", "addText", "deleteText", "addText", "cursorRight",
 "cursorLeft", "deleteText", "cursorLeft", "cursorRight"]
[[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]]
->  [null, null, 4, null, "etpractice", "leet", 4, "", "practi"]
```

**Constraints:** `1 <= text.length, k <= 40`; `text` consists of
lowercase English letters; at most `2 * 10^4` calls **in total** will
be made to `addText`, `deleteText`, `cursorLeft` and `cursorRight`.

**Follow-up:** Could you find a solution with time complexity of
`O(k)` per call?

Keep the text before the cursor on one stack and the text after it,
reversed, on another. The cursor is the gap between their tops: adding
pushes on the first, deleting pops from it, and a move pops letters
from one stack onto the other, `k` at most. The tail is the top ten of
the first stack. O(k) per call.

## Approaches

| file | mechanism |
|---|---|
| `editor.kara` ★ | two stacks of letters, `left: Vec[char]` in order and `right: Vec[char]` reversed; adding pushes on `left`, deleting pops from it, a move pops from one onto the other |
| `editor_naive.kara` | one `String` and the cursor as a byte offset; adding and deleting build the text again around the cursor with an f-string of slices, a move is arithmetic on the offset. O(n) per call |
| `editor_list.kara` | a doubly linked list of letters in parallel `Vec`s of letters and `prev` / `next` indices behind a sentinel node 0, the cursor the node just before it; unlinked nodes stay in the `Vec`s |
| `editor_gap.kara` | `struct GapBuffer`: one `Vec[char]` with a gap at the cursor, `buf[start..end]`; adding fills the gap from the left and doubles the buffer when it closes, deleting widens it, a move copies letters across it |
| `editor_iter.kara` | two `String`s, `right` reversed; a move slices the last `n` letters of one, `chars().rev().collect()`s them onto the other and `truncate`s the first; the tail is `chars().skip(..).collect()`, which walks the whole text before the cursor. O(n) per move |
| `editor_solution.kara` | LeetCode's Rust template: `struct TextEditor` with `&mut self` methods over two `Vec<char>`, `i32` counts, a `match` on `pop()` for each step and `saturating_sub(10)` for the tail; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm runs each call list through `run`, which answers each
`deleteText` with its count and each move with its tail, and prints the
same 6 lines: LeetCode's example; a delete and moves on an empty
editor and past either end; text typed into the middle; a long text
whose tail is ten letters; then 3000 random editors of 1 to 30 calls,
and 5 of `2 * 10^4` calls, as many as the constraints allow, each with
the count of answers and a checksum over them. Texts are 1 to 40
lowercase letters and `k` is 1 to 40. `editor.py` mirrors the ★ arm and
its output is byte-identical.

`karac fix` carries the template in one call, reporting 14 edits: the
brackets of the two `Vec<char>` fields; `Vec::new()` to `Vec.new()`
twice; `&mut self` to `mut ref self` four times and `&self` to `self`;
`k as usize` to `k as i64`; the `.clone()` of a text handed to
`add_text`, which borrows it, dropped; and
`self.left.len().saturating_sub(10)` to `(self.left.len() - 10).max(0)`.
A length is an `i64` in Kāra, and `saturating_sub` on an `i64` stops at
`i64.MIN`, not at 0: the template as first carried kept it, and with
fewer than ten letters before the cursor its tail began at a negative
index and the arm panicked. `karac fix` now rewrites a length's
`saturating_sub` to the clamp at 0 the Rust meant (B-2026-11-18-88).

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the text is a list of letters with the cursor in it as a
`|`; adding puts each letter just before the `|`, deleting removes the
letter before it one at a time while there is one, and a move swaps the
`|` with its neighbour one step at a time. No stack, no offset
arithmetic. It checks 300 random editors of 1 to 30 calls with texts of
1 to 8 letters and `k` from 1 to 12, so that moves and deletes often
reach an end; then 30 with texts and `k` up to 40; then 30 that type
once and then only move and delete. All 360 are drawn before any arm
answers.

| | property |
|---|---|
| P1 | the answers are the literal reading's |
| P2 | each delete answers 0 to `k`, and each move at most ten lowercase letters |
| P3 | every text typed one letter at a time: the same answers |
| P4 | every call with `k` above 1 made as `k` calls of 1: the deletes summed, and each move's last tail, give the same answers |
| P5 | the text after the calls, read out by moving to the end and then back ten letters at a time: the literal reading's text |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 766175351, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that does
the same walk with a list. On a failure it prints the first ten and
then the count by property.

The fold of single steps back, `for i in at..at + k` with `at` an
unannotated `let mut at = 0`, was refused at first: "range bounds must
have same type: 'i64' and 'i64'". Reading the end bound fixed `at` to
`i64` while the start was still the unfixed variable. It was a fresh
regression from reading range bounds open, fixed in the compiler
(B-2026-11-18-54), and the differential keeps the loop as written.

P5 as first drafted raised every letter one on in the alphabet and
expected every answer's letters one on. No arm reads a letter's value,
so it failed for none of the thirty-one mutations, and it was replaced
by the read-out, which checks the whole text the calls leave rather
than only the answers along the way.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: one letter fewer deleted than counted | P1 255, P4 257, P5 278, P6 255 |
| M5 | ★: each text added reversed | P1 271, P3 271, P5 253, P6 271 |
| M6 | ★: a delete answering k | P1 304, P6 304 |
| M7 | naive: the cursor left before added text | P1 279, P3 279, P5 243, P6 279 |
| M9 | naive: a move right of at most ten | P1 33, P4 33, P5 64, P6 33 |
| M11 | naive: a move left of at most k - 1 | P1 195, P4 243, P5 168, P6 195 |
| M12 | list: a deleted node still the prev of its follower | P1 83, P5 99, P6 83 |
| M13 | list: the follower of new text never told | P1 92, P5 125, P6 92 |
| M16 | list: the tail read backwards | P1 266, P5 251, P6 266 |
| M18 | gap: a move left that leaves the letter behind | P1 204, P2 199, P5 205, P6 204 |
| M19 | gap: a delete of the text after the cursor | P1 288, P5 272, P6 288 |
| M21 | gap: the letters after the gap lost when the buffer grows | P1 40, P2 40, P5 53, P6 40 |
| M22 | iter: the letters shifted unreversed | P1 133, P4 133, P5 126, P6 133 |
| M23 | iter: the shifted letters kept where they were | P1 249, P4 208, P5 292, P6 249 |
| M26 | iter: a move right no longer than the text before | P1 179, P4 63, P5 173, P6 179 |
| M30 | solution: a move left of one letter at most | P1 235, P4 235, P5 254, P6 235 |
| M31 | solution: a move right that drops each letter | P1 209, P5 211, P6 209 |

P1 and P6 kill all seventeen, P5 sixteen, P4 seven, and P2 and P3 two
each. P5 misses only the ★ arm's delete answering `k`, which leaves the
text right and gets only the count wrong. P4, the calls made one step at
a time, fails where an edit's error depends on `k`: one letter fewer
deleted than counted, a move right of at most ten, a move left of at
most `k - 1`, the iter arm's letters shifted unreversed and kept where
they were, its move right no longer than the text before, and the
template's move left of one letter at most. P3, every text typed one
letter at a time, fails only for the two edits that care how a text
arrives: the ★ arm's text added reversed and the naive arm's cursor left
before added text. P2 fails only where a tail can hold something that
is not a lowercase letter or more than ten of them: the gap buffer's
letter left behind and letters lost on growing, which read the gap's
blanks.

Of the thirty-one, fourteen were not kept. The gap buffer's end kept
when it grows (M17) crashes with an index out of bounds under both
backends. The ★ arm's move left that drops the letter (M2) fails as the
template's move right that drops each letter (M31); its tail of nine
(M3) as the list arm's tail of nine nodes (M14); its text added
reversed (M5) as the template's (M29); the naive arm's delete of at
most `k - 1` (M8) as the template's (M27); its tail from the start of
the text (M10) as the iter arm's tail the first ten letters (M24); and
the gap buffer's tail of eleven (M20) as the template's (M28). The ★
arm's move right of at most `k - 1` (M4), the list arm's move right a
letter short of the end (M15) and the iter arm's delete one letter too
many (M25) fail in ways of their own, past the three kept for their
arms.

## Verification

Every arm prints the same output as `editor.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the naive arm takes 1.6 s, the gap-buffer arm
3.7 s, the ★ arm 4.3 s and the linked-list arm 4.9 s. The iterator arm
takes 39 s there, because its tail walks `chars().skip(..)` from the
front of the text before the cursor, which grows to about 10^5 letters
in the two largest editors, at every move; under `karac
__mir-llvm-run` it takes 0.4 s. The differential takes 5.5 s.

## Benchmarks

The bench builds 10 editors of `2 * 10^4` random calls once, then makes
10 passes over all of them with the ★ arm in all five languages, each
pass a fresh editor per call list. Every implementation prints `10
passes over 10 editors of 2 * 10^4 calls: checksum 292841327`. C keeps
each stack in a `realloc`-grown `char` array, Rust in a `Vec<char>`, Go
in a `[]byte` and Python in a list.

BENCHTAB
