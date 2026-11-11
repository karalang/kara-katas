// LeetCode #1120: Maximum Average Subtree -- the bench in Rust, the ★ arm
// over LeetCode's own `Rc<RefCell<TreeNode>>`, the same 16 trees and 200
// rounds.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn walk(node: &Option<Rc<RefCell<TreeNode>>>, best: &mut f64) -> (i64, i64) {
    let n = match node {
        None => return (0, 0),
        Some(n) => n.borrow(),
    };
    let (ls, lc) = walk(&n.left, best);
    let (rs, rc) = walk(&n.right, best);
    let sum = ls + rs + n.val as i64;
    let count = lc + rc + 1;
    let average = sum as f64 / count as f64;
    if average > *best {
        *best = average;
    }
    (sum, count)
}

fn maximum_average_subtree(root: &Option<Rc<RefCell<TreeNode>>>) -> f64 {
    let mut best = 0.0;
    walk(root, &mut best);
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i32 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    ((hi * 32768 + lo) % 100001) as i32
}

fn new_node(v: i32) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn random_tree(seed: &mut i64) -> Vec<Rc<RefCell<TreeNode>>> {
    let mut nodes = vec![new_node(random_value(seed))];
    for _ in 1..10000 {
        let c = new_node(random_value(seed));
        loop {
            let at = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
            let mut at = at.borrow_mut();
            if next_random(seed) % 2 == 0 {
                if at.left.is_none() {
                    at.left = Some(c.clone());
                    break;
                }
            } else if at.right.is_none() {
                at.right = Some(c.clone());
                break;
            }
        }
        nodes.push(c);
    }
    nodes
}

fn main() {
    let mut seed = 1120;
    let trees: Vec<Vec<Rc<RefCell<TreeNode>>>> = (0..16).map(|_| random_tree(&mut seed)).collect();
    let mut total = 0.0;
    let mut check: i64 = 0;
    for round in 0..200i64 {
        for j in 0..trees.len() {
            let at = ((round * 7919 + j as i64 * 104729) % 10000) as usize;
            {
                let mut n = trees[j][at].borrow_mut();
                n.val = ((n.val as i64 * 7 + round) % 100001) as i32;
            }
            let answer = maximum_average_subtree(&Some(trees[j][0].clone()));
            total += answer;
            check = (check * 31 + (answer * 1000.0) as i64) % 1000000007;
        }
    }
    println!("200 rounds over 16 trees of 10^4 nodes: answers total {:.3}, checksum {}", total, check);
}
