// Benchmark for #572: Rust mirror of the ★ arm (recursion); see
// is_subtree.kara. Nodes are `Rc<RefCell<TreeNode>>`, LeetCode's Rust
// tree, counted as the Kāra `shared struct` is.

use std::cell::RefCell;
use std::rc::Rc;

type Tree = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Tree,
    right: Tree,
}

fn same_tree(a: &Tree, b: &Tree) -> bool {
    match (a, b) {
        (None, None) => true,
        (Some(x), Some(y)) => {
            let x = x.borrow();
            let y = y.borrow();
            x.val == y.val && same_tree(&x.left, &y.left) && same_tree(&x.right, &y.right)
        }
        _ => false,
    }
}

fn is_subtree(root: &Tree, sub_root: &Tree) -> bool {
    if same_tree(root, sub_root) {
        return true;
    }
    match root {
        None => false,
        Some(n) => {
            let n = n.borrow();
            is_subtree(&n.left, sub_root) || is_subtree(&n.right, sub_root)
        }
    }
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn random_tree(size: i64, seed: &mut i64) -> Rc<RefCell<TreeNode>> {
    let root = leaf(next_random(seed) % 2);
    for _ in 1..size {
        let c = leaf(next_random(seed) % 2);
        let mut node = root.clone();
        loop {
            if next_random(seed) % 2 == 0 {
                let next = node.borrow().left.clone();
                match next {
                    Some(l) => node = l,
                    None => {
                        node.borrow_mut().left = Some(c);
                        break;
                    }
                }
            } else {
                let next = node.borrow().right.clone();
                match next {
                    Some(r) => node = r,
                    None => {
                        node.borrow_mut().right = Some(c);
                        break;
                    }
                }
            }
        }
    }
    root
}

fn copy_tree(node: &Tree) -> Tree {
    match node {
        None => None,
        Some(n) => {
            let n = n.borrow();
            Some(Rc::new(RefCell::new(TreeNode {
                val: n.val,
                left: copy_tree(&n.left),
                right: copy_tree(&n.right),
            })))
        }
    }
}

fn all_nodes(node: &Tree, out: &mut Vec<Rc<RefCell<TreeNode>>>) {
    if let Some(n) = node {
        out.push(n.clone());
        let b = n.borrow();
        all_nodes(&b.left, out);
        all_nodes(&b.right, out);
    }
}

fn main() {
    let count: i64 = 20;
    let rounds: i64 = 1000;
    let mut seed: i64 = 572;
    let mut pairs: Vec<(Rc<RefCell<TreeNode>>, Rc<RefCell<TreeNode>>)> = Vec::new();
    for g in 0..count {
        let root = random_tree(2000, &mut seed);
        let mut nodes = Vec::new();
        all_nodes(&Some(root.clone()), &mut nodes);
        let mut picked;
        loop {
            picked = nodes[(next_random(&mut seed) % nodes.len() as i64) as usize].clone();
            let mut inside = Vec::new();
            all_nodes(&Some(picked.clone()), &mut inside);
            if inside.len() >= 20 {
                break;
            }
        }
        let sub = copy_tree(&Some(picked)).unwrap();
        if g % 2 == 1 {
            let mut inside = Vec::new();
            all_nodes(&Some(sub.clone()), &mut inside);
            let n = inside[(next_random(&mut seed) % inside.len() as i64) as usize].clone();
            let v = n.borrow().val;
            n.borrow_mut().val = 1 - v;
        }
        pairs.push((root, sub));
    }
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        for g in 0..count {
            let (root, sub) = &pairs[((round * 7 + g) % count) as usize];
            let got = is_subtree(&Some(root.clone()), &Some(sub.clone()));
            if got {
                found += 1;
            }
            checksum = (checksum * 31 + if got { g + 2 } else { 1 }) % 1000000007;
        }
    }
    println!("{} pairs, {} rounds: {} found, checksum {}", count, rounds, found, checksum);
}
