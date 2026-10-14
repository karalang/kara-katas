// Benchmark mirror for #637: the same workload and algorithm as
// average_of_levels.kara (breadth first with a deque, one level at a
// time). The tree is LeetCode's `Option<Rc<RefCell<TreeNode>>>`, as the
// Kāra arm's `shared struct` node is reference-counted.
use std::cell::RefCell;
use std::collections::VecDeque;
use std::rc::Rc;

type Tree = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i64,
    left: Tree,
    right: Tree,
}

fn average_of_levels(root: &Tree) -> Vec<f64> {
    let mut averages = Vec::new();
    let mut queue: VecDeque<Rc<RefCell<TreeNode>>> = VecDeque::new();
    if let Some(r) = root {
        queue.push_back(r.clone());
    }
    while !queue.is_empty() {
        let count = queue.len();
        let mut sum: i64 = 0;
        for _ in 0..count {
            let node = queue.pop_front().unwrap();
            let n = node.borrow();
            sum += n.val;
            if let Some(l) = &n.left {
                queue.push_back(l.clone());
            }
            if let Some(r) = &n.right {
                queue.push_back(r.clone());
            }
        }
        averages.push(sum as f64 / count as f64);
    }
    averages
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_value(seed: &mut i64) -> i64 {
    let high = next_random(seed) % 65536;
    let low = next_random(seed) % 65536;
    high * 65536 + low - 2147483648
}

fn random_tree(size: i64, seed: &mut i64) -> Tree {
    let mut root: Tree = None;
    for _ in 0..size {
        let c = Rc::new(RefCell::new(TreeNode { val: random_value(seed), left: None, right: None }));
        match &root {
            None => root = Some(c),
            Some(r) => {
                let mut node = r.clone();
                loop {
                    let left = next_random(seed) % 2 == 0;
                    let next = {
                        let n = node.borrow();
                        if left { n.left.clone() } else { n.right.clone() }
                    };
                    match next {
                        Some(child) => node = child,
                        None => {
                            if left {
                                node.borrow_mut().left = Some(c);
                            } else {
                                node.borrow_mut().right = Some(c);
                            }
                            break;
                        }
                    }
                }
            }
        }
    }
    root
}

fn main() {
    let mut seed: i64 = 637;
    let trees: Vec<Tree> = (0..10).map(|_| random_tree(10000, &mut seed)).collect();
    let mut levels = 0;
    let mut total = 0.0f64;
    for round in 0..4000 {
        for a in average_of_levels(&trees[round % 10]) {
            levels += 1;
            total += a;
        }
    }
    println!("10 trees of 10000 nodes, 4000 rounds: {levels} levels, sum of averages {total:.3}");
}
