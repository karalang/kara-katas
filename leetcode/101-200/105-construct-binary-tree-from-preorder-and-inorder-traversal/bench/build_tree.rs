// Benchmark workload for LeetCode #103 — construct binary tree, Rust mirror (Box).
// The tree is single-owner (built then dropped, never shared), so Box is the honest Rust
// node. Build 8 (preorder, inorder) input pairs once, then K reps of the recursive
// index-bounds reconstruction on a data-dependent-selected pair, folding the rebuilt tree's
// serialization into a rolling hash. Each rep allocates a fresh 15-node tree and drops it.
// Linear inorder scan (O(n^2)) for parity.
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
fn find_in(inorder: &[i64], lo: i64, hi: i64, target: i64) -> i64 {
    let mut i = lo;
    while i <= hi { if inorder[i as usize] == target { return i; } i += 1; }
    -1
}
fn build(pre: &[i64], ino: &[i64], plo: i64, phi: i64, ilo: i64, ihi: i64) -> Option<Box<Node>> {
    if plo > phi { return None; }
    let rv = pre[plo as usize];
    let mid = find_in(ino, ilo, ihi, rv);
    let lsize = mid - ilo;
    Some(Box::new(Node {
        val: rv,
        left: build(pre, ino, plo + 1, plo + lsize, ilo, mid - 1),
        right: build(pre, ino, plo + lsize + 1, phi, mid + 1, ihi),
    }))
}
fn ser(node: &Option<Box<Node>>, acc: i64) -> i64 {
    match node {
        None => (acc * 131 + 1) % MOD,
        Some(n) => {
            let mut a = (acc * 131 + (n.val + 2)) % MOD;
            a = ser(&n.left, a);
            a = ser(&n.right, a);
            a
        }
    }
}
fn preorder_of(node: &Option<Box<Node>>, out: &mut Vec<i64>) {
    if let Some(n) = node { out.push(n.val); preorder_of(&n.left, out); preorder_of(&n.right, out); }
}
fn inorder_of(node: &Option<Box<Node>>, out: &mut Vec<i64>) {
    if let Some(n) = node { inorder_of(&n.left, out); out.push(n.val); inorder_of(&n.right, out); }
}

fn main() {
    let base: [i64; 15] = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15];
    let bn = base.len();
    let mut pres: Vec<Vec<i64>> = Vec::new();
    let mut inos: Vec<Vec<i64>> = Vec::new();
    for t in 0..8 {
        let mut root: Option<Box<Node>> = None;
        for k in 0..bn { root = insert(root, base[(k + t) % bn]); }
        let (mut pre, mut ino) = (Vec::new(), Vec::new());
        preorder_of(&root, &mut pre);
        inorder_of(&root, &mut ino);
        pres.push(pre);
        inos.push(ino);
    }
    let mut acc: i64 = 1;
    for _ in 0..800000i64 {
        let idx = (acc % 8) as usize;
        let rebuilt = build(&pres[idx], &inos[idx], 0, (bn - 1) as i64, 0, (bn - 1) as i64);
        let s = ser(&rebuilt, 0);
        acc = (acc * 131 + s) % MOD;
    }
    println!("{}", acc);
}
