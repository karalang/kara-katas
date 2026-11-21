// LeetCode #2471: Minimum Number of Operations to Sort a Binary Tree by
// Level -- the bench, the ★ arm in Rust: the levels by a breadth-first
// walk, and in each the cycles of the permutation that sorts it, a
// `HashMap` from each value to its sorted place. The nodes are LeetCode's
// `Rc<RefCell<TreeNode>>`.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

type Node = Rc<RefCell<TreeNode>>;

struct TreeNode {
    val: i32,
    left: Option<Node>,
    right: Option<Node>,
}

fn minimum_operations(root: Option<Node>) -> i64 {
    let mut total = 0i64;
    let mut level: Vec<Node> = Vec::new();
    if let Some(r) = root {
        level.push(r);
    }
    while !level.is_empty() {
        let values: Vec<i64> = level.iter().map(|n| n.borrow().val as i64).collect();
        let mut sorted = values.clone();
        sorted.sort();
        let mut target: HashMap<i64, usize> = HashMap::new();
        for (i, &v) in sorted.iter().enumerate() {
            target.insert(v, i);
        }
        let mut seen = vec![false; values.len()];
        for i in 0..values.len() {
            let mut length = 0i64;
            let mut at = i;
            while !seen[at] {
                seen[at] = true;
                at = target[&values[at]];
                length += 1;
            }
            if length > 1 {
                total += length - 1;
            }
        }
        let mut next: Vec<Node> = Vec::new();
        for n in level.iter() {
            let n = n.borrow();
            if let Some(c) = &n.left {
                next.push(c.clone());
            }
            if let Some(c) = &n.right {
                next.push(c.clone());
            }
        }
        level = next;
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

// the nodes of a random tree, the root first: the values 1 to `n` in a
// random order, each node after the first hung below a random earlier
// one, a random side taken down from it until a free one is found
fn random_tree(n: usize, seed: &mut i64) -> Vec<Node> {
    let mut values: Vec<i32> = (1..=n as i32).collect();
    for i in (1..n).rev() {
        let j = (wide(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let nodes: Vec<Node> =
        values.iter().map(|&v| Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))).collect();
    for k in 1..n {
        let mut at = nodes[(wide(seed) % k as i64) as usize].clone();
        loop {
            if next_random(seed) % 2 == 0 {
                let child = at.borrow().left.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().left = Some(nodes[k].clone());
                        break;
                    }
                }
            } else {
                let child = at.borrow().right.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().right = Some(nodes[k].clone());
                        break;
                    }
                }
            }
        }
    }
    nodes
}

fn main() {
    // 20 random trees of 10^4 nodes built once; then 110 passes, each
    // answering every tree, folding the count plus the pass into the
    // checksum, then swapping two of its values chosen by the checksum
    let n = 10000i64;
    let mut seed = 2471;
    let trees: Vec<Vec<Node>> = (0..20).map(|_| random_tree(n as usize, &mut seed)).collect();
    let mut check = 0i64;
    for p in 0..110i64 {
        for nodes in trees.iter() {
            check = (check * 31 + minimum_operations(Some(nodes[0].clone())) + p) % 1000000007;
            let a = nodes[(check % n) as usize].clone();
            let b = nodes[((check / n + p) % n) as usize].clone();
            let first = a.borrow().val;
            let second = b.borrow().val;
            a.borrow_mut().val = second;
            b.borrow_mut().val = first;
        }
    }
    println!("110 passes over 20 trees of 10^4: checksum {check}");
}
