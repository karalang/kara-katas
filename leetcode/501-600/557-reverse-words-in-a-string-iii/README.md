# 557. Reverse Words in a String III

Given a string `s`, reverse the order of characters in each word within
a sentence while still preserving whitespace and initial word order.

```
s = "Let's take LeetCode contest"  ->  "s'teL ekat edoCteeL tsetnoc"
s = "Mr Ding"                      ->  "rM gniD"
```

**Constraints:** `1 <= s.length <= 5 * 10^4`; `s` contains printable
ASCII characters and no leading or trailing spaces; there is at least
one word, and all the words are separated by a single space.

## Approaches

Every arm is `fn reverse_words(s: String) -> String`.

| file | mechanism |
|---|---|
| `reverse_words_in_a_string_iii.kara` ★ | `split(" ")`, each word's `chars().rev()` collected into a `String`, the words joined with single spaces; O(length) |
| `reverse_words_in_a_string_iii_bytes.kara` | the text copied once into a `Vec[u8]`, each word found by scanning for the next space and reversed in place by swapping its ends inwards, read back with `String.from_utf8` |
| `reverse_words_in_a_string_iii_stack.kara` | one pass over the chars: letters pushed onto a stack, popped empty into the output at each space and at the end |
| `reverse_words_in_a_string_iii_chain.kara` | one iterator chain: `split(" ").iter().map(\|w\| w.chars().rev().collect()).collect()` into a `Vec[String]`, then joined |
| `differential.kara` | the four arms against the definition, five properties |

Every arm prints the same 9 lines: six texts at the edges (the two
examples, one letter, two short words, palindromes, and punctuation with
brackets), a checksum over 300 random texts of 1 to 20 words of 1 to
12 characters, and the problem's largest texts, 50,000 characters as one
word and 49,999 as 25,000 words of one letter.
`reverse_words_in_a_string_iii.py` mirrors the ★ arm and its output is
byte-identical.

The chain arm did not build when the kata was written; see Compiler
findings. It was kept as written, and since both of its findings were
fixed it builds and prints the same output as the others.

## Differential

`differential.kara` holds copies of the four arms and the definition,
the statement read place by place: a space stays a space, and any other
character at place i is the one at the mirror place of the word i falls
in, found by walking out to the spaces on either side. Each arm is held
to the properties below on 1,000 random texts: 1 to 6 words of 1 to
5 letters from `a`, `b` and `c`, or 1 to 3 words of 1 to 60 printable
characters, in turn.

