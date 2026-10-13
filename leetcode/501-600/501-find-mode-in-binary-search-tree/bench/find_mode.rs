// Benchmark for #501: Rust mirror of the ★ arm (in-order with a running
// count); see find_mode.kara. The tree is `Rc<RefCell<TreeNode>>`, the
// closest match to a `shared struct`.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Rc<RefCell<TreeNode>>>,
    right: Option<Rc<RefCell<TreeNode>>>,
}

type Node = Option<Rc<RefCell<TreeNode>>>;

struct Walk {
    prev: i64,
    run: i64,
    best: i64,
    modes: Vec<i64>,
}

fn visit(node: &Node, walk: &mut Walk) {
    let Some(n) = node else {
        return;
    };
    let n = n.borrow();
    visit(&n.left, walk);
    if walk.run > 0 && n.val == walk.prev {
        walk.run += 1;
    } else {
        walk.prev = n.val;
        walk.run = 1;
    }
    if walk.run > walk.best {
        walk.best = walk.run;
        walk.modes.clear();
        walk.modes.push(n.val);
    } else if walk.run == walk.best {
        walk.modes.push(n.val);
    }
    visit(&n.right, walk);
}

fn find_mode(root: &Node) -> Vec<i64> {
    let mut walk = Walk { prev: 0, run: 0, best: 0, modes: Vec::new() };
    visit(root, &mut walk);
    walk.modes
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
    // 100 random search trees of 10,000 values, drawn from 1 to 10
    // values, 1,000 values, or the whole range -100,000 to 100,000 in
    // turn, built once. Then the modes of each tree are found 30 times.
    let trees = 100;
    let mut seed: i64 = 501;
    let mut all: Vec<Node> = Vec::new();
    for t in 0..trees {
        let range = if t % 3 == 0 { 1 + next_random(&mut seed) % 10 } else if t % 3 == 1 { 1000 } else { 200001 };
        let mut values: Vec<i64> = Vec::new();
        for _ in 0..10000 {
            let v = next_random(&mut seed) * 7 % range;
            values.push(if range == 200001 { v - 100000 } else { v });
        }
        all.push(build(&values, &mut seed));
    }
    let mut modes = 0i64;
    let mut checksum: i64 = 0;
    for _ in 0..30 {
        for t in 0..trees {
            for m in find_mode(&all[t]) {
                modes += 1;
                checksum = (checksum * 31 + m + 100000) % 1000000007;
            }
        }
    }
    println!("{} trees of 10000 values, 30 times each: {} modes, checksum {}", trees, modes, checksum);
}
