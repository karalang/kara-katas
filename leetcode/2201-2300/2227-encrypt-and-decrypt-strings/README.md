# 2227. Encrypt and Decrypt Strings

You are given a character array `keys` containing **unique** characters
and a string array `values` containing strings of length 2. You are also
given another string array `dictionary` that contains all permitted
original strings after decryption. You should implement a data structure
that can encrypt or decrypt a **0-indexed** string.

A string is **encrypted** with the following process:

1. For each character `c` in the string, we find the index `i`
   satisfying `keys[i] == c` in `keys`.
2. Replace `c` with `values[i]` in the string.

Note that in case a character of the string is **not present** in
`keys`, the encryption process cannot be carried out, and an empty
string `""` is returned.

A string is **decrypted** with the following process:

1. For each substring `s` of length 2 occurring at an even index in the
   string, we find an `i` such that `values[i] == s`. If there are
   multiple valid `i`, we choose **any** one of them. This means a
   string could have multiple possible strings it can decrypt to.
2. Replace `s` with `keys[i]` in the string.

Implement the `Encrypter` class:

- `Encrypter(char[] keys, String[] values, String[] dictionary)`
  Initializes the `Encrypter` class with `keys`, `values`, and
  `dictionary`.
- `String encrypt(String word1)` Encrypts `word1` with the encryption
  process described above and returns the encrypted string.
- `int decrypt(String word2)` Returns the number of possible strings
  `word2` could decrypt to that also appear in `dictionary`.

```
keys = ['a','b','c','d'], values = ["ei","zf","ei","am"],
dictionary = ["abcd","acbd","adbc","badc","dacb","cadb","cbda","abad"]
encrypt("abcd")      ->  "eizfeiam"
decrypt("eizfeiam")  ->  2   ("abad" and "abcd"; "cbad" and "cbcd" are not in it)
```

**Constraints:** `1 <= keys.length == values.length <= 26`;
`values[i].length == 2`; `1 <= dictionary.length <= 100`; `1 <=
dictionary[i].length <= 100`; all `keys[i]` and `dictionary[i]` are
unique; `1 <= word1.length <= 2000`; `1 <= word2.length <= 200`; all
`word1[i]` appear in `keys`; `word2.length` is even; `keys[i]`,
`values[i][j]`, `word1[i]` and `word2[i]` are lowercase letters; at most
200 calls are made to `encrypt` and `decrypt` in total.

Since values may repeat, a string decrypts to every word that encrypts
to it. So the dictionary's words are encrypted once, when the
`Encrypter` is made, and counted by their encryption: `decrypt` is one
look-up. A word with a letter that is no key never encrypts and is left
out. O(dictionary letters) to build, then O(length) a call.

## Approaches

Every arm defines `Encrypter` with `new`, `encrypt` and `decrypt`, and a
`replay` that answers a list of calls on a new one, each an encryption
or a decryption with its count written out.

| file | mechanism |
|---|---|
| `encrypter.kara` ★ | a `Map[char, String]` of values, and a `Map[String, i64]` counting the dictionary's encryptions; `encrypt` returns `""` from a `match` on the look-up |
| `encrypter_array.kara` | the values in a `Vec` of 26 indexed by the key's letter, `""` for a letter that is no key, the words read as bytes; the counts a `Map` as in the ★ arm |
| `encrypter_trie.kara` | decryption as the statement puts it: the dictionary kept as a trie of `Node`s, a `Map` from each value to the keys that have it, and the string walked a pair at a time, branching where values repeat, by a recursive `walk`; nothing about the encryptions kept ahead |
| `encrypter_scan.kara` | nothing counted ahead: the `Encrypter` keeps the dictionary, and each `decrypt` encrypts every word of it again and counts those equal to the string |
| `encrypter_iter.kara` | the table `zip`ped from the keys and values and `collect`ed into a `Map`; `encrypt` checks with `all` and then `map`s and `join`s; the counts a `fold` of the dictionary's encryptions |
| `encrypter_solution.kara` | LeetCode's Rust template: a `HashMap<char, String>` built by `zip`ping `into_iter`s, the counts a `HashMap<String, i32>` through `*entry(..).or_insert(0) += 1`, `encrypt(&self, ...)` returning `String::new()` from a `match` on `self.map.get(&c)`, and `decrypt` reading `*self.count.get(&word2).unwrap_or(&0)`; carried by `karac fix` in one round |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 5 lines: LeetCode's example, one with no
repeated values, and one where every key shares the value `"qq"`, each
with its answers; then a checksum of 2000 random cases of 1 to 26 keys,
values of 2 to 4 letters (so that they repeat), up to 30 dictionary
words of 1 to 5 letters that may use a letter past the keys, and 20
calls; then the constraints' largest, 26 keys, 100 dictionary words of
100 letters and 200 calls, with 5306 letters encrypted and 55 words
found. `encrypter.py` mirrors the ★ arm and its output is
byte-identical.

`karac fix` carries the template in one round of 27 edits: `use
std::collections::HashMap` dropped, `HashMap<..>` and `HashMap::new()`
to `Map[..]` and `Map.new()`, `Vec<char>` to `Vec[char]`, `&self` to
`self`, `String::new()` to `String.new()`, `get(&c)` to `get(c)`,
`unwrap_or(&0)` to `unwrap_or(0)`, `!s.is_empty()` to `not
s.is_empty()`, and `keys.into_iter()` and `values.into_iter()` to
`keys.clone().into_iter()` and `values.clone().into_iter()`, since a
bare parameter borrows and `into_iter` takes its argument whole. The
struct literal's shorthand `Encrypter { map, ... }`, the `Self` return
and `*entry(..).or_insert(0) += 1` are Kāra's too.

