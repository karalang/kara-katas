// Benchmark workload for LeetCode #99 — recover BST, Rust mirror.
// Rc<RefCell<Node>> matches Kara's `shared struct TreeNode` (reference-counted,
// interior-mutable) so the collect-nodes-then-mutate-values shape is the same.
use std::cell::RefCell;
use std::rc::Rc;

const MOD: i64 = 1_000_000_007;

type Link = Option<Rc<RefCell<Node>>>;

struct Node {
    val: i64,
    left: Link,
    right: Link,
}

fn insert(root: Link, v: i64) -> Link {
    match root {
        None => Some(Rc::new(RefCell::new(Node { val: v, left: None, right: None }))),
        Some(n) => {
            if v < n.borrow().val {
                let l = n.borrow_mut().left.take();
                n.borrow_mut().left = insert(l, v);
            } else {
                let r = n.borrow_mut().right.take();
                n.borrow_mut().right = insert(r, v);
            }
            Some(n)
        }
    }
}
fn collect(node: &Link, out: &mut Vec<Rc<RefCell<Node>>>) {
    if let Some(n) = node {
        collect(&n.borrow().left, out);
        out.push(n.clone());
        collect(&n.borrow().right, out);
    }
}
fn sum_inorder(node: &Link, acc: &mut i64) {
    if let Some(n) = node {
        sum_inorder(&n.borrow().left, acc);
        *acc = (*acc * 131 + n.borrow().val) % MOD;
        sum_inorder(&n.borrow().right, acc);
    }
}
fn recover(root: &Link) {
    let mut nodes: Vec<Rc<RefCell<Node>>> = Vec::new();
    collect(root, &mut nodes);
    let (mut fi, mut si): (i64, i64) = (-1, -1);
    for i in 1..nodes.len() as i64 {
        if nodes[(i - 1) as usize].borrow().val > nodes[i as usize].borrow().val {
            if fi < 0 {
                fi = i - 1;
            }
            si = i;
        }
    }
    if fi >= 0 {
        let t = nodes[fi as usize].borrow().val;
        let s = nodes[si as usize].borrow().val;
        nodes[fi as usize].borrow_mut().val = s;
        nodes[si as usize].borrow_mut().val = t;
    }
}
fn corrupt2(root: &Link, a: i64, b: i64) {
    let mut ns: Vec<Rc<RefCell<Node>>> = Vec::new();
    collect(root, &mut ns);
    if a != b {
        let t = ns[a as usize].borrow().val;
        let s = ns[b as usize].borrow().val;
        ns[a as usize].borrow_mut().val = s;
        ns[b as usize].borrow_mut().val = t;
    }
}
fn main() {
    let vals: [i64; 31] = [16, 8, 24, 4, 12, 20, 28, 2, 6, 10, 14, 18, 22, 26, 30, 1, 3, 5, 7, 9, 11, 13, 15, 17, 19, 21, 23, 25, 27, 29, 31];
    let n: i64 = 31;
    let mut root: Link = None;
    for v in vals {
        root = insert(root, v);
    }
    let mut acc: i64 = 1;
    for _ in 0..700_000 {
        let a = acc % n;
        let b = (acc * 7 + 3) % n;
        corrupt2(&root, a, b);
        let mut cs: i64 = 0;
        sum_inorder(&root, &mut cs);
        acc = (acc * 131 + cs) % MOD;
        recover(&root);
    }
    println!("{}", acc);
}
