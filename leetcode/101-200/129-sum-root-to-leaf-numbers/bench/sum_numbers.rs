// Benchmark harness for LeetCode #129 — Sum Root to Leaf Numbers.
// Mirrors sum_numbers.kara algorithm-for-algorithm.
//
// Uses Rc<TreeNode> to match kara's `shared struct`, which is reference
// counted. `sum_dfs` takes Option<Rc<..>> BY VALUE and the recursive calls
// clone, so this lane pays the same retain/release traffic kara does. Go (GC
// pointers) and C (raw malloc'd pointers) do not — see ../README.md.
//
// The tree is built bottom-up so the children are finished before the parent is
// constructed, which avoids needing RefCell for kara's post-construction
// `node.left = ...`. That is a setup-only difference; the measured DFS is
// identical.

use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<TreeNode>>,
    right: Option<Rc<TreeNode>>,
}

fn sum_dfs(node: Option<Rc<TreeNode>>, acc: i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let cur = acc * 10 + n.val;
            if n.left.is_none() && n.right.is_none() {
                cur
            } else {
                sum_dfs(n.left.clone(), cur) + sum_dfs(n.right.clone(), cur)
            }
        }
    }
}

fn sum_numbers(root: Option<Rc<TreeNode>>) -> i64 {
    sum_dfs(root, 0)
}

fn digit(i: i64, seed: i64) -> i64 {
    ((i * 7 + seed * 3) % 9) + 1
}

fn build_balanced(lo: i64, hi: i64, seed: i64) -> Option<Rc<TreeNode>> {
    if lo > hi {
        return None;
    }
    let mid = (lo + hi) / 2;
    let l = build_balanced(lo, mid - 1, seed);
    let r = build_balanced(mid + 1, hi, seed);
    Some(Rc::new(TreeNode {
        val: digit(mid, seed),
        left: l,
        right: r,
    }))
}

fn main() {
    let np: i64 = 4;
    let n: i64 = 2047;
    let iters: i64 = 40000;

    let trees: Vec<Option<Rc<TreeNode>>> =
        (0..np).map(|j| build_balanced(0, n - 1, j + 1)).collect();

    let mut sink: i64 = 0;
    for it in 0..iters {
        let idx = ((it * 3) % np) as usize;
        sink = (sink + sum_numbers(trees[idx].clone())) % 1000000007;
    }
    println!("{}", sink);
}
