// LeetCode #1382 bench -- Rust: the ★ arm: the values read off in order,
// then a new tree built with the middle value at the root and each half
// built the same way beneath it. A Kāra `shared struct` is reference
// counted, so the Rust tree is `Rc<RefCell<TreeNode>>`, as LeetCode's
// Rust tree problems have it.

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

fn values_in_order(node: &Option<Node>, values: &mut Vec<i32>) {
    if let Some(n) = node {
        let n = n.borrow();
        values_in_order(&n.left, values);
        values.push(n.val);
        values_in_order(&n.right, values);
    }
}

fn build(values: &[i32], lo: usize, hi: usize) -> Option<Node> {
    if lo >= hi {
        return None;
    }
    let mid = (lo + hi) / 2;
    Some(Rc::new(RefCell::new(TreeNode {
        val: values[mid],
        left: build(values, lo, mid),
        right: build(values, mid + 1, hi),
    })))
}

fn balance_bst(root: &Node) -> Node {
    let mut values = Vec::new();
    values_in_order(&Some(root.clone()), &mut values);
    build(&values, 0, values.len()).unwrap()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn search_tree(values: &[i32]) -> Node {
    let root = new_node(values[0]);
    for &v in &values[1..] {
        let mut at = root.clone();
        loop {
            let next = {
                let a = at.borrow();
                if v < a.val { a.left.clone() } else { a.right.clone() }
            };
            match next {
                Some(child) => at = child,
                None => {
                    let mut a = at.borrow_mut();
                    if v < a.val {
                        a.left = Some(new_node(v));
                    } else {
                        a.right = Some(new_node(v));
                    }
                    break;
                }
            }
        }
    }
    root
}

fn main() {
    let mut seed: i64 = 1382;
    let mut trees: Vec<Node> = Vec::new();
    for _ in 0..10 {
        let step = 1 + next_random(&mut seed) % 99990;
        let start = next_random(&mut seed) % 99991;
        let mut values: Vec<i32> = (0..10000i64).map(|k| (1 + (start + k * step) % 99991) as i32).collect();
        for i in (1..10000usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            values.swap(i, j);
        }
        trees.push(search_tree(&values));
    }
    let mut check: i64 = 0;
    for _ in 0..500 {
        let t = ((check + next_random(&mut seed)) % 10) as usize;
        let balanced = balance_bst(&trees[t]);
        let mut at = Some(balanced.clone());
        while let Some(node) = at {
            let n = node.borrow();
            check = (check * 131 + n.val as i64) % 1000000007;
            at = if next_random(&mut seed) % 2 == 0 { n.left.clone() } else { n.right.clone() };
        }
        trees[t] = balanced;
    }
    println!("500 rounds over 10 trees of 10000 nodes: checksum {}", check);
}
