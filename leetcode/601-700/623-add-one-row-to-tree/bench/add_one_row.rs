// LeetCode #623: Add One Row to Tree -- Rust mirror of the Kāra bench.
//
// The ★ arm's recursion with the level, on the same trees and rounds,
// each row taken out again by the same `undo`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn node(val: i64, left: Option<Node>, right: Option<Node>) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left, right }))
}

fn add_one_row(root: Option<Node>, val: i64, depth: i64) -> Option<Node> {
    if depth == 1 {
        return Some(node(val, root, None));
    }
    insert(&root, val, depth, 1);
    root
}

fn insert(n: &Option<Node>, val: i64, depth: i64, level: i64) {
    if let Some(n) = n {
        if level == depth - 1 {
            let mut b = n.borrow_mut();
            let l = b.left.take();
            let r = b.right.take();
            b.left = Some(node(val, l, None));
            b.right = Some(node(val, None, r));
        } else {
            let b = n.borrow();
            insert(&b.left, val, depth, level + 1);
            insert(&b.right, val, depth, level + 1);
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(size: i64, lean: i64, seed: &mut i64) -> Node {
    let root = node(next_random(seed) % 201 - 100, None, None);
    for _ in 1..size {
        let c = node(next_random(seed) % 201 - 100, None, None);
        let mut cur = root.clone();
        loop {
            let go_left = next_random(seed) % 100 < lean;
            let next = {
                let mut b = cur.borrow_mut();
                let slot = if go_left { &mut b.left } else { &mut b.right };
                match slot {
                    Some(child) => child.clone(),
                    None => {
                        *slot = Some(c.clone());
                        break;
                    }
                }
            };
            cur = next;
        }
    }
    root
}

fn undo(n: &Option<Node>, depth: i64, level: i64, count: &mut i64, h: &mut i64) {
    if let Some(n) = n {
        if level == depth - 1 {
            let mut b = n.borrow_mut();
            let l = b.left.take().unwrap();
            let r = b.right.take().unwrap();
            *count += 2;
            *h = (*h * 31 + l.borrow().val + r.borrow().val + 400000) % 1000000007;
            b.left = l.borrow_mut().left.take();
            b.right = r.borrow_mut().right.take();
        } else {
            let b = n.borrow();
            undo(&b.left, depth, level + 1, count, h);
            undo(&b.right, depth, level + 1, count, h);
        }
    }
}

fn main() {
    let trees = 20;
    let rounds = 4000;
    let mut seed: i64 = 623;
    let mut all: Vec<Node> = Vec::new();
    for _ in 0..trees {
        let lean = 30 + next_random(&mut seed) % 41;
        all.push(random_tree(10000, lean, &mut seed));
    }
    let mut count: i64 = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let depth = 2 + (r / trees) % 20;
        let root = add_one_row(Some(all[(r % trees) as usize].clone()), r % 201 - 100, depth);
        undo(&root, depth, 1, &mut count, &mut checksum);
    }
    println!("{} trees, {} rounds: {} row nodes, checksum {}", trees, rounds, count, checksum);
}
