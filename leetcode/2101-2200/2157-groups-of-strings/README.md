# 2157. Groups of Strings

You are given a **0-indexed** array of strings `words`. Each string
consists of **lowercase English letters** only. No letter occurs more
than once in any string of `words`.

Two strings `s1` and `s2` are said to be **connected** if the set of
letters of `s2` can be obtained from the set of letters of `s1` by any
**one** of the following operations:

- Adding exactly one letter to the set of the letters of `s1`.
- Deleting exactly one letter from the set of the letters of `s1`.
- Replacing exactly one letter from the set of the letters of `s1` with
  any letter, **including** itself.

The array `words` can be divided into one or more non-intersecting
**groups**. A string belongs to a group if any **one** of the following
is true:

- It is connected to **at least one** other string of the group.
- It is the **only** string present in the group.

Note that the strings in `words` should be grouped in such a manner
that a string belonging to a group cannot be connected to a string
present in any other group. It can be proved that such an arrangement
is always unique.

Return *an array* `ans` *of size* `2` *where:*

- `ans[0]` *is the **maximum number** of groups* `words` *can be divided
  into, and*
- `ans[1]` *is the **size of the largest** group*.

```
words = ["a","b","ab","cde"]  ->  [2,3]
words = ["a","ab","abc"]      ->  [1,3]
```

**Constraints:** `1 <= words.length <= 2 * 10^4`; `1 <= words[i].length
<= 26`; `words[i]` consists of lowercase English letters only; no letter
occurs more than once in `words[i]`.

A word is its set of letters, 26 bits. A word one letter shorter is a
set the other makes by losing a letter, and two words one letter
replaced make the same set by losing the letter that differs, so every
join is found by looking up the 26 or fewer sets each word makes by
losing a letter. O(26 n) map lookups.

## Approaches

| file | mechanism |
|---|---|
| `groups.kara` ★ | a union-find over the words with path halving and union by size, as free functions taking `mut ref Vec`s; each word joined to the first word of its own set, to the first word of each set it makes by losing a letter, and, through a second map of those shorter sets, to the first word that made the same one |
| `groups_struct.kara` | a `struct Groups` union-find whose `root` points the whole path at the root by recursion (`mut ref self`), with `join` and `tally`; one map keyed by each set and, tagged with a 27th bit by a `const`, by each shorter set; each word's letters peeled off lowest first with `rest & -rest` |
| `groups_bfs.kara` | a breadth-first search over the sets, not the words: each set's count of words in a map through `entry().or_insert(0)`, and a `VecDeque` walking to every set one letter added, taken away or replaced, each set's count taken out of the map by `remove` as it is reached |
| `groups_graph.kara` | a graph of the words and the sets they meet at: each word an edge to its own set and to each set it makes by losing a letter, one kind of key serving all three rules; components by a depth-first search with an explicit stack |
| `groups_merge.kara` | each group a list of its words and each word a label naming its list; two groups merge by moving the smaller list's words into the larger, through the ★ arm's two maps |
| `groups_solution.kara` | LeetCode's Rust template: two `HashMap<i32, usize>`s, a union-find whose `find` is a function nested in the method, `vec![1; n]`, `c as u8 - b'a'`; carried by `karac fix` in five rounds |
| `differential.kara` | the six arms against the statement read literally, six properties |

Every arm prints the same 9 lines: LeetCode's two examples and four more
(one word, the same letters in two orders, three words apart, and three
joined only by replacing), each with its answer; then the total and a
checksum over 2000 random lists of 1 to 8 words of 1 to 4 distinct
letters from the first 4, 6 or 26 in turn; then the constraints'
largest, 20000 words of 1 to 5 letters from the first 10 and of 1 to 26
from all 26. `groups.py` mirrors the ★ arm and its output is
byte-identical.

