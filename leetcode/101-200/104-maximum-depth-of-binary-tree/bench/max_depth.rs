// Benchmark workload for LeetCode #104 — max depth, Rust mirror (Box + &-borrow).
// The tree is never mutated or shared during traversal, so a single-owner Box walked by
// reference is the honest Rust node. Build 8 BSTs once, then K reps of recursive max_depth
// on a data-dependent-selected tree, folding each depth into a rolling hash. Read-only.
const MOD: i64 = 1000000007;

struct Node { val: i64, left: Option<Box<Node>>, right: Option<Box<Node>> }

fn insert(root: Option<Box<Node>>, v: i64) -> Option<Box<Node>> {
    match root {
        None => Some(Box::new(Node { val: v, left: None, right: None })),
        Some(mut n) => {
            if v < n.val { n.left = insert(n.left.take(), v); }
            else { n.right = insert(n.right.take(), v); }
            Some(n)
        }
    }
}
fn max_depth(node: &Option<Box<Node>>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let lh = max_depth(&n.left);
            let rh = max_depth(&n.right);
            1 + if lh > rh { lh } else { rh }
        }
    }
}

fn main() {
    let base: [i64; 15] = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30];
    let bn = base.len();
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for t in 0..8 {
        let mut root: Option<Box<Node>> = None;
        for k in 0..bn { root = insert(root, base[(k + t) % bn]); }
        pool.push(root);
    }
    let mut acc: i64 = 1;
    for _ in 0..4000000i64 {
        let idx = (acc % 8) as usize;
        let d = max_depth(&pool[idx]);
        acc = (acc * 131 + d + 1) % MOD;
    }
    println!("{}", acc);
}
