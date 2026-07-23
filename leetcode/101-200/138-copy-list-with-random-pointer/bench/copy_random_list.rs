// Benchmark workload for LeetCode #138 — Copy List with Random Pointer.
//
// Pointer-graph mirror of copy_random_list.kara: N nodes (linear `next` chain +
// one `random` edge each) are built once; the graph is deep-copied K times, one
// `random` edge repointed before each copy (the punch) so nothing hoists. Node
// is an Rc<RefCell<Node>> with a strong `next` and a `weak` (Weak) `random` —
// the same strong/weak split as Kāra's `shared struct Node { next, weak random
// }`, so the cyclic-through-random graph reclaims without leaking. Sink = running
// total of a checksum over each copy's (val, next-id, random-id).
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    val: i64,
    id: i64,
    next: Option<Rc<RefCell<Node>>>,
    random: Weak<RefCell<Node>>,
}

fn build(vals: &[i64], rnd: &[i64]) -> Vec<Rc<RefCell<Node>>> {
    let n = vals.len();
    let mut nodes: Vec<Rc<RefCell<Node>>> = Vec::with_capacity(n);
    for i in 0..n {
        nodes.push(Rc::new(RefCell::new(Node {
            val: vals[i],
            id: i as i64,
            next: None,
            random: Weak::new(),
        })));
    }
    for i in 0..n {
        if i + 1 < n {
            nodes[i].borrow_mut().next = Some(Rc::clone(&nodes[i + 1]));
        }
        if rnd[i] >= 0 {
            nodes[i].borrow_mut().random = Rc::downgrade(&nodes[rnd[i] as usize]);
        }
    }
    nodes
}

fn deep_copy(orig: &[Rc<RefCell<Node>>]) -> Vec<Rc<RefCell<Node>>> {
    let n = orig.len();
    let mut copies: Vec<Rc<RefCell<Node>>> = Vec::with_capacity(n);
    for node in orig.iter() {
        let o = node.borrow();
        copies.push(Rc::new(RefCell::new(Node {
            val: o.val,
            id: o.id,
            next: None,
            random: Weak::new(),
        })));
    }
    for i in 0..n {
        if i + 1 < n {
            copies[i].borrow_mut().next = Some(Rc::clone(&copies[i + 1]));
        }
        let rid = orig[i].borrow().random.upgrade().map(|r| r.borrow().id);
        if let Some(r) = rid {
            copies[i].borrow_mut().random = Rc::downgrade(&copies[r as usize]);
        }
    }
    copies
}

fn checksum(copies: &[Rc<RefCell<Node>>]) -> i64 {
    let mut s: i64 = 0;
    for c in copies {
        let cb = c.borrow();
        let next_id = cb.next.as_ref().map(|m| m.borrow().id).unwrap_or(-1);
        let rand_id = cb.random.upgrade().map(|r| r.borrow().id).unwrap_or(-1);
        s += cb.val + next_id * 7 + rand_id * 13;
    }
    s
}

fn main() {
    let n: i64 = 3000;
    let k: i64 = 4000;
    let nu = n as usize;

    let mut vals: Vec<i64> = Vec::with_capacity(nu);
    let mut rnd: Vec<i64> = Vec::with_capacity(nu);
    let mut state: i64 = 12345;
    for _ in 0..nu {
        state = (state * 1103515245 + 12345) & 2147483647;
        vals.push((state >> 16) % 1000);
        state = (state * 1103515245 + 12345) & 2147483647;
        let r = state >> 16;
        rnd.push(if r % 4 == 0 { -1 } else { r % n });
    }

    let orig = build(&vals, &rnd);

    let mut sink: i64 = 0;
    for p in 0..k {
        let ii = (p % n) as usize;
        let target = ((p * 37 + 11) % n) as usize;
        orig[ii].borrow_mut().random = Rc::downgrade(&orig[target]);
        let copies = deep_copy(&orig);
        sink += checksum(&copies);
    }
    println!("{}", sink);
}
