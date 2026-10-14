// Benchmark mirror for #617: the same workload and algorithm as
// merge_trees.kara (recursion, a new tree). The tree is LeetCode's
// `Option<Rc<RefCell<TreeNode>>>`; a subtree only one tree has is shared
// with an `Rc` clone, as the Kāra arm shares the `shared struct` node.
use std::cell::RefCell;
use std::rc::Rc;

type Tree = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Tree,
    right: Tree,
}

fn merge_trees(root1: &Tree, root2: &Tree) -> Tree {
    match (root1, root2) {
        (Some(a), Some(b)) => {
            let (a, b) = (a.borrow(), b.borrow());
            Some(Rc::new(RefCell::new(TreeNode {
                val: a.val + b.val,
                left: merge_trees(&a.left, &b.left),
                right: merge_trees(&a.right, &b.right),
            })))
        }
        (Some(a), None) => Some(a.clone()),
        (None, other) => other.clone(),
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn random_tree(size: i64, lean: i64, seed: &mut i64) -> Tree {
    let root = leaf(next_random(seed) % 20001 - 10000);
    for _ in 1..size {
        let c = leaf(next_random(seed) % 20001 - 10000);
        let mut node = root.clone();
        loop {
            let go_left = next_random(seed) % 100 < lean;
            let next = {
                let mut n = node.borrow_mut();
                let slot = if go_left { &mut n.left } else { &mut n.right };
                match slot {
                    Some(child) => child.clone(),
                    None => {
                        *slot = Some(c.clone());
                        break;
                    }
                }
            };
            node = next;
        }
    }
    Some(root)
}

fn walk(node: &Tree, count: &mut i64, h: &mut i64) {
    if let Some(n) = node {
        let n = n.borrow();
        *count += 1;
        *h = (*h * 31 + n.val + 20000) % 1000000007;
        walk(&n.left, count, h);
        walk(&n.right, count, h);
    }
}

fn main() {
    let trees = 20i64;
    let rounds = 10000i64;
    let mut seed: i64 = 617;
    let mut all: Vec<Tree> = Vec::new();
    for _ in 0..trees {
        let lean = 30 + next_random(&mut seed) % 41;
        all.push(random_tree(2000, lean, &mut seed));
    }
    let (mut count, mut checksum) = (0i64, 0i64);
    for r in 0..rounds {
        let merged = merge_trees(&all[((r * 7) % trees) as usize], &all[((r * 3 + 1) % trees) as usize]);
        walk(&merged, &mut count, &mut checksum);
    }
    println!("{} trees, {} rounds: {} nodes, checksum {}", trees, rounds, count, checksum);
}
