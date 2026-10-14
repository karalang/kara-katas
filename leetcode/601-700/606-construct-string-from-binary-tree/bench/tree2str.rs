// Benchmark for #606: Rust mirror of the ★ arm (write it out); see
// tree2str.kara. The tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`,
// reference counted as Kāra's `shared` struct is, and each value is
// formatted into a string of its own before it is appended, as the Kāra
// arm's `f"{node.val}"` is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn write(node: &Rc<RefCell<TreeNode>>, out: &mut String) {
    let n = node.borrow();
    out.push_str(&n.val.to_string());
    if n.left.is_some() || n.right.is_some() {
        out.push('(');
        if let Some(l) = &n.left {
            write(l, out);
        }
        out.push(')');
    }
    if let Some(r) = &n.right {
        out.push('(');
        write(r, out);
        out.push(')');
    }
}

fn tree2str(root: Option<Rc<RefCell<TreeNode>>>) -> String {
    let mut out = String::new();
    if let Some(r) = &root {
        write(r, &mut out);
    }
    out
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn main() {
    let trees = 20i64;
    let rounds = 200i64;
    let mut seed: i64 = 606;
    let mut all: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    for g in 0..trees {
        let lean = 50 + 2 * g;
        let root = new_node(next_random(&mut seed) % 2001 - 1000);
        let mut nodes = vec![root.clone()];
        for _ in 1..10000 {
            let c = new_node(next_random(&mut seed) % 2001 - 1000);
            let mut node = root.clone();
            loop {
                if next_random(&mut seed) % 100 < lean {
                    let next = node.borrow().left.clone();
                    match next {
                        Some(l) => node = l,
                        None => {
                            node.borrow_mut().left = Some(c.clone());
                            break;
                        }
                    }
                } else {
                    let next = node.borrow().right.clone();
                    match next {
                        Some(r) => node = r,
                        None => {
                            node.borrow_mut().right = Some(c.clone());
                            break;
                        }
                    }
                }
            }
            nodes.push(c);
        }
        all.push(nodes);
    }
    let mut length = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        for t in 0..trees {
            let k = ((r * 37 + t * 11) % 16) as usize;
            let s = tree2str(Some(all[t as usize][k].clone()));
            length += s.len();
            for (i, c) in s.chars().enumerate() {
                if i % 101 == 0 {
                    checksum = (checksum * 31 + c as i64) % 1000000007;
                }
            }
        }
    }
    println!("{} trees, {} times each: {} characters, checksum {}", trees, rounds, length, checksum);
}
