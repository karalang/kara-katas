# 535. Encode and Decode TinyURL

TinyURL is a URL shortening service: given a URL such as
`https://leetcode.com/problems/design-tinyurl` it returns a short URL
such as `http://tinyurl.com/4e9iAk`. Design a class that encodes a URL
to a tiny URL and decodes the tiny URL back to the original. How it
does so is up to the design; a URL only has to come back from its
tiny URL.

- `Codec()` makes an empty codec.
- `encode(longUrl)` returns a tiny URL for `longUrl`.
- `decode(shortUrl)` returns the original URL for `shortUrl`, which is
  guaranteed to have come from `encode` on the same codec.

**Constraints:** `1 <= url.length <= 10^4`; `url` is a valid URL.

## Approaches

Every arm is a `Codec` with `fn new() -> Codec`, `fn encode(mut ref
self, long_url: Str) -> String` and `fn decode(ref self, short_url:
Str) -> String`, and every short URL is `http://tinyurl.com/` and a
code of letters and digits. The arms differ in how they make the code
and what a URL encoded twice gets.

| file | code | a URL encoded twice |
|---|---|---|
| `encode_and_decode_tinyurl.kara` ★ | the next number, in base 62 | one short URL, from a second map |
| `encode_and_decode_tinyurl_index.kara` | the URL's place in a list, in decimal | two short URLs |
| `encode_and_decode_tinyurl_hash.kara` | a hash of the URL in base 62, the next number while the slot holds another URL | one short URL: the probe finds it |
| `encode_and_decode_tinyurl_random.kara` | six random letters and digits, drawn again while taken | one short URL, from a second map |
| `differential.kara` | the four arms, five properties | |

The hash arm hashes as Java's `String.hashCode` does (`h * 31 + c`),
kept below 1,000,000,007, so URLs that differ only in `Aa` for `BB`
share a hash. The harness and the differential put such twins in on
purpose: over the whole harness the hash arm moves on to a next slot
398 times.

Every arm prints the same 8 lines: the example URL and what comes back,
whether a URL encoded twice comes back from both short URLs, three
URLs on two codecs, then for each of these the count that come back,
whether different URLs got different short URLs, whether every short
URL is well formed and a checksum over what came back: six URLs that
differ in `Aa` for `BB`, the shortest URL, one of 10,000 characters
(the problem's most), 300 random rounds of 1 to 40 URLs (some
repeated, some twins), and last 10,000 random URLs of up to 200
characters, a fifth of them repeats. Short URLs are decoded in a
shuffled order, after every URL is encoded. No line depends on the
codes themselves, so the arms can make different ones.
`encode_and_decode_tinyurl.py` mirrors the ★ arm and its output is
byte-identical.

## Differential

`differential.kara` holds copies of the four arms. Each arm is held to
the properties below on 1,000 random lists of URLs, a third of them 63
to 150 long, so that the ★ arm's counter needs two base-62 digits, and
the rest 1 to 30. A quarter of the URLs repeat an earlier one, a
quarter are an earlier one's twin under the hash arm's hash, and the
rest are fresh, from a host of 1 to 4 letters and a path of up to 12
characters from `a`, `b`, `A`, `B`, `0` and `/`.

| | property |
|---|---|
| P1 | every short URL decodes to its URL, decoded in a shuffled order after every encode |
| P2 | different URLs get different short URLs |
| P3 | every short URL is `http://tinyurl.com/` and a code of letters and digits |
| P4 | on a fresh codec, each short URL decodes right at once, and the one before it still does after this encode |
| P5 | two codecs fed the URLs in turn each decode their own |

It prints `1000 cases, 4 arms, 20000 checks, 0 failures` under `karac
__mir-run`.

## Mutation testing

Twelve edits to `differential.kara`, two to each arm that change its
answers, and four that do not, each run under `karac __mir-run`. All
eight that change answers are killed.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: the counter never moves on | P1 976, P2 976, P4 976, P5 958 |
| M2 | ★: the digits 36 to 61 written as `a`-`z` | P1 332, P2 332, P4 295, P5 234 |
| M3 | index: the list read from the end | P1 974, P4 976, P5 958 |
| M4 | index: each URL stored without its last character | P1 1000, P4 1000, P5 1000 |
| M5 | hash: a slot that holds another URL used anyway | P1 657, P2 657, P4 657, P5 597 |
| M6 | hash: `a`-`z` read back as 36 to 61 | panics: `slots[h]` on a missing key |
| M7 | random: a URL seen before given a fresh code it never stored | panics: `unwrap()` on `None` in `decode` |
| M8 | random: the URL stored lower-cased | P1 995, P4 995, P5 995 |
| E1 | ★: the digits written least significant first | 0 |
| E2 | index: a URL equal to the last one not stored again | 0 |
| E3 | hash: 37 for 31 in the hash | 0 |
| E4 | random: a URL seen before looked up in the wrong map | 0 |

