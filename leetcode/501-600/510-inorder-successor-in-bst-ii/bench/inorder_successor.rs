// Benchmark for #510: Rust mirror of the ★ arm (down the right subtree,
// or up to the first larger ancestor); see inorder_successor.kara. The
// tree is `Rc<RefCell<Node>>` with a `Weak` parent link, the closest
// match to a `shared struct` with a `weak` field: each step up upgrades.
use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    val: i64,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
    parent: Weak<RefCell<Node>>,
}

type Handle = Rc<RefCell<Node>>;

fn inorder_successor(node: &Handle) -> Option<Handle> {
    let n = node.borrow();
    if let Some(r) = &n.right {
        let mut cur = r.clone();
        loop {
            let next = cur.borrow().left.clone();
            match next {
                Some(l) => cur = l,
                None => break,
            }
        }
        return Some(cur);
    }
    let mut up = n.parent.upgrade();
    while let Some(p) = up {
        if p.borrow().val > n.val {
            return Some(p);
        }
        up = p.borrow().parent.upgrade();
    }
    None
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(v: i64) -> Handle {
    Rc::new(RefCell::new(Node { val: v, left: None, right: None, parent: Weak::new() }))
}

// Every node of the search tree of the values, in insertion order.
fn build(values: &[i64]) -> Vec<Handle> {
    let root = new_node(values[0]);
    let mut nodes = vec![root.clone()];
    for &v in &values[1..] {
        let leaf = new_node(v);
        let mut node = root.clone();
        loop {
            let go_left = v < node.borrow().val;
            let next = if go_left { node.borrow().left.clone() } else { node.borrow().right.clone() };
            match next {
                Some(c) => node = c,
                None => {
                    leaf.borrow_mut().parent = Rc::downgrade(&node);
                    if go_left {
                        node.borrow_mut().left = Some(leaf.clone());
                    } else {
                        node.borrow_mut().right = Some(leaf.clone());
                    }
                    break;
                }
            }
        }
        nodes.push(leaf);
    }
    nodes
}

fn main() {
    // 100 random search trees of 10,000 different values, the j-th value
    // j * 20 plus less than 20, shuffled, built once. Then the successor
    // of every node, 50 times over.
    let trees = 100;
    let size: i64 = 10000;
    let mut seed: i64 = 510;
    let mut all: Vec<Vec<Handle>> = Vec::new();
    for _ in 0..trees {
        let mut values: Vec<i64> = Vec::new();
        for j in 0..size {
            values.push(j * 20 + next_random(&mut seed) % 20 - 100000);
        }
        for i in 1..size {
            let k = next_random(&mut seed) % (i + 1);
            values.swap(i as usize, k as usize);
        }
        all.push(build(&values));
    }
    let mut nulls = 0i64;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for t in 0..trees {
            for node in all[t].iter() {
                match inorder_successor(node) {
                    Some(s) => checksum = (checksum + s.borrow().val + 100000) % 1000000007,
                    None => nulls += 1,
                }
            }
        }
    }
    println!("{} trees of {} nodes, 50 times each: {} without a successor, checksum {}", trees, size, nulls, checksum);
}
