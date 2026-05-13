//! Benchmark workload — recursive DFS invert.
//!
//! Algorithmic mirror of bench/recursive.kara and bench/recursive.py.
//! See ../README.md § Benchmarks for N / K, LCG seed, and sink choice.
//!
//! Uses `Rc<RefCell<TreeNode>>` so the data model matches Kāra's
//! `shared struct` semantics (heap-allocated nodes with RC-backed
//! reference-semantic mutation through shared handles).

use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

type Tree = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Tree,
    right: Tree,
}

fn invert(root: Tree) -> Tree {
    if let Some(node) = root.as_ref() {
        let (l, r) = {
            let n = node.borrow();
            (n.left.clone(), n.right.clone())
        };
        let new_left = invert(r);
        let new_right = invert(l);
        let mut n = node.borrow_mut();
        n.left = new_left;
        n.right = new_right;
    }
    root
}

fn build_tree(n: i64) -> Tree {
    if n <= 0 {
        return None;
    }
    let n_us = n as usize;
    let nodes: Vec<Rc<RefCell<TreeNode>>> = (0..n)
        .map(|i| {
            Rc::new(RefCell::new(TreeNode {
                val: i,
                left: None,
                right: None,
            }))
        })
        .collect();
    let mut state: i64 = 12345;
    for i in 1..n_us {
        let mut cur: Rc<RefCell<TreeNode>> = nodes[0].clone();
        loop {
            state = (state * 1103515245 + 12345) & 2147483647;
            let bit = state & 1;
            let next = if bit == 0 {
                let child = cur.borrow().left.clone();
                match child {
                    None => {
                        cur.borrow_mut().left = Some(nodes[i].clone());
                        break;
                    }
                    Some(c) => c,
                }
            } else {
                let child = cur.borrow().right.clone();
                match child {
                    None => {
                        cur.borrow_mut().right = Some(nodes[i].clone());
                        break;
                    }
                    Some(c) => c,
                }
            };
            cur = next;
        }
    }
    Some(nodes[0].clone())
}

fn bfs_sink(root: Tree) -> i64 {
    let Some(root_node) = root else {
        return 0;
    };
    let mut queue: VecDeque<Rc<RefCell<TreeNode>>> = VecDeque::new();
    queue.push_back(root_node);
    let mut sum: i64 = 0;
    let mut pos: i64 = 0;
    while let Some(cur) = queue.pop_front() {
        pos += 1;
        let n = cur.borrow();
        sum += n.val * pos;
        if let Some(ref l) = n.left {
            queue.push_back(l.clone());
        }
        if let Some(ref r) = n.right {
            queue.push_back(r.clone());
        }
    }
    sum
}

fn main() {
    let mut root = build_tree(2000);
    for _ in 0..10 {
        root = invert(root);
    }
    println!("{}", bfs_sink(root));
}