| | property |
|---|---|
| P1 | the answer is the definition's |
| P2 | the answer is as long as the text |
| P3 | the spaces are where they were |
| P4 | answering the answer gives the text back |
| P5 | the answer has the same characters as the text |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run` and `karac __mir-llvm-run`, and runs clean under `karac
__mir-llvm-asan`. While the chain arm did not build, neither did the
differential, and the measurements below were taken on a copy outside
this directory with the chain arm's inner `collect()` moved into a named
function.

## Mutation testing

Twelve edits to that workaround copy of the differential, two to each
arm that change its answers and one to each that does not, each run
under `karac __mir-run`. All eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the words joined with nothing between | 729 on each of P1 to P5 |
| M2 | ★: the words not reversed | P1 952 |
| M3 | bytes: each word's last byte left out of the swaps | P1 969 |
| M4 | bytes: the swapping stops one pair early | P1 650 |
| M5 | stack: the spaces not written | 729 on each of P1 to P5 |
| M6 | stack: letters written straight out, not stacked | P1 952 |
| M7 | chain: the whole text reversed for every word | 729 on each of P1 to P5 |
| M8 | chain: the words joined with two spaces | 729 on each of P1 to P5 |
| E1 | ★: split on the char `' '`, not the string | 0 |
| E2 | bytes: a word's middle byte swapped with itself | 0 |
| E3 | stack: any whitespace taken as the break | 0 |
| E4 | chain: the reversed word named before it is returned | 0 |

The 729 is the number of the 1,000 texts with more than one word: a
one-word text has no space to lose or double, and reversing the whole of
it is reversing its word. Every other mutant keeps the length, the
spaces and the characters and only puts them in the wrong places, so
only P1 sees it. M2 and M6 fail on exactly the 952 texts with a word
that does not read the same backwards; the small `a`, `b`, `c` texts
make palindromes common. E3 is safe because the only whitespace in the
text is the space.

## Verification

The four arms print the same output as
`reverse_words_in_a_string_iii.py` under `karac __mir-run` (the v2 MIR
interpreter) and `karac __mir-llvm-run`, and run clean under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer): output identical,
no error, no leak. `karac check` passes on every arm, the differential
and the bench program. The chain arm and the differential were rechecked
at kara `f6052c659c`, after B-2026-10-14-7 and B-2026-10-14-6 were
fixed; before that `karac check` and both MIR backends refused them.

The frozen legacy backends refuse every arm and the differential under
`karac run --interp`, `karac run` and `karac build`. The ★, bytes and
stack arms stop at ownership checking in the harness, at `{got[..10]}`
and `{checksum(got)}` in one f-string ("cannot move `got` while a slice
borrow into it is still live"); under v2 `checksum` borrows its
argument. Legacy refuses the bench program too (see Benchmarks). Legacy
is frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It builds 100 random texts of just
under 50,000 characters once, words of 1 to 12 printable characters;
then 50 times over every text is answered. Every implementation prints
`100 texts, 666566 words, 50 rounds each: checksum 865978134`, the Kāra
program under `karac __mir-run` included (611 s).

Rust splits with `split(' ')` and collects each word's `chars().rev()`
into a `String` as the Kāra arm does; Go reverses each word as a
`[]rune`, C copies each word backwards into its own `malloc`'d string,
and Python uses `w[::-1]`. Spot timings on a shared 4-core container,
three runs each (two for Python; `bench.sh` timings need a quiet
machine):

| | time |
|---|---|
| C (`clang -O3`) | 1.82 to 2.00 s |
| Rust (`rustc -O`) | 3.23 to 3.37 s |
| Rust (`rustc -O -C overflow-checks=on`) | 3.14 to 3.30 s |
| Go | 3.67 to 3.79 s |
| Python | 5.19 to 5.28 s |
| Kāra (`karac build --mir`) | 6.30 to 6.95 s |

The legacy `karac build` refuses this program: it moves `texts[(round *
7 + g) % count]` out of the index where v2 borrows it. So `bench.sh`
builds the Kāra program with `karac build --mir`, the v2 compiled
backend; that edit is by hand, on top of the `scripts/new-bench.sh`
output. The `--mir` row is timed at kara `af2123abc5`. Under `karac
__mir-llvm-run` the program prints the same line in 30.6 s, compile
included; that JITs the MIR's IR without optimization passes, so it is
not a benchmark.

The Kāra row is about twice Rust's. Most of the gap is `split`.
With the reversing and joining taken out, splitting the texts alone
takes 2.37 s against Rust's 0.57: Kāra's `split` builds a `Vec[String]`,
a fresh allocation and copy for every word, where Rust's yields views
into the text. The language's own spec has `split` return an iterator
(kara B-2026-10-12-7), and B-2026-10-03-10 records its allocation per
word. Reversing a 6-character word ten million times costs 0.86 s
against Rust's 0.44, the rest of the gap: on the compiled MIR backend
each char walked backwards is an out-of-line runtime call,
`karac_mir_char_before_byte`, and each char pushed is another,
`karac_mir_string_push_char`
(B-2026-10-13-30, B-2026-10-13-31, B-2026-10-13-35).

## Compiler findings

Three filed from the chain arm, all on a `collect()` that is a closure's
result or sits inside a closure's body, and all three now fixed:

- **B-2026-10-14-7**, fixed in kara `86f1298387`. `karac check` refused
  `let words: Vec[String] = s.split(" ").iter().map(|w| w.chars().rev().collect()).collect();`
  with "expected 'Vec[String]', found 'Vec[Vec[char]]'": the inner
  `collect()` was not given the closure's expected result type, so it
  fell back to a `Vec`. A sibling of B-2026-10-12-33.
- **B-2026-10-14-6**, fixed in kara `0c4bec8fa5`. On the MIR backends
  the same line did not build: "an expression whose type does not lower
  (UnknownParam C)", with or without a type on the binding.
- **B-2026-10-14-8**, fixed in kara `d0d9435e8a`. `karac check` refused
  any `collect()` into a non-`Vec` target inside a closure body, `|w| {
  let s: String = w.chars().collect(); s.len() }`, with an ownership
  error about a binding the user never wrote, `__karac_collect_dst_N`,
  "moved inside a loop".

Rechecked at kara `f6052c659c`: the chain arm runs as written on both
MIR backends and passes `karac check`.

The chain arm writes `s.split(" ").iter()` because `split` returns a
`Vec` today; the spec's `split` is an iterator and would take the `map`
directly (B-2026-10-12-7). The legacy failures above are not filed
because legacy is frozen.
