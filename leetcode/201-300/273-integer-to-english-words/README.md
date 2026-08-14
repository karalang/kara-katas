# 273. Integer to English Words

Convert a non-negative integer to its English words spelling.

```
0           -> Zero
123         -> One Hundred Twenty Three
1000010     -> One Million Ten
12345       -> Twelve Thousand Three Hundred Forty Five
2147483647  -> Two Billion One Hundred Forty Seven Million
               Four Hundred Eighty Three Thousand Six Hundred Forty Seven
```

**Constraints:** `0 ≤ num ≤ 2³¹ − 1`.

## Approaches

| file | mechanism | cost |
|---|---|---|
| `int_to_words.kara` ★ | split into three-digit groups, name each, tag with a scale | O(digits) |
| `int_to_words_places.kara` | walk the decimal digits, decide each from its position | O(digits) |
| `int_to_words_table.kara` | precompute all 1,000 groups bottom-up, then look up | O(1) after O(1000) |
| `differential.kara` | 50,032 probes, three solvers plus a shape oracle | — |
| `bench/spell.kara` | the ★ chunker as a benchmark kernel, five languages | — |

## English numerals are periodic with period 1000

Every group of three digits is spelled by the same rules and then labelled
Thousand / Million / Billion, so the whole problem is one function over `1..999`
plus a loop. The ★ solver peels `n % 1000` off the right; the recursion inside a
group is only two levels deep.

Three things go wrong, and none of them are the arithmetic.

**A zero group emits nothing.** `1000000` is "One Million", not "One Million Zero
Thousand Zero" — but `0` itself is "Zero". The empty string is the natural return
for a zero group, which forces the whole-number case to be special-cased *before*
the loop rather than inside it.

**Ten through nineteen are not compositional.** "Fifteen" is not "Ten Five", so
`10..19` needs its own table and the tens digit cannot be handled uniformly.

**The join is where the bugs actually live.** Every piece is separated by exactly
one space, none leading and none trailing, and each piece may itself be empty.

## Three joins, on purpose

Since all three solvers are doing the same joining job, they would happily share
a joining bug. So each does it differently:

| solver | join |
|---|---|
| ★ chunker | prepend — `out = piece + " " + out` |
| positional walk | collect into a `Vec[String]`, join once at the end |
| table | append with a leading-space guard |

## The positional walk is where the teens bite

That solver never splits the number at all: it renders `n` as decimal text and
decides each digit from its position — `p % 3` gives the place inside the group,
`p / 3` gives the scale. Every digit is a pure function of its own value and its
own index.

Except a `1` in the tens place, which **binds to the next digit**. So the loop is
not a per-digit map: it carries one lookahead, and consuming the units digit early
is also what ends the group, so the scale word has to be emitted from two places
in the loop rather than from the `place == 0` arm alone. That coupling is the
entire difficulty of writing it this way, and it is the rule a positional scheme
cannot express.

## The table solver reads its own table while writing it

`g[837] = g[8] + " Hundred " + g[37]` — the two-digit half of every three-digit
name is read back out of the table that is still being filled. It is the exact
inverse of the ★ solver's top-down recursion, and it makes the query O(1).

It also carries **a different transcription of the lexicon** — array literals
where the other two use an `if`-chain. That is what lets the harness catch a typo
in the twenty-eight words; the other two share theirs and could only agree on
"Fourty".

## A fourth check that computes nothing

Agreement between solvers cannot catch a mistake all three make — and all three
are joining words with spaces. So every produced string also goes through a
**shape oracle**: split on a single space, require that no token is empty and
every token is in the vocabulary. An empty token is *exactly* a leading space, a
trailing space or a doubled space, so one condition covers all three, and the
check holds no opinion about which number was being spelled.

```
cases 50032
numbers with a ZERO GROUP below a nonzero one 11191
numbers ending in a teen 4262
longest spelling, bytes 110
shape violations 0
digest 333427260
mismatches 0
```

Uniform draws over `0 .. 2³¹−1` almost never produce a zero group — each group is
zero with probability 1/1000, so 20,000 draws yielded 91. They are therefore
constructed: four groups, each independently zeroed a third of the time. Same
discipline as #270's constructed midpoints.

## Benchmark

`bench/` draws **200,000 integers** spanning the whole range once, then spells
every one of them with the ★ chunker **5 times** — 1,000,000 spellings — folding
a checksum over the bytes each produces. Sink `396935809`, reproduced by all four
compiled mirrors and by Python.

