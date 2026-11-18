# 2325. Decode the Message

You are given the strings `key` and `message`, which represent a cipher
key and a secret message, respectively. The steps to decode `message`
are as follows:

1. Use the **first** appearance of all 26 lowercase English letters in
   `key` as the **order** of the substitution table.
2. Align the substitution table with the regular English alphabet.
3. Each letter in `message` is then **substituted** using the table.
4. Spaces `' '` are transformed to themselves.

- For example, given `key = "happy boy"` (actual key would have at least
  one instance of each letter in the alphabet), we have the partial
  substitution table of (`'h' -> 'a'`, `'a' -> 'b'`, `'p' -> 'c'`,
  `'y' -> 'd'`, `'b' -> 'e'`, `'o' -> 'f'`).

Return *the decoded message*.

```
key = "the quick brown fox jumps over the lazy dog"
message = "vkbs bs t suepuv"                       ->  "this is a secret"

key = "eljuxhpwnyrdgtqkviszcfmabo"
message = "zwx hnfx lqantp mnoeius ycgk vcnjrdb"   ->  "the five boxing wizards jump quickly"
```

**Constraints:** `26 <= key.length <= 2000`; `key` consists of
lowercase English letters and `' '`; `key` contains every letter in the
English alphabet (`'a'` to `'z'`) **at least once**; `1 <=
message.length <= 2000`; `message` consists of lowercase English
letters and `' '`.

One walk over the key gives each letter, at its first appearance, the
next letter of the alphabet; a table of 26 holds them, and the message
is read through it. O(|key| + |message|).

## Approaches

| file | mechanism |
|---|---|
| `decode.kara` ★ | a `[0u8; 26]` table filled over `key.bytes()`, a byte counter from `b'a'` for the next letter, and the message's bytes read through it into a `String` |
| `decode_naive.kara` | no table: for each letter of the message the key is read from the start, counting the distinct letters before it, each found distinct by looking back over the key. O(26 \|key\| \|message\|) |
| `decode_map.kara` | a `Map[char, char]` from each letter at its first appearance to the alphabet's letter at the map's size, then looked up with `get` and a `match` |
| `decode_order.kara` | the key's distinct letters gathered into a `String` by `contains`, and each letter of the message decoded by its place there, from `find` |
| `decode_iter.kara` | iterators: the key's letters `filter`ed of spaces and `fold`ed into the distinct ones, and the message `map`ped through `position` in them and `collect`ed |
| `decode_solution.kara` | LeetCode's Rust template: a `HashMap<char, char>` filled with `insert` while `!map.contains_key(&c)`, and `map[&c]` in a `map` over the message's `chars()`; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples; the
alphabet as its own key; the alphabet backwards; a message of spaces
alone; then 2000 random keys, the 26 letters in a random order with
spaces and repeated letters among them, each with a message of 1 to 100
letters and spaces, with a checksum of the decoded bytes and the count
of `a`s. `decode.py` mirrors the ★ arm and its output is byte-identical.

`karac fix` carries the template in one call, reporting 14 edits.
`check` first offers 12: the `use std::collections::HashMap;` line
deleted, since `Map` is in the prelude; `struct Solution;` to `struct
Solution {}`; the two brackets of `HashMap<char, char>`; `HashMap::new`
to `HashMap.new`; `&&` to `and` and `!` to `not`; the `&` of
`contains_key(&c)` and of the index `map[&c]` dropped; and, in the
harness's wrapper, the two `&str` parameters to `Str` and `Solution::`
to `Solution.`. The other two follow: `HashMap` to `Map`, in the type
and in the call.

