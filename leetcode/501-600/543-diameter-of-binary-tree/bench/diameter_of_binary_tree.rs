// Benchmark for #543: Rust mirror of the ★ arm (heights, recursively);
// see diameter_of_binary_tree.kara. The tree is LeetCode's
// `Option<Rc<RefCell<TreeNode>>>`, reference counted as Kāra's `shared`
// struct is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    #[allow(dead_code)]
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

fn height(node: &Option<Rc<RefCell<TreeNode>>>, best: &mut i64) -> i64 {
    match node {
        None => 0,
        Some(n) => {
            let n = n.borrow();
            let l = height(&n.left, best);
            let r = height(&n.right, best);
            if l + r > *best {
                *best = l + r;
            }
            1 + l.max(r)
        }
    }
}

fn diameter_of_binary_tree(root: Option<Rc<RefCell<TreeNode>>>) -> i64 {
    let mut best = 0;
    height(&root, &mut best);
    best
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
    // added. Then 200 times over every tree the subtree at one of its
    // first 16 nodes, picked by the round and the tree, is answered.
    let trees = 20i64;
    let mut seed: i64 = 543;
    let mut all: Vec<Vec<Rc<RefCell<TreeNode>>>> = Vec::new();
    for g in 0..trees {
        let lean = 50 + 2 * g;
        let root = new_node(next_random(&mut seed) % 201 - 100);
        let mut nodes = vec![root.clone()];
        for _ in 1..10000 {
            let c = new_node(next_random(&mut seed) % 201 - 100);
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
    for r in 0..200i64 {
        for t in 0..trees {
            let k = ((r * 37 + t * 11) % 16) as usize;
            let d = diameter_of_binary_tree(Some(all[t as usize][k].clone()));
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    println!("{trees} trees, 200 times each: diameters {total}, checksum {checksum}");
}
