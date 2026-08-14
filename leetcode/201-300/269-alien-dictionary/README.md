# 269. Alien Dictionary

A list of words is sorted according to an unknown alphabet. Recover an order of
the letters consistent with that sorting, or `""` if none exists.

```
[wrt, wrf, er, ett, rftt]  ->  "wertf"
[z, x]                     ->  "zx"
[abc, ab]                  ->  ""       a word cannot precede its own prefix
[ab, adc]                  ->  "abcd"   c is unconstrained but must still appear
[z, x, z]                  ->  ""       a cycle
```

**Constraints:** `1 ≤ words.length ≤ 100`; lowercase English letters only.

## Approaches

| file | direction | order produced |
|---|---|---|
| `alien_dictionary.kara` ★ | Kahn — peel letters nothing depends on | lexicographically **least** |
| `alien_dictionary_dfs.kara` | DFS — record after all successors, reverse | *a* valid order |
| `alien_dictionary_brute.kara` | try every arrangement in order, keep the first valid | lexicographically least |
| `differential.kara` | 1,500 cases, equality **and** property checks | — |

## The input is not a graph

The whole first half of this problem is turning a sorted list into one, and both
rules that do it are places to go wrong.

**Rule 1 — only the first differing character says anything.** From
`["wrt", "wrf"]` the sort tells us `t < f`. It says nothing about later
positions, and nothing about non-adjacent pairs — those follow by transitivity,
and adding them as edges is redundant at best.

**Rule 2 — a word may not be followed by its own prefix.** `["abc", "ab"]` cannot
be sorted under any alphabet: no letter comparison is ever reached, and a shorter
word sorts first when one is a prefix of the other. This yields **no edge**, so a
solver that only ever adds edges accepts it silently and returns a plausible
order for an impossible input. It is the single most missed case here.

## Making the answer testable

The problem accepts *any* valid order, and "any" is not a testable answer — it
makes two correct implementations disagree and a differential meaningless. So the
★ file always takes the **smallest ready letter**, which yields the
lexicographically least valid order. That is unique, so the ★ file, the brute
force, and every mirror must produce the same string.

The DFS deliberately does **not** produce it. Reversed post-order depends on the
visit sequence, not on letter values, so its output is a different — equally
valid — order. The differential therefore checks it by **property**: same verdict
(empty or not), same letter set, and its output satisfies every derived
constraint. Checking a non-unique answer by equality against one implementation
asserts an implementation detail; checking it by property tests the problem.

## How each one breaks

- **Kahn** discovers a cycle by *exhaustion* — letters remain but nothing is
  ready. Its own trap is the in-degree: record a duplicate edge and the successor
  is stranded forever.
- **DFS** must catch a cycle *in the act*, which needs three states rather than a
  visited bit — `0` unvisited, `1` on the current path, `2` finished. Collapsing
  `1` and `2` doesn't merely miss cycles, it reports **success** for them.
- **Brute force** contains no topological argument at all: no frontier, no finish
  order, no notion of a cycle. An unsatisfiable set simply exhausts the
  permutations. That is why it can adjudicate the other two.

## Generator design

Random word lists are almost never sortable under *any* alphabet, so a naive
generator answers `""` nearly always and never exercises the accept path. The
main families work **backwards**: draw a hidden alphabet, generate random words,
and sort them under it. Every such input is satisfiable by construction, and the
solvers must recover an order consistent with a permutation they never see.

The rest attack the two rules directly — swapping an adjacent pair of a sorted
list usually contradicts it, and one family plants a word immediately before its
own prefix.

Over 1,500 cases: **850 solvable** (57%) and **349 rejected by the prefix rule**
(23%), so both paths are well travelled.

## The harness had to be un-refactored

The obvious tidy-up is to derive the constraints once in a shared helper and hand
them to all three solvers. **That is wrong here, and the harness measured how
wrong.** Rules 1 and 2 are the hardest part of the problem, and a shared helper
makes a bug in either break all three solvers *identically*, so the cross-check
goes silent on exactly the code most worth checking:

| injected bug | shared helper | own derivation |
|---|---|---|
| prefix rule dropped | **0 detected** | **292** |
| an edge at every differing position, not the first | **0 detected** | **286** |

Both scored zero until each solver derived its own constraints. The duplication
in `differential.kara` is deliberate and commented, and the two bugs that only
live in the topological half were already caught either way:

| injected bug | detected by |
|---|---|
| DFS collapses on-path and finished into one bit | 301 verdict + 301 invalid orders |
| duplicate edges inflate the in-degree | 107 |

## Kāra features exercised

- **`Vec[Vec[bool]]` as an adjacency matrix** over a fixed 26-letter space, and
  `Vec[Vec[i64]]` as a word list under construction.
- **Recursion with three `mut ref` accumulators** (`state`, `order`, `ok`) — the
  DFS threads all three and forwards them without re-marking, since they are
  already `mut ref` in scope.
- **Insertion sort with a custom comparator** (`before(a, b, rank)`), used by the
  generator to sort under the hidden alphabet.
- **`(x + 97i64) as u8 as char` inside an f-string** to render letter indices.
- **Early loop exit by assigning the bound** (`k = lim`), the idiom this corpus
  uses in place of `break` inside a `while` with a carried index.

## Verification

Every program is byte-identical under `karac run --interp`, `karac run` (JIT),
`karac build` (auto-par default) and `KARAC_AUTO_PAR=0 karac build`; the ★ solver
and the differential match their Python mirrors.

No compiler bugs found.

## Running

```bash
karac run alien_dictionary.kara
karac run alien_dictionary_dfs.kara      # a different, equally valid order
karac run alien_dictionary_brute.kara

diff <(karac run alien_dictionary.kara) <(python3 alien_dictionary.py) && echo OK
diff <(karac run alien_dictionary.kara) <(karac run alien_dictionary_brute.kara) && echo OK

# 1,500 cases: star==brute by equality, dfs by property
diff <(karac run differential.kara) <(python3 differential.py) && echo "differential OK"

for f in alien_dictionary alien_dictionary_dfs alien_dictionary_brute differential; do
    karac build $f.kara && diff <(karac run --interp $f.kara) <(./$f) && echo "$f OK"
done
```
