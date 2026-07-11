// Benchmark workload — Binary Tree Inorder Traversal (LeetCode #94).
// Rust mirror of bench/inorder.kara. Each of K=320,000 iterations builds a fresh 63-node
// balanced tree (Box per node), folds a recursive inorder walk into a rolling hash in
// visit order; the Box tree drops at end of iteration — the Rust analogue of Kāra's
// per-iteration RC build/traverse/drop. The tree is read-only during traversal (no
// aliasing, no mutation), so single-owner Box is the honest node — same choice as the
// sibling tree kata #98. Compiled with `rustc -O`. See ../README.md § Benchmarks.

struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn build(lo: i64, hi: i64, shift: i64) -> Option<Box<Node>> {
    if lo > hi {
        return None;
    }
    let mid = lo + (hi - lo) / 2;
    Some(Box::new(Node {
        val: shift + mid,
        left: build(lo, mid - 1, shift),
        right: build(mid + 1, hi, shift),
    }))
}

fn inorder_fold(node: &Option<Box<Node>>, acc: &mut i64) {
    if let Some(n) = node {
        inorder_fold(&n.left, acc);
        *acc = (*acc * 131 + (n.val + 1)) % 1_000_000_007;
        inorder_fold(&n.right, acc);
    }
}

fn main() {
    const TOTAL: i64 = 320_000;
    const MODULUS: i64 = 1_000_000_007;
    const SIZE: i64 = 63;
    let mut sum = 0i64;
    for k in 0..TOTAL {
        let shift = k % 1000;
        let root = build(0, SIZE - 1, shift);
        let mut acc = 0i64;
        inorder_fold(&root, &mut acc);
        sum = (sum * 131 + acc) % MODULUS;
    }
    println!("{}", sum);
}
