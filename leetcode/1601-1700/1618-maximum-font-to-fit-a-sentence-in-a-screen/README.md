# 1618. Maximum Font to Fit a Sentence in a Screen

You are given a string `text`. We want to display `text` on a screen of
width `w` and height `h`. You can choose any font size from array
`fonts`, which contains the available font sizes **in ascending order**.

You can use the `FontInfo` interface to get the width and height of any
character at any available font size:

```
interface FontInfo {
  // Returns the width of character ch on the screen using font size fontSize.
  // O(1) per call
  public int getWidth(int fontSize, char ch);

  // Returns the height of any character on the screen using font size fontSize.
  // O(1) per call
  public int getHeight(int fontSize);
}
```

The calculated width of `text` for some `fontSize` is the **sum** of every
`getWidth(fontSize, text[i])` call for each `0 <= i < text.length`
(**0-indexed**). The calculated height of `text` for some `fontSize` is
`getHeight(fontSize)`. Note that `text` is displayed on a **single
line**.

It is guaranteed that `FontInfo` will return the same value if you call
`getHeight` or `getWidth` with the same parameters, and that for any font
size `fontSize` and any character `ch`:
`getHeight(fontSize) <= getHeight(fontSize+1)` and
`getWidth(fontSize, ch) <= getWidth(fontSize+1, ch)`.

Return *the maximum font size you can use to display* `text` *on the
screen*. If `text` cannot fit on the display with any font size, return
`-1`.

```
text = "helloworld",   w = 80,   h = 20,  fonts = [6,8,10,12,14,16,18,24,36]  ->  6
text = "leetcode",     w = 1000, h = 50,  fonts = [1,2,4]                     ->  4
text = "easyquestion", w = 100,  h = 100, fonts = [10,15,20,25]               ->  -1
```

**Constraints:** `1 <= text.length <= 50000`; `text` contains only
lowercase English letters; `1 <= w <= 10^7`; `1 <= h <= 10^4`;
`1 <= fonts.length <= 10^5`; `1 <= fonts[i] <= 10^5`; `fonts` is sorted
in ascending order and does not contain duplicates.

## Approaches

| file | mechanism |
|---|---|
| `fonts.kara` ★ | the sizes that fit are a prefix of `fonts`, so a binary search for the last one that does: a probe checks the height, then adds up the widths with `chars().map(..).sum()`. The font is a `trait FontInfo` and the parameter `info: impl FontInfo`. O(n log m) for n letters and m sizes |
| `fonts_scan.kara` | the sizes from the largest down (`iter().rev()`), the first that fits answering; the widths summed with an early exit once past `w`. O(n m) |
| `fonts_partition.kara` | the letters counted once into `[0; 26]`, then `Slice.partition_point` over "fits", each probe adding 26 counts times widths. O(n + 26 log m) |
| `fonts_solution.kara` | LeetCode's Rust template carried by `karac fix`, a binary search through a `fits` closure. LeetCode hands Rust a concrete `&FontInfo`; here the harness's font is a trait, so the template's parameter is `&impl FontInfo` |
| `differential.kara` | the four arms against the statement read literally, six properties |

The harness's font gives a letter of base width `b` the width
`(size * b + 3) / 4` and a line the height `size + size / 4`, both rising
with the size as the problem promises. LeetCode's own font is hidden, so
on its first example, with every letter of base 4, the harness answers 8,
not 6; the other two agree.

Every arm prints the same 6 lines: the three examples, then the letters,
how many screens a size fits and a checksum of every answer for 3000
random screens of up to 10 letters, 300 of up to 1000, and 30 of up to
50000, each with its own random font and up to 20 sizes. `fonts.py`
mirrors the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the four arms and the statement read
literally: every size on offer, kept when its height is no more than `h`
and its letters' widths, added up in `i64`, no more than `w`; the largest
kept, or -1. It checks 3000 random screens of 1 to 40 letters drawn from
an alphabet of 1 to 26, fonts of 1 to 12 sizes and a line height of
`size + size * t / 4` for `t` from 0 to 2. Every random choice, the
shuffle of P2 included, is drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the letters shuffled leave the answer |
| P3 | the sizes above the answer dropped leave the answer |
| P4 | a screen exactly as wide as the text at the answer keeps it; one unit narrower takes a smaller size or none |
| P5 | a screen twice as wide, or twice as tall, never lowers the answer |
| P6 | each arm agrees with at least two of the other three |

The differential prints `3000 problems: checksum 462776957, 72000 checks
over 4 arms: 0 failures` under every lane in Verification. On a failure
it prints the first ten and then the count by property.

## Mutation testing

