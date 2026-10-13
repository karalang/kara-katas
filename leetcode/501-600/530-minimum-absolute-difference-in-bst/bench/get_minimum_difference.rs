// Benchmark for #530: Rust mirror of the ★ arm (in-order, recursively);
// see get_minimum_difference.kara. The tree is `Rc<RefCell<TreeNode>>`,
// the closest match to a `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

struct Walk {
    prev: Option<i64>,
    best: i64,
}

fn visit(node: &Node, walk: &mut Walk) {
    let Some(n) = node else {
        return;
    };
    let n = n.borrow();
    visit(&n.left, walk);
    if let Some(p) = walk.prev {
        walk.best = walk.best.min(n.val - p);
    }
    walk.prev = Some(n.val);
    visit(&n.right, walk);
}

fn get_minimum_difference(root: &Node) -> i64 {
    let mut walk = Walk { prev: None, best: i64::MAX };
    visit(root, &mut walk);
    walk.best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn fresh(v: i64) -> Rc<RefCell<TreeNode>> {
    Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
}

fn build(values: &[i64], seed: &mut i64) -> Node {
    let root = fresh(values[0]);
    for &v in &values[1..] {
        let mut node = root.clone();
        loop {
            let go_left = {
                let val = node.borrow().val;
                v < val || (v == val && next_random(seed) % 2 == 0)
            };
            let next = if go_left { node.borrow().left.clone() } else { node.borrow().right.clone() };
            match next {
                Some(child) => node = child,
                None => {
                    if go_left {
                        node.borrow_mut().left = Some(fresh(v));
                    } else {
                        node.borrow_mut().right = Some(fresh(v));
                    }
                    break;
                }
            }
        }
    }
    Some(root)
}

fn main() {
    // 100 random search trees of 10,000 different values, drawn from 0
    // to 10,000, 0 to 20,000, ... up to 0 to 100,000 in turn, built once.
    // Then the answer for each tree is found 50 times.
    let trees: usize = 100;
    let mut seed: i64 = 530;
    let mut all: Vec<Node> = Vec::new();
    for t in 0..trees {
        let range = 10000 * (1 + (t % 10) as i64) + 1;
        let mut pool: Vec<i64> = (0..range).collect();
        for i in 0..10000 {
            let high = next_random(&mut seed);
            let j = i + (high * 32768 + next_random(&mut seed)) % (range - i);
            pool.swap(i as usize, j as usize);
        }
        pool.truncate(10000);
        all.push(build(&pool, &mut seed));
    }
    let mut total = 0i64;
    let mut checksum: i64 = 0;
    for _ in 0..50 {
        for t in 0..trees {
            let answer = get_minimum_difference(&all[t]);
            total += answer;
            checksum = (checksum * 31 + answer) % 1000000007;
        }
    }
    println!("{} trees of 10000 values, 50 times each: total {}, checksum {}", trees, total, checksum);
}
