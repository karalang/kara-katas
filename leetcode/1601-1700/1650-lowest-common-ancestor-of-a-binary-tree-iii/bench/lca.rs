// LeetCode #1650: Lowest Common Ancestor of a Binary Tree III -- the
// bench's Rust mirror: the ★ arm on 30 random trees of 100000 nodes with
// parent links, each asked about 50000 pairs of its nodes, all drawn
// first. Nodes are `Rc<RefCell<Node>>` with a `Weak` parent, as Kāra's
// `shared struct` with a `weak` field is.

use std::cell::RefCell;
use std::rc::{Rc, Weak};

struct Node {
    val: i32,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
    parent: Weak<RefCell<Node>>,
}

type Handle = Rc<RefCell<Node>>;

fn leaf(val: i32) -> Handle {
    Rc::new(RefCell::new(Node { val, left: None, right: None, parent: Weak::new() }))
}

fn lowest_common_ancestor(p: &Handle, q: &Handle) -> Handle {
    let mut a = Rc::clone(p);
    let mut b = Rc::clone(q);
    while a.borrow().val != b.borrow().val {
        let up = a.borrow().parent.upgrade();
        a = match up {
            Some(up) => up,
            None => Rc::clone(q),
        };
        let up = b.borrow().parent.upgrade();
        b = match up {
            Some(up) => up,
            None => Rc::clone(p),
        };
    }
    a
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, seed: &mut i64) -> Vec<Handle> {
    let mut values: Vec<i32> = (0..n as i32).collect();
    for i in (1..n as usize).rev() {
        let j = ((next_random(seed) * 32768 + next_random(seed)) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let mut nodes: Vec<Handle> = Vec::new();
    for i in 0..n as usize {
        let node = leaf(values[i]);
        if i > 0 {
            let mut at = Rc::clone(&nodes[((next_random(seed) * 32768 + next_random(seed)) % i as i64) as usize]);
            loop {
                let left_side = next_random(seed) % 2 == 0;
                let child = {
                    let b = at.borrow();
                    if left_side { b.left.clone() } else { b.right.clone() }
                };
                match child {
                    Some(c) => at = c,
                    None => {
                        node.borrow_mut().parent = Rc::downgrade(&at);
                        let mut b = at.borrow_mut();
                        if left_side {
                            b.left = Some(Rc::clone(&node));
                        } else {
                            b.right = Some(Rc::clone(&node));
                        }
                        break;
                    }
                }
            }
        }
        nodes.push(node);
    }
    nodes
}

fn main() {
    let mut seed: i64 = 1650;
    let mut trees = Vec::new();
    for _ in 0..30 {
        let nodes = random_tree(100000, &mut seed);
        let mut pairs = Vec::new();
        for _ in 0..50000 {
            let p = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000;
            let mut q = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 100000;
            if q == p {
                q = (q + 1) % 100000;
            }
            pairs.push((p as usize, q as usize));
        }
        trees.push((nodes, pairs));
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for (nodes, pairs) in &trees {
        for &(p, q) in pairs {
            let found = lowest_common_ancestor(&nodes[p], &nodes[q]).borrow().val as i64;
            total += found;
            check = (check * 31 + found + 1) % 1000000007;
        }
    }
    println!("30 trees of 100000 nodes, 50000 pairs each: answers sum to {}, checksum {}", total, check);
}
