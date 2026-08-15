# 271. Encode and Decode Strings

Encode a list of strings into **one** string, and decode it back.

```
["abc","de"]  ->  "3#abc2#de"  ->  ["abc","de"]
[]            ->  ""
[""]          ->  "0#"          ← and these two must not collide
```

**Constraints:** `1 ≤ strs.length ≤ 200`; `0 ≤ strs[i].length ≤ 200`; any
characters.

## Approaches

| file | structure | looks at the payload? |
|---|---|---|
| `encode_decode.kara` ★ | `len#payload`, decimal length, `#` terminator | never |
| `encode_decode_fixed.kara` | fixed 8-digit length, no terminator | never |
| `encode_decode_escape.kara` | `;`-prefixed runs, `;` and `\` escaped | every byte |
| `differential.kara` | 4,000 lists, round-trip property | — |

## The problem is that any delimiter can appear in the data

"Join with a comma and split on commas" is the first idea everyone has, and it
is wrong for the obvious reason. Escaping fixes it at the cost of a scan.
**Length-prefixing avoids the question entirely**: if a payload is known to be
exactly *n* bytes, nothing inside it can be misread, because nothing inside it is
ever examined. The separator is only ever searched for *inside the header*.

## Two empty cases, and they must not collide

`[]` encodes to `""` and `[""]` encodes to `"0#"`. A codec that renders both as
`""` round-trips one of them wrongly — and a joining separator **cannot tell them
apart at all**, which is why the escaping form here *prefixes* each element
rather than joining them: `[]` → `""`, `[""]` → `";"`. The decoder then reads
"a run starts at every unescaped separator" instead of "elements are what lies
between separators".

All three codecs keep the two distinct; the harness asserts it rather than
assuming it.

## The trap that is not about delimiters at all

The length is in **bytes**, and the payload must be reassembled *as bytes*.
Writing the decoder the natural-looking way:

```kara
s.push(bytes[p + k] as u8 as char);       // wrong
```

is correct for ASCII and silently wrong above it. A `char` is a **codepoint**:
pushing byte 200 appends U+00C8, which is *two* UTF-8 bytes, so the string comes
back longer than it went in and every subsequent offset is wrong. The escaping
form is more exposed to this than the other two, because it is the only one that
inspects the payload byte by byte — encoding `"héllo"` that way yields `"hÃ©llo"`,
the classic mojibake.

Both directions have to work in bytes and convert once, via `String.from_utf8`
on the exact slice. I wrote this bug twice while building the kata — once in the
★ decoder and once in the escaping encoder — which is why it has its own section.

## Generator design

A random alphabet of ordinary letters exercises none of this: the whole problem
is what happens when the payload contains the thing the codec uses to structure
its output. So the draws are weighted toward the hazards — `;` and `\` for the
escaping form, `#` and digits for the length-prefixed one, two-byte UTF-8 for all
three, and empty strings throughout.

Over 4,000 lists: **1,388 containing `;`**, **1,436 containing `\`**, **1,413
containing `#`**, **1,410 containing multi-byte text**, and **1,938 with an empty
element or no elements at all**.

## What the injected bugs did — three loud, one silent

The check is a property, `decode(encode(x)) == x`, since the three codecs produce
three different encodings and there is nothing to compare between them directly.

