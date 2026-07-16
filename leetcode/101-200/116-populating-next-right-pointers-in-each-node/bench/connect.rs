// LeetCode #116 — Rust mirror, O(1)-space next-pointer population.
// Rc<RefCell<Node>> — the *safe* interior-mutability peer to Kara's `shared` (RC): the `next`/`left`
// /`right` handles are rewritten in place, so RefCell is the honest safe-Rust counterpart (an unsafe
// raw-pointer Rust would match C). Same algorithm + workload as connect.kara: depth-9 perfect tree,
// data-dependent base, K = 40000. Kara checks integer overflow by default, so the like-for-like row
// is `rustc -O -C overflow-checks=on`.
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

fn build_perfect(idx: i64, max_idx: i64, base: i64) -> Link {
    if idx > max_idx {
        return None;
    }
    let node = Rc::new(RefCell::new(Node {
        val: idx + base,
        left: None,
        right: None,
        next: None,
    }));
    let l = build_perfect(2 * idx, max_idx, base);
    let r = build_perfect(2 * idx + 1, max_idx, base);
    node.borrow_mut().left = l;
    node.borrow_mut().right = r;
    Some(node)
}

fn connect(root: &Link) {
    let mut leftmost = root.clone();
    while let Some(lm) = leftmost.clone() {
        if lm.borrow().left.is_none() {
            break;
        }
        let mut head = Some(lm.clone());
        while let Some(h) = head.clone() {
            let right = h.borrow().right.clone();
            if let Some(l) = h.borrow().left.clone() {
                l.borrow_mut().next = right.clone();
            }
            let hnext = h.borrow().next.clone();
            if let (Some(r), Some(hn)) = (right, hnext.clone()) {
                r.borrow_mut().next = hn.borrow().left.clone();
            }
            head = hnext;
        }
        leftmost = lm.borrow().left.clone();
    }
}

fn level_hash(root: &Link) -> i64 {
    let mut h: i64 = 1;
    let mut leftmost = root.clone();
    while let Some(lm) = leftmost.clone() {
        let mut cur = Some(lm.clone());
        while let Some(c) = cur.clone() {
            h = (h * 131 + c.borrow().val + 1) % MOD;
            cur = c.borrow().next.clone();
        }
        h = (h * 31 + 7) % MOD;
        leftmost = lm.borrow().left.clone();
    }
    h
}

fn main() {
    let max_idx: i64 = 511; // depth-9 perfect tree
    let mut acc: i64 = 0;
    for _ in 0..40000 {
        let base = acc % 100;
        let root = build_perfect(1, max_idx, base);
        connect(&root);
        let h = level_hash(&root);
        acc = (acc * 131 + h) % MOD;
        // root dropped here — Rc refcounts fall to zero, tree freed.
    }
    println!("{}", acc);
}
