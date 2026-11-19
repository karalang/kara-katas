// LeetCode #1644: Lowest Common Ancestor of a Binary Tree II -- the bench's
// Rust mirror: the ★ arm on 60 random trees of 10000 nodes, each asked
// about 50 pairs of values, one in five of them not in the tree, all drawn
// first. The tree is LeetCode's `Rc<RefCell<TreeNode>>`, counted as
// Kāra's `shared struct` is.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn leaf(val: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn lowest_common_ancestor(root: &Option<Node>, p: &Node, q: &Node) -> Option<Node> {
    let mut found = None;
    count_below(root, p.borrow().val, q.borrow().val, &mut found);
    found
}

fn count_below(node: &Option<Node>, p: i32, q: i32, found: &mut Option<Node>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let b = n.borrow();
            let here = if b.val == p || b.val == q { 1 } else { 0 };
            let count = count_below(&b.left, p, q, found) + count_below(&b.right, p, q, found) + here;
            if count == 2 && found.is_none() {
                *found = Some(Rc::clone(n));
            }
            count
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, seed: &mut i64) -> Option<Node> {
    let mut values: Vec<i32> = (0..n as i32).collect();
    for i in (1..n as usize).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let mut nodes: Vec<Node> = Vec::new();
    for i in 0..n as usize {
        let node = leaf(values[i]);
        if i > 0 {
            let mut at = Rc::clone(&nodes[(next_random(seed) % i as i64) as usize]);
            loop {
                let next = if next_random(seed) % 2 == 0 {
                    let mut b = at.borrow_mut();
                    match &b.left {
                        Some(child) => Rc::clone(child),
                        None => {
                            b.left = Some(Rc::clone(&node));
                            break;
                        }
                    }
                } else {
                    let mut b = at.borrow_mut();
                    match &b.right {
                        Some(child) => Rc::clone(child),
                        None => {
                            b.right = Some(Rc::clone(&node));
                            break;
                        }
                    }
                };
                at = next;
            }
        }
        nodes.push(node);
    }
    Some(Rc::clone(&nodes[0]))
}

fn main() {
    let mut seed: i64 = 1644;
    let mut trees = Vec::new();
    for _ in 0..60 {
        let root = random_tree(10000, &mut seed);
        let mut pairs = Vec::new();
        for _ in 0..50 {
            let p = next_random(&mut seed) % 12500;
            let mut q = next_random(&mut seed) % 12500;
            if q == p {
                q = (q + 1) % 12500;
            }
            pairs.push((p as i32, q as i32));
        }
        trees.push((root, pairs));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (root, pairs) in &trees {
        for &(p, q) in pairs {
            let found = match lowest_common_ancestor(root, &leaf(p), &leaf(q)) {
                Some(node) => node.borrow().val as i64,
                None => -1,
            };
            total += found + 1;
            check = (check * 31 + found + 2) % 1000000007;
        }
    }
    println!("60 trees of 10000 nodes, 50 pairs each: answers sum to {}, checksum {}", total, check);
}
