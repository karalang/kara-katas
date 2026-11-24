// LeetCode #1339 bench in Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>` (one recursive walk for the total, a second for
// every subtree's sum, keeping the best product, taken modulo 10^9 + 7 at
// the end) on the same 10 trees of 5 * 10^4 nodes and 20 passes.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn total(node: &Option<Node>) -> i64 {
    match node {
        Some(n) => {
            let n = n.borrow();
            n.val as i64 + total(&n.left) + total(&n.right)
        }
        None => 0,
    }
}

fn best_cut(node: &Option<Node>, all: i64, best: &mut i64) -> i64 {
    match node {
        Some(n) => {
            let n = n.borrow();
            let s = n.val as i64 + best_cut(&n.left, all, best) + best_cut(&n.right, all, best);
            *best = (*best).max(s * (all - s));
            s
        }
        None => 0,
    }
}

fn max_product(root: Option<Node>) -> i32 {
    let all = total(&root);
    let mut best = 0;
    best_cut(&root, all, &mut best);
    (best % 1_000_000_007) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(seed: &mut i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: (1 + next_random(seed) % 10000) as i32, left: None, right: None }))
}

fn build(seed: &mut i64, n: usize) -> Vec<Node> {
    let root = new_node(seed);
    let mut nodes = vec![root.clone()];
    let mut places: Vec<(Node, bool)> = vec![(root.clone(), true), (root, false)];
    while nodes.len() < n {
        let k = (next_random(seed) % places.len() as i64) as usize;
        let (parent, left) = places.swap_remove(k);
        let node = new_node(seed);
        if left {
            parent.borrow_mut().left = Some(node.clone());
        } else {
            parent.borrow_mut().right = Some(node.clone());
        }
        places.push((node.clone(), true));
        places.push((node.clone(), false));
        nodes.push(node);
    }
    nodes
}

fn main() {
    let n = 50000;
    let mut seed = 1339;
    let trees: Vec<Vec<Node>> = (0..10).map(|_| build(&mut seed, n)).collect();
    let mut check: i64 = 0;
    for pass in 0..20 {
        for nodes in &trees {
            nodes[(check % n as i64) as usize].borrow_mut().val = (1 + (check / 7) % 10000) as i32;
            let answer = max_product(Some(nodes[0].clone()));
            check = (check * 31 + answer as i64 + pass) % 1000000007;
        }
    }
    println!("20 passes over 10 trees of 5 * 10^4: checksum {}", check);
}
