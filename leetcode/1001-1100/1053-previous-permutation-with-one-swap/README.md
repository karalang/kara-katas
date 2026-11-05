# 1053. Previous Permutation With One Swap

Given an array of positive integers `arr` (not necessarily distinct),
return the **lexicographically largest** permutation that is smaller than
`arr`, that can be **made with exactly one swap**. If it cannot be done,
then return the same array.

**Note** that a *swap* exchanges the positions of two numbers `arr[i]` and
`arr[j]`.

```
arr = [3,2,1]        ->  [3,1,2]
arr = [1,1,5]        ->  [1,1,5]
arr = [1,9,4,6,7]    ->  [1,7,4,6,9]
```

**Constraints:** `1 <= arr.length <= 10^4`; `1 <= arr[i] <= 10^4`.

## Approaches

A swap makes the array smaller only when it moves a smaller value left, and
the largest such result changes the array as far right as it can. So the
place to change is the last `i` where a value is larger than the next one;
the values after it rise. It takes the largest value after it that is still
smaller, and of several equal ones the leftmost, which leaves the larger
value as far left as it can go. An array that never falls has nothing
smaller one swap away.

| file | mechanism |
|---|---|
| `prev_perm.kara` ★ | one scan from the right for `i`, a second from the right for the largest smaller value, then left along its run of equals. O(n) |
| `prev_perm_search.kara` | `i` by `(0..n - 1).rev().find(..)` in a `let ... else`, then the rising values after it searched twice with `partition_point`: once for the largest smaller value, once for the start of its run. O(n) for `i`, O(log n) for the rest |
| `prev_perm_map.kara` | a `SortedMap` from each value seen, walking from the right, to its leftmost place so far; the first value with a smaller one in the map takes `seen.range(0, v).last()`. O(n log n) |
| `prev_perm_iter.kara` | `arr.windows(2).iter().rposition(\|w\| w[0] > w[1])` for `i`, then `(i + 1..n).filter(..).max_by_key(\|j\| (arr[j], -j))` for the partner. O(n) |
| `prev_perm_candidates.kara` | each smaller value after `i` swapped in turn, the arrays compared with `>` and the largest kept. O(n^2) |
| `differential.kara` | the five arms against the statement read literally, six properties |

Every arm prints the same 14 lines: the answers for LeetCode's three
examples and seven more (`[3, 1, 1, 3]`, whose answer takes the first of
the two 1s, and `[6, 2, 2, 5, 5, 1]`, whose fall is the last pair, among
them); the number changed and a checksum of the answers for 3000 random
arrays of 1 to 8 values of 1 to 4 and for 300 arrays of 1 to 2000 values of
1 to 10000; and two arrays of 10000, the limit: rising but for a first
value of 5000, and rising with the last two swapped. `prev_perm.py` mirrors
the ★ arm and its output is byte-identical.

## Differential

`differential.kara` holds copies of the five arms and the statement read
literally: every swap of two places is tried, and the largest result that is
smaller than the array is kept, or the array itself when there is none. It
checks 3000 random arrays: 2000 of 1 to 8 values of 1 to 3, where values
repeat, and 1000 of 1 to 30 values of 1 to 100.

| | property |
|---|---|
| P1 | the answer is the statement read literally |
| P2 | the answer holds the same values, differs from the array in no place or in two, is no larger, and is the array itself exactly when the array never falls |
| P3 | dropping the values before the first place the answer changes leaves the rest of the answer (an unchanged array drops its first value) |
| P4 | every value 3 larger, or doubled, moves the answer the same way |
| P5 | a value no larger than any added at the front, and one larger than any added at the back, leave the answer between them |
| P6 | each arm agrees with at least two of the other four |

P3 holds because the answer's swap lies at or after its first changed place,
so the values before it decide nothing. P4 holds because the answer depends
only on how the values compare. P5's front value is no larger than anything
after it, so it starts no fall, and the back value is larger than every
value, so it ends no fall and is never the smaller partner.