The array arm was first written reading `self.table[...]` into a plain
`let`, and the trie arm with its map of keys filled by
`get(..).unwrap_or(Vec.new())` and a `Node` list made with `to_vec()`;
`karac fix` made the first a `ref`, and gave the second `.cloned()` on
the look-up and `#[derive(Clone)]` on `Node`. In the same pass it also
put a `.clone()` on the list handed back to `insert`, answering a borrow
that the `.cloned()` beside it had already ended, so the trie arm keeps
one copy it does not need.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: a letter encrypted by finding its place among the keys, and
a string decrypted by trying every key whose value is each pair in
turn, every decryption written out into a `Set` and those in the
dictionary counted; nothing kept ahead. It checks 300 random cases of 1
to 8 keys, values of 2 and 3 letters, up to 8 words of 1 to 4 letters
and 12 calls; then 30 with every value `"aa"`; then 30 with values of
all 26 letters, so that they seldom repeat. All 360 are drawn before any
arm answers.

| | property |
|---|---|
| P1 | the answers are the statement read literally |
| P2 | each encryption `""` or twice as long as its word, each count from 0 to the size of the dictionary |
| P3 | the dictionary reversed: the same answers |
| P4 | each dictionary word's encryption, unless `""`, decrypts to at least 1, and the counts of the distinct encryptions add up to the words that encrypt |
| P5 | one more word in the dictionary: each count the same, or one more exactly where the string is that word's encryption |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 cases: checksum 987164755, 12960 checks
over 6 arms: 0 failures` under every lane in Verification; the checksum
of the literal answers was checked against a Python reading that writes
out the decryptions with `itertools.product` over each pair's keys. On a
failure it prints the first ten and then the count by property.

## Mutation testing

Thirty-one edits to the differential, six to the ★ arm and five to each
of the others, each run under `karac __mir-llvm-run`, and the kept ones
under `karac __mir-run` too. Seventeen are kept, three to each Kāra arm
and two to the Rust-template arm. Each kept one is killed, fails the
same way under both backends and not by a crash, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M3 | ★: every key given the first value | P1 262, P5 241, P6 262 |
| M5 | ★: a letter that is no key skipped, not failing the word | P1 265, P2 226, P6 265 |
| M6 | ★: the first dictionary word left out | P1 143, P3 169, P4 204, P6 143 |
| M7 | array: the table one letter off | P1 347, P5 320, P6 347 |
| M9 | array: each encryption counted twice | P1 276, P2 30, P4 312, P5 347, P6 276 |
| M11 | array: the pairs written in reverse order | P1 214, P5 152, P6 214 |
| M13 | trie: every node counted as a word | P1 163, P4 77, P5 93, P6 163 |
| M14 | trie: only the first key of each pair followed | P1 76, P4 97, P5 83, P6 76 |
| M15 | trie: each value standing for its last key only | P1 137, P4 170, P5 142, P6 137 |
| M17 | scan: a count of 1 at most | P1 28, P4 30, P5 19, P6 28 |
| M20 | scan: a word counted when its encryption begins the string | P1 329, P4 266, P5 96, P6 329 |
| M21 | scan: the values in reverse order | P1 256, P5 243, P6 256 |
| M22 | iter: each encryption reversed | P1 283, P5 253, P6 283 |
| M24 | iter: the values shifted one key along | P1 331, P5 325, P6 331 |
| M25 | iter: one-letter words not counted | P1 141, P4 202, P5 67, P6 141 |
| M27 | solution: each count starting at 1 | P1 276, P2 29, P4 312, P5 328, P6 276 |
| M30 | solution: a count one short | P1 360, P2 360, P4 312, P6 360 |

P1 and P6 kill all seventeen, P5 fourteen, P4 ten, P2 four, and P3
one. P3 reverses the dictionary, and only an edit that treats one place
in it differently notices (M6). P2 catches what leaves the answer's
range: an encryption shortened by a skipped letter (M5), and counts past
the dictionary or below 0 (M9, M27, M30). P5 misses the edits that are
wrong the same way with one more word as without it: a skipped letter
(M5), a word left out (M6), and every count one short (M30).

Of the thirty-one, fourteen were not kept. One survives and is
equivalent: the ★ arm counting `""` among the encryptions (M1), which no
call can ask for, since every string to decrypt has two letters or
more. None crashes, and none differs between the backends. Eleven fail
as a kept one does: the ★ arm's encryptions counted once or capped at 1
and the iter arm's counted once (M2, M4, M23) as the scan arm's count of
1 at most (M17); the array, scan and template arms' letter that is no
key skipped (M8, M19, M29) as the ★ arm's (M5); the scan arm's first
word dropped (M18) as the ★ arm's (M6); the array and template arms'
one-letter words not counted (M10, M28) as the iter arm's (M25); the
iter arm's counts doubled (M26) as the array arm's (M9); and the
template's values reversed (M31) as the scan arm's (M21). Two fail
their own way and are left out for the count of three: the trie arm's
word ends never marked and its pairs read backwards (M12, M16).

## Verification

Every arm prints the same output as `encrypter.py` under `karac
__mir-run` (the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 1.8 s to 2.6 s, and the scan arm,
which encrypts the dictionary again at every decryption, 6.8 s. The
differential takes 2.0 s.

## Benchmarks

The bench draws 26 keys with values of 3 letters, 100 dictionary words
of 100 letters and 200 calls once (encryptions of up to 2000 letters,
and decryptions of dictionary words' encryptions or of random letters),
then plays 500 rounds, one dictionary word drawn again before each, a
new `Encrypter` made and all 200 calls answered, with the ★ arm in all
five languages. C has no map of its own: its values sit in a table of
256 indexed by the character and its counts in an open-addressing hash
table of strings. Every implementation prints `500 rounds of 200 calls:
checksum 342466385`.

BENCHTAB
