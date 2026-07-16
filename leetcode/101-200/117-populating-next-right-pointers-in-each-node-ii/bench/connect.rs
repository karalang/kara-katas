// LeetCode #117 — Rust mirror, O(1)-space next-pointer population on an arbitrary tree.
// Rc<RefCell<Node>> — the *safe* interior-mutability peer to Kara's `shared` (RC); the `next`/`left`
// /`right` handles are rewritten in place, so RefCell is the honest safe-Rust counterpart (an unsafe
// raw-pointer Rust would match C). Same algorithm + workload as connect.kara: ~500-node BST (fixed
// shape, data-dependent value base), dummy-head + tail threading, K = 16000. Kara checks integer
// overflow by default, so the like-for-like row is `rustc -O -C overflow-checks=on`.
use std::cell::RefCell;
use std::rc::Rc;

const MOD: i64 = 1000000007;

struct Node {
    val: i64,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
    next: Option<Rc<RefCell<Node>>>,
}

type Link = Option<Rc<RefCell<Node>>>;

fn new_node(v: i64) -> Rc<RefCell<Node>> {
    Rc::new(RefCell::new(Node {
        val: v,
        left: None,
        right: None,
        next: None,
    }))
}

fn insert(root: Link, v: i64) -> Link {
    match root {
        None => Some(new_node(v)),
        Some(n) => {
            if v < n.borrow().val {
                let l = n.borrow().left.clone();
                n.borrow_mut().left = insert(l, v);
            } else {
                let r = n.borrow().right.clone();
                n.borrow_mut().right = insert(r, v);
            }
            Some(n)
        }
    }
}

fn build_bst(count: i64, base: i64) -> Link {
    let mut root: Link = None;
    let mut s: i64 = 88172645;
    for _ in 0..count {
        s = (s * 1103515245 + 12345) % 2147483648;
        root = insert(root, (s % 100000) + base);
    }
    root
}

fn connect(root: &Link) {
    let mut leftmost = root.clone();
    while leftmost.is_some() {
        let dummy = new_node(0);
        let mut tail = dummy.clone();
        let mut cur = leftmost.clone();
        while let Some(c) = cur.clone() {
            let l = c.borrow().left.clone();
            if let Some(l) = l {
                tail.borrow_mut().next = Some(l.clone());
                tail = l;
            }
            let r = c.borrow().right.clone();
            if let Some(r) = r {
                tail.borrow_mut().next = Some(r.clone());
                tail = r;
            }
            cur = c.borrow().next.clone();
        }
        leftmost = dummy.borrow().next.clone();
    }
}

fn level_hash(root: &Link) -> i64 {
    let mut h: i64 = 1;
    let mut head = root.clone();
    while let Some(hd) = head.clone() {
        let mut cur = Some(hd.clone());
        while let Some(c) = cur.clone() {
            h = (h * 131 + c.borrow().val + 1) % MOD;
            cur = c.borrow().next.clone();
        }
        h = (h * 31 + 7) % MOD;
        let mut nh: Link = None;
        let mut scan = Some(hd.clone());
        while let Some(s) = scan.clone() {
            let l = s.borrow().left.clone();
            if l.is_some() {
                nh = l;
                break;
            }
            let r = s.borrow().right.clone();
            if r.is_some() {
                nh = r;
                break;
            }
            scan = s.borrow().next.clone();
        }
        head = nh;
    }
    h
}

fn main() {
    let mut acc: i64 = 0;
    for _ in 0..16000 {
        let base = acc % 100;
        let root = build_bst(500, base);
        connect(&root);
        let h = level_hash(&root);
        acc = (acc * 131 + h) % MOD;
    }
    println!("{}", acc);
}
