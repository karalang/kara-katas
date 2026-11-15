# 2166. Design Bitset

A **Bitset** is a data structure that compactly stores bits.

Implement the `Bitset` class:

- `Bitset(int size)` Initializes the Bitset with `size` bits, all of
  which are `0`.
- `void fix(int idx)` Updates the value of the bit at the index `idx` to
  `1`. If the value was already `1`, no change occurs.
- `void unfix(int idx)` Updates the value of the bit at the index `idx`
  to `0`. If the value was already `0`, no change occurs.
- `void flip()` Flips the values of each bit in the Bitset. In other
  words, all bits with value `0` will now have value `1` and vice versa.
- `boolean all()` Checks if the value of **each** bit in the Bitset is
  `1`. Returns `true` if it satisfies the condition, `false` otherwise.
- `boolean one()` Checks if there is **at least one** bit in the Bitset
  with value `1`. Returns `true` if it satisfies the condition, `false`
  otherwise.
- `int count()` Returns the **total number** of bits in the Bitset which
  have value `1`.
- `String toString()` Returns the current composition of the Bitset.
  Note that in the resultant string, the character at the `i`th index
  should coincide with the value at the `i`th bit of the Bitset.

```
["Bitset", "fix", "fix", "flip", "all", "unfix", "flip", "one", "unfix", "count", "toString"]
[[5], [3], [1], [], [], [0], [], [], [0], [], []]
->  [null, null, null, null, false, null, null, true, null, 2, "01010"]
```

**Constraints:** `1 <= size <= 10^5`; `0 <= idx <= size - 1`; at most
`10^5` calls will be made in total to `fix`, `unfix`, `flip`, `all`,
`one`, `count`, and `toString`; at least one call will be made to `all`,
`one`, `count`, or `toString`; at most `5` calls will be made to
`toString`.

A flip need not touch the bits: a flag says whether every bit is read
the other way, and the count of ones becomes `size` less itself. Every
call is then O(1) but `toString`, which is O(n).

## Approaches

| file | mechanism |
|---|---|
| `bitset.kara` ★ | a `Vec[bool]` read through a `flipped` flag beside the count of ones; `toString` pushes a character for each bit onto a `String` |
| `bitset_pair.kara` | the bitset's text and its complement's, each a `Vec[u8]` of `b'0'` and `b'1'`, with the count of ones and of zeros; a fix or an unfix writes both, a flip swaps the texts and the counts by `mem.swap`, and `toString` is `String.from_utf8` of the first |
| `bitset_words.kara` | 64 bits to a `u64`, read through a mask that is all ones while flipped and 0 otherwise; a fix or an unfix turns one bit of its word by `^=` and `<<`, a flip turns the mask by `~` |
| `bitset_set.kara` | a `Set[i64]` of only the places that differ from the background, which a flip turns; the count of ones is the set's size or what it leaves, and `toString` asks the set about every place, so no walk of the set is ever seen |
| `bitset_calls.kara` | every call a value of an `enum Call`, answered by one `apply` that `match`es it and returns an `enum Answer`; LeetCode's methods build their call and take their answer back out; the bits are `u8`s read through a flip by `^` |
| `bitset_solution.kara` | LeetCode's Rust template: `Vec<bool>`, `vec![false; size as usize]`, `idx as usize`, `&mut self`, `!self.flipped`, `self.bits.len() as i32`, the text by `iter().map(\|&b\| ..).collect()`; `Bits` adapts its `i32`s to the harness; carried by `karac fix` in four rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 7 lines: LeetCode's example and three more
(one bit, every bit flipped on and then fixed again, and a flip undone),
each as LeetCode prints its answers; then a checksum over the answers to
2000 random scripts of 1 to 30 calls on 1 to 8 bits, fixing and
unfixing more often than the rest; then the constraints' largest, 100000
calls on 100000 bits, five of them `toString`. `bitset.py` mirrors the ★
arm and its output is byte-identical.

