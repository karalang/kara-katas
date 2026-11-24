// LeetCode #1325 bench in Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>` (a recursive walk that settles both children first
// and deletes a leaf with the target's value) on the same 30 trees of 3000
// nodes and 300 passes, each linking every node back to its children first.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn remove_leaf_nodes(root: Option<Node>, target: i32) -> Option<Node> {
    let node = root?;
    let left = remove_leaf_nodes(node.borrow_mut().left.take(), target);
    let right = remove_leaf_nodes(node.borrow_mut().right.take(), target);
    {
        let mut n = node.borrow_mut();
        n.left = left;
        n.right = right;
        if n.left.is_none() && n.right.is_none() && n.val == target {
            return None;
        }
    }
    Some(node)
}

fn count(node: &Option<Node>) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let n = n.borrow();
            1 + count(&n.left) + count(&n.right)
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

struct Tree {
    nodes: Vec<Node>,
    left: Vec<i64>,
    right: Vec<i64>,
}

fn build(seed: &mut i64, n: usize, deep: bool) -> Tree {
    let mut t = Tree { nodes: Vec::new(), left: Vec::new(), right: Vec::new() };
    let mut places: Vec<(usize, bool)> = vec![(0, true), (0, false)];
    for i in 0..n {
        t.nodes.push(Rc::new(RefCell::new(TreeNode { val: (1 + next_random(seed) % 3) as i32, left: None, right: None })));
        t.left.push(-1);
        t.right.push(-1);
        if i > 0 {
            let r = next_random(seed);
            let at = if deep && r % 4 != 0 {
                places.len() - 1 - (next_random(seed) % 2) as usize
            } else {
                (next_random(seed) % places.len() as i64) as usize
            };
            let (parent, is_left) = places.swap_remove(at);
            if is_left {
                t.left[parent] = i as i64;
            } else {
                t.right[parent] = i as i64;
            }
            places.push((i, true));
            places.push((i, false));
        }
    }
    t
}

fn main() {
    let n = 3000usize;
    let mut seed = 1325i64;
    let trees: Vec<Tree> = (0..30).map(|t| build(&mut seed, n, t % 2 == 1)).collect();
    let mut check: i64 = 0;
    for pass in 0..300i64 {
        for tree in trees.iter() {
            tree.nodes[(check % n as i64) as usize].borrow_mut().val = (1 + (check / 7) % 3) as i32;
            let target = (1 + (check / 11) % 3) as i32;
            for i in 0..n {
                let mut node = tree.nodes[i].borrow_mut();
                node.left = if tree.left[i] >= 0 { Some(tree.nodes[tree.left[i] as usize].clone()) } else { None };
                node.right = if tree.right[i] >= 0 { Some(tree.nodes[tree.right[i] as usize].clone()) } else { None };
            }
            let root = remove_leaf_nodes(Some(tree.nodes[0].clone()), target);
            let top = match &root {
                Some(r) => r.borrow().val as i64,
                None => 0,
            };
            check = (check * 31 + count(&root) * 7 + top + pass) % 1000000007;
        }
    }
    println!("300 passes over 30 trees of 3000: checksum {}", check);
}
