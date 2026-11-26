// LeetCode #1448 bench in Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>` (a walk down by recursion, carrying the largest
// value on the path above each node) on the same 50 trees of 10^4 nodes and
// 50 passes.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn good_nodes(root: Option<Node>) -> i32 {
    below(&root, i32::MIN)
}

// the good nodes under `node`, `high` the largest value on the path above
// it: the node is good when it is at least as large
fn below(node: &Option<Node>, high: i32) -> i32 {
    let Some(n) = node else {
        return 0;
    };
    let n = n.borrow();
    let good = if n.val >= high { 1 } else { 0 };
    let high = high.max(n.val);
    good + below(&n.left, high) + below(&n.right, high)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(seed: &mut i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: (1 + next_random(seed) % 100) as i32, left: None, right: None }))
}

fn build(seed: &mut i64, n: usize, level_order: bool) -> Vec<Node> {
    let root = new_node(seed);
    let mut nodes = vec![root.clone()];
    if level_order {
        let mut level: VecDeque<Node> = VecDeque::new();
        level.push_back(root);
        while nodes.len() < n {
            let at = level.pop_front().unwrap();
            for side in 0..2 {
                if nodes.len() < n && next_random(seed) % 4 != 0 {
                    let node = new_node(seed);
                    if side == 0 {
                        at.borrow_mut().left = Some(node.clone());
                    } else {
                        at.borrow_mut().right = Some(node.clone());
                    }
                    level.push_back(node.clone());
                    nodes.push(node);
                }
            }
            if level.is_empty() {
                level.push_back(at);
            }
        }
    } else {
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
    }
    nodes
}

fn main() {
    let n = 10000usize;
    let mut seed = 1448i64;
    let trees: Vec<Vec<Node>> = (0..50).map(|t| build(&mut seed, n, t % 2 == 1)).collect();
    let mut check: i64 = 0;
    for pass in 0..50i64 {
        for nodes in &trees {
            nodes[(check % n as i64) as usize].borrow_mut().val = (1 + (check / 7) % 100) as i32;
            let good = good_nodes(Some(nodes[0].clone()));
            check = (check * 31 + good as i64 + pass) % 1000000007;
        }
    }
    println!("50 passes over 50 trees of 10^4: checksum {check}");
}
