# 68. Text Justification

> **Difficulty:** Hard &nbsp;·&nbsp; **Topics:** Array · String · Simulation &nbsp;·&nbsp; **Source:** [leetcode.com/problems/text-justification](https://leetcode.com/problems/text-justification/)

Format an array of `words` into lines of **exactly** `max_width` characters, **fully justified**: pack as many words per line as fit (at least one space between words), then pad each line to the width by spreading the leftover spaces as evenly as possible between the words — and when they do not divide evenly, the **left** gaps take one extra each. Two lines break the rule: the **last** line and any line holding a **single word** are *left*-justified (single spaces, padded on the right).

```
words = ["This","is","an","example","of","text","justification."], max_width = 16

"This    is    an"      full-justified: 6 spare spaces over 2 gaps → 3 and 3
"example  of text"      6 spare over 2 gaps unevenly → 2 (left) and 1
"justification.  "      last line: left-justified, right-padded
```

**Constraints:** `1 ≤ words.length ≤ 300`; `1 ≤ word.length ≤ max_width ≤ 100`; each word is non-empty, no word exceeds `max_width`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Greedy pack + spread** ★ — one pass: fit the widest run, build the line inline | O(total chars) time, O(line) extra | [`text_justification.kara`](text_justification.kara) ✓ via `karac run` / `karac build` | [`text_justification.py`](text_justification.py) ✓ |
| **Two-phase** — pack every line's word indices into groups, then format each group | O(total chars) time, O(lines) extra | [`text_justification_twophase.kara`](text_justification_twophase.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all eight test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Two decisions per line

Text Justification is a **simulation**, not a search: the words appear in order and never split, so there is no choice about *which* words go where beyond "take as many as fit." Each line is two mechanical decisions.

**1. Greedy pack.** Starting at word `i`, keep adding words while the minimal layout still fits: with `count` words chosen totalling `line_chars` characters, the tightest width is `line_chars + (count - 1)` — one space per gap. The next word fits iff `line_chars + word_len + count ≤ max_width` (the `count` counting the single-space gaps that would precede it). This greedy choice is *forced* to be optimal here — fewer words on a line can only push work to later lines — so unlike the grid DP of katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/) there is no table to fill; the "min over choices" that needed a DP there is absent because order + no-split removes the choice.

**2. Distribute the slack.** `total = max_width - line_chars` spaces fill `gaps = count - 1` slots. Each slot gets `base = total / gaps`; the leftmost `extra = total % gaps` slots get one more. That "extra spaces go left" rule is the whole spacing subtlety, and it is pure integer division — `base` and `extra` from one `/` and one `%`, no floats. The two exceptions collapse to a simpler rule: a **single-word** line (`gaps == 0`, no slot to divide by) and the **last** line are left-justified with single spaces and right-padded to the width.

**Greedy pack + spread** ([`text_justification.kara`](text_justification.kara)) is the ★: one loop per line finds the run and builds the string in place. **Two-phase** ([`text_justification_twophase.kara`](text_justification_twophase.kara)) splits the two concerns — Phase 1 collects every line's word indices into a `Vec[Vec[i64]]` of groups; Phase 2 formats each, where "is this the last line?" is a plain `gi == groups.len() - 1` against the materialised list rather than the ★'s inline `j == n`. It costs the extra index groups the ★ folds away, buying a cleaner separation of *which words* from *how spaced* — the clarity-vs-allocation contrast and an independent cross-check of the identical spacing arithmetic.

## Kāra features exercised

- **`Vec[String]` input + `String` building** — words are a `Vec[String]` (`words[j].len()`, `words[i + g]`); each line is built with `let mut line: String = ""` then `push_str(words[…])` and `push(' ')`, the string-assembly idiom of katas [#67](../67-add-binary/) and [#14](../14-longest-common-prefix/).
- **`Vec[String]` result + re-scan for the checksum** — `full_justify` returns a fresh `Vec[String]`; the harness borrows each line, `line.bytes()` gives a `Slice[u8]` for the positional checksum `Σ (k+1)·byte[k]` (the same byte-scan shape as kata [#58](../58-length-of-last-word/)).
- **`Vec[Vec[i64]]` index groups** (two-phase) — nested `Vec.new()`/`push` of word-index runs, the same nested-Vec shape as katas [#62](../62-unique-paths/)–[#64](../64-minimum-path-sum/)'s DP tables, here holding indices rather than counts.
- **Integer `/` and `%` for even spacing** — `base = total / gaps`, `extra = total % gaps`; the leftmost `extra` gaps get `base + 1`. No floats, exactly as the width arithmetic demands.
- **Quoted-line + `sums:` harness** — each output line is printed wrapped in `"…"` so trailing spaces are visible in a diff, plus the folded `sums:` checksum, the byte-for-byte anchor shared with katas [#54](../54-spiral-matrix/) and [#62](../62-unique-paths/)–[#66](../66-plus-one/). A one-space spacing error changes a checksum even when the line width does not.

**v1 note — `group` is a reserved keyword.** The natural name for a line's collected words is `group`, but Kāra reserves `group` (task-group concurrency), so `let mut group: Vec[i64] = …` fails to parse (`Expected pattern, found Group`) — identically under `karac run` and `karac build` (a consistent parse rejection, not a divergence). The two-phase solver uses `grp` instead; the plural `groups` is fine (only the bare keyword collides). Inputs are ASCII, so `String.len()` / `String.bytes()` measure the character width the problem counts, and every width and checksum fits i64 (`max_width ≤ 100`, `words.length ≤ 300`).

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   text_justification.kara
karac build text_justification.kara && ./text_justification

# The two-phase approach (identical output):
karac run text_justification_twophase.kara

# Python
python3 text_justification.py

# Verify they all agree
diff <(karac run text_justification.kara) <(python3 text_justification.py)                  && echo OK
diff <(karac run text_justification.kara) <(karac run text_justification_twophase.kara)     && echo OK
```
