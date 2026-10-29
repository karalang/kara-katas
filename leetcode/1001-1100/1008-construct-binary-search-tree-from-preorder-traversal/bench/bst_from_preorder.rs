// LeetCode #1008 bench: the ★ arm (recursion with an upper bound) over 50
// preorders of 100 values, drawn once; each of 4000 rounds builds every
// tree, starting from a different preorder, and folds it into a checksum.
// The tree is LeetCode's Rust shape, Rc<RefCell<TreeNode>>, the
// counterpart of Kāra's reference-counted `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn bst_from_preorder(preorder: &[i64]) -> Option<Rc<RefCell<TreeNode>>> {
    let mut next = 0;
    build(preorder, &mut next, i64::MAX)
}

fn build(preorder: &[i64], next: &mut usize, bound: i64) -> Option<Rc<RefCell<TreeNode>>> {
    if *next == preorder.len() || preorder[*next] >= bound {
        return None;
    }
    let val = preorder[*next];
    *next += 1;
    let left = build(preorder, next, val);
    let right = build(preorder, next, bound);
    Some(Rc::new(RefCell::new(TreeNode { val, left, right })))
}

fn fold(node: &Option<Rc<RefCell<TreeNode>>>, depth: i64) -> i64 {
    match node {
        Some(n) => {
            let n = n.borrow();
            (n.val * depth + fold(&n.left, depth + 1) * 3 + fold(&n.right, depth + 1) * 7) % 1000000007
        }
        None => 0,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_preorder(n: usize, most: i64, seed: &mut i64) -> Vec<i64> {
    let mut seen = vec![false; most as usize + 1];
    let mut vals: Vec<i64> = Vec::new();
    let mut left: Vec<i64> = Vec::new();
    let mut right: Vec<i64> = Vec::new();
    while vals.len() < n {
        let v = 1 + next_random(seed) % most;
        if seen[v as usize] {
            continue;
        }
        seen[v as usize] = true;
        vals.push(v);
        left.push(-1);
        right.push(-1);
        let me = (vals.len() - 1) as i64;
        if me > 0 {
            let mut at = 0usize;
            loop {
                if v < vals[at] {
                    if left[at] == -1 {
                        left[at] = me;
                        break;
                    }
                    at = left[at] as usize;
                } else {
                    if right[at] == -1 {
                        right[at] = me;
                        break;
                    }
                    at = right[at] as usize;
                }
            }
        }
    }
    let mut out = Vec::new();
    let mut stack = vec![0usize];
    while let Some(at) = stack.pop() {
        out.push(vals[at]);
        if right[at] != -1 {
            stack.push(right[at] as usize);
        }
        if left[at] != -1 {
            stack.push(left[at] as usize);
        }
    }
    out
}

fn main() {
    let count = 50;
    let rounds = 4000;
    let mut seed = 1008;
    let preorders: Vec<Vec<i64>> = (0..count).map(|_| random_preorder(100, 1000, &mut seed)).collect();
    let mut check: i64 = 0;
    for r in 0..rounds {
        for k in 0..count {
            let tree = bst_from_preorder(&preorders[(r + k) % count]);
            check = (check * 31 + fold(&tree, 1)) % 1000000007;
        }
    }
    println!("{} rounds over {} preorders of 100 values: checksum {}", rounds, count, check);
}