Ten edits to the differential, two or three to each arm, each run under
`karac __mir-run` and `karac __mir-llvm-run`. All ten are killed, each
the same way under both backends: M2 by never finishing, the rest by
their failures. P3 lets five of them through, since a screen that a
wrong arm misjudges stays misjudged with fewer sizes on offer.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: a line as high as the screen refused | P1 67, P2 67, P3 67, P4 67, P5 67, P6 67 |
| M2 | ★: `lo = mid` on a fit, not `mid + 1` | never finishes (past 300 s under both) |
| M3 | ★: the answer read from `fonts[lo / 2]`, not `fonts[lo - 1]` | P1 1380, P2 1380, P3 1380, P4 1380, P5 1380, P6 1380 |
| M4 | scan: the sizes from the smallest up | P1 1887, P2 1887, P3 1887, P4 1887, P5 1887, P6 1887 |
| M5 | scan: a text exactly as wide as the screen refused | P1 54, P2 54, P3 54, P4 2507, P5 54, P6 54 |
| M6 | scan: -1 at the first size too high, not the next size down | P1 516, P2 516, P4 516, P5 516, P6 516 |
| M7 | partition: a letter's count set to 1, not added to | P1 1384, P2 1384, P4 2233, P6 1384 |
| M8 | partition: the letter `z` left out of the width | P1 7, P2 7, P4 45, P6 7 |
| M9 | template: a line as high as the screen refused | P1 67, P2 67, P3 67, P4 67, P5 67, P6 67 |
| M10 | template: one unit of width to spare | P1 48, P2 48, P4 2507, P6 48 |

A first M9, the template's `mid` taken a third of the way rather than
half, was not killed, and could not be: any `mid` in `[lo, hi)` is still
a correct binary search. It was replaced.

## Benchmarks

The bench makes 200 random texts of 5000 letters and one font, all of it
first. Then each text is asked about 40 random screens against 60 sizes
(3, 6, .., 180), the ★ binary search in all five languages. Every
implementation prints `8000 screens of 5000 letters: sizes total 130103,
checksum 636392522`. C and Go index the text's bytes, Kāra and Rust walk
its `chars()`; Go takes the font as its concrete type, as Kāra and Rust
monomorphize the `impl FontInfo` generic.

Timings on a 4-core container, medians of eight interleaved runs of each
compiled program and one of Python, with kara `f949423e35` on LLVM 22:

| | median |
|---|---|
| C (`clang -O3`) | 0.138 s |
| Rust (`rustc -O`) | 0.189 s |
| Go | 0.241 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.292 s |
| Kāra (`karac build`) | 0.320 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.321 s |
| Python | 15 s |

Kāra is within a tenth of Rust under overflow checks, the equal-safety
comparison, and 1.7 times plain Rust: both walk the text as `char`s and
add widths with a checked `i64` add, which `rustc -O` leaves unchecked.
C and Go index bytes.

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time is not above its real time (0.335 s and 0.343 s on one run).

## Verification

All four arms print the same output as `fonts.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and
`karac __mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no
error. `karac run` and a `karac build` binary print the same output for
them, the differential and the bench. `karac check` reports nothing on
any of them, and `karac fix` has nothing left to change. Checked at kara
`f949423e35`.

## Writing it

The ★ arm was first written with `info: ref impl FontInfo`, the borrow
spelled out, and passing it on from `max_font` to `fits` was refused:
"expected 'ref impl FontInfo', found 'ref impl FontInfo'", and each call
with a `Font` "expected 'impl FontInfo', found 'Font'". Argument-position
`impl Trait` is sugar for an anonymous generic (design.md § `impl
Trait`), but the desugar rewrote only a bare `impl Trait`, so under
`ref` the type stayed an opaque existential that nothing matched. Kara
f949423e35 desugars `ref impl Trait` and `mut ref impl Trait` too
(B-2026-11-18-42). The arms now take the plain `info: impl FontInfo`, since a bare
parameter borrows; `ref impl` checks as well.

`karac fix` made the ★ arm's `let (mut lo, mut hi)` into `let mut (lo,
hi)` and took off `as i64` casts the widening makes redundant, in the
harness index `(ch as u32 - 'a' as u32) as i64` among them. The scan
and partition arms were written in Kāra; `karac fix` took the same casts
off the partition arm. The differential's `text.clone()` arguments to
parameters that only borrow were flagged `redundant_clone` and dropped.

The Rust template took one `karac fix` of 12 edits: `struct Solution;`
to `struct Solution {}`, `Vec<i32>` to `Vec[i32]`, `&impl FontInfo` to
`impl FontInfo`, the closure's `-> bool` dropped, `let (mut lo, mut hi)`
to `let mut (lo, hi)`, and the harness's `"..".to_string()` arguments to
plain literals. It then checks and agrees with no hand edit.
