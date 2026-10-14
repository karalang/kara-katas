// Benchmark for #545: Rust mirror of the ★ arm (three walks); see
// boundary_of_binary_tree.kara. The tree is LeetCode's
// `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's `shared`
// struct is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn is_leaf(n: &Node) -> bool {
    let n = n.borrow();
    n.left.is_none() && n.right.is_none()
}

fn leaves(node: &Option<Node>, out: &mut Vec<i64>) {
    if let Some(n) = node {
        if is_leaf(n) {
            out.push(n.borrow().val);
        } else {
            let n = n.borrow();
            leaves(&n.left, out);
            leaves(&n.right, out);
        }
    }
}

fn boundary_of_binary_tree(root: Option<Node>) -> Vec<i64> {
    let mut out = Vec::new();
    let Some(r) = root else {
        return out;
    };
    out.push(r.borrow().val);
    if is_leaf(&r) {
        return out;
    }
    let mut node = r.borrow().left.clone();
    while let Some(n) = node {
        if is_leaf(&n) {
            break;
        }
        let b = n.borrow();
        out.push(b.val);
        node = if b.left.is_some() { b.left.clone() } else { b.right.clone() };
    }
    leaves(&r.borrow().left, &mut out);
    leaves(&r.borrow().right, &mut out);
    let mut right = Vec::new();
    let mut node = r.borrow().right.clone();
    while let Some(n) = node {
        if is_leaf(&n) {
            break;
        }
        let b = n.borrow();
        right.push(b.val);
        node = if b.right.is_some() { b.right.clone() } else { b.left.clone() };
    }
    for v in right.iter().rev() {
        out.push(*v);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn main() {
    // 20 random trees of 10,000 nodes (the problem's most) with values
    // from -1,000 to 1,000, each new node walking down from the root and
    // going left with chance 50 to 88 in 100, built once, the nodes kept
    // in the order they were added. Then 200 times over every tree the
    // subtree at one of its first 16 nodes, picked by the round and the
    // tree, is answered; every value on the boundary goes into the
    // checksum.
    let trees = 20i64;
    let mut seed: i64 = 545;
    let mut all: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    for g in 0..trees {
        let lean = 50 + 2 * g;
        let root = new_node(next_random(&mut seed) % 2001 - 1000);
        let mut nodes = vec![root.clone()];
        for _ in 1..10000 {
            let c = new_node(next_random(&mut seed) % 2001 - 1000);
            let mut node = root.clone();
            loop {
                let go_left = next_random(&mut seed) % 100 < lean;
                let next = {
                    let mut n = node.borrow_mut();
                    let slot = if go_left { &mut n.left } else { &mut n.right };
                    match slot {
                        Some(x) => Some(x.clone()),
                        None => {
                            *slot = Some(c.clone());
                            None
                        }
                    }
                };
                match next {
                    Some(x) => node = x,
                    None => break,
                }
            }
            nodes.push(c);
        }
        all.push(nodes);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for r in 0..200i64 {
        for t in 0..trees {
            let k = ((r * 37 + t * 11) % 16) as usize;
            let b = boundary_of_binary_tree(Some(all[t as usize][k].clone()));
            total += b.len();
            for v in b.iter() {
                checksum = (checksum * 31 + *v + 1001) % 1000000007;
            }
        }
    }
    println!("{trees} trees, 200 times each: {total} on the boundary, checksum {checksum}");
}