Two arms were first written with a slip that `karac check` names and
`karac fix` mends. The ★ arm indexed its table with `(b - b'a') as
i64`; each cast is unnecessary, since a `u8` index widens on its own,
and fix drops the three, and one more in the harness. The order arm
passed a `char` to `String.contains` and `String.find`, which take a
`Str` pattern; fix writes `c.to_string()` at both.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: the first appearance of each letter in the key, found by
checking the key before it, makes the substitution table, kept as a
list of pairs of the key's letter and the alphabet's; each letter of
the message is looked up in the list, and a space stays a space. No
table indexed by letter and no counter. It checks 300 random keys and
messages as in the harness; then 30 keys where most letters come round
again and spaces are common; then 30 with the alphabet in order and
messages of 200. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is as long as the message, with spaces where it has them and lowercase letters everywhere else |
| P3 | the key with its spaces taken out: the same answer |
| P4 | the key, a space, and the key again: the same answer |
| P5 | every letter of the key and the message moved 7 on in the alphabet, wrapping: the same answer |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 862326267, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that
builds the same cases and the table from `dict.fromkeys` of the key's
letters. On a failure it prints the first ten and then the count by
property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a repeated letter given a new letter each time | P1 353, P2 329, P4 360, P6 353 |
| M4 | ★: the counter moved on for a space too | P1 356, P2 330, P3 356, P6 356 |
| M5 | ★: the counter moved on twice | P1 360, P2 353, P6 360 |
| M7 | naive: a repeated letter counted again | P1 352, P2 325, P6 352 |
| M9 | naive: spaces in the key counted | P1 356, P2 273, P3 356, P6 356 |
| M10 | naive: the earlier letters checked from the second | P1 186, P2 149, P6 186 |
| M12 | map: the next letter one on | P1 360, P6 360 |
| M13 | map: `z` never put in the table | P1 346, P2 272, P5 345, P6 346 |
| M14 | map: the twenty-sixth letter given `a` | P1 275, P6 275 |
| M19 | order: each place one on | P1 360, P2 275, P6 360 |
| M20 | order: the place found in the whole key, not the order | P1 360, P2 344, P3 356, P6 360 |
| M21 | order: a space decoded as `a` | P1 273, P2 273, P6 273 |
| M22 | iter: spaces kept in the order | P1 357, P2 315, P3 357, P4 1, P6 357 |
| M25 | iter: no more than 20 letters kept in the order | P1 344, P2 344, P6 344 |
| M26 | iter: the message's first letter skipped | P1 360, P2 360, P6 360 |
| M27 | solution: the counter back to `a` after `m` | P1 353, P6 353 |
| M29 | solution: `q` left as it is | P1 239, P5 310, P6 239 |

P1 and P6 kill all seventeen, P2 thirteen, P3 four, P4 two and P5 two.
P2 fails for an answer of the wrong length or with a letter where a
space belongs, or a byte past `z`, which most miscounts reach; it
misses only the edits that still give every letter some lowercase
letter: the next letter one on, `a` given twice, and the template's
counter back to `a` and `q` left alone. P3, the key's spaces taken out,
fails where a space in the key counts for something: the counter moved
on for it, spaces counted, the place in the whole key, spaces kept in
the order. P4, the key written twice, fails where a letter's second
appearance counts: a repeat given a new letter each time, and once for
the iter arm's spaces in the order, where the joining space falls
among the first 26 different characters. P5, the letters moved 7 on,
fails only where one letter is treated apart from the rest by name:
`z` never put in the table and `q` left as it is.

Of the thirty-one, fourteen were not kept. The table begun at `b` (M2)
and each letter decoded as the one after (M6) in the ★ arm and the
naive arm's letter itself counted (M8) fail as the order arm's each
place one on (M19); a space decoded as `a` in the ★ (M3), naive (M11),
iter (M24) and template (M30) arms, and as `z` in the map arm (M16), as
the order arm's `a` (M21); the map arm's alphabet reversed (M15) and the
template's counter held for the first letter (M31) as the map arm's
next letter one on (M12); repeats counted again in the order (M17) and
iter (M23) arms as the naive arm's (M7); the order arm's space put in
the order (M18) as the naive arm's spaces counted (M9); and the
template's repeated letter given a new letter each time (M28) as the ★
arm's (M1).

M13, M14, M20, M25, M27 and M29 replace edits that crashed or failed
as others did: a later appearance written over the first and a space
put in the table in the map arm, which both run past the 26 letters of
its alphabet and stop on an index out of bounds; the order arm's first
letter of the key left out, which `unwrap`s a `None` at the letter's
lookup; the iter arm's key read from the end, the template's counter
begun at `b` and its space put in the map.

## Verification

Every arm prints the same output as `decode.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the ★, map, order and template arms take 0.7
to 1.1 s, the iter arm 1.7 s, and the naive arm, which checks the key
before each letter for an earlier appearance, 4.6 s. The differential
takes 7.3 s there, its literal reading looking each letter up in a
list of pairs, and 0.6 s under `karac __mir-llvm-run`.

## Benchmarks

The bench builds 100 keys of 2000 letters and spaces, each ending in
the alphabet so that every letter is there, and as many messages of
2000, once, then makes 1000 passes with the ★ arm in all five
languages: each pass decodes every message with its key, folds two of
its bytes into the checksum, and rotates the key by one letter, so the
table changes from pass to pass. Every implementation prints `1000
passes over 100 keys and messages of 2000: checksum 175575630`. Each
builds a fresh decoded string and a fresh rotated key for every call;
C with `malloc`, Go with a `strings.Builder` and a string
concatenation.

BENCHTAB