`karac fix` carries the template in four rounds of 20, 2, 3 and 1
edits: Rust's spellings (`Vec<bool>` to `Vec[bool]`, `&mut self` to `mut
ref self`, `&self` to `self`, `!` to `not`, `Bitset::new` to
`Bitset.new`, the closure's `|&b|` to `|b|`); then `vec![false; size as
usize]` to `Vec.filled(size as usize, false)` and the adapter's widening
`as i64` dropped; then every `as usize` to `as i64`; then the `as i64`
of `Vec.filled`'s `i32` count dropped. The third round exists because
the second's `Vec.filled(size as usize, ..)` hands a `usize` to an `i64`
count, and once a program mixes the two, every `as usize` in it goes, the
two `idx as usize` that index the bits as well (B-2026-11-08-49); before
that, the program checks clean with them.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a list of bits, every one turned by a flip, `all`, `one` and
`count` asked of every bit; no flag and no count kept. It checks 300
random scripts of 1 to 30 calls on 1 to 8 bits; then 30 that call on
one place only; then 30 on 50 to 199 bits that flip more than they do
anything else. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | two flips put in the middle of the script: the same answers, but for their two nulls |
| P3 | a flip put first, and every fix and unfix, and every `all` and `one`, swapped: each answer turned (a count `n - c`, a text its complement, `all` and `one` each the other's negation) |
| P4 | every place reversed: the same answers, each text reversed |
| P5 | a `count`, an `all`, a `one` and a `toString` asked after every call: they agree (`all` when the count is n, `one` when it is over 0, the text n long with as many ones as the count) |
| P6 | each arm agrees with at least three of the other five |

P3 holds since the turned script, started from every bit 1, keeps the
complement of the first script's bits at every step: a fix there is an
unfix here, and `all` here asks what `one` asked there, negated.

The differential prints `360 scripts: checksum 417676450, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading of the same
scripts. On a failure it prints the first ten and then the count by
property.

The third group was first drawn on 1 to 8 bits like the rest, and the
words arm's bit read 32 to a word (M11) survived, since no place reached
32; it now takes 50 to 199 bits, which span four words.

## Mutation testing

Twenty-seven edits to the differential, four to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Seventeen are
kept, three to each Kāra arm and two to the Rust-template arm. Each kept
one is killed, fails the same way under both backends and not by a
crash, and no two kept ones fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a fix never counted | P1 203, P3 243, P5 298, P6 203 |
| M4 | ★: the text read without the flip | P1 119, P3 243, P5 270, P6 119 |
| M27 | ★: the count by the bits, not the flip | P1 100, P3 225, P5 270, P6 100 |
| M6 | pair: a flip leaving the counts | P1 168, P3 309, P5 264, P6 168 |
| M7 | pair: a fix never writing the complement | P1 95, P3 127, P5 184, P6 95 |
| M9 | pair: an unfix of a 0 taken | P1 184, P3 212, P5 275, P6 184 |
| M10 | words: a flip turning only the low bit | P1 166, P3 261, P4 138, P5 243, P6 166 |
| M11 | words: a bit read 32 to a word | P1 12, P4 11, P5 20, P6 12 |
| M12 | words: an unfix of a 0 turning it | P1 216, P3 261, P5 275, P6 216 |
| M14 | set: a flip clearing the set | P1 154, P2 73, P6 154 |
| M15 | set: a place marked whatever the background | P1 177, P3 287, P6 177 |
| M16 | set: the count ignoring the background | P1 139, P3 287, P5 270, P6 139 |
| M18 | calls: a fix ignoring the flip | P1 154, P3 256, P5 155, P6 154 |
| M20 | calls: `all` answered as `one` | P1 152, P3 210, P5 285, P6 152 |
| M22 | calls: an unfix counted as a fix | P1 164, P3 209, P5 243, P6 164 |
| M23 | solution: the adapter's unfix a fix | P1 248, P3 293, P6 248 |
| M24 | solution: the text turned | P1 243, P5 360, P6 243 |

P1 and P6 kill all seventeen, P3 and P5 fourteen each, P4 two and P2
one. P5 asks every question after every call and sees an edit whose
answers disagree with each other; it misses the three whose bits are
wrong but whose count, `all`, `one` and text still agree (M14, M15,
M23). P3 compares an arm with itself on the complement script; it misses
an edit wrong the same way on both (the text turned, M24, and the set
cleared by a flip, M14), and the words arm's word size (M11), which no
complement changes. P4 reverses the places, which only the words arm
tells apart: its words' low bits (M10) and its bits read 32 to a word
(M11). P2 puts two flips in the middle; every edit here keeps a flip its
own inverse but the set cleared by one (M14).

Of the twenty-seven, ten were not kept. None is equivalent and none
crashes. Five fail as a kept one does: the ★ and calls arms' flip
leaving the count, as M6; the ★ arm's unfix of a 0 counted, as M9; and
the set and calls arms' text ignoring the background or the flip, as
M4. Three fail alike and none of their arms has room: `all` when one
bit is missing, in the ★ and template arms, and when one zero is left in
the pair arm (P1 64, P3 131, P5 238). Two were left out to keep three to
the words arm and two to the template: `one` when the count is over 1
(P1 90, P3 131, P5 301) and the template's fix writing 1 whatever the
flip (P1 81, P3 143, P5 122).

## Verification

Every arm prints the same output as `bitset.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 0.9 s to 1.6 s and the
differential 2.8 s.

## Benchmarks

The bench makes one bitset of 100000 bits and 5000000 calls on it, each
drawn as it is made: fix, unfix, flip, a question of `all` and `one`, or
`count`, and every 500000th a `toString`, with the ★ arm in all five
languages. Every implementation prints `5000000 calls: checksum
141618476`.

BENCHTAB
