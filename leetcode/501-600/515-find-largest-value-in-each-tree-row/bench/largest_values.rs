// Benchmark for #515: Rust mirror of the ★ arm (level by level); see
// largest_values.kara. The tree is `Rc<RefCell<TreeNode>>`, the closest
// match to a `shared struct`, and the queue a fresh `VecDeque`
// for every call.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Handle = Rc<RefCell<TreeNode>>;

fn largest_values(root: Option<&Handle>) -> Vec<i64> {
    let mut largest: Vec<i64> = Vec::new();
    let mut queue: VecDeque<Handle> = VecDeque::new();
    if let Some(r) = root {
        queue.push_back(r.clone());
    }
    while !queue.is_empty() {
        let mut best = i64::MIN;
        for _ in 0..queue.len() {
            let node = queue.pop_front().unwrap();
            let n = node.borrow();
            best = best.max(n.val);
            if let Some(l) = &n.left {
                queue.push_back(l.clone());
            }
            if let Some(r) = &n.right {
                queue.push_back(r.clone());
            }
        }
        largest.push(best);
    }
    largest
}

// ---- benchmark --------------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn build(values: &[i64], lo: i64, hi: i64, seed: &mut i64) -> Option<Handle> {
    if lo >= hi {
        return None;
    }
    let mid = lo + next_random(seed) % (hi - lo);
    let left = build(values, lo, mid, seed);
    let right = build(values, mid + 1, hi, seed);
    Some(Rc::new(RefCell::new(TreeNode { val: values[mid as usize], left, right })))
}

fn main() {
    // 100 random trees of 10,000 nodes, the values from the whole range
    // -2^31 to 2^31 - 1, built once. Then each is solved 50 times.
    let trees = 100;
    let mut seed: i64 = 515;
    let mut all: Vec<Handle> = Vec::new();
    for _ in 0..trees {
        let mut values: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            let a = next_random(&mut seed);
            let b = next_random(&mut seed);
            let c = next_random(&mut seed);
            values.push(a * 65536 + b * 2 + c % 2 - 2147483648);
        }
        all.push(build(&values, 0, 10000, &mut seed).unwrap());
    }
    let mut rows: usize = 0;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for t in 0..trees {
            let largest = largest_values(Some(&all[t]));
            rows += largest.len();
            for v in largest.iter() {
                checksum = (checksum * 31 + *v + 2147483648) % 1000000007;
            }
        }
    }
    println!("{} trees of 10000 nodes, 50 times each: {} rows, checksum {}", trees, rows, checksum);
}
