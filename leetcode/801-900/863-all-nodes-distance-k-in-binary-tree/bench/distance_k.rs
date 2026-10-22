// LeetCode #863: All Nodes Distance K in Binary Tree -- Rust mirror of the
// bench program (the ★ arm, parents, then a breadth-first search), on
// LeetCode's Rust tree type, `Option<Rc<RefCell<TreeNode>>>`.
use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn distance_k(root: &Option<Node>, target: i64, k: i64) -> Vec<i64> {
    let mut parent: HashMap<i64, Node> = HashMap::new();
    let mut start: Option<Node> = None;
    let mut stack: Vec<Node> = Vec::new();
    if let Some(r) = root {
        stack.push(r.clone());
    }
    while let Some(node) = stack.pop() {
        let b = node.borrow();
        if b.val == target {
            start = Some(node.clone());
        }
        if let Some(child) = &b.left {
            parent.insert(child.borrow().val, node.clone());
            stack.push(child.clone());
        }
        if let Some(child) = &b.right {
            parent.insert(child.borrow().val, node.clone());
            stack.push(child.clone());
        }
    }
    let mut found: Vec<i64> = Vec::new();
    let Some(s) = start else {
        return found;
    };
    let mut seen: HashSet<i64> = HashSet::new();
    seen.insert(s.borrow().val);
    let mut level: Vec<Node> = vec![s];
    for _ in 0..k {
        let mut next: Vec<Node> = Vec::new();
        for node in &level {
            let b = node.borrow();
            let mut near: Vec<Node> = Vec::new();
            if let Some(child) = &b.left {
                near.push(child.clone());
            }
            if let Some(child) = &b.right {
                near.push(child.clone());
            }
            if let Some(up) = parent.get(&b.val) {
                near.push(up.clone());
            }
            for m in near {
                let v = m.borrow().val;
                if !seen.contains(&v) {
                    seen.insert(v);
                    next.push(m);
                }
            }
        }
        level = next;
    }
    for node in &level {
        found.push(node.borrow().val);
    }
    found.sort();
    found
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(seed: &mut i64, n: i64) -> Option<Node> {
    let mut vals: Vec<i64> = (0..n).collect();
    for i in 1..n {
        let j = next_random(seed) % (i + 1);
        vals.swap(i as usize, j as usize);
    }
    let mut nodes: Vec<Node> = Vec::new();
    for k in 0..n as usize {
        let node = Rc::new(RefCell::new(TreeNode { val: vals[k], left: None, right: None }));
        if k > 0 {
            loop {
                let parent = nodes[(next_random(seed) % nodes.len() as i64) as usize].clone();
                let mut p = parent.borrow_mut();
                if next_random(seed) % 2 == 0 {
                    if p.left.is_none() {
                        p.left = Some(node.clone());
                        break;
                    }
                } else if p.right.is_none() {
                    p.right = Some(node.clone());
                    break;
                }
            }
        }
        nodes.push(node);
    }
    if n == 0 { None } else { Some(nodes[0].clone()) }
}

fn main() {
    let n: i64 = 500;
    let queries = 200000;
    let mut seed: i64 = 863;
    let root = random_tree(&mut seed, n);
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..queries {
        let target = next_random(&mut seed) % n;
        let k = next_random(&mut seed) % 20;
        let found = distance_k(&root, target, k);
        total += found.len() as i64;
        for v in &found {
            check = (check * 31 + v + 1) % 1000000007;
        }
    }
    println!("{} queries on {} nodes: {} nodes found, checksum {}", queries, n, total, check);
}
