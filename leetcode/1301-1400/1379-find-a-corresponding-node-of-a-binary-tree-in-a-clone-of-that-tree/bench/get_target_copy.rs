// LeetCode #1379 bench -- Rust: the ★ arm: the two trees walked together,
// depth first; the clone's node where the original's is the target itself
// is the answer. A Kāra `shared struct` is reference counted, so the Rust
// tree is `Rc<RefCell<TreeNode>>`, as LeetCode's Rust tree problems have it.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn new_node(val: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn find(o: &Node, c: &Node, target: &Node) -> Option<Node> {
    if Rc::ptr_eq(o, target) {
        return Some(c.clone());
    }
    let (ob, cb) = (o.borrow(), c.borrow());
    if let (Some(lo), Some(lc)) = (&ob.left, &cb.left) {
        if let Some(found) = find(lo, lc, target) {
            return Some(found);
        }
    }
    if let (Some(ro), Some(rc)) = (&ob.right, &cb.right) {
        return find(ro, rc, target);
    }
    None
}

fn get_target_copy(original: &Node, cloned: &Node, target: &Node) -> Node {
    find(original, cloned, target).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn clone_tree(node: &Node) -> Node {
    let b = node.borrow();
    let copy = new_node(b.val);
    if let Some(l) = &b.left {
        copy.borrow_mut().left = Some(clone_tree(l));
    }
    if let Some(r) = &b.right {
        copy.borrow_mut().right = Some(clone_tree(r));
    }
    copy
}

fn main() {
    // 10 trees of 10^4 nodes built once, with their clones; then 3000
    // rounds, each asking one tree's clone for the copy of one node (see
    // the Kāra bench)
    let n = 10000i64;
    let mut seed = 1379i64;
    let mut trees: Vec<(Node, Node, Vec<Node>)> = Vec::new();
    for _ in 0..10 {
        let root = new_node(1);
        let mut nodes: Vec<Node> = vec![root.clone()];
        let mut open: Vec<(Node, bool)> = vec![(root.clone(), true), (root.clone(), false)];
        for k in 1..n {
            let at = (next_random(&mut seed) % open.len() as i64) as usize;
            let (parent, left) = open.swap_remove(at);
            let node = new_node((k + 1) as i32);
            if left {
                parent.borrow_mut().left = Some(node.clone());
            } else {
                parent.borrow_mut().right = Some(node.clone());
            }
            open.push((node.clone(), true));
            open.push((node.clone(), false));
            nodes.push(node);
        }
        let copy = clone_tree(&root);
        trees.push((root, copy, nodes));
    }
    let mut check: i64 = 0;
    for r in 0..3000i64 {
        let (original, cloned, nodes) = &trees[(check % 10) as usize];
        let target = &nodes[((check / 10 + r) % n) as usize];
        let found = get_target_copy(original, cloned, target);
        let own = if Rc::ptr_eq(&found, target) { 0 } else { 1 };
        check = (check * 31 + found.borrow().val as i64 * 2 + own + r) % 1000000007;
    }
    println!("3000 rounds over 10 trees of 10000 nodes: checksum {check}");
}
