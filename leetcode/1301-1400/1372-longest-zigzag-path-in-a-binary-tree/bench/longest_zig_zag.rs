// LeetCode #1372 bench -- Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>`: one walk up from the leaves, each node
// reporting the longest zigzag starting at it going left and going right,
// each one more than its child's the other way.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

// (the longest zigzag from `node` going left first, going right first)
fn lengths(node: &Node, best: &mut i64) -> (i64, i64) {
    let n = node.borrow();
    let mut left = 0;
    let mut right = 0;
    if let Some(l) = &n.left {
        left = 1 + lengths(l, best).1;
    }
    if let Some(r) = &n.right {
        right = 1 + lengths(r, best).0;
    }
    *best = (*best).max(left).max(right);
    (left, right)
}

fn longest_zig_zag(root: Option<Node>) -> i32 {
    let mut best = 0;
    if let Some(r) = &root {
        lengths(r, &mut best);
    }
    best as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node() -> Node {
    Rc::new(RefCell::new(TreeNode { val: 1, left: None, right: None }))
}

fn hang(free: &mut Vec<(Node, bool)>, k: usize) {
    let (parent, left) = free.swap_remove(k);
    let node = new_node();
    if left {
        parent.borrow_mut().left = Some(node.clone());
    } else {
        parent.borrow_mut().right = Some(node.clone());
    }
    free.push((node.clone(), true));
    free.push((node, false));
}

fn main() {
    // 20 trees of 5 * 10^4 nodes, the constraints' most, each node hung
    // on a random empty child place, built once; then 300 rounds, each
    // hanging one more leaf on one tree, on a place drawn from the
    // checksum so far, and finding that tree's longest zigzag
    let mut seed = 1372i64;
    let mut roots: Vec<Node> = Vec::new();
    let mut places: Vec<Vec<(Node, bool)>> = Vec::new();
    for _ in 0..20 {
        let root = new_node();
        let mut free = vec![(root.clone(), true), (root.clone(), false)];
        for _ in 1..50000 {
            let k = (next_random(&mut seed) % free.len() as i64) as usize;
            hang(&mut free, k);
        }
        roots.push(root);
        places.push(free);
    }
    let mut check: i64 = 0;
    for r in 0..300i64 {
        let t = (check % 20) as usize;
        let k = ((check / 20) % places[t].len() as i64) as usize;
        hang(&mut places[t], k);
        let got = longest_zig_zag(Some(roots[t].clone())) as i64;
        check = (check * 31 + got + r) % 1000000007;
    }
    println!("300 rounds over 20 trees of 50000 nodes: checksum {}", check);
}
