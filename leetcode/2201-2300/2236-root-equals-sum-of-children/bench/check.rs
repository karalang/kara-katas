// LeetCode #2236: Root Equals Sum of Children -- the benchmark's Rust
// mirror of check.kara: 10^6 trees of three nodes built as LeetCode's
// `Rc<RefCell<TreeNode>>`, the reference-counted node that Kāra's
// `shared struct` is, and checked.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

impl TreeNode {
    fn new(val: i32) -> Self {
        TreeNode { val, left: None, right: None }
    }
}

fn check_tree(root: Option<Rc<RefCell<TreeNode>>>) -> bool {
    match root {
        Some(node) => {
            let node = node.borrow();
            match (&node.left, &node.right) {
                (Some(left), Some(right)) => node.val == left.borrow().val + right.borrow().val,
                _ => false,
            }
        }
        None => false,
    }
}

fn tree(root: i64, left: i64, right: i64) -> Option<Rc<RefCell<TreeNode>>> {
    let node = Rc::new(RefCell::new(TreeNode::new(root as i32)));
    node.borrow_mut().left = Some(Rc::new(RefCell::new(TreeNode::new(left as i32))));
    node.borrow_mut().right = Some(Rc::new(RefCell::new(TreeNode::new(right as i32))));
    Some(node)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2236i64;
    let mut holding = 0i64;
    let mut check = 0i64;
    for _ in 0..1000000 {
        let left = next_random(&mut seed) % 101 - 50;
        let right = next_random(&mut seed) % 101 - 50;
        let root = left + right + next_random(&mut seed) % 3 - 1;
        let holds = check_tree(tree(root, left, right));
        if holds {
            holding += 1;
        }
        check = (check * 2 + if holds { 1 } else { 0 }) % 1000000007;
    }
    println!("10^6 trees: {} hold, checksum {}", holding, check);
}
