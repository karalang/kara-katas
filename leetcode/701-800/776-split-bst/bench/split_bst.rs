// Benchmark for #776: Split BST -- mirror of the ★ arm (recursive), with
// the same workload as split_bst.kara. The tree is `Rc<RefCell<TreeNode>>`,
// the closest match to a `shared struct`.
use std::cell::RefCell;
use std::collections::HashSet;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn split_bst(root: Node, target: i64) -> (Node, Node) {
    let node = match root {
        Some(node) => node,
        None => return (None, None),
    };
    let val = node.borrow().val;
    if val <= target {
        let right = node.borrow_mut().right.take();
        let (small, large) = split_bst(right, target);
        node.borrow_mut().right = small;
        (Some(node), large)
    } else {
        let left = node.borrow_mut().left.take();
        let (small, large) = split_bst(left, target);
        node.borrow_mut().left = large;
        (small, Some(node))
    }
}

fn insert(root: Node, v: i64) -> Node {
    let fresh = Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }));
    let top = match root {
        Some(top) => top,
        None => return Some(fresh),
    };
    let mut node = top.clone();
    loop {
        let next = {
            let n = node.borrow();
            if v < n.val { n.left.clone() } else { n.right.clone() }
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

fn weigh(root: &Node, depth: i64) -> i64 {
    match root {
        Some(node) => {
            let n = node.borrow();
            n.val * depth + weigh(&n.left, depth + 1) + weigh(&n.right, depth + 1)
        }
        None => 0,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let mut seed: i64 = 776;
    let mut orders: Vec<Vec<i64>> = Vec::new();
    let mut targets: Vec<i64> = Vec::new();
    for _ in 0..count {
        let mut used: HashSet<i64> = HashSet::new();
        let mut values: Vec<i64> = Vec::new();
        while values.len() < 50 {
            let v = next_random(&mut seed) % 1001;
            if used.insert(v) {
                values.push(v);
            }
        }
        orders.push(values);
        targets.push(next_random(&mut seed) % 1001);
    }
    let mut checksum: i64 = 0;
    for round in 0..200000 {
        let g = round % count;
        let mut root: Node = None;
        for &v in &orders[g] {
            root = insert(root, v);
        }
        let (small, large) = split_bst(root, targets[g]);
        checksum = (checksum * 31 + weigh(&small, 1) + 3 * weigh(&large, 1)) % 1000000007;
    }
    println!("200000 rounds of 50 values: checksum {}", checksum);
}
