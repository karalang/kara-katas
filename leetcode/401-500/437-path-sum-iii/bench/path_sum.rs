// Benchmark for #437: mirror of path_sum.kara (prefix sums along the
// path) on one random tree of 100,000 nodes, queried for 200 targets.
// The nodes are Rc<RefCell<TreeNode>>, as a Kāra shared struct is
// reference counted, and std's HashMap hashes with SipHash-1-3 under a
// random key, as Kāra's Map does.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Tree = Option<Rc<RefCell<TreeNode>>>;

fn count_from(node: &Tree, prefix: i64, target: i64, seen: &mut HashMap<i64, i64>) -> i64 {
    match node {
        None => 0,
        Some(t) => {
            let t = t.borrow();
            let sum = prefix + t.val;
            let mut found = *seen.get(&(sum - target)).unwrap_or(&0);
            *seen.entry(sum).or_insert(0) += 1;
            found += count_from(&t.left, sum, target, seen);
            found += count_from(&t.right, sum, target, seen);
            *seen.entry(sum).or_insert(0) -= 1;
            found
        }
    }
}

fn path_sum(root: &Tree, target: i64) -> i64 {
    let mut seen: HashMap<i64, i64> = HashMap::new();
    seen.insert(0, 1);
    count_from(root, 0, target, &mut seen)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(val: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val, left: None, right: None }))
}

fn main() {
    let size = 100000;
    let queries = 200;
    let mut seed: i64 = 437;
    // Each node hangs under a random earlier node that still has a free
    // side, values in [-1000, 1000].
    let root = leaf(next_random(&mut seed) % 2001 - 1000);
    let mut open: Vec<Rc<RefCell<TreeNode>>> = vec![root.clone()];
    for _ in 1..size {
        let at = (next_random(&mut seed) % open.len() as i64) as usize;
        let parent = open[at].clone();
        let child = leaf(next_random(&mut seed) % 2001 - 1000);
        {
            let mut p = parent.borrow_mut();
            if p.left.is_none() && (p.right.is_some() || next_random(&mut seed) % 2 == 0) {
                p.left = Some(child.clone());
            } else {
                p.right = Some(child.clone());
            }
        }
        let full = {
            let p = parent.borrow();
            p.left.is_some() && p.right.is_some()
        };
        if full {
            open.swap_remove(at);
        }
        open.push(child);
    }
    let tree: Tree = Some(root);
    let mut total = 0;
    let mut checksum: i64 = 0;
    for _ in 0..queries {
        let target = next_random(&mut seed) % 4001 - 2000;
        let count = path_sum(&tree, target);
        total += count;
        checksum = (checksum * 31 + count) % 1000000007;
    }
    println!("{} targets on a tree of {}: {} paths, checksum {}", queries, size, total, checksum);
}
