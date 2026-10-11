# 369. Plus One Linked List

Given a non-negative integer as a non-empty singly linked list of digits,
most significant digit first, add one to it and return the head of the
result.

```
head = [1, 2, 3]   -> [1, 2, 4]
head = [0]         -> [1]
```

**Constraints:** `1 <= number of nodes <= 100`; `0 <= Node.val <= 9`; no
leading zeros except the number 0 itself.

## Approaches

Every arm uses `shared struct ListNode { mut val: i64, mut next:
Option[ListNode] }` and changes the digits in place; a new node appears only
when every digit is a 9.

| file | mechanism | time |
|---|---|---|
| `plus_one.kara` ★ | put a 0 in front, find the last node that is not a 9 in one walk, raise it, zero everything after it; keep the front node only if it was raised | O(n) |
| `plus_one_recursive.kara` | recursion to the last node, adding the carry back up the list | O(n), O(n) stack |
| `plus_one_reverse.kara` | reverse the list, add the carry from the least significant digit until it runs out, reverse back | O(n) |
| `plus_one_stack.kara` | push every node onto a `Vec[ListNode]`, pop and add the carry | O(n), O(n) space |
| `differential.kara` | the four arms against a schoolbook oracle on a `Vec` of digits, 60,000 checks, five properties | — |

Every arm prints the same 10 lines: the two LeetCode examples, seven edge
cases (one 9, all 9s, trailing 9s, a carry that stops at an 8, zeros before
the last digit, a 9 that is not at the end, and sixty 9s), and the digit
count and a checksum over 500 random numbers of up to 30 digits, half of
them ending in a run of 9s. `plus_one.py` mirrors the ★ arm and its output
is byte-identical.

## Differential

`differential.kara` holds copies of the four arms. The oracle adds `k` to a
`Vec` of digits from the last digit up, with no list in sight. The test
draws 3,000 random numbers of 1 to 25 digits: a sixth of them all 9s, a
third ending in a run of 9s, the rest anything without a leading zero.

| | property |
|---|---|
| P1 | each arm gives the oracle's digits |
| P2 | the result has one more digit exactly when every digit was a 9 |
| P3 | the result is one more than the input modulo 1,000,000,007 |
| P4 | applying the arm `k` times, `k` from 1 to 12, adds `k` |
| P5 | every result digit is in `0..=9` and the first is not 0 |

It prints `3000 cases, 60000 checks, 0 failures` under `karac run --interp`,
LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac build`. It does not run
under `karac __mir-run` yet, because its list builder uses
`(0..n).rev()`: see Compiler findings.

## Mutation testing

Nine edits to the copies inside `differential.kara`, each run as a
`karac build` binary. All nine are killed.

| # | mutation | how |
|---|---|---|
| M1 | last: an 8 is skipped like a 9 | P1 to P4, 1951 failures |
| M2 | last: keeps the front node when it reaches 2, so never | P1 to P5, 2850 failures |
| M3 | last: never zeroes the 9s after the raised digit | P1, P3 and P4, 5746 failures |
| M4 | recursive: the last node gets a carry of 0 | P1 to P5, 9569 failures |
| M5 | recursive: keeps the sum, 10 included, as the digit | P1, P3, P4 and P5, 7397 failures |
| M6 | reverse: the new leading digit is 0 | P1, P3, P4 and P5, 2285 failures |
| M7 | reverse: never reverses back | P1, P3, P4 and P5, 10435 failures |
| M8 | stack: adds the carry to one digit only | P1 to P5, 6378 failures |
| M9 | oracle: skips the last digit | P1 and P4, 23968 failures |

## Verification

All four arms print the same output as `plus_one.py` under
`karac run --interp`, LLJIT, `karac build` and `KARAC_AUTO_PAR=1 karac
build`. `karac __mir-run` stops at the test harness's list builder (see
Compiler findings). With that one loop rewritten as a `while` in a scratch
copy, not committed, all four arms and the differential match under
`karac __mir-run` too, so the gap is in the harness's loop, not in the arms.

## Benchmarks

The bench program builds 20 random numbers of 100,000 digits as linked
lists, half of them ending in 50,000 nines, and gives each plus one 20
times with the ★ arm. The Rust mirror uses `Rc<RefCell<..>>` for the shared
struct; the C mirror frees each list once it is summed; Go uses plain
pointers. The Kāra build and all four mirrors print `2000000 digits,
checksum 873681137`. Timings are not taken yet; they need a quiet machine.

## Compiler findings

- **`(0..n).rev()` is not lowered by the MIR builder.** The harness builds
  each list back to front with `for i in (0..digits.len()).rev()`, and
  `karac __mir-run` stops there with `an iterator value is not lowered yet`.
  This is the corpus's existing `mir-gap:an iterator value` bucket, the same
  gap kata 368 hits.
