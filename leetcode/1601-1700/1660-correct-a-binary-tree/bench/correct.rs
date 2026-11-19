// LeetCode #1660: Correct a Binary Tree -- the bench's Rust mirror: the
// ★ arm on 40 random trees of 100000 nodes, each broken once, all built
// first. Nodes are `Rc<RefCell<TreeNode>>`, as Kāra's `shared struct` is,
// and the values met are a `HashSet`.

use std::cell::RefCell;
use std::collections::{HashSet, VecDeque};
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Handle = Rc<RefCell<TreeNode>>;

fn leaf(val: i32) -> Handle {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn correct(node: Option<Handle>, seen: &mut HashSet<i32>) -> Option<Handle> {
    let node = node?;
    let right = node.borrow().right.clone();
    if let Some(r) = &right {
        if seen.contains(&r.borrow().val) {
            return None;
        }
    }
    seen.insert(node.borrow().val);
    let fixed = correct(right, seen);
    node.borrow_mut().right = fixed;
    let left = node.borrow().left.clone();
    let fixed = correct(left, seen);
    node.borrow_mut().left = fixed;
    Some(node)
}

fn correct_binary_tree(root: Option<Handle>) -> Option<Handle> {
    let mut seen = HashSet::new();
    correct(root, &mut seen)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn big(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn random_tree(n: i64, seed: &mut i64) -> Handle {
    let mut values: Vec<i32> = (0..n as i32).collect();
    for i in (1..n as usize).rev() {
        let j = (big(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let root = leaf(values[0]);
    let mut free: Vec<(Handle, bool)> = vec![(Rc::clone(&root), true), (Rc::clone(&root), false)];
    for i in 1..n as usize {
        let k = (big(seed) % free.len() as i64) as usize;
        let (parent, left) = free.swap_remove(k);
        let child = leaf(values[i]);
        if left {
            parent.borrow_mut().left = Some(Rc::clone(&child));
        } else {
            parent.borrow_mut().right = Some(Rc::clone(&child));
        }
        free.push((Rc::clone(&child), true));
        free.push((child, false));
    }
    root
}

fn break_tree(root: &Handle, seed: &mut i64) -> Option<(i32, i32)> {
    let mut pairs: i64 = 0;
    let mut level = vec![Rc::clone(root)];
    let mut levels: Vec<Vec<Handle>> = Vec::new();
    while !level.is_empty() {
        let mut below = Vec::new();
        for (i, node) in level.iter().enumerate() {
            let b = node.borrow();
            if b.right.is_none() {
                pairs += (level.len() - 1 - i) as i64;
            }
            if let Some(l) = &b.left {
                below.push(Rc::clone(l));
            }
            if let Some(r) = &b.right {
                below.push(Rc::clone(r));
            }
        }
        levels.push(level);
        level = below;
    }
    if pairs == 0 {
        return None;
    }
    let mut k = big(seed) % pairs;
    for level in &levels {
        for (i, node) in level.iter().enumerate() {
            if node.borrow().right.is_none() {
                let after = (level.len() - 1 - i) as i64;
                if k < after {
                    let to = Rc::clone(&level[i + 1 + k as usize]);
                    let pair = (node.borrow().val, to.borrow().val);
                    node.borrow_mut().right = Some(to);
                    return Some(pair);
                }
                k -= after;
            }
        }
    }
    None
}

fn fold(root: Option<Handle>, check: &mut i64) -> i64 {
    let mut count = 0;
    let mut queue: VecDeque<Option<Handle>> = VecDeque::new();
    queue.push_back(root);
    while let Some(slot) = queue.pop_front() {
        match slot {
            Some(node) => {
                count += 1;
                let b = node.borrow();
                *check = mix(*check, b.val as i64 + 1);
                queue.push_back(b.left.clone());
                queue.push_back(b.right.clone());
            }
            None => *check = mix(*check, 0),
        }
    }
    count
}

fn main() {
    let mut seed: i64 = 1660;
    let mut roots: Vec<Handle> = Vec::new();
    while roots.len() < 40 {
        let root = random_tree(100000, &mut seed);
        if break_tree(&root, &mut seed).is_some() {
            roots.push(root);
        }
    }
    let mut check: i64 = 0;
    let mut kept: i64 = 0;
    for root in &roots {
        kept += fold(correct_binary_tree(Some(Rc::clone(root))), &mut check);
    }
    println!("40 trees of 100000 nodes: {} nodes kept, checksum {}", kept, check);
}
