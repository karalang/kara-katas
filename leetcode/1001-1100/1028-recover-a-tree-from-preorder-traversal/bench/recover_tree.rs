// LeetCode #1028: Recover a Tree From Preorder Traversal -- bench
// Mirrors ./recover_tree.kara; see ../README.md § Benchmarks.

use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn recover_from_preorder(traversal: &str) -> Option<Rc<RefCell<TreeNode>>> {
    let bytes = traversal.as_bytes();
    let mut path: Vec<Rc<RefCell<TreeNode>>> = Vec::new();
    let mut i = 0;
    while i < bytes.len() {
        let mut depth = 0;
        while bytes[i] == b'-' {
            depth += 1;
            i += 1;
        }
        let mut value = 0i64;
        while i < bytes.len() && bytes[i] != b'-' {
            value = value * 10 + (bytes[i] - b'0') as i64;
            i += 1;
        }
        let node = Rc::new(RefCell::new(TreeNode { val: value, left: None, right: None }));
        while path.len() > depth {
            path.pop();
        }
        if let Some(parent) = path.last() {
            let mut parent = parent.borrow_mut();
            if parent.left.is_none() {
                parent.left = Some(Rc::clone(&node));
            } else {
                parent.right = Some(Rc::clone(&node));
            }
        }
        path.push(node);
    }
    path.into_iter().next()
}

// a fold of the tree's values and shape
fn digest(node: &Option<Rc<RefCell<TreeNode>>>) -> i64 {
    match node {
        None => 1,
        Some(n) => {
            let n = n.borrow();
            (n.val + 3 * digest(&n.left) + 7 * digest(&n.right)) % 1000000007
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64, top: i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    (a * 32768 + b) % top + 1
}

fn write(at: usize, depth: usize, vals: &[i64], left: &[i64], right: &[i64], out: &mut String) {
    for _ in 0..depth {
        out.push('-');
    }
    out.push_str(&vals[at].to_string());
    if left[at] >= 0 {
        write(left[at] as usize, depth + 1, vals, left, right, out);
    }
    if right[at] >= 0 {
        write(right[at] as usize, depth + 1, vals, left, right, out);
    }
}

fn make_traversal(seed: &mut i64, n: usize) -> String {
    let mut vals: Vec<i64> = Vec::new();
    let mut left: Vec<i64> = Vec::new();
    let mut right: Vec<i64> = Vec::new();
    for k in 0..n {
        let v = random_value(seed, 1000000000);
        vals.push(v);
        left.push(-1);
        right.push(-1);
        let mut at = 0usize;
        while k > 0 {
            if v < vals[at] {
                if left[at] < 0 {
                    left[at] = k as i64;
                    break;
                }
                at = left[at] as usize;
            } else {
                if right[at] < 0 {
                    right[at] = k as i64;
                    break;
                }
                at = right[at] as usize;
            }
        }
    }
    let mut out = String::new();
    write(0, 0, &vals, &left, &right, &mut out);
    out
}

fn main() {
    let count = 200;
    let rounds = 50;
    let mut seed = 1028;
    let mut traversals: Vec<String> = Vec::new();
    let mut letters = 0;
    for _ in 0..count {
        let s = make_traversal(&mut seed, 1000);
        letters += s.len();
        traversals.push(s);
    }
    let mut check = 0i64;
    for _ in 0..rounds {
        for s in traversals.iter() {
            check = (check * 131 + digest(&recover_from_preorder(s))) % 1000000007;
        }
    }
    println!("{} traversals of 1000 nodes, {} letters, {} rounds: checksum {}", count, letters, rounds, check);
}
