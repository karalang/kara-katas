// Benchmark workload for LeetCode #101 — symmetric tree, Rust mirror.
// Box<Node> owned tree + &-borrow traversal (is_symmetric is read-only).
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
fn mirror(n: &Option<Box<Node>>) -> Option<Box<Node>> {
    n.as_ref().map(|node| Box::new(Node {
        val: node.val,
        left: mirror(&node.right),
        right: mirror(&node.left),
    }))
}
fn copy_tree(n: &Option<Box<Node>>) -> Option<Box<Node>> {
    n.as_ref().map(|node| Box::new(Node {
        val: node.val,
        left: copy_tree(&node.left),
        right: copy_tree(&node.right),
    }))
}
fn is_mirror(a: &Option<Box<Node>>, b: &Option<Box<Node>>) -> bool {
    match (a, b) {
        (None, None) => true,
        (Some(an), Some(bn)) => {
            an.val == bn.val && is_mirror(&an.left, &bn.right) && is_mirror(&an.right, &bn.left)
        }
        _ => false,
    }
}
fn is_symmetric(root: &Option<Box<Node>>) -> bool {
    match root {
        None => true,
        Some(n) => is_mirror(&n.left, &n.right),
    }
}
fn main() {
    let base: [i64; 15] = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15];
    let bn = base.len() as i64;
    let mut pool: Vec<Option<Box<Node>>> = Vec::new();
    for i in 0..8i64 {
        let mut sub: Option<Box<Node>> = None;
        for k in 0..bn {
            sub = insert(sub, base[((k + i) % bn) as usize]);
        }
        let other = if (i % 2) == 0 { mirror(&sub) } else { copy_tree(&sub) };
        let root = Some(Box::new(Node { val: 0, left: sub, right: other }));
        pool.push(root);
    }
    let mut acc: i64 = 1;
    for _ in 0..8_000_000 {
        let idx = (acc % 8) as usize;
        let sym = is_symmetric(&pool[idx]);
        acc = (acc * 131 + if sym { 1 } else { 0 } + 1) % MOD;
    }
    println!("{}", acc);
}
