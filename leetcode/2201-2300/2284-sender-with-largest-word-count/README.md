# 2284. Sender With Largest Word Count

You have a chat log of `n` messages. You are given two string arrays
`messages` and `senders` where `messages[i]` is a **message** sent by
`senders[i]`.

A **message** is a list of **words** separated by a single space with
no leading or trailing spaces. The **word count** of a sender is the
total number of **words** sent by the sender. Note that a sender may
send more than one message.

Return *the sender with the **largest** word count. If there is more
than one sender with the largest word count, return the one with the
**lexicographically largest** name*.

**Note:** uppercase letters come before lowercase letters in
lexicographical order, and `"Alice"` and `"alice"` are distinct.

```
messages = ["Hello userTwooo","Hi userThree","Wonderful day Alice","Nice day userThree"],
senders  = ["Alice","userTwo","userThree","Alice"]                        ->  "Alice"
messages = ["How is leetcode for everyone","Leetcode is useful for practice"],
senders  = ["Bob","Charlie"]                                              ->  "Charlie"
```

**Constraints:** `n == messages.length == senders.length`;
`1 <= n <= 10^4`; `1 <= messages[i].length <= 100`;
`1 <= senders[i].length <= 10`; `messages[i]` consists of uppercase
and lowercase English letters and `' '`; all the words in `messages[i]`
are separated by a single space; `messages[i]` does not have leading or
trailing spaces; `senders[i]` consists of uppercase and lowercase
English letters only.

Add each message's words, its spaces plus one, to its sender's total,
then take the largest total, the larger name on a tie. O(total length).
The answer is a maximum over a total order, (total, name), so it does
not depend on the order a `Map` is walked in: every arm prints the same
thing under every hash seed.

## Approaches

| file | mechanism |
|---|---|
| `words.kara` ★ | a `Map[String, i64]` of totals over `zip`, `split(" ").count()` words to each, then a walk of the map keeping the best by total and name |
| `words_naive.kara` | for each sender met for the first time, every message walked again, its words counted space by space. O(n^2 * length) |
| `words_sorted.kara` | (sender, words) pairs sorted by sender, each run of one sender totalled; runs come in name order, so `>=` lets a later tie win |
| `words_struct.kara` | `struct Tally` of a name and its words, found by `position`; `beats` says which of two leads |
| `words_iter.kara` | one `fold` of the zipped messages and senders into a `Map`, then `max_by_key` on (total, name) |
| `words_solution.kara` | LeetCode's Rust template: `Vec<String>` twice in, `String` out; a `HashMap<String, i32>` over `split_whitespace().count()`, then the largest by count and name; carried by `karac fix` |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 6 lines: LeetCode's two examples, a tie broken
by case (`bob` over `Bob`), a tie broken by a prefix (`Alice` over
`Al`), one sender; then 3000 random cases of 1 to 40 messages, each from
one of the first 2 to 8 names of a pool of ten that differ by case and
by prefix, of 1 to 6 words, with a checksum of the winners' places in
the pool. `words.py` mirrors the ★ arm and its output is byte-identical.

The ★ arm was first written with Rust's `||`, `&&` and `vec![..]`, and
`count() as i64`; `karac fix` rewrote the operators to `or` and `and`,
the lists to `[..]` literals, and dropped the cast, since `count()` is
already an `i64`. It dropped the same cast in the sorted and struct
arms. In the iterator arm it rewrote the closure parameter `mut acc`,
which Kāra has no pattern for, to `acc` rebound as `let mut acc = acc;`
in the body, and dropped the cast.

The iterator arm keys `max_by_key` on `(total, name)` over the map's
owned pairs. `name` is a `ref String` into the pair, and `max_by_key`
moves the pair while it keeps the best key, so the key cannot hold it.
`karac check` passed it and the run failed borrowck inside the
library's `max_by_key`. Check now refuses it and `karac fix` writes
`name.clone()` (kara B-2026-11-18-84). Probing it turned up the same shape in
`collect`: `let m: Vec[ref String] = w.into_iter().collect()` passed
check and a build wrote past the stack under AddressSanitizer; it is
refused now (kara B-2026-11-18-85). A key borrowed from a capture rather than
the item, `[0, 1].into_iter().min_by_key(|i| ref names[i])`, is kept by
check; the borrow check inside the library's `min_by_key` took that
key for a borrow of the index it was computed from and refused the
next index's write, and no longer does (kara B-2026-11-18-89).

