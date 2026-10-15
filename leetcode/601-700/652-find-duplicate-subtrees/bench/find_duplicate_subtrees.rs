// Benchmark for #652: a number for every shape, as the Kara ★ arm.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn find_duplicate_subtrees(root: Option<Node>) -> Vec<Node> {
    let mut ids: HashMap<(i64, i64, i64), i64> = HashMap::new();
    let mut counts: Vec<i64> = Vec::new();
    let mut found: Vec<Node> = Vec::new();
    number(&root, &mut ids, &mut counts, &mut found);
    found
}

fn number(
    node: &Option<Node>,
    ids: &mut HashMap<(i64, i64, i64), i64>,
    counts: &mut Vec<i64>,
    found: &mut Vec<Node>,
) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let b = n.borrow();
            let key = (b.val, number(&b.left, ids, counts, found), number(&b.right, ids, counts, found));
            let id = match ids.get(&key) {
                Some(i) => *i,
                None => {
                    counts.push(0);
                    ids.insert(key, counts.len() as i64);
                    counts.len() as i64
                }
            };
            counts[id as usize - 1] += 1;
            if counts[id as usize - 1] == 2 {
                found.push(n.clone());
            }
            id
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(size: i64, spread: i64, seed: &mut i64) -> Option<Node> {
    let leaf = |v: i64| Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }));
    let root = leaf(next_random(seed) % spread);
    for _ in 1..size {
        let c = leaf(next_random(seed) % spread);
        let mut node = root.clone();
        loop {
            let next = if next_random(seed) % 2 == 0 {
                let mut b = node.borrow_mut();
                match &b.left {
                    Some(l) => l.clone(),
                    None => {
                        b.left = Some(c);
                        break;
                    }
                }
            } else {
                let mut b = node.borrow_mut();
                match &b.right {
                    Some(r) => r.clone(),
                    None => {
                        b.right = Some(c);
                        break;
                    }
                }
            };
            node = next;
        }
    }
    Some(root)
}

fn main() {
    let inputs = 4usize;
    let rounds = 40usize;
    let spreads = [2, 3, 5, 401];
    let mut seed: i64 = 652;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for i in 0..inputs {
        trees.push(random_tree(100000, spreads[i], &mut seed));
    }
    let mut kinds = 0;
    let mut checksum: i64 = 0;
    for r in 0..rounds {
        let found = find_duplicate_subtrees(trees[r % inputs].clone());
        kinds += found.len();
        for n in found.iter() {
            checksum = (checksum * 31 + n.borrow().val + 1) % 1000000007;
        }
    }
    println!("{inputs} trees, {rounds} rounds: {kinds} kinds, checksum {checksum}");
}