The differential prints `3000 arrays: checksum 697749268, 90000 checks over
5 arms: 0 failures` under `karac __mir-run` (4.6 s), `karac __mir-llvm-run`
and `karac __mir-llvm-asan` with no error, and the same line under `karac
run` and from a `karac build` binary. On a failure it prints the first ten
and then the count by property.

## Mutation testing

Thirty-six edits to the differential, six to each arm and three more to the
iter and candidates arms, each run under `karac __mir-run` and `karac
__mir-llvm-run`. Fifteen are kept, three to each arm. All fifteen are
killed, each fails the same way under both backends, and no two kept ones
fail the same checks.

| # | mutation | failures by property |
|---|---|---|
| M1 | ★: of equal values the rightmost | P1 420, P6 420 |
| M2 | ★: an equal value taken as smaller | P1 413, P2 413, P6 413 |
| M3 | ★: the last pair never tried | P1 934, P2 169, P3 72, P5 934, P6 934 |
| M4 | search: the smallest value after `i` | P1 384, P6 384 |
| M5 | search: the first fall, not the last | P1 1571, P2 168, P3 18, P5 372, P6 1571 |
| M6 | search: the swap one place left | P1 2368, P2 1984, P6 2368 |
| M7 | map: an equal value taken as smaller | P1 802, P2 802, P6 802 |
| M8 | map: the scan goes on after a swap | P1 1869, P2 1636, P6 1869 |
| M9 | map: the last value never seen | P1 1303, P2 262, P5 1303, P6 1303 |
| M10 | iter: the smallest smaller value | P1 770, P6 770 |
| M11 | iter: the first fall (`position`) | P1 1571, P6 1571 |
| M12 | iter: the value after `i` swapped instead | P1 2368, P2 2368, P3 384, P6 2368 |
| M13 | candidates: each candidate swapped from the best so far | P1 384, P2 384, P6 384 |
| M14 | candidates: the last value never tried | P1 1303, P2 1027, P5 1303, P6 1303 |
| M15 | candidates: every candidate swaps with the last place | P1 1065, P2 790, P5 2368, P6 1065 |

P1 and P6 kill all fifteen, P2 eleven, P5 five, P3 three and P4 none. M1,
M4, M10 and M11 are seen only by P1 and P6: each picks a wrong smaller
value or a wrong fall, and the result is still one swap down, in range,
and moved the same way by the edits to the ends. P4 kills nothing because
every edit kept, like every arm, reads only how the values compare, and
P4 holds for anything built from comparisons alone. P3 sees the edits that
change a place other than the true fall (M3, M5, M12), whose answer then
depends on values the true answer ignores. P5 sees the edits that treat
the last place apart (M3, M9, M14, M15), and the binary search run on
values that do not rise (M5), which a longer array probes differently.

