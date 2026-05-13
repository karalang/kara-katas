# 226. Invert Binary Tree

> **Difficulty:** Easy &nbsp;·&nbsp; **Topics:** Tree, DFS, BFS &nbsp;·&nbsp; **Source:** [leetcode.com/problems/invert-binary-tree](https://leetcode.com/problems/invert-binary-tree/)

Given the root of a binary tree, invert the tree (mirror every node's two children) and return its root.

**Constraints:** `0 ≤ nodes ≤ 100`, `-100 ≤ Node.val ≤ 100`.

## Approaches

| Approach | Complexity | Kāra | Python |
|---|---|---|---|
| Recursive DFS (post-order swap) | O(n) time, O(h) stack | [`recursive.kara`](recursive.kara) ✓ via `karac run` | [`recursive.py`](recursive.py) ✓ |
| Iterative BFS (queue + in-place swap) | O(n) time, O(w) queue | [`iterative.kara`](iterative.kara) ✓ via `karac run` | [`iterative.py`](iterative.py) ✓ |

`✓` runs end-to-end today. `h` is tree height; `w` is max width.

### Why both?

Recursive DFS is the textbook formulation — three lines if you let the language carry the stack. Iterative BFS is the "what if `n = 10⁵` and the tree degenerates to a chain" answer: a queue caps memory at `O(w)` instead of letting the call stack grow to `O(n)`. Both are O(n) wall-clock; the choice is which auxiliary space you'd rather spend.

The two approaches also exercise different Kāra surface area — recursive uses self-call + Option pattern matching; iterative uses `VecDeque`, in-place field mutation through `shared struct` reference semantics, and a `loop { match queue.pop_front() { ... } }` drain idiom.

## Kāra features exercised

- **`shared struct` with mutable fields** — `shared struct TreeNode { val: i64, mut left: Option[TreeNode], mut right: Option[TreeNode] }`. RC-backed reference semantics mean `current.left = ...` mutates through the shared handle without explicit `Rc<RefCell<…>>` machinery.
- **Recursive types via `Option[Self]`** — no `Box[T]` needed; `shared` already implies heap indirection.
- **Pattern matching on `Option`** — `match root { None => …, Some(node) => … }`, plus the `if let Some(x) = …` shorthand in the BFS drain loop.
- **`VecDeque`** — `VecDeque.new()`, `push_back`, `pop_front`, and the `loop { match pop_front() { None => { break; }, Some(_) => … } }` drain idiom.

No `Vec`, `Map`, or strings — pure tree manipulation.

## API shape

Each solution exposes `invert(root: Option[TreeNode]) -> Option[TreeNode]` and a thin `report` that prints. `main` calls `report` per test case. Logic is separate from I/O so the function is testable once a harness exists.

## Output format

`report` prints the level-order traversal of the **inverted** tree, one node value per line, skipping `None` children. The test cases use (near-)full binary trees, so level-order without nulls is unambiguous — `[4,7,2,9,6,3,1]` reconstructs uniquely back to a full depth-3 tree.

Kāra and Python output is line-for-line identical so the four files can be diffed directly.

```
4
7
2
9
6
3
1
2
3
1
```

(The third test case is an empty tree and prints nothing.)

## Running

```bash
# Kāra
karac run recursive.kara
karac run iterative.kara

# Python (3.10+ for PEP 604 union syntax)
python3 recursive.py
python3 iterative.py
```

## Planned

- `recursive.rs` / `iterative.rs` Rust siblings — once added, completes the {Kāra, Python, Rust} triad used in `1-two-sum`.
- `bench/` parity workload — large random trees (e.g., 100k nodes, mixed balanced + skewed) so this kata can join the hyperfine harness.