| injected bug | outcome |
|---|---|
| join with `;`, no escaping | **crash** — `index 2 out of bounds (len 2)` |
| escape `;` but not `\` itself | **crash** — same class |
| length counts characters, not bytes | **crash** — `index 8 out of bounds (len 8)` |
| encoder pushes bytes as codepoints | **1,410 silent round-trip failures** |

**The structural bugs fail loudly and the encoding bug fails silently**, and that
asymmetry is the useful thing here. A wrong length or a missing escape
desynchronises the byte stream, so the very next header is read out of position
and the decoder runs off the end — you get a bounds error, not a wrong answer.
The byte-versus-codepoint bug keeps the stream perfectly synchronised and just
corrupts the contents.

And 1,410 is exactly the number of generated lists containing multi-byte text.
The generator and the harness agree on their own arithmetic.

## Kāra features exercised

- **`String.from_utf8(Vec[u8]) -> Result[String, Utf8Error]`** and `match` on
  the result — the byte-exact way back from a slice.
- **`String.bytes()` vs `String.chars()`** — the distinction the length header
  turns on.
- **`String.push(char)`**, and the reason it is the wrong tool for a byte.
- **String escape literals** — `"\;"` is backslash-semicolon; `"\;"` is a parse
  error, correctly.
- **A reserved-word collision**: `distinct` is a keyword and cannot name a
  variable, which the diagnostic says plainly.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

The four solvers found no compiler bug. **The bench kernel found one, and it was
a bad one** — [`B-2026-08-14-16`](https://github.com/karalang/kara/blob/main/docs/bug-ledger.md),
a silent out-of-bounds heap write, now fixed.

Building the bench corpus is a nested loop whose inner statement is
`src.push(97u8 + ((i + p) % 26i64) as u8)` — a byte computed into a `Vec[u8]`,
which is about as ordinary as Kāra gets. The interpreter printed the right
answer; the JIT and both AOT modes aborted in glibc with `realloc(): invalid
next size`.

The auto-par analyzer recognizes a `while` loop whose body is a single push as a
*tabulate* and rewrites it — one hoisted `realloc` plus a raw `base[idx] = v`
store, instead of a grow-check and a store per push. That rewrite is a second
element-store site, and it never narrowed the value to the element width the way
the push it replaces always has. So a computed byte, which compiles at the
default i64, was stored **eight bytes wide over a one-byte slot**:

```
mov  %rsi,-0xc(%rax,%r14,1)     ; 64-bit store ...
mov  %r9,-0xb(%rax,%r14,1)      ; ... at consecutive ONE-BYTE offsets
mov  %r9,-0xa(%rax,%r14,1)
```

The bisect is a one-token pair. `src.push(97u8 + (…) as u8)` corrupts;
`src.push((…) as u8)` does not — because a bare `as` already yields an `i8`, so
the missing coercion is a no-op there. Any `u8` binary operator triggers it
(`+`, `-`, `*`, `|`), which rules out the overflow check; `Vec[i64]` is immune,
which makes it sub-word-specific.

**The scary part is why it took 271 katas to surface.** Little-endian, each
over-wide store writes its byte and zeros the next seven, which the following
iteration overwrites — so every value *inside* the buffer reads back correct and
only the final element's spill escapes. Whether that is fatal is up to the
allocator: `u8` aborted at twenty elements, while `u16`, `u32`, `i16` and `i32`
printed correct sums at 40, 128, 512, 2048 and 8192 elements while emitting the
identical wide store (`mov %rdx,(%rax,%rcx,2)` — 64-bit at a 2-byte stride).
A green run of a `Vec[u16]` program was never evidence of anything.

Per the corpus rule the kernel was not rewritten around the bug. It stayed as
written, the compiler was fixed, and the bench lane below was run afterwards.

<!-- placement-caveat -->
**Measurement caveat — code placement.** This kata's runtime moves by up to **6%** with code placement alone: rebuilt with its machine code sitting at a different address, the same program, same compiler and same input runs that much faster or slower. That is wider than the **0.1%** margin against `rustc -O` quoted below, so read that comparison as a tie rather than as a result. Measured across four code placements against a same-binary control — see [`placement-spread.json`](../../../placement-spread.json) and [BENCHMARKS.md](../../../BENCHMARKS.md#code-placement-arm64).

## Benchmark

`bench/` builds one **50,000-string flat corpus** once — a byte array plus
offset and length arrays, string lengths drawn 0..24 — then punches the ★
length-prefixed codec over it **250 times**: encode the whole corpus, decode it
back, fold a checksum. Sink `446190680`, reproduced by all four compiled mirrors
and by Python.

**This is the corpus's serialisation lane.** Per item the encoder writes a
decimal length, a separator and a bulk byte copy; the decoder parses the decimal
back and copies the payload out — a header parse plus a memcpy, 50,000 times a
round. That is a different shape from the string-*building* lane
([#257](../257-binary-tree-paths/)) and the byte-*scanning* lane
([#266](../266-palindrome-permutation/)): here the bytes move in bulk and only
the headers are examined.

Two parity decisions were taken up front rather than after a phantom result. The
decimal length is **formatted and parsed by hand in every mirror** — `f"{n}"`,
`format!`, `strconv.Itoa` and `snprintf` are four different amounts of
machinery, and picking each language's own would measure four standard
libraries. And every buffer — corpus, encoded stream, decoded output — is
**hoisted out of the punch loop**, so no mirror allocates while timed;
[#267](../267-palindrome-permutation-ii/) measured what happens otherwise.

### Runtime — sequential lane

Apple M5 Pro (6P+12E), 2026-08-15, `karac 0.1.0-dev.6106+g50267795a`, hyperfine
30 runs, `KARAC_AUTO_PAR=0`, every lane 99% CPU. This is the canonical host —
`bench/results.json`.

| Impl | Mean ± σ | vs Kāra |
|---|---|---|
| C `clang -O3` | 124.2 ± 4.9 ms | 0.53× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 233.2 ± 8.0 ms | 0.99× |
| Rust `-O` | 234.8 ± 9.0 ms | 1.00× |
| **Kāra (codegen)** | **235.0 ± 8.8 ms** | 1.00× |
| Go | 237.9 ± 7.0 ms | 1.01× |

**Kāra, both Rust builds and Go finish in a 2% band — a genuine four-way tie —
and C is 1.89× ahead of all of them.** That is the shape of a `memcpy`-bound
lane: the codec is bulk copying with a length prefix, so the four managed-string
implementations converge on the same `memcpy` throughput plus their own bookkeeping,
while C's flat buffer skips the bookkeeping entirely.

**The gap to C compresses sharply from the container's 2.82× to 1.89×**, the
largest compression in the block. Kāra's overhead over C is per-`String`
allocation and length tracking, and that is exactly the cost the M5's cheaper
allocator discounts.

Overflow checks are free here (233.2 vs 234.8 ms), as expected for a lane that
does almost no arithmetic.

### The x86 corroboration run

| lang | mean (ms) | σ |
|---|---|---|
| C (`-march=x86-64-v3`) | 252.7 ± 2.7 | 1.1% |
| C | 259.1 ± 9.2 | 3.6% |
| Rust | 723.2 ± 12.3 | 1.7% |
| **Kāra** | **729.7 ± 11.7** | 1.6% |
| Rust (checked + `target-cpu=v3`) | 786.8 ± 15.4 | 2.0% |
| Rust (checked, equal-safety) | 791.7 ± 25.9 | 3.3% |
| Go | 1072.4 ± 12.1 | 1.1% |

σ is 1.1–3.6% and the two C builds are within 2.5% of each other, so there is no
ISA phantom to chase. **Against the equal-safety column — the apples-to-apples
one, since Kāra checks integer overflow by default and plain `rustc -O` wraps —
Kāra is 1.08× ahead**, and it is within noise of plain `rust -O`. Go is last at
1.47× behind Kāra.

### C is 2.8× ahead, and it is one idiom

That gap is far too large for the same algorithm, so it was probed before it was
published. The inner payload copy is `enc[w + p] = src[base + p]` in all five
mirrors — and `clang -O3` is the only compiler that turns it into a call to
glibc's `memcpy`. Its `main` contains exactly one `memcpy` call and zero vector
registers; `rustc -O`'s `main` contains neither.

Disabling that promotion changes only the codegen, not the workload or the
source, and the sink is unchanged at `446190680`:

| build | mean | `memcpy` calls in `main` |
|---|---:|---:|
| `clang -O3` (the lane) | 255.8 ± 7.2 ms | 1 |
| `clang -O3 -mllvm -disable-loop-idiom-all` | 339.0 ± 3.1 ms | 0 |
| `clang -O3 -fno-builtin` | **525.3 ± 12.6 ms** | 0 |

So roughly **2× of C's 2.8× advantage is one loop-idiom recognition**, and
against a C that copies bytes the way the other four do, Kāra is 1.38× behind
rather than 2.8×. The remaining gap is the bounds check: C indexes unchecked,
while Kāra, Rust and Go all check, and a byte-at-a-time copy is where that is
most expensive.

The honest reading is that this lane measures *idiom recognition on a byte
copy*, not raw arithmetic throughput — which is a real thing to know about a
serialiser, and a concrete thing for Kāra's backend to go get. It is left in the
table at its true 255.8 ms, with the mechanism named, rather than tuned away.
Full write-up and reproduction commands in [`bench/probe/`](bench/probe/).

## Running

```bash
karac run encode_decode.kara
karac run encode_decode_fixed.kara
karac run encode_decode_escape.kara

diff <(karac run encode_decode.kara) <(python3 encode_decode.py) && echo OK

# 4,000 lists, round-tripped through all three codecs
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in encode_decode encode_decode_fixed encode_decode_escape differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done

# cross-language benchmark (needs hyperfine, rustc, clang, go)
bash bench/bench.sh
```
