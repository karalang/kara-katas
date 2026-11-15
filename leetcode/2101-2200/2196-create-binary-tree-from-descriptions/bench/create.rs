// benchmark's Rust mirror of create.kara (LeetCode #2196, the ★ arm): a
// HashMap of nodes made as named, a HashSet of children.
use std::cell::RefCell;
use std::collections::{HashMap, HashSet};
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn node_of(nodes: &mut HashMap<i64, Node>, v: i64) -> Node {
    if let Some(n) = nodes.get(&v) {
        return n.clone();
    }
    let n = leaf(v);
    nodes.insert(v, n.clone());
    n
}

fn create_binary_tree(descriptions: &[[i64; 3]]) -> Option<Node> {
    let mut nodes: HashMap<i64, Node> = HashMap::new();
    let mut children: HashSet<i64> = HashSet::new();
    for d in descriptions {
        let parent = node_of(&mut nodes, d[0]);
        let child = node_of(&mut nodes, d[1]);
        if d[2] == 1 {
            parent.borrow_mut().left = Some(child);
        } else {
            parent.borrow_mut().right = Some(child);
        }
        children.insert(d[1]);
    }
    for d in descriptions {
        if !children.contains(&d[0]) {
            return nodes.get(&d[0]).cloned();
        }
    }
    None
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn random_descriptions(seed: &mut i64) -> Vec<[i64; 3]> {
    let n = 10001usize;
    let mut values: Vec<i64> = (1..100001).collect();
    for i in 0..n {
        let j = i + (wide_random(seed) % (100000 - i as i64)) as usize;
        values.swap(i, j);
    }
    let mut free: Vec<(usize, i64)> = vec![(0, 1), (0, 0)];
    let mut descriptions: Vec<[i64; 3]> = Vec::new();
    for k in 1..n {
        let pick = (wide_random(seed) % free.len() as i64) as usize;
        let (p, side) = free.swap_remove(pick);
        descriptions.push([values[p], values[k], side]);
        free.push((k, 1));
        free.push((k, 0));
    }
    for i in (1..descriptions.len()).rev() {
        let j = (wide_random(seed) % (i as i64 + 1)) as usize;
        descriptions.swap(i, j);
    }
    descriptions
}

fn weigh(root: Option<Node>) -> (i64, i64) {
    let mut stack: Vec<(Node, i64)> = Vec::new();
    if let Some(r) = root {
        stack.push((r, 1));
    }
    let (mut count, mut weight) = (0i64, 0i64);
    while let Some((n, depth)) = stack.pop() {
        let n = n.borrow();
        count += 1;
        weight += n.val * depth;
        if let Some(l) = &n.left {
            stack.push((l.clone(), depth + 1));
        }
        if let Some(r) = &n.right {
            stack.push((r.clone(), depth + 1));
        }
    }
    (count, weight)
}

fn main() {
    let mut seed = 2196;
    let sets: Vec<Vec<[i64; 3]>> = (0..20).map(|_| random_descriptions(&mut seed)).collect();
    let mut check: i64 = 0;
    for _ in 0..50 {
        for d in &sets {
            let (count, weight) = weigh(create_binary_tree(d));
            check = (check * 31 + count + weight % 1000000007) % 1000000007;
        }
    }
    println!("50 passes over 20 trees: checksum {}", check);
}
