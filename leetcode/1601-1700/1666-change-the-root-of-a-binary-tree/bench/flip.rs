// LeetCode #1666: Change the Root of a Binary Tree -- the bench's Rust
// mirror: the ★ arm on 30 random trees of 100000 nodes with parent links,
// each turned 50000 times to hang from a leaf reached by a random walk
// down from a random node, the start nodes drawn first. Nodes are
// `Rc<RefCell<Node>>` with a `Weak` parent, as Kāra's `shared struct`
// with a `weak` field is.

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

fn flip_binary_tree(_root: &Handle, leaf: &Handle) -> Handle {
    let mut cur = Rc::clone(leaf);
    let mut below: Weak<RefCell<Node>> = Weak::new();
    loop {
        let above = std::mem::replace(&mut cur.borrow_mut().parent, below).upgrade();
        let Some(p) = above else {
            break;
        };
        {
            let mut pb = p.borrow_mut();
            if pb.left.as_ref().is_some_and(|l| Rc::ptr_eq(l, &cur)) {
                pb.left = None;
            } else {
                pb.right = None;
            }
        }
        {
            let mut cb = cur.borrow_mut();
            if cb.left.is_some() {
                cb.right = cb.left.take();
            }
            cb.left = Some(Rc::clone(&p));
        }
        below = Rc::downgrade(&cur);
        cur = p;
    }
    Rc::clone(leaf)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, seed: &mut i64) -> Vec<Handle> {
    let mut values: Vec<i32> = (0..n as i32).collect();
    for i in (1..n as usize).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let mut nodes: Vec<Handle> = Vec::new();
    for i in 0..n as usize {
        let node = leaf(values[i]);
        if i > 0 {
            let mut at = Rc::clone(&nodes[(next_random(seed) % i as i64) as usize]);
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
    let mut seed: i64 = 1666;
    let mut trees = Vec::new();
    for _ in 0..30 {
        let nodes = random_tree(100000, &mut seed);
        let mut starts = Vec::new();
        for _ in 0..50000 {
            starts.push((next_random(&mut seed) % 100000) as usize);
        }
        trees.push((nodes, starts));
    }
    let mut check: i64 = 0;
    let mut steps: i64 = 0;
    for (nodes, starts) in &trees {
        let mut root = Rc::clone(&nodes[0]);
        for &s in starts {
            let mut at = Rc::clone(&nodes[s]);
            loop {
                let child = {
                    let b = at.borrow();
                    let first = if next_random(&mut seed) % 2 == 0 { &b.left } else { &b.right };
                    first.as_ref().or(b.left.as_ref()).or(b.right.as_ref()).cloned()
                };
                match child {
                    Some(c) => at = c,
                    None => break,
                }
                steps += 1;
            }
            root = flip_binary_tree(&root, &at);
            check = (check * 31 + root.borrow().val as i64 + 1) % 1000000007;
        }
    }
    println!("30 trees of 100000 nodes, 50000 turns each: {} steps down, checksum {}", steps, check);
}
