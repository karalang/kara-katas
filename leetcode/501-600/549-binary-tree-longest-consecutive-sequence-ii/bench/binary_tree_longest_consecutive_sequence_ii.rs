// Benchmark for #549: Rust mirror of the ★ arm (post-order, two lengths
// a node); see binary_tree_longest_consecutive_sequence_ii.kara. The
// tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`, reference counted
// as Kāra's `shared` struct is.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Rc<RefCell<TreeNode>>;

fn walk(node: &Node, best: &mut i64) -> (i64, i64) {
    let n = node.borrow();
    let mut rise = 1;
    let mut fall = 1;
    if let Some(l) = &n.left {
        let (r1, f1) = walk(l, best);
        let lv = l.borrow().val;
        if lv == n.val + 1 {
            rise = r1 + 1;
        } else if lv == n.val - 1 {
            fall = f1 + 1;
        }
    }
    if let Some(r) = &n.right {
        let (r2, f2) = walk(r, best);
        let rv = r.borrow().val;
        if rv == n.val + 1 {
            rise = rise.max(r2 + 1);
        } else if rv == n.val - 1 {
            fall = fall.max(f2 + 1);
        }
    }
    *best = (*best).max(rise + fall - 1);
    (rise, fall)
}

fn longest_consecutive(root: Option<Node>) -> i64 {
    let mut best = 0;
    if let Some(n) = root {
        walk(&n, &mut best);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn leaf(v: i64) -> Node {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn main() {
    let count = 20;
    let mut seed: i64 = 549;
    let mut firsts: Vec<Vec<Node>> = Vec::new();
    for g in 0..count {
        let spread = 3 + (g % 4) as i64;
        let root = leaf(next_random(&mut seed) % spread);
        let mut kept = vec![root.clone()];
        for _ in 1..30000 {
            let c = leaf(next_random(&mut seed) % spread);
            let mut node = root.clone();
            loop {
                let go_left = next_random(&mut seed) % 2 == 0;
                let next = {
                    let b = node.borrow();
                    if go_left { b.left.clone() } else { b.right.clone() }
                };
                match next {
                    Some(n) => node = n,
                    None => {
                        let mut b = node.borrow_mut();
                        if go_left {
                            b.left = Some(c.clone());
                        } else {
                            b.right = Some(c.clone());
                        }
                        break;
                    }
                }
            }
            if kept.len() < 16 {
                kept.push(c);
            }
        }
        firsts.push(kept);
    }
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for round in 0..60 {
        for g in 0..count {
            let n = firsts[g][(round * 7 + g) % 16].clone();
            let d = longest_consecutive(Some(n));
            total += d;
            checksum = (checksum * 31 + d) % 1000000007;
        }
    }
    println!("{} trees, 60 rounds each: lengths {}, checksum {}", count, total, checksum);
}
