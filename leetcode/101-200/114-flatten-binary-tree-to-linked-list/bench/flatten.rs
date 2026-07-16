// LeetCode #114 bench — flatten, Rust mirror (Rc<RefCell> — the safe RC interior-mutability peer to
// Kara's `shared`; Kara `shared` is RC without RefCell's dynamic borrow flag).
use std::rc::Rc;
use std::cell::RefCell;
const MOD: i64 = 1000000007;
type Link = Option<Rc<RefCell<Node>>>;
struct Node { val: i64, left: Link, right: Link }
fn build_balanced(lo: i64, hi: i64) -> Link {
    if lo > hi { return None; }
    let mid = (lo + hi) / 2;
    Some(Rc::new(RefCell::new(Node { val: mid, left: build_balanced(lo, mid - 1), right: build_balanced(mid + 1, hi) })))
}
fn flatten(root: &Link) {
    let mut curr = root.clone();
    while let Some(c) = curr {
        let left = c.borrow().left.clone();
        if let Some(l) = left {
            let mut prev = l;
            loop {
                let nxt = prev.borrow().right.clone();
                match nxt { Some(r) => prev = r, None => break }
            }
            prev.borrow_mut().right = c.borrow().right.clone();
            let lft = c.borrow().left.clone();
            c.borrow_mut().right = lft;
            c.borrow_mut().left = None;
        }
        let nx = c.borrow().right.clone();
        curr = nx;
    }
}
fn spine_hash(root: &Link) -> i64 {
    let mut h: i64 = 1;
    let mut cur = root.clone();
    while let Some(c) = cur {
        h = (h * 131 + c.borrow().val + 1000) % MOD;
        let nx = c.borrow().right.clone();
        cur = nx;
    }
    h
}
fn main() {
    let mut acc: i64 = 1;
    for _ in 0..200000i64 {
        let base = acc % 100;
        let root = build_balanced(base, base + 62);
        flatten(&root);
        let h = spine_hash(&root);
        acc = (acc * 1000003 + h + 1) % MOD;
    }
    println!("{}", acc);
}
