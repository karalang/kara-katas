// LeetCode #1676: Lowest Common Ancestor of a Binary Tree IV -- the bench's
// Rust mirror: the ★ arm on one tree of 10000 nodes asked about 500 sets
// of 1 to 50 nodes, all drawn first, each asked 10 times. Nodes are
// LeetCode's `Rc<RefCell<TreeNode>>`, the values a `HashSet`.

use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn lowest_common_ancestor(root: &Option<Node>, nodes: &[Node]) -> Option<Node> {
    let wanted: HashSet<i32> = nodes.iter().map(|n| n.borrow().val).collect();
    search(root, &wanted)
}

fn search(node: &Option<Node>, wanted: &HashSet<i32>) -> Option<Node> {
    let n = node.as_ref()?;
    let b = n.borrow();
    if wanted.contains(&b.val) {
        return Some(n.clone());
    }
    match (search(&b.left, wanted), search(&b.right, wanted)) {
        (Some(_), Some(_)) => Some(n.clone()),
        (Some(l), None) => Some(l),
        (None, r) => r,
    }
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
    let queries = 500;
    let rounds: i64 = 10;
    let mut seed: i64 = 1676;
    let mut nodes = random_tree(n, &mut seed);
    let root = Some(nodes[0].clone());
    let mut sets: Vec<Vec<Node>> = Vec::new();
    for _ in 0..queries {
        let k = next_random(&mut seed) % 50 + 1;
        for i in 0..k {
            let j = i + next_random(&mut seed) % (n - i);
            nodes.swap(i as usize, j as usize);
        }
        sets.push(nodes[..k as usize].to_vec());
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for set in &sets {
            let found = lowest_common_ancestor(&root, set).unwrap().borrow().val as i64;
            total += found;
            check = (check * 31 + found + r) % 1000000007;
        }
    }
    println!("{} nodes, {} sets, {} rounds: answers sum to {}, checksum {}", n, queries, rounds, total, check);
}
