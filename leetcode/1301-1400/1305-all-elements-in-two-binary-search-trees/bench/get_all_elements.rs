// LeetCode #1305 bench in Rust: the ★ arm over LeetCode's own
// `Rc<RefCell<TreeNode>>` (each tree read in order into its own `Vec`, then
// the two merged) on the same 20 pairs of search trees and 100 passes.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn in_order(node: &Option<Node>, out: &mut Vec<i32>) {
    if let Some(n) = node {
        let n = n.borrow();
        in_order(&n.left, out);
        out.push(n.val);
        in_order(&n.right, out);
    }
}

fn get_all_elements(root1: &Option<Node>, root2: &Option<Node>) -> Vec<i32> {
    let mut a = Vec::new();
    let mut b = Vec::new();
    in_order(root1, &mut a);
    in_order(root2, &mut b);
    let mut out = Vec::new();
    let (mut i, mut j) = (0, 0);
    while i < a.len() || j < b.len() {
        if j == b.len() || (i < a.len() && a[i] <= b[j]) {
            out.push(a[i]);
            i += 1;
        } else {
            out.push(b[j]);
            j += 1;
        }
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(v: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn insert(root: &Node, v: i32) {
    let mut at = root.clone();
    loop {
        let next = {
            let n = at.borrow();
            if v == n.val {
                return;
            }
            if v < n.val { n.left.clone() } else { n.right.clone() }
        };
        match next {
            Some(child) => at = child,
            None => {
                let mut n = at.borrow_mut();
                if v < n.val {
                    n.left = Some(new_node(v));
                } else {
                    n.right = Some(new_node(v));
                }
                return;
            }
        }
    }
}

fn random_bst(seed: &mut i64, n: usize) -> Node {
    let root = new_node((next_random(seed) % 200001 - 100000) as i32);
    for _ in 1..n {
        insert(&root, (next_random(seed) % 200001 - 100000) as i32);
    }
    root
}

fn main() {
    let mut seed = 1305i64;
    let mut firsts = Vec::new();
    let mut seconds = Vec::new();
    for _ in 0..20 {
        firsts.push(random_bst(&mut seed, 4900));
        seconds.push(random_bst(&mut seed, 4900));
    }
    let mut check: i64 = 0;
    for pass in 0..100i64 {
        for p in 0..20 {
            insert(&firsts[p], (check % 200001 - 100000) as i32);
            let got = get_all_elements(&Some(firsts[p].clone()), &Some(seconds[p].clone()));
            let x = got[(check % got.len() as i64) as usize] as i64;
            check = (check * 31 + x + 100000 + got.len() as i64 + pass) % 1000000007;
        }
    }
    println!("100 passes over 20 pairs of trees: checksum {check}");
}