**This is the corpus's owned-string-construction lane.** Per spelling the work is
three or four `a + b` concatenations of short strings, each allocating and
copying. #271 copies bytes in *bulk* through hoisted buffers and measures memcpy;
#266 *scans* bytes without producing any. This one produces, and nothing can be
hoisted — each step's output is the next step's input.

The algorithm **prepends**, and that is preserved in all five mirrors.
`out = piece + " " + out` cannot reuse the left buffer in any language, so every
mirror allocates and copies at every step. An append-based rewrite would let
Rust, Go and Kāra amortize into one growing buffer while C still copied — four
growth strategies rather than one algorithm, which is #267's phantom in a new
costume. C has no owned string type, so one is built explicitly: a malloc'd
buffer that its holder frees, with `join` extending the left operand by `realloc`
exactly as an owned-string `+` does.

### What the x86 corroboration run shows

| lang | mean (ms) | σ |
|---|---|---|
| C | 1015.7 ± 12.4 | 1.2% |
| C (`-march=x86-64-v3`) | 1025.9 ± 22.2 | 2.2% |
| **Kāra** | **1048.4 ± 16.3** | 1.6% |
| Rust (checked, equal-safety) | 1073.7 ± 25.8 | 2.4% |
| Rust (checked + `target-cpu=v3`) | 1082.5 ± 40.0 | 3.7% |
| Rust | 1084.4 ± 14.4 | 1.3% |
| Go | 1266.4 ± 51.5 | 4.1% |

**Kāra is second of five**, 1.03× behind C and *ahead* of both Rust builds and Go.
On a lane that is nothing but string allocation, that is a good result — and a
narrow one, which is why it was probed rather than celebrated.

### The probe: Kāra's `+` never reuses the left buffer

Appending and prepending cost Kāra **the same**, which is the measurement:

| | append `s = s + lit` | prepend `s = lit + s` |
|---|---:|---:|
| Kāra | 52.4 ms | 53.2 ms |
| `rustc -O` | **3.0 ms** | 93.2 ms |

Nobody can reuse a buffer when prepending, so 93.2 ms is what the work costs when
it must be done and 3.0 ms is what it costs when it need not. Kāra pays the
prepend price for both. This lane prepends, so the missing optimization would not
have applied here — Kāra's second place is honest, and it does not generalize.

Three findings came out of that probe, all filed:

| spelling | 20,000 appends | peak RSS | |
|---|---:|---:|---|
| `s.push_str(x)` | 2.5 ms | 2,476 KB | matches Rust |
| `s = s + x` | 53.4 ms | 2,804 KB | **21×** — [`B-2026-08-14-23`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md) |
| `s += x` | 6.1 s | **1,565,032 KB** | leaks every buffer — [`B-2026-08-14-22`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md) |

1.5 GB of RSS for a 160 KB string is exactly `sum(8i, i=1..20000)` — every
intermediate, never freed. And through a `mut ref String` parameter the same
operator **silently drops the append**, so the caller sees an empty string while
the interpreter is correct ([`B-2026-08-14-21`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md)).

The fast path already exists — `push_str` matches Rust. One change closes all
three: lower `s += x`, and `s = s + x` where the target is the left operand, to
that in-place append. Full write-up in [`bench/probe/`](bench/probe/).

## Kāra features exercised

- **`String` `+` concatenation** in three joining styles, and `Vec[String]`
  `push` / index / `join`.
- **`Set[String]`** as the shape oracle's vocabulary.
- **`String.split(" ")`** returning `Vec[String]`, including the empty-token case
  that the oracle turns on.
- **`f"{n}"`** as the integer-to-decimal-text conversion the positional walk
  drives off, and **`.bytes()`** to walk it.
- **A `Vec[String]` read at an index it is still being appended to** — the table
  solver's `g[837] = g[8] + " Hundred " + g[37]`.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors. The bench kernel is checked
under the JIT and both AOT modes at full size, and across all four surfaces plus
Python at reduced size.

The solvers found no compiler bug. **The bench probe found three**, all in the
same `String` append lowering: `B-2026-08-14-21` (silent wrong answer through a
`mut ref` parameter, high), `B-2026-08-14-22` (a leak of every intermediate
buffer, high) and `B-2026-08-14-23` (the missing left-buffer reuse, medium).

## Running

```bash
karac run int_to_words.kara
karac run int_to_words_places.kara
karac run int_to_words_table.kara

diff <(karac run int_to_words.kara) <(python3 int_to_words.py) && echo OK

# 50,032 probes, three solvers plus the shape oracle
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in int_to_words int_to_words_places int_to_words_table differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done

# cross-language benchmark (needs hyperfine, rustc, clang, go)
bash bench/bench.sh
```