`karac fix` carries the template in one round, reporting 15 edits: the
`use std::collections::HashMap` line deleted, `Vec<String>` to
`Vec[String]` twice, `HashMap<String, i32>` and `HashMap::new()` to
`Map[String, i32]` and `Map.new()`, `String::new()` to `String.new()`,
`||` and `&&` to `or` and `and`, `for (s, c) in cnt` to
`cnt.into_iter()`, and `struct Solution;` to `struct Solution {}`. The
`split_whitespace().count() as i32` stays as written.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: each sender's words counted as the runs of letters in its
messages, and the answer the one sender no other outranks, by more
words or by as many and a larger name. No map and no sort. It checks
300 random cases drawn as the arms' harness draws them; then 30 cases
where every sender has the same total, split over 1 to 3 messages each
and shuffled, so the answer is decided by name alone; then 30 with one
sender. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the literal reading's |
| P2 | the answer is one of the senders |
| P3 | the messages in reverse order: the same answer |
| P4 | one word more on the answer's last message: the same answer |
| P5 | a new sender `zzz` with as many words as the answer, in one more message: `zzz` |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 562064689, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading by
`collections.Counter` and `max` on (total, name). On a failure it
prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to
each of the others, each run under both `karac __mir-llvm-run` and
`karac __mir-run`. Seventeen are kept, three to each Kāra arm and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash, and no two kept ones fail the same
checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: the name before the total | P1 207, P6 207 |
| M5 | ★: the first message skipped | P1 54, P2 11, P3 69, P6 54 |
| M6 | ★: the lead starting at 5 | P1 18, P2 18, P6 18 |
| M8 | naive: a sender's first message only | P1 204, P3 184, P6 204 |
| M9 | naive: every sender already seen | P1 360, P2 360, P6 360 |
| M11 | naive: the last message never counted | P1 38, P3 69, P5 360, P6 38 |
| M12 | sorted: sorted the other way | P1 44, P5 360, P6 44 |
| M15 | sorted: never sorted | P1 118, P3 68, P6 118 |
| M16 | sorted: every message one word | P1 105, P5 340, P6 105 |
| M18 | struct: the second tally never contests | P1 91, P3 125, P5 45, P6 91 |
| M19 | struct: a found tally replaced | P1 199, P3 184, P6 199 |
| M21 | struct: names of one length merged | P1 146, P3 154, P5 301, P6 146 |
| M22 | iter: min_by_key for max_by_key | P1 315, P4 94, P5 360, P6 315 |
| M23 | iter: the fewest words first | P1 283, P4 98, P6 283 |
| M26 | iter: each message one word more | P1 35, P5 339, P6 35 |
| M28 | solution: the characters counted, not the words | P1 50, P5 80, P6 50 |
| M31 | solution: the messages paired in reverse | P1 134, P4 20, P5 342, P6 134 |

P1 and P6 kill all seventeen, P5 nine, P3 seven, P2 and P4 three each.
P5 is the tie rule under test: a new sender `zzz` with exactly the
answer's words must win on its name, so every edit that breaks ties the
wrong way, or miscounts the one extra message, fails it on every case.
P3 catches the edits whose answer depends on the order of the
messages: a first or last message dropped, a total replaced rather
than added, runs never sorted together, a tally that never contests. P4 fails only
where the answer is a minimum or reads the messages against the wrong
senders. P2 fails only when an arm can answer with no sender at all.

Of the thirty-one, fourteen were not kept, and none crashes or differs
between the backends. Each fails as a kept one does: the tie to the
smaller name in the ★, naive, struct and template arms and a tie never
taken in the sorted arm (M1, M10, M17, M27, M13) as the sorted arm's
sorted the other way (M12); each total or count replaced, not added, in
the ★, iter and template arms and each run's last pair only (M4, M24,
M29, M14) as the struct arm's found tally replaced (M19); beats by name
alone and the key the name alone (M20, M25) as the ★ arm's name before
the total (M3); and each message one word short in the ★ and template
arms and the spaces counted, not the words (M2, M30, M7), which shift
every total alike and so fail only the literal reading, P1 31, P6 31,
a signature no arm's three needed.

One edit of the first draft crashed: the iterator arm's first message
skipped leaves a one-message case with an empty map, and `max_by_key`
then has nothing to unwrap. It is replaced by the key the name alone
(M25).

## Verification

Every arm prints the same output as `words.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` every arm takes about 2 s and the differential
6 s.

## Benchmarks

The bench builds 1000 cases once, each of 100 messages of 1 to 8 words
of 1 to 5 letters from 20 consecutive names of a pool of 40 random
names, then makes 20 passes over all of them, summing the bytes of each
winner into a checksum, with the ★ arm in all five languages. Every
implementation prints `20 passes over 1000 cases of 100 messages:
checksum 525877108`. Kāra, Rust, Go and Python key their maps by the
sender's string and count words by splitting; Kāra and Rust clone the
key on each insert as the arm does, Go and Python share it. C keeps an
open-addressing table of 64 slots keyed by a pointer to the sender's
string (FNV-1a over its bytes, `strcmp` on a collision), and counts the
spaces.

BENCHTAB
