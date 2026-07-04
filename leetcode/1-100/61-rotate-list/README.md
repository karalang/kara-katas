# 61. Rotate List

> **Difficulty:** Medium &nbsp;·&nbsp; **Topics:** Linked List · Two Pointers &nbsp;·&nbsp; **Source:** [leetcode.com/problems/rotate-list](https://leetcode.com/problems/rotate-list/)

Given the head of a singly linked list, rotate it to the **right** by `k` places — the last `k` nodes wrap around to the front, keeping their order.

```
[1, 2, 3, 4, 5], k = 2   →   [4, 5, 1, 2, 3]   (the tail pair 4,5 moves to the head)
[0, 1, 2],       k = 4   →   [2, 0, 1]         (4 % 3 == 1, so one place)
```

**Constraints:** `0 ≤ list length ≤ 500`; `-100 ≤ Node.val ≤ 100`; `0 ≤ k ≤ 2·10⁹`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| **Close the ring, then cut** — join `tail → head` into a ring, walk `L - k%L - 1` steps to the new tail, sever right after it | O(L) time, O(1) space | [`rotate_list.kara`](rotate_list.kara) ✓ via `karac run` / `karac build` | [`rotate_list.py`](rotate_list.py) ✓ |
| **Two-segment splice** — cut into front/back segments first, then re-join front behind back with `tail.next = head` | O(L) time, O(1) space | [`rotate_list_splice.kara`](rotate_list_splice.kara) ✓ | — |

`✓` runs end-to-end today. Interpreter and codegen produce identical output across all ten test cases, under default (auto-par on) and `KARAC_AUTO_PAR=0` builds alike, and both approaches agree with each other and with the Python mirror.

## Why reduce `k` first, and why a ring?

Two observations do all the work:

1. **`k` and `k % L` land on the same list.** `L` rotations return a list of length `L` to itself, so only `k mod L` matters. LeetCode lets `k` reach **2·10⁹** against a list of at most 500 nodes — the naive "shift one node, `k` times" loop would spin two billion times for a list you could rotate in ≤ 500 steps. Reducing modulo `L` is not an optimization here, it is what makes the problem O(L). Case 8 (`[1,2,3]`, `k = 2·10⁹`) is the one that would hang without it.
2. **After reduction, the new head is the node at index `L - k%L`.** Its predecessor, index `L - k%L - 1`, is the new tail.

**Close the ring** ([`rotate_list.kara`](rotate_list.kara)) realizes the cut with the fewest branches: point the old tail back at the old head to form a cycle, walk `L - s - 1` steps (`s = k % L`) to the new tail, then `result = new_tail.next; new_tail.next = None`. Whether the split lands deep in the list or right at the head, the cut is the same two lines — the same "spend one structural move to erase the special cases" idea as the dummy node in kata [#19](../19-remove-nth-node-from-end-of-list/). The transient cycle is severed before returning, and every node stays reachable from the result, so nothing leaks or is freed early.

**Two-segment splice** ([`rotate_list_splice.kara`](rotate_list_splice.kara)) makes the cut *first* — splitting `[.. new_tail]` from `[new_head .. tail]` — then stitches the front segment behind the back with `tail.next = head`. Because `s` is in `1 .. L-1` once the no-op case is handled, the new tail is strictly before the old tail, so the two field writes never touch the same node. It is the same arithmetic and the same early return, expressed as two independent splices instead of ring-plus-cut — a useful independent cross-check that the modulo/index math, not the ring trick, is what's correct.

Both share the ownership discipline the linked-list corpus turns on: **read before you null.** `result = new_tail.next` (or `new_head = nt.next`) retains the back segment into a local *before* `new_tail.next = None` clears that edge, so nulling the field never frees the node the local now names. `tail.next = head` then stores an *alias* — the same retain-on-store flavor as kata [#24](../24-swap-nodes-in-pairs/)'s `second.next = Some(first)`.

## Kāra features exercised

- **`shared struct ListNode { val, mut next: Option[ListNode] }`** — the corpus's Rc-like linked-node model from kata [#2](../2-add-two-numbers/): reassigning a cursor (`cur = node.next`) re-points without copying, and a field store through the shared reference (`tail.next = head`, `nt.next = None`) mutates the graph in place. Reassigning a `next` drops the previous edge's reference automatically.
- **Transient reference cycle, then severed** — `tail.next = head` deliberately forms a ring, which is broken again by `new_tail.next = None` before the function returns; the result chain keeps every node reachable, so the Rc refcounts settle with no leak and no early free. This is the sharpest ownership case in the kata — read-into-a-local before the cut is what keeps the retained node alive.
- **`Option[ListNode]` cursor walk via `match` / `if let Some(node) = …`** — the measure loop (`match cur { Some(node) => { … cur = node.next; } None => break }`) and the fixed-step advance (`while i < steps { if let Some(node) = new_tail { new_tail = node.next; } }`) are the same cursor idioms as katas [#19](../19-remove-nth-node-from-end-of-list/) and [#24](../24-swap-nodes-in-pairs/).
- **`k % len` modular reduction** — the whole reason the 2·10⁹ bound is harmless; `%` on `i64`, reduced once against the measured length.
- **`Slice[i64]` param + `Array[i64, N]` literals** — `from_array(arr: Slice[i64])` fed by sized array literals (including the empty `Array[i64, 0] = []`), same harness shape as the other list katas.

**v1 note.** `k` reaches 2·10⁹, which still fits `i32` (max 2.147·10⁹); the arithmetic is `i64` for uniformity with the rest of the corpus, not because the width is forced. The load-bearing part is the modulo, not the range — contrast kata [#18](../18-4sum/), where the 10⁹ *sum* bound genuinely requires `i64`.

## Running

```bash
# Kāra — interpreter and codegen produce the same output today.
karac run   rotate_list.kara
karac build rotate_list.kara && ./rotate_list

# The alternative approach (identical output):
karac run rotate_list_splice.kara

# Python
python3 rotate_list.py

# Verify they all agree
diff <(karac run rotate_list.kara) <(python3 rotate_list.py)                  && echo OK
diff <(karac run rotate_list.kara) <(karac run rotate_list_splice.kara)       && echo OK
diff <(karac run rotate_list.kara) <(./rotate_list)                           && echo OK
```
