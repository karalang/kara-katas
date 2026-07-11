// LeetCode #95: Unique Binary Search Trees II — recursive divide & conquer.
// Rust mirror of generate_trees.kara. Same algorithm: for each root value i in
// [lo, hi], cross-product every left subtree (lo..i-1) with every right subtree
// (i+1..hi). Kara shares subtree instances via RC; this uses single-owner
// `Box<Node>` and clones each (left, right) pair into the new root — the same
// set of trees, the same canonical preorder serialization and fold, so stdout
// is byte-identical.
const MOD: i64 = 1_000_000_007;

#[derive(Clone)]
struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

// Every BST over the contiguous value range [lo, hi].
fn build_all(lo: i64, hi: i64) -> Vec<Option<Box<Node>>> {
    let mut result: Vec<Option<Box<Node>>> = Vec::new();
    if lo > hi {
        result.push(None);
        return result;
    }
    for i in lo..=hi {
        let lefts = build_all(lo, i - 1);
        let rights = build_all(i + 1, hi);
        for l in &lefts {
            for r in &rights {
                result.push(Some(Box::new(Node {
                    val: i,
                    left: l.clone(),
                    right: r.clone(),
                })));
            }
        }
    }
    result
}

// Canonical preorder serialization with '#' null markers, appended to out.
fn serialize(node: &Option<Box<Node>>, out: &mut String) {
    match node {
        None => out.push_str("#,"),
        Some(n) => {
            out.push_str(&format!("{},", n.val));
            serialize(&n.left, out);
            serialize(&n.right, out);
        }
    }
}

// Benchmark workload: 250 repeats of building every BST over 1..8, folding each
// tree's canonical preorder serialization into a rolling hash. See ../README.md.
fn bench_report(n: i64, acc: &mut i64) {
    let trees = build_all(1, n);
    let count = trees.len() as i64;
    let mut a = (*acc * 131 + (count + 1)) % MOD;
    for tree in &trees {
        let mut s = String::new();
        serialize(tree, &mut s);
        for b in s.bytes() {
            a = (a * 131 + b as i64) % MOD;
        }
        a = (a * 131 + 7) % MOD;
    }
    *acc = a;
}

fn main() {
    let mut acc: i64 = 0;
    for _ in 0..250 {
        for n in 1..=8 {
            bench_report(n, &mut acc);
        }
    }
    println!("{}", acc);
}
