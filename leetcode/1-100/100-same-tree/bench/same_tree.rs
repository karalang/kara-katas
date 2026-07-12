// Benchmark workload for LeetCode #100 — same tree, Rust mirror.
// Box<Node> owned tree + &-borrow traversal: is_same is read-only, so the natural
// Rust representation is a single-owner Box (no Rc/RefCell), traversed by reference.
const MOD: i64 = 1_000_000_007;

struct Node {
    val: i64,
    left: Option<Box<Node>>,
    right: Option<Box<Node>>,
}

fn insert(root: Option<Box<Node>>, v: i64) -> Option<Box<Node>> {
    match root {
        None => Some(Box::new(Node { val: v, left: None, right: None })),
        Some(mut n) => {
            if v < n.val {
                n.left = insert(n.left.take(), v);
            } else {
                n.right = insert(n.right.take(), v);
            }
            Some(n)
        }
    }
}
fn is_same(p: &Option<Box<Node>>, q: &Option<Box<Node>>) -> bool {
    match (p, q) {
        (None, None) => true,
        (Some(pn), Some(qn)) => {
            pn.val == qn.val && is_same(&pn.left, &qn.left) && is_same(&pn.right, &qn.right)
        }
        _ => false,
    }
}
fn main() {
    let base: [i64; 15] = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30];
    let bn = base.len() as i64;
    let mut pool_p: Vec<Option<Box<Node>>> = Vec::new();
    let mut pool_q: Vec<Option<Box<Node>>> = Vec::new();
    for i in 0..8i64 {
        let mut p: Option<Box<Node>> = None;
        let mut q: Option<Box<Node>> = None;
        for k in 0..bn {
            p = insert(p, base[k as usize]);
            let bump = if (i % 2) == 1 && k == (i % bn) { 1 } else { 0 };
            q = insert(q, base[k as usize] + bump);
        }
        pool_p.push(p);
        pool_q.push(q);
    }
    let mut acc: i64 = 1;
    for _ in 0..6_000_000 {
        let idx = (acc % 8) as usize;
        let same = is_same(&pool_p[idx], &pool_q[idx]);
        acc = (acc * 131 + if same { 1 } else { 0 } + 1) % MOD;
    }
    println!("{}", acc);
}
