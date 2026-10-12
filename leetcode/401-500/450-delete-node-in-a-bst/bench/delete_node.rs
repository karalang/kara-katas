// Benchmark for #450: mirror of delete_node.kara (recursive, successor's
// value copied in) on one random search tree of 1,000,000 values, built
// once, then 1,000,000 deletes of random keys.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn delete_node(root: Node, key: i64) -> Node {
    let node = root?;
    let val = node.borrow().val;
    if key < val {
        let left = node.borrow_mut().left.take();
        node.borrow_mut().left = delete_node(left, key);
        return Some(node);
    }
    if key > val {
        let right = node.borrow_mut().right.take();
        node.borrow_mut().right = delete_node(right, key);
        return Some(node);
    }
    let (left, right) = {
        let n = node.borrow();
        (n.left.clone(), n.right.clone())
    };
    match (left, right) {
        (None, right) => right,
        (left, None) => left,
        (Some(_), Some(right)) => {
            let mut successor = right;
            loop {
                let smaller = successor.borrow().left.clone();
                match smaller {
                    Some(s) => successor = s,
                    None => break,
                }
            }
            let next = successor.borrow().val;
            let mut n = node.borrow_mut();
            n.val = next;
            let right = n.right.take();
            n.right = delete_node(right, next);
            drop(n);
            Some(node)
        }
    }
}

fn insert(root: Node, v: i64) -> Node {
    let fresh = Rc::new(RefCell::new(TreeNode {
        val: v,
        left: None,
        right: None,
    }));
    let Some(top) = root else {
        return Some(fresh);
    };
    let mut node = top.clone();
    loop {
        let next = {
            let n = node.borrow();
            if v < n.val {
                n.left.clone()
            } else {
                n.right.clone()
            }
        };
        match next {
            Some(child) => node = child,
            None => {
                let mut n = node.borrow_mut();
                if v < n.val {
                    n.left = Some(fresh);
                } else {
                    n.right = Some(fresh);
                }
                break;
            }
        }
    }
    Some(top)
}

fn walk(node: &Node, out: &mut Vec<i64>) {
    if let Some(n) = node {
        let n = n.borrow();
        walk(&n.left, out);
        out.push(n.val);
        walk(&n.right, out);
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: i64 = 1000000;
    let deletes = 1000000;
    let mut seed: i64 = 450;
    // A shuffle of the even numbers below 2n.
    let mut values: Vec<i64> = (0..n).map(|i| i * 2).collect();
    for i in 0..n {
        let r = next_random(&mut seed) * 32768 + next_random(&mut seed);
        values.swap(i as usize, (i + r % (n - i)) as usize);
    }
    let mut root: Node = None;
    for v in values {
        root = insert(root, v);
    }
    for _ in 0..deletes {
        let key = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (2 * n);
        root = delete_node(root, key);
    }
    let mut left: Vec<i64> = Vec::new();
    walk(&root, &mut left);
    let mut checksum: i64 = 0;
    for v in &left {
        checksum = (checksum * 31 + v) % 1000000007;
    }
    println!(
        "{deletes} deletes from {n} values: {} nodes left, checksum {checksum}",
        left.len()
    );
}
