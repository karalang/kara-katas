# 1807. Evaluate the Bracket Pairs of a String

You are given a string `s` that contains some bracket pairs, with each
pair containing a non-empty key. You know the values of a wide range of
keys, represented by a 2D string array `knowledge` where each
`knowledge[i] = [keyi, valuei]`. You start evaluating all of the bracket
pairs: when you evaluate a bracket pair that contains some key `keyi`,
you replace `keyi` and the bracket pair with the key's corresponding
`valuei`; if you do not know the value of the key, you replace `keyi`
and the bracket pair with a question mark `"?"`. Each key appears at
most once in `knowledge`, and there will not be any nested brackets in
`s`. Return the resulting string after evaluating all of the bracket
pairs.

```
s = "(name)is(age)yearsold", knowledge = [["name","bob"],["age","two"]]  ->  "bobistwoyearsold"
s = "hi(name)", knowledge = [["a","b"]]                                  ->  "hi?"
s = "(a)(a)(a)aaa", knowledge = [["a","yes"]]                            ->  "yesyesyesaaa"
```

**Constraints:** `1 <= s.length <= 10^5`, `0 <= knowledge.length <=
10^5`, `1 <= keyi.length, valuei.length <= 10`, `s` consists of
lowercase English letters and round brackets, every `(` has a matching
`)`, every bracket pair holds a non-empty key, there are no nested
brackets, and `keyi` and `valuei` consist of lowercase English letters,
each `keyi` unique.

The arms are `fn evaluate(s: String, knowledge: Vec[Vec[String]]) ->
String`.

## Approaches

| file | mechanism |
|---|---|
| `evaluate.kara` ★ | the knowledge put in a `Map[String, String]`, and one walk of `s`'s chars: the text outside brackets copied, a key gathered inside them, and at each `)` the key's value, or `?` for a key the map lacks, written. O(n + total knowledge length) |
| `evaluate_split.kara` | `s` split at every `(` with `split`: the first piece is text as it stands, and every other piece a key, its `)` and text, parted by `split_once(")")`. O(n + total knowledge length) |
| `evaluate_sorted.kara` | no `Map`: the knowledge sorted by key with `sort_by`, and each key looked up by binary search over the sorted pairs, two `partition_point`s. O(n log k + k log k) |
| `evaluate_views.kara` | no copies until the answer: a `Map[Str, Str]` of views into the knowledge, `s` walked by byte index, and each key looked up as a `Str` view `s[start..end]`. O(n + k) |
| `evaluate_solution.kara` | a Rust solution as LeetCode's Rust users write it (a `HashMap<&str, &str>` collected from `as_str` pairs, a `match c` with a guarded arm, `unwrap_or(&"?")`), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 6 lines: LeetCode's three examples
(`bobistwoyearsold`, `hi?`, `yesyesyesaaa`); four edges, no brackets, no
knowledge, two keys that are each other's values, and a value of 10
letters for a key of 1 (`plain ?b? yx abcdefghij`); the constraints'
most, `10^5` knowledge pairs and an `s` of 99984 characters of letters
and bracketed keys, its answer folded to a hash (`the most: 99984
characters to 69507, fold 100734004`); and 3000 random cases of up to 8
keys of 1 to 3 letters from a to c and up to 12 pieces of text and keys
(`3000 random cases: checksum 893844942`). `evaluate.py` mirrors the ★
arm, and its output is byte-identical. Every arm gives the same output
under `karac __mir-run`, `karac run`, `karac build` and `karac
__mir-llvm-run`.

