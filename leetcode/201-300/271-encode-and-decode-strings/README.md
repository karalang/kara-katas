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

No compiler bugs found.

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
```
