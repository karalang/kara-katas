// LeetCode #1602: Find Nearest Right Node in Binary Tree -- the bench in
// Rust, mirroring nearest_right.kara: breadth first, a level at a time,
// over a `VecDeque`. Each node is an `Rc<RefCell<TreeNode>>`, as in
// LeetCode's template and as Kāra's `shared struct` is counted.

use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn find_nearest_right_node(root: Option<Node>, u: &Node) -> Option<Node> {
    let mut queue = VecDeque::new();
    if let Some(r) = root {
        queue.push_back(r);
    }
    while !queue.is_empty() {
        let width = queue.len();
        for i in 0..width {
            let node = queue.pop_front().unwrap();
            if Rc::ptr_eq(&node, u) {
                return if i + 1 < width { queue.pop_front() } else { None };
            }
            let n = node.borrow();
            if let Some(l) = &n.left {
                queue.push_back(l.clone());
            }
            if let Some(r) = &n.right {
                queue.push_back(r.clone());
            }
        }
    }
    None
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn leaf(v: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn random_tree(n: i64, seed: &mut i64) -> Vec<Node> {
    let mut values: Vec<i32> = (1..n + 1).map(|v| v as i32).collect();
    for i in (1..n).rev() {
        let j = big(seed) % (i + 1);
        values.swap(i as usize, j as usize);
    }
    let mut nodes = vec![leaf(values[0])];
    let mut free = vec![(nodes[0].clone(), true), (nodes[0].clone(), false)];
    for v in values[1..].iter() {
        let k = big(seed) % free.len() as i64;
        let (parent, left) = free.swap_remove(k as usize);
        let child = leaf(*v);
        if left {
            parent.borrow_mut().left = Some(child.clone());
        } else {
            parent.borrow_mut().right = Some(child.clone());
        }
        free.push((child.clone(), true));
        free.push((child.clone(), false));
        nodes.push(child);
    }
    nodes
}

fn main() {
    let mut seed = 1602;
    let mut trees = Vec::new();
    let mut picks = Vec::new();
    for _ in 0..10 {
        let tree = random_tree(100000, &mut seed);
        picks.push((0..100).map(|_| big(&mut seed) % 100000).collect::<Vec<i64>>());
        trees.push(tree);
    }
    let mut check = 0;
    let mut found = 0;
    for (tree, us) in trees.iter().zip(picks.iter()) {
        for k in us.iter() {
            let a = match find_nearest_right_node(Some(tree[0].clone()), &tree[*k as usize]) {
                Some(n) => n.borrow().val as i64,
                None => 0,
            };
            if a > 0 {
                found += 1;
            }
            check = mix(check, a);
        }
    }
    println!("10 trees of 100000 nodes: 1000 queries, {} found, checksum {}", found, check);
}
