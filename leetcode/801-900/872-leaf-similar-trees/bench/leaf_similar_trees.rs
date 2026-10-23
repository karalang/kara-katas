// LeetCode #872: Leaf-Similar Trees -- Rust mirror of the bench program
// (the ★ arm, the leaves of each collected by recursion), with LeetCode's
// `Option<Rc<RefCell<TreeNode>>>` nodes, reference counted as the Kāra
// program's `shared struct` is.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn new_node(val: i64, left: Node, right: Node) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left, right }))
}

fn leaf_similar(root1: &Node, root2: &Node) -> bool {
    let mut first = Vec::new();
    let mut second = Vec::new();
    leaves(root1, &mut first);
    leaves(root2, &mut second);
    first == second
}

fn leaves(node: &Node, out: &mut Vec<i64>) {
    if let Some(n) = node {
        let n = n.borrow();
        if n.left.is_none() && n.right.is_none() {
            out.push(n.val);
        } else {
            leaves(&n.left, out);
            leaves(&n.right, out);
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(seed: &mut i64, n: i64, limit: i64) -> Node {
    let mut nodes: Vec<Rc<RefCell<TreeNode>>> = Vec::new();
    for k in 0..n {
        let node = new_node(next_random(seed) % limit, None, None);
        if k > 0 {
            loop {
                let parent = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
                let mut p = parent.borrow_mut();
                if next_random(seed) % 2 == 0 {
                    if p.left.is_none() {
                        p.left = Some(node.clone());
                        break;
                    }
                } else if p.right.is_none() {
                    p.right = Some(node.clone());
                    break;
                }
            }
        }
        nodes.push(node);
    }
    if n == 0 { None } else { Some(nodes[0].clone()) }
}

fn tree_with_leaves(seed: &mut i64, vals: &[i64], lo: usize, hi: usize, limit: i64) -> Rc<RefCell<TreeNode>> {
    if hi - lo == 1 {
        return new_node(vals[lo], None, None);
    }
    let mid = lo + 1 + (next_random(seed) % (hi - lo - 1) as i64) as usize;
    let left = tree_with_leaves(seed, vals, lo, mid, limit);
    let right = tree_with_leaves(seed, vals, mid, hi, limit);
    new_node(next_random(seed) % limit, Some(left), Some(right))
}

fn main() {
    let mut seed: i64 = 872;
    let mut pairs: Vec<(Node, Node)> = Vec::new();
    for k in 0..2000 {
        let a = random_tree(&mut seed, 200, 201);
        if k % 2 == 0 {
            let mut vals = Vec::new();
            leaves(&a, &mut vals);
            let b = tree_with_leaves(&mut seed, &vals, 0, vals.len(), 201);
            pairs.push((a, Some(b)));
        } else {
            let b = random_tree(&mut seed, 200, 201);
            pairs.push((a, b));
        }
    }
    let mut check: i64 = 0;
    for (_, b) in &pairs {
        let mut vals = Vec::new();
        leaves(b, &mut vals);
        for v in vals {
            check = (check * 31 + v + 1) % 1000000007;
        }
    }
    let mut similar = 0;
    for _ in 0..50 {
        for (a, b) in &pairs {
            if leaf_similar(a, b) {
                similar += 1;
            }
        }
    }
    println!("100000 comparisons of 2000 pairs: {} leaf-similar, leaf checksum {}", similar, check);
}