No compiler gap was met. The harness was first written with Rust's
`w.contains(c)` for a `char`, and `karac fix` made it
`w.contains(c.to_string())`, since Kāra's `contains` takes a string.
`karac fix` carries the template in five rounds of 39, 2, 4, 13 and 1
edits: Rust's spellings (the `use` dropped, `<..>` to `[..]`, `&mut Vec`
to `mut ref Vec`, `find(&mut p, ..)` to `find(mut p, ..)`, `HashMap::new`
to `HashMap.new`, `Some(&j) = first.get(&x)` to `Some(j) =
first.get(x).cloned()`, `struct Solution;` to `struct Solution {}`, the
adapter's `&Vec` to `ref Vec` and `|&x|` to `|x|`, `Solution::` to `.`);
then the nested `fn find` moved out of the method to the top level,
since Kāra nests no functions; then `HashMap` to `Map`; then every
`usize` to `i64`, the nested call's `p` passed on as `mut p`, `vec![1;
n]` and `vec![0i32; n]` to `Vec.filled`, `c as u8` to `c as u32 as u8`,
since a `char` does not cast to `u8` in one step, and `vec![..]` to
`[..]`; then the `ref` dropped from the adapter's parameter, which
borrows already.

## Differential

`differential.kara` holds copies of the six arms and the statement read
literally: every two words compared letter by letter for the three
rules (a letter added, taken away, or replaced by any letter, itself
included), and the groups found by relabelling until no join changes a
label; no bits, maps or union-find. It checks 300 random lists of 1 to 8
words of 1 to 3 letters from the first 3, 5 or 26 in turn; then 30 of
words from the first 2 letters, so that many repeat; then 30 of 1 to 4
words of up to 26 letters. All 360 are drawn before any arm answers.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the words in reverse order: the same answer |
| P3 | every word's letters reversed: the same answer |
| P4 | every letter moved on by one, z to a: the same answer |
| P5 | every word listed twice: the same groups, the largest twice as big |
| P6 | each arm agrees with at least three of the other five |

The differential prints `360 lists: checksum 91670446, 12960 checks over
6 arms: 0 failures` under every lane in Verification; the checksum of
the literal answers was checked against a Python reading of the same
lists by the same comparing. On a failure it prints the first ten and
then the count by property.

## Mutation testing

Twenty-eight edits to the differential, three to six to each arm, each
run under `karac __mir-llvm-run` and `karac __mir-run`. Eighteen are
kept: three to each Kāra arm but the struct, which has four, and two to
the Rust-template arm. Each kept one is killed, fails the same way under
both backends and not by a crash or a hang, and no two kept ones fail
the same checks. The breadth-first arm walks its sets in the map's
order, which differs from run to run, so a wrong edit there can fail a
different number of checks on each run; its edits were run under
`KARAC_HASH_SEED=1`, which makes the two backends agree, and the counts
below are from that seed.

| # | mutation | failures by property |
|---|---|---|
| M2 | ★: a letter taken away never joined | P1 162, P6 162 |
| M4 | ★: the sizes never added | P1 234, P5 360, P6 234 |
| M5 | ★: the letter z never taken away | P1 8, P4 12, P6 8 |
| M6 | struct: a joined tree's size added to the wrong root | P1 149, P2 82, P5 93, P6 149 |
| M9 | struct: no root counting itself | P1 360, P6 360 |
| M26 | struct: a set with a letter blanked out never remembered | P1 136, P6 136 |
| M28 | struct: a word's first letter never counted | P1 110, P3 60, P6 110 |
| M11 | bfs: letters only taken away, never added | P1 106, P2 94, P6 106 |
| M12 | bfs: a group's sets counted, not its words | P1 86, P2 48, P5 216, P6 86 |
| M13 | bfs: a letter replaced by one already there | P1 135, P2 49, P6 135 |
| M14 | graph: no key for a letter taken away | P1 221, P6 221 |
| M15 | graph: the first key counted as a word | P1 328, P2 44, P5 328, P6 328 |
| M17 | graph: only the lowest letter taken away | P1 131, P4 2, P6 131 |
| M18 | merge: the moved words never relabelled | P1 144, P2 70, P5 234, P6 144 |
| M21 | merge: a letter added rather than taken away | P1 151, P4 1, P6 151 |
| M27 | merge: the moved words never added to the larger list | P1 234, P2 40, P5 360, P6 234 |
| M23 | solution: the letter a never taken away | P1 133, P4 140, P6 133 |
| M24 | solution: a word's set its last letter alone | P1 170, P6 170 |

P1 and P6 kill all eighteen; P2 kills seven, P5 six, P4 four and P3
one. The answer depends only on which sets the words hold and how they
touch, so a wrong edit mostly shows at once against the literal reading
and the other arms, and the other properties tell apart edits that are
wrong in different ways. P2 reverses the words, which changes which
word comes first to a set or to a merge; it sees all three bfs edits,
the wrong-root sizes (M6), the first key counted as a word (M15), and
the merge arm's lists (M18, M27). P5 doubles every word, which sees
edits that count words wrongly, among them M4, M12 and M15. P4 moves
every letter on by one, which sees edits that treat one letter or one
end of the alphabet apart (M5, M17, M21, M23). P3 reverses each
word's letters, which every right answer ignores; it sees only M28,
which skips a word's first letter, since reversing makes another letter
first.

Of the twenty-eight, ten were not kept. Four are equivalent, and they
are one finding: a word's join to the first word of its own set (M1,
M8, M20, M22, in the ★, struct, merge and template arms) can be dropped,
since two words of the same set also make the same shorter set, which
the replacing rule joins, a letter replaced by itself. One hangs: the
struct arm's lowest letter found by `rest & (rest - 1)`, which never
empties `rest`. Five fail as a kept one does: the ★ arm's blanked set
never remembered and the bfs arm's letters never replaced, as M26; the
graph arm's key never leading back to its words and the merge arm's
smaller list never emptied, as M4; and the graph arm's word with no key
for its own set, as M2.

## Verification

Every arm prints the same output as `groups.py` under `karac __mir-run`
(the v2 MIR interpreter), `karac __mir-llvm-run`, and `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every
arm and the differential. `karac check --output=json` reports nothing on
any of them, and `karac fix --dry-run` has nothing to apply.

Under `karac __mir-run` the arms take 2.4 s to 5.2 s and the
differential 1.6 s.

## Benchmarks

The bench builds 4 lists of 5000 words of 1 to 8 distinct letters from
the first 20 once; then solves every list 25 times, one word replaced
by a new one before each solve so that no solve repeats one before,
with the ★ arm in all five languages; C's two maps are open-addressing
tables, since C has none of its own. Every implementation prints `100
solves: 96196 groups in all, checksum 434720038`.

BENCHTAB
