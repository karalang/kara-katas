// Benchmark workload — Validate Binary Search Tree (LeetCode #98).
// Rust mirror of bench/validate_bst.kara. Each iteration builds a fresh 63-node
// balanced BST (Box per node), runs the ★'s recursive (lo,hi)-bounds validator,
// folds shift+valid into a rolling polynomial hash; the Box tree drops at end of
// iteration — the Rust analogue of Kāra's per-iteration RC build/validate/drop.
// Compiled with `rustc -O`. See ../README.md § Benchmarks.

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

// lo/hi are Option<i64> bounds (None = no bound on that side).
fn is_valid(node: &Option<Box<Node>>, lo: Option<i64>, hi: Option<i64>) -> bool {
    match node {
        None => true,
        Some(n) => {
            let v = n.val;
            if let Some(l) = lo {
                if v <= l {
                    return false;
                }
            }
            if let Some(h) = hi {
                if v >= h {
                    return false;
                }
            }
            is_valid(&n.left, lo, Some(v)) && is_valid(&n.right, Some(v), hi)
        }
    }
}

fn main() {
    let total: i64 = 200_000;
    let modulus: i64 = 1_000_000_007;
    let size: i64 = 63;

    let mut acc: i64 = 0;
    for k in 0..total {
        let shift = k % 1000;
        let root = build(0, size - 1, shift);
        let bit = if std::hint::black_box(is_valid(&root, None, None)) { 1 } else { 0 };
        acc = (acc * 131 + shift + bit) % modulus;
    }

    println!("{}", acc);
}