The Mend loop: the ★, split and views arms check clean as first written.
The harness's hash cast each byte `b as i64`, a widening Kāra makes
implicitly (`lossless_cast`), and `karac fix` removed it, 1 fix. The
sorted arm was first written with Rust's `sorted.binary_search_by(|pair|
pair[0].cmp(key))` matched on `Ok(at)` and `Err(_)`; Kāra has no
`binary_search_by`, and check names the two `partition_point`s that give
Rust's `Ok` and `karac fix` rewrote the `match` through them, 1 fix: the
upper bound `partition_point(|pair| pair[0].cmp(key) !=
Ordering.Greater)`, and a match when the lower bound lies below it, the
pair at the upper bound less one. The Rust solution takes 22 fixes by
`karac fix`'s count, and its diff is: `use std::collections::HashMap;`
dropped and `struct Solution {}` added above the `impl`;
`Vec<Vec<String>>` to `Vec[Vec[String]]`; `HashMap<&str, &str>` to
`Map[Str, Str]`; `String::new()` to `String.new()`; `unwrap_or(&"?")` to
`unwrap_or("?")`; and `Solution::` to `Solution.` in the harness. Every
arm's output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the first bracket pair found with `find`, its key looked for
pair by pair through the knowledge, the pair replaced by the value found
or by `?`, and again until no `(` is left. LeetCode's examples, the
edges, the constraints' most, and 1992 random cases drawn as the
harness's are. Each arm meets six properties on each case:

| property | what it checks |
|---|---|
| P1 | the statement read literally, for an `s` of at most 1000 characters |
| P2 | the knowledge in reverse order gives the same answer |
| P3 | a pair for a key that is not in `s` changes nothing |
| P4 | no answer holds a bracket, and with no knowledge each bracket pair becomes one `?` |
| P5 | `s` written twice gives the answer twice |
| P6 | the ★ arm's answer |

Check refused three lines of the differential, each with a fix: two `|c|
*c == ..` closures over a string's chars, a `char` that is copied, and
the literal reading's `out[..open].to_string() + value + out[close +
1..]`, whose last operand is a `Str` view where `+` takes an owned
`String`; its caret is under the left operand,
`out[..open].to_string() + value`, as B-2026-11-26-84 reports, and its fix appends `.to_string()`
to the right one. `karac fix` made all three, 3 fixes. All 60,000 checks
pass on every arm: `2000 cases: checksum 593621398, 60000 checks over 5
arms: 0 failures`, under `karac __mir-run`, `karac run`, `karac build`
and `karac __mir-llvm-run`. Python, running the ★ arm's mirror over the
same cases, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: a key never cleared after its `)` | P1 588, P5 379, P6 2356 |
| M2 | ★: a key the map lacks written as it stands | P1 1759, P4 1847, P6 7040 |
| M3 | split: the text after each `)` left out | P1 1513, P5 850, P6 1514 |
| M4 | split: the text before the first `(` left out | P1 1003, P5 850, P6 1003 |
| M5 | sorted: the pairs sorted by value, not by key | P1 457, P2 5, P3 262, P6 458 |
| M6 | sorted: any key with a smaller one before it taken as found | P1 1401, P6 1402 |
| M7 | views: the walk resumed at the `)`, not past it | P1 1846, P4 1847, P6 1847 |
| M8 | views: each key and value swapped in the map | P1 770, P2 2, P6 771 |
| M9 | solution: a key never cleared after its `)` | P1 588, P5 379, P6 589 |
| M10 | solution: a missing key written as nothing, not `?` | P1 1759, P4 1847, P6 1760 |

## Benchmarks

The bench builds 40 strings of about `10^5` characters, letters and keys
of up to 8 letters from a to d in brackets, and 40 knowledge lists of
`2 * 10^4` pairs once, and makes 200 calls of the ★ arm, each string and
list drawn from the checksum so far. The first draft drew `2 * 10^4`
distinct keys of up to 6 letters from a to d, of which there are only
5460, and never finished; keys of up to 8 letters fixed it. Check warned
once that `out.len() as i64` casts a value already `i64`
(`redundant_cast`) and once that a `u8` widens to `i64` implicitly, and
both casts were removed by hand. The C mirror keeps the map as an
open-addressed table of copied keys and values hashed by FNV-1a. Every
implementation prints `200 calls over 40 strings of 10^5 characters:
checksum 291793240`.

BENCHTAB

Measured by hand, best of three on a machine shared with a test run,
Kāra takes 2.0 s against Rust's 2.0 s (2.0 s with
overflow checks on), C's 0.75 s and Go's 1.9 s; Python takes 10.7 s.
