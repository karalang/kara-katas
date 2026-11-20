// LeetCode #1261 bench, in Rust: the ★ arm (the tree recovered from the
// root down, every value kept in a hash set) on 20 random contaminated trees
// of 10000 nodes, at most 20 levels deep, built once; 120 rounds, each tree
// recovered again and asked 10000 targets, half of them nodes' places;
// the targets found counted and folded into a checksum.
// The tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`, as Kāra's
// `shared struct` is reference counted.

use std::cell::RefCell;
use std::collections::{BTreeSet, HashSet};
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn recover(node: &Option<Rc<RefCell<TreeNode>>>, value: i64, values: &mut HashSet<i64>) {
    if let Some(n) = node {
        let mut n = n.borrow_mut();
        n.val = value;
        values.insert(value);
        recover(&n.left, 2 * value + 1, values);
        recover(&n.right, 2 * value + 2, values);
    }
}

struct FindElements {
    values: HashSet<i64>,
}

impl FindElements {
    fn new(root: &Option<Rc<RefCell<TreeNode>>>) -> Self {
        let mut values = HashSet::new();
        recover(root, 0, &mut values);
        FindElements { values }
    }

    fn find(&self, target: i64) -> bool {
        self.values.contains(&target)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build(present: &BTreeSet<i64>, at: i64) -> Option<Rc<RefCell<TreeNode>>> {
    if !present.contains(&at) {
        return None;
    }
    Some(Rc::new(RefCell::new(TreeNode {
        val: -1,
        left: build(present, 2 * at + 1),
        right: build(present, 2 * at + 2),
    })))
}

fn random_places(n: usize, seed: &mut i64) -> BTreeSet<i64> {
    let mut places = vec![0i64];
    let mut present = BTreeSet::new();
    present.insert(0);
    while places.len() < n {
        let p = places[(next_random(seed) % places.len() as i64) as usize];
        let child = 2 * p + 1 + next_random(seed) % 2;
        if child < 2097151 && !present.contains(&child) {
            present.insert(child);
            places.push(child);
        }
    }
    present
}

fn main() {
    let mut seed = 1261;
    let mut trees = Vec::new();
    let mut targets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let present = random_places(10000, &mut seed);
        let places: Vec<i64> = present.iter().cloned().collect();
        let deepest = places[places.len() - 1];
        trees.push(build(&present, 0));
        targets.push(
            (0..10000)
                .map(|q| {
                    if q % 2 == 0 {
                        places[(next_random(&mut seed) % 10000) as usize]
                    } else {
                        next_random(&mut seed) * 64 % (deepest + 1)
                    }
                })
                .collect(),
        );
    }
    let mut found = 0;
    let mut check: i64 = 0;
    for _ in 0..120 {
        for t in 0..20 {
            let tree = FindElements::new(&trees[t]);
            for &target in &targets[t] {
                if tree.find(target) {
                    found += 1;
                    check = (check * 131 + target) % 1000000007;
                }
            }
        }
    }
    println!("120 rounds of 20 trees of 10000 nodes: {found} found, checksum {check}");
}