M4 fails every case. M1 passes only a list of one URL, once or repeated,
M3 only a list that reads the same from either end, and M8 only a list
with no capital letter in it. M2 needs a counter of 36 or more, which
only the long lists reach, and it fails 332 of their 334. M5 needs two
URLs with one hash, which is why the lists hold twins. E1 to E4 make
other codes, or give a repeated URL a second one, and the problem allows
both: E2 hands out the place of the last copy, which holds the same URL;
E3 changes only which URLs share a hash, and the probe handles any; and
E4 never finds a URL it has seen, so it draws a new code for each copy.

## Verification

Every arm prints the same output as `encode_and_decode_tinyurl.py`
under `karac __mir-run` (the v2 MIR interpreter) and `karac
__mir-llvm-run`, and runs clean under `karac __mir-llvm-asan`
(AddressSanitizer and LeakSanitizer): output identical, no error, no
leak. The differential prints `20000 checks, 0 failures` on the first
two and runs clean under the third. `karac check` passes on every arm,
the differential and the bench program.

The frozen legacy backends refuse every file at type checking. Legacy
wants a `String` key in a `Map`'s `get`, so it refuses the `Str` URL
in the ★ and random arms ("expected 'String', found 'StringSlice'");
it takes the slice `short_url[a..b]` of a `Str` for a move out of an
index (`E_INDEX_MOVE_NON_COPY`), in every arm with a slice; and in the
hash arm it types the items of a slice's `iter()` by value, so it
refuses `*b`, and cannot compare a `String` with a `Str`. Legacy is
frozen, so this is noted, not filed.

## Benchmarks

The bench program uses the ★ arm. It makes 20,000 random URLs of up to
100 path characters once, a fifth of them repeats; then in each of 50
rounds a fresh codec encodes every URL and decodes every short URL
back. Every implementation prints `20000 URLs, 50 rounds: 1000000 back,
short length 21663200`, the Kāra program under `karac __mir-run`
included (in 25.7 s).

Every mirror keeps the ★ arm's two maps and makes a fresh short URL
for every encode. Rust uses `HashMap<String, String>` with its default
SipHash-1-3, the hasher Kāra's `Map` uses too, and clones the URL on
decode as Kāra does; Go and Python return the stored string, which
they share rather than copy. C has no map, so its mirror holds two
open-addressing tables with FNV-1a, a much cheaper hash, that own
copies of their keys and values, and copies the URL on decode. Spot
timings on a shared 4-core container, three runs each (two for
Python; `bench.sh` timings need a quiet machine):

| | time |
|---|---|
| C (`clang -O3`) | 0.75 to 0.83 s |
| Rust (`rustc -O`) | 0.76 to 0.86 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.83 to 0.91 s |
| Go | 0.70 to 0.73 s |
| Python | 1.29 to 1.32 s |
| Kāra (`karac build --mir`) | 0.85 to 0.88 s |

The legacy `karac build` refuses this program (see Verification). So
`bench.sh` builds the Kāra program with `karac build --mir`, the v2
compiled backend. That edit is by hand, on top of the
`scripts/new-bench.sh` output. The `--mir` row is timed at kara
`5fa208779d`. Python is close here because the work is almost all
inside its dict and string calls, which are C.

Under `karac __mir-llvm-run` the program prints the same line in 6.1 s,
compile included; that JITs the MIR's IR without optimization passes, so
it is not a benchmark.

## Compiler findings

None filed. Every arm, the differential and the bench program run
right on the v2 backends, and `karac check` passes on all of them.
Two first drafts were refused by `karac check`, each by the spec: `m[k]`
on a `Map[String, String]` takes a `String`, since only the lookup
methods (`get`, `contains_key` and the rest) take a `Str` view
(`docs/library/collections.md`, Lookup by view); and `*u != url` over
the `ref String` that `get` gives reads the value out of a borrow,
where `u != url` compares in place.
