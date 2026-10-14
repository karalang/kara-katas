# 591. Tag Validator

Given a string representing a code snippet, implement a tag validator to
parse the code and return whether it is valid. A code snippet is valid
if all the following rules hold:

1) The code must be wrapped in a valid closed tag. Otherwise, the code
is invalid. 2) A closed tag (not necessarily valid) has exactly the
following format: `<TAG_NAME>TAG_CONTENT</TAG_NAME>`. Among them,
`<TAG_NAME>` is the start tag, and `</TAG_NAME>` is the end tag. The
`TAG_NAME` in start and end tags should be the same. A closed tag is
valid if and only if the `TAG_NAME` and `TAG_CONTENT` are valid. 3) A
valid `TAG_NAME` only contains upper-case letters, and has length in
range `[1,9]`. Otherwise, the `TAG_NAME` is invalid. 4) A valid
`TAG_CONTENT` may contain other valid closed tags, cdata and any
characters EXCEPT unmatched `<`, unmatched start and end tag, and
unmatched or closed tags with invalid `TAG_NAME`. Otherwise, the
`TAG_CONTENT` is invalid. 5) A start tag is unmatched if no end tag
exists with the same `TAG_NAME`, and vice versa. However, you also need
to consider the issue of unbalanced when tags are nested. 6) A `<` is
unmatched if you cannot find a subsequent `>`. And when you find a `<`
or `</`, all the subsequent characters until the next `>` should be
parsed as `TAG_NAME` (not necessarily valid). 7) The cdata has the
following format: `<![CDATA[CDATA_CONTENT]]>`. The range of
`CDATA_CONTENT` is defined as the characters between `<![CDATA[` and the
first subsequent `]]>`. 8) `CDATA_CONTENT` may contain any characters.
The function of cdata is to forbid the validator to parse
`CDATA_CONTENT`, so even if it has some characters that can be parsed as
a tag (no matter valid or invalid), you should treat it as regular
characters.

```
"<DIV>This is the first line <![CDATA[<div>]]></DIV>"  ->  true
"<DIV>>>  ![cdata[]] <![CDATA[<div>]>]]>]]>>]</DIV>"    ->  true
"<A>  <B> </A>   </B>"                                  ->  false
```

**Constraints:** `1 <= code.length <= 500`; `code` consists of English
letters, digits, `<`, `>`, `/`, `!`, `[`, `]`, `.`, and `' '`.

## Approaches

Every arm is `fn is_valid(code: Str) -> bool`.

| file | mechanism |
|---|---|
| `tag_validator.kara` ★ | one scan with a `Vec[String]` stack of open tags: a cdata section is skipped to its `]]>`, an end tag must name the top of the stack, a start tag with a valid name is pushed, and the stack may be empty only at the start and the end; O(n) |
| `tag_validator_slices.kara` | the same scan over `rest`, a `Str` view of what is left, cut from the front as each piece is read, with the open names kept as views in a `Vec[Str]`; O(n) |
| `tag_validator_descent.kara` | recursive descent over the code's `Vec[char]`: the rules as a grammar, a closed tag being a start tag, content and the matching end tag, and content being text, cdata and closed tags; O(n) |
| `tag_validator_reduce.kara` | rewriting: every cdata section becomes `#`, then an innermost closed tag (valid name, text with no `<`, matching end tag) becomes `@` over and over; the code was valid when one `@` is left; O(n^2) |
| `differential.kara` | the four arms against the definition, five properties |

The reduce arm is the rewriting the problem is often solved with by
regular expression, written without one. Its marks, `#` and `@`, are
outside the characters the problem allows, so neither can be mistaken
for the code's own text; with a letter for the mark, a code of that one
letter would pass.

Every arm prints the same 25 lines: the problem's examples (the three
above and the five from its earlier statement), 14 cases at the edges
(names of 9 and 10 letters, an empty name, text or cdata outside the
outer tag, two tags side by side, a cdata section hiding an end tag, the
first `]]>` ending a cdata section, an unclosed one, nesting right and
wrong, and a lone start tag or letter), a count and checksum over
300 random snippets, and two codes of 500 characters, the problem's
longest: tags nested 38 deep, and 25 tags side by side with a cdata
section in each. `tag_validator.py` mirrors the ★ arm and its output is
byte-identical.

The harness picks its random names and text from `Vec[Str]` lists with
`let name = names[..]`, which `karac check` refuses; see Compiler
findings. The arms themselves are not affected.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the rules read as a grammar and decided for every stretch of the code at
once: whether the characters from one position to another are valid
content (empty, or a character other than `<`, a cdata section through
the first `]]>` after its start, or a valid closed tag, followed by more
content), and whether the whole code is one valid closed tag, its name
read up to the next `>`. It builds a table over every pair of positions,
so it shares no scanning with the arms. Each arm is held to the
properties below on 1,000 random snippets of tags, cdata and text up to
two deep, with wrong names, missing or wrong end tags, stray `<` and
open cdata sections, and text before or a second tag after the outer one
now and then; 310 of them are valid.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | a valid code is still valid inside one more tag, and not valid twice over |
| P3 | a cdata section put in just after the first `>` changes nothing |
| P4 | swapping `X` with `Y` and `x` with `y` throughout changes nothing |
| P5 | a space after the code makes it invalid |

