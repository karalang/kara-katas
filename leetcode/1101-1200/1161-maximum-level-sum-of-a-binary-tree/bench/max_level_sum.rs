// LeetCode #1161: Maximum Level Sum of a Binary Tree -- the bench in Rust,
// the ★ arm over LeetCode's own `Rc<RefCell<TreeNode>>`, the same 16 trees
// and 200 rounds. Each level's nodes go in a fresh `Vec`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i32,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn max_level_sum(root: Option<Node>) -> i64 {
    let mut level: Vec<Node> = Vec::new();
    if let Some(r) = root {
        level.push(r);
    }
    let (mut best, mut best_sum, mut depth) = (0i64, 0i64, 0i64);
    while !level.is_empty() {
        depth += 1;
        let mut sum = 0i64;
        let mut next: Vec<Node> = Vec::new();
        for node in &level {
            let n = node.borrow();
            sum += n.val as i64;
            if let Some(l) = &n.left {
                next.push(Rc::clone(l));
            }
            if let Some(r) = &n.right {
                next.push(Rc::clone(r));
            }
        }
        if best == 0 || sum > best_sum {
            best = depth;
            best_sum = sum;
        }
        level = next;
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i32 {
    let a = next_random(seed);
    let b = next_random(seed);
    ((a * 32768 + b) % 200001 - 100000) as i32
}

fn new_node(val: i32) -> Node {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn grow(nodes: &mut Vec<Node>, seed: &mut i64) {
    let c = new_node(random_value(seed));
    loop {
        let at = Rc::clone(&nodes[(next_random(seed) % nodes.len() as i64) as usize]);
        let mut a = at.borrow_mut();
        if next_random(seed) % 2 == 0 {
            if a.left.is_none() {
                a.left = Some(Rc::clone(&c));
                break;
            }
        } else if a.right.is_none() {
            a.right = Some(Rc::clone(&c));
            break;
        }
    }
    nodes.push(c);
}

fn main() {
    let mut seed: i64 = 1161;
    let mut trees: Vec<Vec<Node>> = Vec::new();
    for _ in 0..16 {
        let mut nodes = vec![new_node(random_value(&mut seed))];
        for _ in 1..10000 {
            grow(&mut nodes, &mut seed);
        }
        trees.push(nodes);
    }
    let (mut total, mut check) = (0i64, 0i64);
    for _ in 0..200 {
        for j in 0..trees.len() {
            grow(&mut trees[j], &mut seed);
            let level = max_level_sum(Some(Rc::clone(&trees[j][0])));
            total += level;
            check = (check * 31 + level) % 1000000007;
        }
    }
    println!("200 rounds over 16 trees of 10^4 nodes: levels total {}, checksum {}", total, check);
}
