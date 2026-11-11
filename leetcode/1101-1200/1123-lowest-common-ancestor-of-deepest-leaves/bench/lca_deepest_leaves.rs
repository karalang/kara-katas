// LeetCode #1123: Lowest Common Ancestor of Deepest Leaves -- the bench in
// Rust, the ★ arm over LeetCode's own `Rc<RefCell<TreeNode>>`, the same 16
// trees and 200 rounds.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn walk(node: &Node) -> (i64, Node) {
    let Some(n) = node else {
        return (0, None);
    };
    let b = n.borrow();
    let (ld, la) = walk(&b.left);
    let (rd, ra) = walk(&b.right);
    if ld == rd {
        (ld + 1, Some(Rc::clone(n)))
    } else if ld > rd {
        (ld + 1, la)
    } else {
        (rd + 1, ra)
    }
}

fn lca_deepest_leaves(root: &Node) -> Node {
    walk(root).1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i32 {
    let hi = next_random(seed);
    let lo = next_random(seed);
    ((hi * 32768 + lo) % 100001) as i32
}

fn new_node(v: i32) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

// Hangs a new node at a random free place below the tree's nodes.
fn grow(nodes: &mut Vec<Rc<RefCell<TreeNode>>>, seed: &mut i64) {
    let c = new_node(random_value(seed));
    loop {
        let at = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
        let mut at = at.borrow_mut();
        if next_random(seed) % 2 == 0 {
            if at.left.is_none() {
                at.left = Some(c.clone());
                break;
            }
        } else if at.right.is_none() {
            at.right = Some(c.clone());
            break;
        }
    }
    nodes.push(c);
}

fn main() {
    let mut seed = 1123;
    let mut trees: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    for _ in 0..16 {
        let mut nodes = vec![new_node(random_value(&mut seed))];
        for _ in 1..10000 {
            grow(&mut nodes, &mut seed);
        }
        trees.push(nodes);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        for nodes in trees.iter_mut() {
            grow(nodes, &mut seed);
            let answer = lca_deepest_leaves(&Some(nodes[0].clone())).unwrap();
            let v = answer.borrow().val as i64;
            total += v;
            check = (check * 31 + v) % 1000000007;
        }
    }
    println!("200 rounds over 16 trees of 10^4 nodes: answers total {total}, checksum {check}");
}
