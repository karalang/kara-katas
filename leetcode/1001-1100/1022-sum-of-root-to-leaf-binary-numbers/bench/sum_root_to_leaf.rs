// LeetCode #1022: Sum of Root To Leaf Binary Numbers -- bench
// Mirrors ./sum_root_to_leaf.kara; see ../README.md § Benchmarks.
// The tree is LeetCode's Rust shape, Rc<RefCell<TreeNode>>, the
// counterpart of a Kāra `shared struct`.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn sum_root_to_leaf(root: &Option<Rc<RefCell<TreeNode>>>) -> i64 {
    sum_from(root, 0)
}

fn sum_from(node: &Option<Rc<RefCell<TreeNode>>>, above: i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let n = n.borrow();
            let value = above * 2 + n.val;
            if n.left.is_none() && n.right.is_none() {
                value
            } else {
                sum_from(&n.left, value) + sum_from(&n.right, value)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn random_tree(seed: &mut i64, n: i64) -> Option<Rc<RefCell<TreeNode>>> {
    let root = new_node(next_random(seed) % 2);
    let mut placed = 1;
    while placed < n {
        let mut node = root.clone();
        let mut level = 1;
        loop {
            let go_left = next_random(seed) % 2 == 0;
            let next = if go_left { node.borrow().left.clone() } else { node.borrow().right.clone() };
            match next {
                Some(child) => {
                    node = child;
                    level += 1;
                    if level == 31 {
                        break;
                    }
                }
                None => {
                    let leaf = new_node(next_random(seed) % 2);
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
    let rounds = 500;
    let mut seed = 1022;
    let mut trees: Vec<Option<Rc<RefCell<TreeNode>>>> = Vec::new();
    let mut nodes = 0;
    for _ in 0..count {
        let n = next_random(&mut seed) % 1000 + 1;
        nodes += n;
        trees.push(random_tree(&mut seed, n));
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for tree in trees.iter() {
            let answer = sum_root_to_leaf(tree);
            total += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{count} trees, {nodes} nodes, {rounds} rounds: sum {total}, checksum {check}");
}
