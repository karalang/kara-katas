// LeetCode #1026: Maximum Difference Between Node and Ancestor -- bench
// Mirrors ./max_ancestor_diff.kara; see ../README.md § Benchmarks.
// The tree is LeetCode's Rust shape, Rc<RefCell<TreeNode>>, the
// counterpart of a Kāra `shared struct`.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn max_ancestor_diff(root: &Option<Rc<RefCell<TreeNode>>>) -> i64 {
    match root {
        None => 0,
        Some(r) => {
            let v = r.borrow().val;
            best_below(root, v, v)
        }
    }
}

fn best_below(node: &Option<Rc<RefCell<TreeNode>>>, low: i64, high: i64) -> i64 {
    match node {
        None => high - low,
        Some(n) => {
            let n = n.borrow();
            let lo = low.min(n.val);
            let hi = high.max(n.val);
            best_below(&n.left, lo, hi).max(best_below(&n.right, lo, hi))
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64, top: i64) -> i64 {
    let high = next_random(seed);
    (high * 32768 + next_random(seed)) % top
}

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode {
        val,
        left: None,
        right: None,
    }))
}

fn random_tree(seed: &mut i64, n: i64) -> Option<Rc<RefCell<TreeNode>>> {
    let root = new_node(random_value(seed, 100001));
    let mut placed = 1;
    while placed < n {
        let mut node = root.clone();
        loop {
            let go_left = next_random(seed) % 2 == 0;
            let next = if go_left {
                node.borrow().left.clone()
            } else {
                node.borrow().right.clone()
            };
            match next {
                Some(child) => {
                    node = child;
                }
                None => {
                    let leaf = new_node(random_value(seed, 100001));
                    if go_left {
                        node.borrow_mut().left = Some(leaf);
                    } else {
                        node.borrow_mut().right = Some(leaf);
                    }
                    placed += 1;
                    break;
                }
            }
        }
    }
    Some(root)
}

fn main() {
    let count = 200;
    let rounds = 50;
    let mut seed = 1026;
    let mut trees: Vec<Option<Rc<RefCell<TreeNode>>>> = Vec::new();
    let mut nodes = 0;
    for _ in 0..count {
        let n = next_random(&mut seed) % 4999 + 2;
        nodes += n;
        trees.push(random_tree(&mut seed, n));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for tree in trees.iter() {
            let answer = max_ancestor_diff(tree);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{count} trees, {nodes} nodes, {rounds} rounds: sum {total}, checksum {check}");
}
