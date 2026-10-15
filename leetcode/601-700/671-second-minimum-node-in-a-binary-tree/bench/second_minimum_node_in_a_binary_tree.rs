// Benchmark for #671: a pruned walk, as the Kara ★ arm.
use std::cell::RefCell;
use std::rc::Rc;

struct TreeNode {
    val: i64,
    left: Option<Node>,
    right: Option<Node>,
}

type Node = Rc<RefCell<TreeNode>>;

fn find_second_minimum_value(root: &Option<Node>) -> i64 {
    match root {
        None => -1,
        Some(r) => smallest_above(root, r.borrow().val),
    }
}

fn smallest_above(node: &Option<Node>, low: i64) -> i64 {
    match node {
        None => -1,
        Some(n) => {
            let b = n.borrow();
            if b.val > low {
                return b.val;
            }
            let x = smallest_above(&b.left, low);
            let y = smallest_above(&b.right, low);
            if x == -1 {
                y
            } else if y == -1 {
                x
            } else {
                x.min(y)
            }
        }
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn special(levels: i64, val: i64, spread: i64, seed: &mut i64) -> Node {
    let n = Rc::new(RefCell::new(TreeNode { val, left: None, right: None }));
    if levels > 1 {
        let other = val + next_random(seed) % (spread + 1);
        let l = special(levels - 1, val, spread, seed);
        let r = special(levels - 1, other, spread, seed);
        let mut b = n.borrow_mut();
        b.left = Some(l);
        b.right = Some(r);
    }
    n
}

fn main() {
    let mut seed: i64 = 671;
    let mut trees: Vec<Option<Node>> = Vec::new();
    for t in 0..16 {
        let spread = if t % 4 == 0 { 0 } else { t };
        trees.push(Some(special(16, 7 + t, spread, &mut seed)));
    }
    let rounds: i64 = 2000;
    let mut sum: i64 = 0;
    for r in 0..rounds {
        let s = find_second_minimum_value(&trees[(r % 16) as usize]);
        sum = (sum * 31 + s + 1) % 1000000007;
    }
    println!("16 trees of 65535 nodes, {} rounds: checksum {}", rounds, sum);
}
