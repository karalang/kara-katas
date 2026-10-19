// LeetCode 783 — Minimum Distance Between BST Nodes: the bench, in Rust.
// Mirrors min_diff_in_bst.kara: ancestor bounds over the same 64 trees.
use std::collections::HashSet;

struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn closest(node: &Option<Box<TreeNode>>, low: i64, high: i64) -> i64 {
    let Some(n) = node else {
        return i64::MAX;
    };
    let mut best = i64::MAX;
    if low != -1 {
        best = best.min(n.val - low);
    }
    if high != -1 {
        best = best.min(high - n.val);
    }
    best = best.min(closest(&n.left, low, n.val));
    best.min(closest(&n.right, n.val, high))
}

fn min_diff_in_bst(root: &Option<Box<TreeNode>>) -> i64 {
    closest(root, -1, -1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn insert(root: &mut Option<Box<TreeNode>>, v: i64) {
    let mut at = root;
    while let Some(n) = at {
        at = if v < n.val { &mut n.left } else { &mut n.right };
    }
    *at = Some(Box::new(TreeNode { val: v, left: None, right: None }));
}

fn middle_first(ordered: &[i64], lo: i64, hi: i64, out: &mut Vec<i64>) {
    if lo > hi {
        return;
    }
    let mid = (lo + hi) / 2;
    out.push(ordered[mid as usize]);
    middle_first(ordered, lo, mid - 1, out);
    middle_first(ordered, mid + 1, hi, out);
}

fn main() {
    let mut seed = 783;
    let mut trees: Vec<Option<Box<TreeNode>>> = Vec::new();
    for t in 0..64 {
        let mut taken = HashSet::new();
        let mut values: Vec<i64> = Vec::new();
        while values.len() < 100 {
            let hi = next_random(&mut seed);
            let v = (hi * 32768 + next_random(&mut seed)) % 100001;
            if taken.insert(v) {
                values.push(v);
            }
        }
        if t % 4 >= 2 {
            values.sort();
        }
        if t % 4 == 2 {
            let mut order = Vec::new();
            middle_first(&values, 0, 99, &mut order);
            values = order;
        }
        let mut root = None;
        for &v in &values {
            insert(&mut root, v);
        }
        trees.push(root);
    }
    let rounds: i64 = 2000000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let answer = min_diff_in_bst(&trees[(r % 64) as usize]);
        total += answer;
        check = (check * 31 + answer) % 1000000007;
    }
    println!("{rounds} rounds of 100-value trees: gaps sum to {total}, checksum {check}");
}
