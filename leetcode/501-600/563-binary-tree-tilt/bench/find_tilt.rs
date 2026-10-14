// Benchmark for #563: Rust mirror of the ★ arm (subtree sums,
// recursively); see find_tilt.kara. The tree is LeetCode's
// `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's `shared`
// struct is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn subtree_sum(node: &Option<Rc<RefCell<TreeNode>>>, total: &mut i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let n = n.borrow();
            let l = subtree_sum(&n.left, total);
            let r = subtree_sum(&n.right, total);
            *total += (l - r).abs();
            n.val + l + r
        }
    }
}

fn find_tilt(root: Option<Rc<RefCell<TreeNode>>>) -> i64 {
    let mut total = 0;
    subtree_sum(&root, &mut total);
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn new_node(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn main() {
    // 20 random trees of 10,000 nodes (the problem's most), each new
    // node walking down from the root and going left with chance 50 to
    // 88 in 100, built once, the nodes kept in the order they were
    // added. Then 1,000 times over every tree the subtree at one of its
    // first 16 nodes, picked by the round and the tree, is answered.
    let trees = 20i64;
    let mut seed: i64 = 563;
    let mut all: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    for g in 0..trees {
        let lean = 50 + 2 * g;
        let root = new_node(next_random(&mut seed) % 2001 - 1000);
        let mut nodes = vec![root.clone()];
        for _ in 1..10000 {
            let c = new_node(next_random(&mut seed) % 2001 - 1000);
            let mut node = root.clone();
            loop {
                let go_left = next_random(&mut seed) % 100 < lean;
                let next = {
                    let mut n = node.borrow_mut();
                    let slot = if go_left { &mut n.left } else { &mut n.right };
                    match slot {
                        Some(x) => Some(x.clone()),
                        None => {
                            *slot = Some(c.clone());
                            None
                        }
                    }
                };
                match next {
                    Some(x) => node = x,
                    None => break,
                }
            }
            nodes.push(c);
        }
        all.push(nodes);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for r in 0..1000i64 {
        for t in 0..trees {
            let k = ((r * 37 + t * 11) % 16) as usize;
            let d = find_tilt(Some(all[t as usize][k].clone()));
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    println!("{trees} trees, 1000 times each: tilts {total}, checksum {checksum}");
}
