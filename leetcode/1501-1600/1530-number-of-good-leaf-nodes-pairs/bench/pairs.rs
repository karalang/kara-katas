// LeetCode #1530: Number of Good Leaf Nodes Pairs -- bench: the ★ arm
// over 1000 random trees of 1 to 1024 nodes, built once and answered 10
// times, each with its own distance from 1 to 10. The tree is LeetCode's
// `Option<Rc<RefCell<TreeNode>>>`.

use std::cell::RefCell;
use std::rc::Rc;

pub struct TreeNode {
    pub val: i64,
    pub left: Option<Rc<RefCell<TreeNode>>>,
    pub right: Option<Rc<RefCell<TreeNode>>>,
}

fn leaves_below(node: &Option<Rc<RefCell<TreeNode>>>, distance: usize, pairs: &mut i64) -> Vec<i64> {
    let mut counts = vec![0i64; distance];
    if let Some(n) = node {
        let n = n.borrow();
        if n.left.is_none() && n.right.is_none() {
            counts[0] = 1;
        } else {
            let l = leaves_below(&n.left, distance, pairs);
            let r = leaves_below(&n.right, distance, pairs);
            for i in 0..distance {
                for j in 0..(distance - i - 1) {
                    *pairs += l[i] * r[j];
                }
            }
            for i in 0..distance - 1 {
                counts[i + 1] = l[i] + r[i];
            }
        }
    }
    counts
}

fn count_pairs(root: &Option<Rc<RefCell<TreeNode>>>, distance: i64) -> i64 {
    let mut pairs = 0;
    leaves_below(root, distance as usize, &mut pairs);
    pairs
}

fn make(at: i64, vals: &[i64], left: &[i64], right: &[i64]) -> Option<Rc<RefCell<TreeNode>>> {
    if at < 0 {
        return None;
    }
    let a = at as usize;
    Some(Rc::new(RefCell::new(TreeNode {
        val: vals[a],
        left: make(left[a], vals, left, right),
        right: make(right[a], vals, left, right),
    })))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn random_tree(most: i64, seed: &mut i64) -> Option<Rc<RefCell<TreeNode>>> {
    let n = next_random(seed) % most + 1;
    let mut vals = Vec::new();
    let mut left: Vec<i64> = Vec::new();
    let mut right: Vec<i64> = Vec::new();
    for i in 0..n {
        vals.push(next_random(seed) % 100 + 1);
        left.push(-1);
        right.push(-1);
        if i > 0 {
            let mut at = (next_random(seed) % i) as usize;
            loop {
                if next_random(seed) % 2 == 0 {
                    if left[at] < 0 {
                        left[at] = i;
                        break;
                    }
                    at = left[at] as usize;
                } else {
                    if right[at] < 0 {
                        right[at] = i;
                        break;
                    }
                    at = right[at] as usize;
                }
            }
        }
    }
    make(0, &vals, &left, &right)
}

fn main() {
    let mut seed = 1530;
    let mut trees = Vec::new();
    for _ in 0..1000 {
        let root = random_tree(1024, &mut seed);
        let distance = next_random(&mut seed) % 10 + 1;
        trees.push((root, distance));
    }
    let mut check = 0;
    for _ in 0..10 {
        for (root, distance) in trees.iter() {
            check = mix(check, count_pairs(root, *distance));
        }
    }
    println!("10 passes over 1000 trees of up to 1024 nodes: checksum {}", check);
}
