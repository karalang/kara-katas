// LeetCode #124 benchmark mirror (Rust). Kara's semantic peer: an RC tree
// (`Option<Rc<TreeNode>>`) mirroring the `shared struct TreeNode`, read-only
// post-order traversal. Same algorithm and tree construction as the other mirrors.
use std::rc::Rc;

const TREE_COUNT: i64 = 2048;
const NODE_COUNT: i64 = 511;
const REPS: i64 = 60;

struct TreeNode {
    val: i64,
    left: Option<Rc<TreeNode>>,
    right: Option<Rc<TreeNode>>,
}

fn node_value(i: i64, seed: i64) -> i64 {
    ((i * 37 + seed * 13) % 41) - 20
}

fn build_balanced(lo: i64, hi: i64, seed: i64) -> Option<Rc<TreeNode>> {
    if lo > hi {
        return None;
    }
    let mid = (lo + hi) / 2;
    Some(Rc::new(TreeNode {
        val: node_value(mid, seed),
        left: build_balanced(lo, mid - 1, seed),
        right: build_balanced(mid + 1, hi, seed),
    }))
}

fn max_gain(node: &Option<Rc<TreeNode>>, best: &mut i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let lg = max_gain(&n.left, best);
            let rg = max_gain(&n.right, best);
            let left_gain = if lg > 0 { lg } else { 0 };
            let right_gain = if rg > 0 { rg } else { 0 };
            let through = n.val + left_gain + right_gain;
            if through > *best {
                *best = through;
            }
            let branch = if left_gain > right_gain { left_gain } else { right_gain };
            n.val + branch
        }
    }
}

fn max_path_sum(root: &Option<Rc<TreeNode>>) -> i64 {
    let mut best: i64 = -1000000000;
    max_gain(root, &mut best);
    best
}

fn main() {
    let forest: Vec<Option<Rc<TreeNode>>> =
        (0..TREE_COUNT).map(|t| build_balanced(0, NODE_COUNT - 1, t + 1)).collect();

    let mut sink: i64 = 0;
    for _ in 0..REPS {
        for root in &forest {
            sink += max_path_sum(root);
        }
    }
    println!("{}", sink);
}
