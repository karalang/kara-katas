// LeetCode #1214: Two Sum BSTs -- the bench in Rust, the ★ arm over
// LeetCode's own `Rc<RefCell<TreeNode>>`, the same 16 pairs of trees and
// 10 rounds.
use std::cell::RefCell;
use std::collections::BTreeSet;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn in_order(node: &Option<Rc<RefCell<TreeNode>>>, out: &mut Vec<i32>) {
    if let Some(n) = node {
        let n = n.borrow();
        in_order(&n.left, out);
        out.push(n.val);
        in_order(&n.right, out);
    }
}

fn two_sum_bsts(root1: &Option<Rc<RefCell<TreeNode>>>, root2: &Option<Rc<RefCell<TreeNode>>>, target: i32) -> bool {
    let mut a = Vec::new();
    let mut b = Vec::new();
    in_order(root1, &mut a);
    in_order(root2, &mut b);
    let mut i = 0usize;
    let mut j = b.len() as i64 - 1;
    while i < a.len() && j >= 0 {
        let sum = a[i] + b[j as usize];
        if sum == target {
            return true;
        }
        if sum < target {
            i += 1;
        } else {
            j -= 1;
        }
    }
    false
}

fn balanced(sorted: &[i32], low: usize, high: usize) -> Option<Rc<RefCell<TreeNode>>> {
    if low >= high {
        return None;
    }
    let mid = (low + high) / 2;
    Some(Rc::new(RefCell::new(TreeNode {
        val: sorted[mid],
        left: balanced(sorted, low, mid),
        right: balanced(sorted, mid + 1, high),
    })))
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    (hi * 32768 + lo) % 2000000001 - 1000000000
}

fn distinct_values(seed: &mut i64, n: usize) -> Vec<i32> {
    let mut seen = BTreeSet::new();
    while seen.len() < n {
        seen.insert(big(seed));
    }
    seen.iter().map(|&v| v as i32).collect()
}

type Tree = Option<Rc<RefCell<TreeNode>>>;

fn main() {
    let mut seed = 1214;
    let mut pairs: Vec<(Tree, Tree, Vec<i32>)> = Vec::new();
    for _ in 0..16 {
        let a = distinct_values(&mut seed, 5000);
        let b = distinct_values(&mut seed, 5000);
        let i = (next_random(&mut seed) % 5000) as usize;
        let j = (next_random(&mut seed) % 5000) as usize;
        let t3 = big(&mut seed) as i32;
        let t4 = big(&mut seed) as i32;
        let targets = vec![a[i] + b[j], a[j] + b[i], t3, t4];
        pairs.push((balanced(&a, 0, 5000), balanced(&b, 0, 5000), targets));
    }
    let mut check: i64 = 0;
    for round in 0..10i64 {
        for (t1, t2, targets) in pairs.iter() {
            for &t in targets.iter() {
                let answer = if two_sum_bsts(t1, t2, t) { 2 } else { 1 };
                check = (check * 131 + answer + round) % 1000000007;
            }
        }
    }
    println!("10 rounds over 16 pairs of 5000-node trees: checksum {}", check);
}
