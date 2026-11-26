# 1410. HTML Entity Parser

HTML entity parser is the parser that takes HTML code as input and
replaces all the entities of the special characters by the characters
themselves. The special characters and their entities for HTML are:
quotation mark, `&quot;` for `"`; single quote mark, `&apos;` for `'`;
ampersand, `&amp;` for `&`; greater than sign, `&gt;` for `>`; less than
sign, `&lt;` for `<`; slash, `&frasl;` for `/`. Given the input `text`
string to the HTML parser, implement the entity parser: return the text
after replacing the entities by the special characters.

```
"&amp; is an HTML entity but &ambassador; is not."  ->  "& is an HTML entity but &ambassador; is not."
"and I quote: &quot;...&quot;"                      ->  "and I quote: \"...\""
```

**Constraints:** `1 <= text.length <= 10^5`, the string may contain any
of the 256 ASCII characters.

Each arm is `fn entity_parser(text: String) -> String`. The text is read
once from the left, so `&amp;gt;` gives `&gt;`, not `>`.

## Approaches

| file | mechanism |
|---|---|
| `entity_parser.kara` ★ | one walk: at each `&`, the name up to the next `;` within the seven characters the longest entity takes, matched as a string against the six, and the `&` kept as it is when it names none. O(n) |
| `entity_parser_replace.kara` | each entity replaced through the whole text in turn with `replace`, `&amp;` last, so an `&` it makes cannot start another. O(n) |
| `entity_parser_map.kara` | the six in a `Map[String, String]`, and at each `&` the four to seven characters from it looked up, the shortest first. O(n) |
| `entity_parser_split.kara` | the text `split` at each `&`: every piece but the first followed an `&`, and starts with an entity's name and `;` or keeps the `&`. O(n) |
| `entity_parser_solution.kara` | a Rust solution as LeetCode's Rust users write it (`text.as_bytes()`, a `'outer:` loop over the six with `starts_with`, `continue 'outer` on a hit), carried to Kāra by `karac fix` |
| `differential.kara` | the five arms against the statement read literally, five more properties |

Every arm prints the same 5 lines: LeetCode's two examples, then five
more joined by ` | ` (`&gt; | &> | x / y <> 'z' | &quot"; | &`); the
constraints' most, 10^5 characters of `&amp;gt;` over and over and a
text of 20000 drawn pieces, each a letter, a space, a lone `&` or `;`,
or a whole or broken entity (`10^5 characters, 20000 pieces: 50000 50225
618446309`); and 2000 random texts of 1 to 30 such pieces (`2000 random
texts: 77274 characters, checksum 538567255`). `entity_parser.py`
mirrors the ★ arm, and its output is byte-identical. Every arm gives the
same output under `karac __mir-run`, `karac run`, `karac build` and
`karac __mir-llvm-run`.

The Mend loop: the ★, replace and map arms check clean as first written.
The split arm was first written with Rust's `!done`, and `karac fix`
writes `not done`, 2 fixes. The Rust solution takes one round of 14
fixes by `karac fix`'s count: `struct Solution;` to `struct Solution
{}`, `text.as_bytes()` to `text.bytes()`, `String::with_capacity` to
`String.with_capacity`, the pattern `&(k, v)` to `(k, v)`, and
`Solution::` to `Solution.`. Its labelled `continue 'outer`, its byte
literal `b'&'` and `bytes[i] as char` are taken as written. Every arm's
output matches on the first run.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: the text read from the left, and wherever one of the six
entities starts, compared letter by letter, its character written in its
place. LeetCode's examples, eight edge cases (a lone `&` and `;`,
`&frasl` cut at the end, `&amp;amp;`, `&&gt;`, all six back to back,
`&gtt;` and `&lt` beside whole ones, a slash) and the constraints' most,
10^5 characters of `&amp;gt;` and 10^5 drawn from the entities' own
letters, `&` and `;`, and 1991 random texts: 1 to 12 drawn pieces two
times in three, else 1 to 40 of those letters. Each case also draws a
second, shorter text.

The differential first printed a failing text with `{text:?}`; Debug
formatting is reserved and not implemented yet, and `karac fix` writes
`{text}`, 5 fixes.

| | property |
|---|---|
| P1 | the statement read literally |
| P2 | a text with no `&` comes back as it is |
| P3 | no entity holds a space, so the text and the second one joined by a space parse as the two parsed and joined |
| P4 | the text with every `&` written `&amp;` parses back to the text |
| P5 | the text with all six characters written as their entities parses back to the text |
| P6 | the ★ arm's answer |

All 60,090 checks pass on every arm: `2003 cases: checksum 598664405,
60090 checks over 5 arms: 0 failures`, under `karac __mir-run`, `karac
run`, `karac build` and `karac __mir-llvm-run`. Python, by one `re.sub`
over the six names, gives the same checksum.

## Mutation testing

Ten edits to the differential, each run under both `karac
__mir-llvm-run` and `karac __mir-run`, two to each arm. Each is killed,
fails the same way under both backends and not by a crash.

| | edit | failures by property |
|---|---|---|
| M1 | ★: the window six characters, too short for `&frasl;` | P1 395, P6 1580 |
| M2 | ★: the walk stepping one short of the entity, so its `;` is copied too | P1 1177, P4 1849, P5 1849, P6 4708 |
| M3 | replace: `&amp;` never replaced | P1 435, P4 1849, P5 1849, P6 435 |
| M4 | replace: `&amp;` replaced first, so the `&` it makes starts another entity | P1 25, P4 1177, P5 1177, P6 25 |
| M5 | map: the names looked up only to six characters | P1 395, P6 395 |
| M6 | map: no name looked up that ends the text | P1 399, P3 399, P4 242, P5 242, P6 399 |
| M7 | split: an `&` that starts no entity dropped | P1 1688, P6 1688 |
| M8 | split: an entity's `;` kept after its character | P1 1177, P4 1849, P5 1849, P6 1177 |
| M9 | solution: the walk stepping one short of the entity, so its `;` is copied too | P1 1177, P4 1849, P5 1849, P6 1177 |
| M10 | solution: the entity's name written out in place of its character | P1 1177, P4 1849, P5 1849, P6 1177 |

A first M10, `continue 'outer` written `break`, so the character after
an entity is copied as if no entity had been found, was killed by a
panic, an index past the end when an entity ends the text, and was
replaced.

## Benchmarks

The bench draws a pool of 3 * 10^5 characters in the same pieces and
runs the ★ arm on 300 windows of 10^5 of them, each window's start drawn
from the checksum so far, folding each answer's length and bytes. Every
implementation prints `300 windows of 10^5 characters: checksum
634362823`.

BENCHTAB

Kāra is within a third of Rust's time here, measured by hand at 0.22 s
against Rust's 0.17 s, with overflow checks on or off, and C's 0.17 s.