Twenty-one other edits were set aside. Eleven fail exactly as a kept one
does: taking the rightmost of equal values in the search, map and iter
arms, or letting every candidate replace the best so the last is kept, as
M1; counting an equal value as smaller in the search,
iter and candidates arms, as M2; and taking the first smaller value after
`i` (map, iter) or keeping the first candidate, as M4; and keeping the
smallest candidate, as M10. Two fail in ways of their own, in arms that had
three kept already: the ★ arm reversing the values after the swap, and the
map arm undoing its swap. Three are equivalent: the ★ arm
searching for the partner from the left, since the values after `i` rise
and the smaller ones are a prefix of them; the candidates arm keeping the
last of equal candidates, which are the same array; and the candidates arm
stopping its scan for `i` at place 0, which it reaches only when the array
never falls. Five crash, each the same way on both backends: the ★ arm
stopping at an equal pair and the search arm taking one as a fall run past
the start ("index out of bounds"), the iter arm taking an equal pair as a
fall or skipping the value just after `i` finds no partner ("called unwrap()
on None"), and the iter arm swapping one place right of its pick runs past
the end.

## Verification

Every arm prints the same output as `prev_perm.py` under `karac __mir-run`
(the v2 MIR interpreter) and `karac __mir-llvm-run`, and under `karac
__mir-llvm-asan` (AddressSanitizer and LeakSanitizer) with no error.
`karac run` and a `karac build` binary print the same output for every arm
and the differential. `karac check --output=json` reports nothing on any
file. The runs used a release build of kara `2579cb70b9`. Under `karac
__mir-run` the arms take 0.6 s (search) to 3.6 s (candidates).

The map and candidates arms passed `karac check` as first written, and
`karac fix` turned the ★ arm's `&&` into `and`. The search and iter arms
and the differential, written the way Rust writes them, found five gaps in
kara, fixed in `9da1fd1978`:

- `tail.partition_point(..)` on a `Vec` was "no method 'partition_point'
  on type 'Vec'", and `windows(2).iter().rposition(..)` was "no method
  'rposition' on type 'VecIter'". The library now has `partition_point` on
  `Slice[T]` and `rposition` on the `Vec` and slice iterators, and a `Vec`
  receiver finds every library `Slice[T]` method, as the library reference
  says it does (`v.clone_from_slice(w)` was refused the same way).
- `let tail = &out[i + 1..];` was fixed to `ref out[i + 1..]`, a borrow of
  a view, which `karac check` then refused. The fix now drops the `&`, since
  a range index is already a view.
- `let tail = out[i + 1..];` kept `out` borrowed to the end of the function,
  so the later `out.swap(..)` was refused, though `tail` was last used two
  lines earlier. A slice bound by `let` is now borrowed to its last use, as
  core semantics §5 says, when nothing it was used for could have kept it.
- `let Some(i) = (0..n - 1).rev().find(|k| out[k] > out[k + 1]) else {
  return out; };` was "value 'out' is moved inside a loop". The `else`
  block runs after the closure is done, and is now treated so.
- In the differential, `tried < arr` (a `Vec` and a `Slice`) was "cannot
  compare" with no fix; it now offers `.as_slice()`, and the view that
  takes in a comparison ends with the comparison, so `best = tried;` on the
  next line is no longer refused. The iter arm's `arr[*j]` on a range item
  drew the existing fix that drops the `*`.

## Benchmarks

The bench builds 200 arrays of 20000 values once in all five languages:
random values of 1 to 10000, then a rising run of random length starting
below 1000. It then runs the ★ arm on every array 25 times, folding the
answer from the place before the run to the end into a checksum. The scan
from the right walks the run to find the fall and back down it for the
partner, so the work is the copy and two passes over the run. Every
implementation prints `200 arrays of 20000 values, 25 rounds: total
18210325, checksum 782973982`.

Each implementation copies the array into a fresh one (`to_vec`,
`memcpy`, `copy`), scans with bounds-checked reads where the language checks
them, and swaps.

Timings on a 4-core container, eight interleaved runs of each compiled
program and one of Python, with kara `2579cb70b9` on LLVM 22:

| | time | median |
|---|---|---|
| C (`clang -O3`) | 0.367 to 0.408 s | 0.372 s |
| Kāra (`karac build`) | 0.371 to 0.396 s | 0.386 s |
| Rust (`rustc -O`) | 0.381 to 0.419 s | 0.389 s |
| Rust (`rustc -O -C overflow-checks=on`) | 0.381 to 0.407 s | 0.389 s |
| Kāra (`KARAC_AUTO_PAR=0 karac build`) | 0.366 to 0.415 s | 0.395 s |
| Go | 0.494 to 0.507 s | 0.503 s |
| Python | 8.7 s | |

`bench.sh` builds the Kāra program with `KARAC_AUTO_PAR=0 karac build`,
the sequential lane. A plain `karac build` parallelizes nothing here: its
user time (0.363 s) is below its real time.

Kāra took 1.02 times Rust's median time under overflow checks, and 1.06
times C's; the spread between runs is wider than those gaps. Go took 1.35
times C's.
