// Benchmark for #814: Binary Tree Pruning -- mirror of the ★ arm
// (post-order recursion), with the same workload as prune_tree.kara. The
// tree is `Rc<RefCell<TreeNode>>`, LeetCode's Rust signature and the
// closest match to a `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

fn prune_tree(root: Node) -> Node {
    let node = root?;
    let left = node.borrow_mut().left.take();
    let right = node.borrow_mut().right.take();
    let left = prune_tree(left);
    let right = prune_tree(right);
    let empty = {
        let mut n = node.borrow_mut();
        n.left = left;
        n.right = right;
        n.val == 0 && n.left.is_none() && n.right.is_none()
    };
    if empty {
        None
    } else {
        Some(node)
    }
}

fn build(vals: &[i64], left: &[i64], right: &[i64], i: i64) -> Node {
    if i < 0 {
        return None;
    }
    let l = build(vals, left, right, left[i as usize]);
    let r = build(vals, left, right, right[i as usize]);
    Some(Rc::new(RefCell::new(TreeNode {
        val: vals[i as usize],
        left: l,
        right: r,
    })))
}

fn weigh(root: &Node, depth: i64) -> i64 {
    match root {
        Some(node) => {
            let n = node.borrow();
            (n.val + 1) * depth + weigh(&n.left, depth + 1) + weigh(&n.right, depth + 1)
        }
        None => 0,
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let n: i64 = 200;
    let rounds: i64 = 300000;
    let mut seed: i64 = 814;
    let mut vals: Vec<Vec<i64>> = Vec::new();
    let mut lefts: Vec<Vec<i64>> = Vec::new();
    let mut rights: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let mut v: Vec<i64> = Vec::new();
        for _ in 0..n {
            v.push(if next_random(&mut seed) % 8 == 0 {
                1
            } else {
                0
            });
        }
        let mut l = vec![-1i64; n as usize];
        let mut r = vec![-1i64; n as usize];
        for i in 1..n {
            loop {
                let p = (next_random(&mut seed) % i) as usize;
                if next_random(&mut seed) % 2 == 0 {
                    if l[p] < 0 {
                        l[p] = i;
                        break;
                    }
                } else if r[p] < 0 {
                    r[p] = i;
                    break;
                }
            }
        }
        vals.push(v);
        lefts.push(l);
        rights.push(r);
    }
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let g = (round % count as i64) as usize;
        let i = (next_random(&mut seed) % n) as usize;
        vals[g][i] = 1 - vals[g][i];
        let root = prune_tree(build(&vals[g], &lefts[g], &rights[g], 0));
        checksum = (checksum * 31 + weigh(&root, 1)) % 1000000007;
    }
    println!("{} rounds of {} nodes: checksum {}", rounds, n, checksum);
}