It prints `1000 cases (310 valid), 4 arms, 20000 checks, 0 failures`
under `karac __mir-run` and `karac __mir-llvm-run`, and runs clean under
`karac __mir-llvm-asan`.

## Mutation testing

Twelve edits to the differential, two to each arm that change its
answers and one to each that does not, each run under `karac __mir-run`.
All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a name of 10 letters allowed | P1 23 |
| M2 | ★: more after the outer tag allowed | P1 34, P2 344 |
| M3 | slices: an end tag closes whatever is open | P1 74 |
| M4 | slices: an empty name allowed | P1 26 |
| M5 | descent: an end tag's name not compared | P1 74 |
| M6 | descent: a `<` in content read as text | P1 105, P2 313 |
| M7 | reduce: a `<` allowed in an innermost tag's text | P1 115, P2 6 |
| M8 | reduce: any `@` left counted as valid | P1 280, P2 590, P5 590 |
| E1 | ★: a `<` found by comparing one character | 0 |
| E2 | slices: upper case tested by range | 0 |
| E3 | descent: an end tag found by its two characters | 0 |
| E4 | reduce: a cdata section turned into `.`, a character the problem allows | 0 |

Most mutants show only against the definition, P1, on the few cases that
reach the rule they break: 23 snippets with a 10-letter name, 26 with an
empty one. M3 and M5 make the same mistake in two arms, an end tag
accepted whatever its name, and fail on the same 74. P2 is what sees
M2, M6 and M8 most: a valid code doubled is the case M2 lets through,
and M8 counts any `@` left as valid, so a valid code doubled, or
followed by a space, passes too. P3 and P4 see no mutant; they are there
for an arm that reads into cdata or treats some letters apart from
others, and none of these does. E4 is safe because a cdata section only
ever stands as text inside a tag, where `.` is text too.

## Verification

Every arm prints the same output as `tag_validator.py` under `karac
__mir-run` (the v2 MIR interpreter) and `karac __mir-llvm-run`, and runs
clean under `karac __mir-llvm-asan` (AddressSanitizer and
LeakSanitizer): output identical, no error, no leak; so does the
differential. `karac check` refuses every arm, the differential and the
bench program, each only in the harness's two reads from a `Vec[Str]`
(kara B-2026-10-12-14); the arms' own code passes. `karac check` and
`karac __mir-run` at kara `7adae1f0aa`, the compiled MIR backend at
`555c29b44e`.

The frozen legacy backends refuse every arm, the differential and the
bench program under `karac run --interp`, `karac run` and `karac build`,
at type checking: each reads a string slice such as `code[start..start +
k]`, or an element of a `Vec[Str]`, as a move out of an index
(E_INDEX_MOVE_NON_COPY). Legacy is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 1,000 random snippets of
200 to 500 characters once, from names that are all valid, text with no
stray `<`, cdata sections, and one end tag in 40 wrong, so that 668 of
them are valid and the scan of most runs to the end; then 1,000 times
over it validates every one. Every implementation prints `1000 snippets,
1000 rounds: 668000 valid, checksum 237470740`, the Kāra program under
`karac __mir-run` included (540 s).

Each implementation is the same scan: Rust over `&str` with
`starts_with` and `find`, and a `Vec<String>` stack as the Kāra arm's
holds `String`s; Go over `string` with `strings.HasPrefix` and
`strings.Index`, its stack holding substrings that share the code's
bytes; C with `memcmp`, a search by hand and a stack of `malloc`'d
copies of the names, freed at the end of each call; Python with
`startswith` and `find`. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.14 to 1.27 s |
| Rust (`rustc -O`) | 1.63 to 1.91 s |
| Rust (`rustc -O -C overflow-checks=on`) | 1.57 to 1.80 s |
| Go | 1.73 to 1.96 s |
| Python | 33.3 to 33.4 s |
| Kāra (`karac build --mir`) | 7.41 to 8.06 s |

So `bench.sh` builds the Kāra program with `karac build --mir`, the
v2 compiled backend; that edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`555c29b44e`. Under `karac __mir-llvm-run` the program prints the same
line in 36.7 s, compile included; that JITs the MIR's IR without
optimization passes, so it is not a benchmark.

The Kāra row is about 4.3 times Rust's. A callgrind profile of the same
program at 30 rounds puts most of its instructions in the string
operations, which the compiled backend makes as calls into the runtime:
`karac_mir_str_test` (the `starts_with` tests, 13%),
`karac_mir_str_view` (the `code[i..]` views, 8%), the `memcmp` under
them (8%), and code inside the runtime next to `karac_mir_str_find`
(15%). Every character of text takes a view and up to three
`starts_with` tests, each a call, where Rust inlines all four. That this
is where the gap comes from is read from the profile; it is not measured
by changing the program.

## Compiler findings

None new. The harness, the differential and the bench program pick
random names and text with `let name = names[..]` from a `Vec[Str]`, and
`karac check` refuses that as a move out of a collection element, though
design.md § Strings says `Str` "is `Copy`"; that is kara
B-2026-10-12-14 (open). Both MIR backends run it. The legacy failures
above are not filed because legacy is frozen.
