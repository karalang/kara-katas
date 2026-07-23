# 58. Length of Last Word

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** String &nbsp;·&nbsp; **Source:** [leetcode.com/problems/length-of-last-word](https://leetcode.com/problems/length-of-last-word/)

Given a string of words separated by spaces, return the length of the **last** word — a maximal run of non-space characters. Trailing spaces are ignored.

```
"Hello World"                  → 5   (World)
"   fly me   to   the moon  "  → 4   (moon, trailing spaces skipped)
"luffy is still joyboy"        → 6   (joyboy)
```

**Constraints:** `1 ≤ s.length ≤ 10^4`; `s` is printable ASCII (letters + spaces); there is at least one word.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Reverse scan** — skip trailing spaces, count the run back to the next space | O(n) time, O(1) space | [`length_of_last_word.kara`](length_of_last_word.kara) ✓ via `karac run` / `karac build` | [`length_of_last_word.py`](length_of_last_word.py) ✓ |
| **Split + last non-empty** — `split(" ")`, take the last piece with `len > 0` | O(n) time, O(n) words | [`length_of_last_word_split.kara`](length_of_last_word_split.kara) ✓ | — |
| **Forward scan** — track current-word and last-completed-word length in one left-to-right pass | O(n) time, O(1) space | [`length_of_last_word_forward.kara`](length_of_last_word_forward.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all nine test cases, and all three approaches agree with each other and with the Python mirror.

## Why reverse scan?

The answer depends only on the **tail** of the string, so scanning from the right touches the fewest characters: skip the trailing spaces, then count non-space characters until the next space (or the string start). One pass, no allocation, and it never looks at the earlier words. The two `while i >= 0 and …` guards are what make the two edge cases safe:

- **All-trailing-space suffix** (`"day "`, `"a   bb   ccc   "`) — the first loop walks `i` back past every trailing space before the counting loop starts.
- **Word runs to the string start** (`"word"`, `"   lead"`) — the second loop stops when `i` falls to `-1`, so a last word with no space before it is still counted fully.

The **forward scan** ([`length_of_last_word_forward.kara`](length_of_last_word_forward.kara)) is the shape to reach for when you can't index from the end (a streaming source): carry `cur` (current word length) and `last` (last completed word); a space commits `cur` into `last` and resets, a non-space extends `cur`, and a non-space-terminated string commits the trailing `cur` after the loop.

The **split** solution ([`length_of_last_word_split.kara`](length_of_last_word_split.kara)) is the Python-idiomatic `s.split()[-1]` reading. Kāra v1 has no whitespace-collapsing `split_whitespace`, so it uses `split(" ")` — which emits an empty piece between consecutive spaces and at the ends — and filters those with a `len > 0` guard, leaving the last real word. Heavier (it allocates the whole word list) but a useful independent cross-check.

## Kāra features exercised

- **`s.bytes()` → `Slice[u8]` zero-copy view** — the corpus's standard string-scan idiom ([kata #28](../28-find-the-index-of-the-first-occurrence-in-a-string/), [#14](../14-longest-common-prefix/)); ASCII input makes byte index == char index, so no `Vec[char]` snapshot is needed. Space is the byte literal `32u8` (`0x20`).
- **Reverse `i64` index scan to `-1`** — `let mut i = s.len() - 1i64; while i >= 0i64 { … i = i - 1i64; }` — the loop guard relies on `i` being signed so the decrement past `0` terminates cleanly rather than wrapping (contrast an unsigned counter, which would need a different sentinel).
- **`String.split(" ")` → iterable of pieces + `for w in words.iter()`** — the split-collection idiom, including the empty-piece semantics for consecutive separators (the `w.len() > 0` filter).
- **`ref String` parameter + f-string report** — `fn length_of_last_word(s: ref String)` borrows the input; `println(f"{s}: {r}")` interpolates the borrowed string and the result, the same reporting shape as the other string katas.

**v1 note.** `split_whitespace` and `trim_end` are not methods on `String` in Kāra v1 — both are rejected identically under `karac run` and `karac build` with a clean `no method … on type 'String'` diagnostic (a consistent absence, not a run/build divergence). The whitespace-split idiom is expressed with `split(" ")` + a `len > 0` filter; `trim()` (leading **and** trailing) does exist if a trim-based phrasing is wanted.

## Benchmarks

The kata's tiny fixed inputs aren't a workload, so [`bench/`](bench/) carries a scaled cross-language variant — the same algorithm and a shared deterministic PRNG in Kāra, C, Rust, Go, and Python, all agreeing on the sink (`12219681`). Workload: reverse-scan last-word length over 6.5M end positions in a 4M letters+spaces buffer (build-once + punch).

Runtime, sequential, one x86 container run (hyperfine, 30 runs; `KARAC_AUTO_PAR=0`):

| Impl | Mean | vs Kāra |
|---|---|---|
| C `clang -O3` | 458.8 ms | 0.89× |
| Rust `-O` | 484.4 ms | 0.94× |
| Rust `-O -C overflow-checks=on` (equal-safety) | 495.3 ms | 0.97× |
| **Kāra (codegen)** | 513.2 ms | 1.00× |
| Go | 586.8 ms | 1.14× |
| Python (scale lane) | 6.11 s | 11.90× |

Kāra checks integer overflow by default, so the honest baseline is `rustc -O -C overflow-checks=on`. Single-machine snapshot (`bench/results.container-x86.json`); see [`BENCHMARKS.md`](../../../BENCHMARKS.md) for methodology. Re-run with `bash bench/bench.sh` (add `KARA_BENCH_INCLUDE_PY=1` for the Python lane).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   length_of_last_word.kara
karac build length_of_last_word.kara && ./length_of_last_word

# The two alternative approaches (identical output):
karac run length_of_last_word_split.kara
karac run length_of_last_word_forward.kara

# Python
python3 length_of_last_word.py

# Verify they all agree
diff <(karac run length_of_last_word.kara) <(python3 length_of_last_word.py)              && echo OK
diff <(karac run length_of_last_word.kara) <(karac run length_of_last_word_split.kara)    && echo OK
diff <(karac run length_of_last_word.kara) <(karac run length_of_last_word_forward.kara)  && echo OK
```
