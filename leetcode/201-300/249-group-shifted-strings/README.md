# 249. Group Shifted Strings

Two strings belong to the same **shifting sequence** if one becomes the other by
adding a constant to every character, wrapping `z` back to `a`. Group the input
so that each group is one such sequence.

```
["abc","bcd","acef","xyz","az","ba","a","z"]
  ->  [["abc","bcd","xyz"], ["acef"], ["az","ba"], ["a","z"]]
```

`"abc" -> "bcd"` shifts by 1; `"xyz" -> "abc"` shifts by 3 with `x,y,z` wrapping
past `z`. Single characters are all shifts of one another, so they form one
group.

**Constraints:** `1 ≤ strings.length ≤ 200`; each string is lowercase letters,
length `1..50`.

## Approaches

| file | key | container |
|---|---|---|
| `group_shifted.kara` | canonical form — shift so the first char is `a` | `Map[String, Vec[String]]` |
| `group_shifted_diffkey.kara` | gap sequence between consecutive chars | `Map[String, i64]` + `Vec[Vec[String]]` |
| `differential.kara` | 4,000 randomized lists, both keys, must agree | — |

## The mechanism

**A shifting sequence is an equivalence class, and the whole problem is picking
a representative.** Two normalisations do it, and they carry the same
information from opposite directions.

The **canonical form** shifts every character down by `s[0] - 'a'`, so the
sequence's member beginning with `a` is the key: `"bcd"` and `"xyz"` both become
`"abc"`. The **gap sequence** records `s[i] - s[i-1]` for each adjacent pair, so
the first character drops out entirely: `"abc"` and `"xyz"` both become `(1,1)`.
A word is exactly its first character plus its gaps, so quotienting out the
first character and normalising it to `a` are the same operation.

**Both need `+ 26` before the modulo, and that is the trap.** The intermediate is
a difference, so it can be negative — `"az"`'s gap is `'z' - 'a' = 25` going up
but `"ba"`'s is `'a' - 'b' = -1`, and those must land on the same key. Kāra's `%`
keeps the sign of the dividend (as C and Rust do, unlike Python), so `-1 % 26`
is `-1`, not `25`. Without the `+ 26` the two keys differ and `"az"`/`"ba"` split
into separate groups — the single most likely wrong answer here, and why `az`,
`ba` and `zy` are all in the test set.

**Single-character words are the other edge.** Their gap sequence is empty, so
every one-character word shares the empty key. The canonical form agrees: they
all normalise to `"0,"`. Both keys must put `"a"` and `"z"` together, and the
spec agrees — a one-character string is a shift of any other.

**Output order is fixed deliberately.** LeetCode accepts any order, but a
cross-language differential does not, and a `Map` fixes no iteration order. Both
solvers emit groups in **first-seen key order** via a side list, and words within
a group in **input order**. That makes the Python twin a line-for-line oracle.

## What it found

**A silent wrong answer under both compiled backends** — kara `B-2026-08-06-2`,
fixed in the same pass.

`differential.kara` builds its random words one computed byte at a time, which is
the natural way to write a generator:

```kara
w.push_str(f"{(ch as u8) as char}");
```

Under `karac run --interp` that appends the character. Under `karac run` (JIT)
**and** `karac build` it appended the **integer codepoint** — the `as char` cast
was dropped inside the f-string hole. The kata caught it because the corrupted
words changed the grouping: 6,135 groups under the interpreter versus 13,217
under AOT, over an identical 14,053 words.

The reduction is three lines, and the cast is only dropped in interpolation —
binding it first is fine:

| spelling | interp | JIT / AOT |
|---|---|---|
| `let c = b as char; f"{c}"` | `a` | `a` |
| `f"{b as char}"` | `a` | **`98`** |

Other casts in the same position were all honoured (`300 as u8` → 44,
`-1 as u8` → 255, `2.9 as i64` → 2), which is what localised it to codegen's
`expr_is_char` rather than to f-string lowering generally: that predicate has one
arm per syntactic form that can yield a char, and **a cast had no arm**. It is
the fourth instance of that gap — the function's own comments record the same
symptom twice for method-call results ("formats the i32 scalar as its integer
codepoint (77 instead of 'M')"). `B-2026-07-24-3` had made `u8 as char` legal at
typecheck; nothing taught the renderer about it.

Worth stating plainly: **both solvers were clean on all four surfaces from the
start.** Only the differential's generator tripped this, because it is the only
file that builds strings from computed bytes — a reminder that the harness is
part of the kata's bug-finding surface, not scaffolding around it.

## Kāra features exercised

- **`Map[String, Vec[String]]` with `entry(k).or_insert(Vec.new()).push(w)`** —
  in-place append into the map's own slot, no read-clone-reinsert. (#49's
  `map_of_lists.kara` keeps the clone form deliberately as an ownership probe and
  warns it is O(k²) per key — kara `B-2026-08-03-9`.)
- **`Map[String, i64]` group-index + side `Vec[Vec[String]]`** — the primitive
  valued map, a different ownership surface from the heap-valued one.
- **`String.bytes()`** for O(1) indexed character access on ASCII input.
- **Sign-preserving `%`** on a difference, with the `+ 26` correction.
- **`(b as u8) as char` in an f-string** — the construct that broke.
- **`not` as the boolean negation** (`!` is not Kāra's operator; `karac fix`
  rewrote it automatically).

## No benchmark

Grouping 200 strings of length ≤ 50 is not a workload — the whole input fits in
L1 and the answer is dominated by map overhead rather than by the algorithm.
`differential.kara` is the load-bearing artifact here; a bench lane would measure
`Map[String, _]` insertion, which [#49](../../1-100/49-group-anagrams/) already
covers with a corpus sized for it.

## Running

```bash
karac run   group_shifted.kara
karac run   group_shifted_diffkey.kara
karac build group_shifted.kara && ./group_shifted

# Both solvers agree with each other and with the Python oracle
diff <(karac run group_shifted.kara) <(python3 group_shifted.py) && echo OK
diff <(karac run group_shifted.kara) <(karac run group_shifted_diffkey.kara) && echo OK

# 4,000 randomized lists, two keyings, cross-checked against Python
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"
```

## Notes

Verified byte-identical under `karac run --interp`, `karac run` (JIT) and
`karac build` — under the default auto-parallelising build and `KARAC_AUTO_PAR=0`
alike — for all three programs, against the Python mirrors.

The differential's corpus is built from **shifts of a small seed set** rather
than uniform random letters. A uniform draw makes almost every word its own
group, so the grouping path would barely execute; drawing shifts of 1–3 seeds
per case yields 6,135 groups over 14,053 words — about 2.3 words per group — so
collisions, not singletons, are the common case.
