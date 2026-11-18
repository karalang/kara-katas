// LeetCode #1609: Even Odd Tree -- the bench in Rust, mirroring
// even_odd.kara: breadth first, a level at a time, over a `VecDeque`.
// Each node is an `Rc<RefCell<TreeNode>>`, as in LeetCode's template and
// as Kāra's `shared struct` is counted.

use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn is_even_odd_tree(root: Option<Node>) -> bool {
    let mut queue = VecDeque::new();
    if let Some(r) = root {
        queue.push_back(r);
    }
    let mut even = true;
    while !queue.is_empty() {
        let mut prev: Option<i32> = None;
        for _ in 0..queue.len() {
            let node = queue.pop_front().unwrap();
            let n = node.borrow();
            let v = n.val;
            let ok = if even {
                v % 2 == 1 && prev.is_none_or(|p| v > p)
            } else {
                v % 2 == 0 && prev.is_none_or(|p| v < p)
            };
            if !ok {
                return false;
            }
            prev = Some(v);
            if let Some(l) = &n.left {
                queue.push_back(l.clone());
            }
            if let Some(r) = &n.right {
                queue.push_back(r.clone());
            }
        }
        even = !even;
    }
    true
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
    let mut nodes = vec![leaf(0)];
    let mut free = vec![(nodes[0].clone(), true), (nodes[0].clone(), false)];
    for _ in 1..n {
        let k = big(seed) % free.len() as i64;
        let (parent, left) = free.swap_remove(k as usize);
        let child = leaf(0);
        if left {
            parent.borrow_mut().left = Some(child.clone());
        } else {
            parent.borrow_mut().right = Some(child.clone());
        }
        free.push((child.clone(), true));
        free.push((child.clone(), false));
        nodes.push(child);
    }
    let mut level = vec![nodes[0].clone()];
    let mut depth = 0;
    while !level.is_empty() {
        let mut v: i32 = if depth % 2 == 0 {
            1 + 2 * (next_random(seed) % 5) as i32
        } else {
            1000000 - 2 * (next_random(seed) % 5) as i32
        };
        let mut below = Vec::new();
        for node in level.iter() {
            let mut n = node.borrow_mut();
            n.val = v;
            let step = 2 * (next_random(seed) % 2 + 1) as i32;
            v = if depth % 2 == 0 { v + step } else { v - step };
            if let Some(l) = &n.left {
                below.push(l.clone());
            }
            if let Some(r) = &n.right {
                below.push(r.clone());
            }
        }
        level = below;
        depth += 1;
    }
    nodes
}

fn swap_values(a: &Node, b: &Node) {
    let t = a.borrow().val;
    let u = b.borrow().val;
    a.borrow_mut().val = u;
    b.borrow_mut().val = t;
}

fn main() {
    let mut seed = 1609;
    let mut trees = Vec::new();
    let mut picks = Vec::new();
    for _ in 0..20 {
        trees.push(random_tree(100000, &mut seed));
        let mut pairs = vec![(0i64, 0i64)];
        for _ in 0..20 {
            let a = big(&mut seed) % 100000;
            let b = big(&mut seed) % 100000;
            pairs.push((a, b));
        }
        picks.push(pairs);
    }
    let mut check = 0;
    let mut checks = 0;
    let mut even_odd = 0;
    for (tree, pairs) in trees.iter().zip(picks.iter()) {
        for &(a, b) in pairs.iter() {
            swap_values(&tree[a as usize], &tree[b as usize]);
            let yes = is_even_odd_tree(Some(tree[0].clone()));
            swap_values(&tree[a as usize], &tree[b as usize]);
            if yes {
                even_odd += 1;
            }
            check = mix(check, if yes { 1 } else { 0 });
            checks += 1;
        }
    }
    println!("20 trees of 100000 nodes: {checks} checks, {even_odd} even-odd, checksum {check}");
}
