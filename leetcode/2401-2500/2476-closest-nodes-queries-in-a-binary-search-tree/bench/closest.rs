// LeetCode #2476: Closest Nodes Queries in a Binary Search Tree -- the
// bench, the ★ arm in Rust: an in-order walk reads the values ascending,
// and a bisection by hand finds the first value at least each query. The
// nodes are LeetCode's `Rc<RefCell<TreeNode>>`.
use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;

type Node = Rc<RefCell<TreeNode>>;

struct TreeNode {
    val: i32,
    left: Option<Node>,
    right: Option<Node>,
}

fn walk(node: &Option<Node>, values: &mut Vec<i64>) {
    if let Some(n) = node {
        let n = n.borrow();
        walk(&n.left, values);
        values.push(n.val as i64);
        walk(&n.right, values);
    }
}

fn closest_nodes(root: &Option<Node>, queries: &[i64]) -> Vec<[i64; 2]> {
    let mut values = Vec::new();
    walk(root, &mut values);
    let mut answers = Vec::with_capacity(queries.len());
    for &q in queries {
        let (mut lo, mut hi) = (0, values.len());
        while lo < hi {
            let mid = (lo + hi) / 2;
            if values[mid] < q {
                lo = mid + 1;
            } else {
                hi = mid;
            }
        }
        let ceiling = if lo < values.len() { values[lo] } else { -1 };
        let floor = if lo < values.len() && values[lo] == q {
            q
        } else if lo > 0 {
            values[lo - 1]
        } else {
            -1
        };
        answers.push([floor, ceiling]);
    }
    answers
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v as i32, left: None, right: None }))
}

// the search tree of `n` distinct random values from 1 to 10^6, inserted
// in the order drawn
fn random_search_tree(n: usize, seed: &mut i64) -> Option<Node> {
    let mut used = HashSet::new();
    let mut root: Option<Node> = None;
    while used.len() < n {
        let v = 1 + wide_random(seed) % 1000000;
        if !used.insert(v) {
            continue;
        }
        let mut at = match &root {
            None => {
                root = Some(leaf(v));
                continue;
            }
            Some(r) => r.clone(),
        };
        loop {
            let go_left = v < at.borrow().val as i64;
            let child = if go_left { at.borrow().left.clone() } else { at.borrow().right.clone() };
            match child {
                Some(c) => at = c,
                None => {
                    if go_left {
                        at.borrow_mut().left = Some(leaf(v));
                    } else {
                        at.borrow_mut().right = Some(leaf(v));
                    }
                    break;
                }
            }
        }
    }
    root
}

fn main() {
    // 10 random search trees of 10^4 nodes built once; then 220 passes,
    // each asking every tree 1000 values stepped from the checksum so far,
    // folding every answer and the pass into the checksum
    let mut seed = 2476;
    let trees: Vec<Option<Node>> = (0..10).map(|_| random_search_tree(10000, &mut seed)).collect();
    let mut check = 0i64;
    for p in 0..220i64 {
        for root in trees.iter() {
            let queries: Vec<i64> = (0..1000).map(|i| 1 + (check + 997 * i) % 1000000).collect();
            for pair in closest_nodes(root, &queries) {
                check = (check * 31 + pair[0] + pair[1] + 2 + p) % 1000000007;
            }
        }
    }
    println!("220 passes over 10 trees of 10^4: checksum {check}");
}
