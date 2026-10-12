// Benchmark for #426: mirror of tree_to_list.kara (the in-order
// recursion). The Kāra `shared struct` is reference counted, so each
// node here is an Rc<RefCell<Node>>; the walk breaks every link, as the
// Kāra program does, so the counts drop to zero and the nodes are freed.
use std::cell::RefCell;
use std::rc::Rc;

struct Node {
    val: i64,
    left: Option<Rc<RefCell<Node>>>,
    right: Option<Rc<RefCell<Node>>>,
}

type Link = Option<Rc<RefCell<Node>>>;

fn link(node: &Link, first: &mut Link, last: &mut Link) {
    if let Some(n) = node {
        let left = n.borrow().left.clone();
        link(&left, first, last);
        match last {
            Some(prev) => {
                prev.borrow_mut().right = Some(n.clone());
                n.borrow_mut().left = Some(prev.clone());
            }
            None => *first = Some(n.clone()),
        }
        *last = Some(n.clone());
        let right = n.borrow().right.clone();
        link(&right, first, last);
    }
}

fn tree_to_doubly_list(root: Link) -> Link {
    let mut first: Link = None;
    let mut last: Link = None;
    link(&root, &mut first, &mut last);
    match (first, last) {
        (Some(head), Some(tail)) => {
            head.borrow_mut().left = Some(tail.clone());
            tail.borrow_mut().right = Some(head.clone());
            Some(head)
        }
        _ => None,
    }
}

fn step(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn insert(root: Link, val: i64) -> Link {
    match root {
        Some(node) => {
            let go_left = val < node.borrow().val;
            if go_left {
                let l = node.borrow_mut().left.take();
                node.borrow_mut().left = insert(l, val);
            } else {
                let r = node.borrow_mut().right.take();
                node.borrow_mut().right = insert(r, val);
            }
            Some(node)
        }
        None => Some(Rc::new(RefCell::new(Node { val, left: None, right: None }))),
    }
}

fn main() {
    let n: i64 = 50000;
    let rounds: i64 = std::env::args().nth(1).map_or(20, |s| s.parse().unwrap());
    let mut seed: i64 = 426;
    let mut order: Vec<i64> = (0..n).collect();
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for i in 0..n - 1 {
            let a = step(&mut seed);
            let b = step(&mut seed);
            let j = i + (a * 32768 + b) % (n - i);
            order.swap(i as usize, j as usize);
        }
        let mut root: Link = None;
        for &v in &order {
            root = insert(root, v);
        }
        let head = tree_to_doubly_list(root).expect("the tree is not empty");
        let tail_val = head.borrow().left.as_ref().expect("a ring has a tail").borrow().val;
        checksum = (checksum * 31 + tail_val) % 1000000007;
        let mut cur = head;
        for _ in 0..n {
            checksum = (checksum * 31 + cur.borrow().val) % 1000000007;
            let next = cur.borrow().right.clone().expect("a ring has no end");
            cur.borrow_mut().left = None;
            cur.borrow_mut().right = None;
            cur = next;
        }
    }
    println!("{} rounds on {} nodes: checksum {}", rounds, n, checksum);
}
