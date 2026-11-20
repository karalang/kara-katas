// LeetCode #1740: Find Distance in a Binary Tree -- the bench's Rust
// mirror: the ★ arm on one tree of 10000 nodes asked about 1000 pairs of
// values, all drawn first, each asked 4 times. Nodes are LeetCode's
// `Rc<RefCell<TreeNode>>`.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn find_distance(root: &Option<Node>, p: i32, q: i32) -> i32 {
    let ancestor = common(root, p, q);
    depth(&ancestor, p) + depth(&ancestor, q)
}

fn common(node: &Option<Node>, p: i32, q: i32) -> Option<Node> {
    let n = node.as_ref()?;
    let b = n.borrow();
    if b.val == p || b.val == q {
        return Some(n.clone());
    }
    match (common(&b.left, p, q), common(&b.right, p, q)) {
        (Some(_), Some(_)) => Some(n.clone()),
        (Some(l), None) => Some(l),
        (None, r) => r,
    }
}

fn depth(node: &Option<Node>, value: i32) -> i32 {
    let Some(n) = node else {
        return -1;
    };
    let b = n.borrow();
    if b.val == value {
        return 0;
    }
    let below = depth(&b.left, value).max(depth(&b.right, value));
    if below < 0 { -1 } else { below + 1 }
}

// ---- the harness ----------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, seed: &mut i64) -> Vec<Node> {
    let mut values: Vec<i32> = (0..n).map(|v| v as i32).collect();
    for i in (1..n).rev() {
        let j = next_random(seed) % (i + 1);
        values.swap(i as usize, j as usize);
    }
    let mut nodes: Vec<Node> = Vec::new();
    for i in 0..n {
        let node = Rc::new(RefCell::new(TreeNode { val: values[i as usize], left: None, right: None }));
        if i > 0 {
            let mut at = nodes[(next_random(seed) % i) as usize].clone();
            loop {
                let next = if next_random(seed) % 2 == 0 {
                    let child = at.borrow().left.clone();
                    match child {
                        Some(c) => c,
                        None => {
                            at.borrow_mut().left = Some(node.clone());
                            break;
                        }
                    }
                } else {
                    let child = at.borrow().right.clone();
                    match child {
                        Some(c) => c,
                        None => {
                            at.borrow_mut().right = Some(node.clone());
                            break;
                        }
                    }
                };
                at = next;
            }
        }
        nodes.push(node);
    }
    nodes
}

fn main() {
    let n: i64 = 10000;
    let queries = 1000;
    let rounds: i64 = 4;
    let mut seed: i64 = 1740;
    let nodes = random_tree(n, &mut seed);
    let root = Some(nodes[0].clone());
    let mut pairs: Vec<(i32, i32)> = Vec::new();
    for _ in 0..queries {
        let p = (next_random(&mut seed) % n) as i32;
        let q = (next_random(&mut seed) % n) as i32;
        pairs.push((p, q));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for &(p, q) in pairs.iter() {
            let found = find_distance(&root, p, q) as i64;
            total += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{} nodes, {} pairs, {} rounds: distances sum to {}, checksum {}", n, queries, rounds, total, check);
}
