// LeetCode #2385: Amount of Time for Binary Tree to Be Infected -- the
// bench, the ★ arm in Rust: one post-order walk returning each subtree's
// height and the start's distance below it. The nodes are
// `Rc<RefCell<TreeNode>>`, LeetCode's and the model of Kāra's `shared
// struct`.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i32,
    left: Link,
    right: Link,
}

fn walk(node: &Link, start: i64, best: &mut i64) -> (i64, i64) {
    let Some(n) = node else {
        return (0, -1);
    };
    let n = n.borrow();
    let (lh, ld) = walk(&n.left, start, best);
    let (rh, rd) = walk(&n.right, start, best);
    let height = 1 + lh.max(rh);
    if n.val as i64 == start {
        *best = (*best).max(lh.max(rh));
        (height, 0)
    } else if ld >= 0 {
        *best = (*best).max(ld + 1 + rh);
        (height, ld + 1)
    } else if rd >= 0 {
        *best = (*best).max(rd + 1 + lh);
        (height, rd + 1)
    } else {
        (height, -1)
    }
}

fn amount_of_time(root: &Link, start: i64) -> i64 {
    let mut best = 0;
    walk(root, start, &mut best);
    best
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: usize, seed: &mut i64) -> Link {
    let mut values: Vec<i32> = (1..=n as i32).collect();
    for i in (1..n).rev() {
        let j = (next_random(seed) % (i as i64 + 1)) as usize;
        values.swap(i, j);
    }
    let nodes: Vec<Rc<RefCell<TreeNode>>> =
        values.iter().map(|&v| Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))).collect();
    for k in 1..n {
        let high = next_random(seed);
        let mut at = nodes[((high * 32768 + next_random(seed)) % k as i64) as usize].clone();
        loop {
            if next_random(seed) % 2 == 0 {
                let child = at.borrow().left.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().left = Some(nodes[k].clone());
                        break;
                    }
                }
            } else {
                let child = at.borrow().right.clone();
                match child {
                    Some(c) => at = c,
                    None => {
                        at.borrow_mut().right = Some(nodes[k].clone());
                        break;
                    }
                }
            }
        }
    }
    Some(nodes[0].clone())
}

fn main() {
    // 200 random trees of 1000 nodes, each asked from 400 starts, start s
    // of tree t being 1 + (37 s + t) % 1000
    let mut seed = 2385;
    let mut check = 0i64;
    for t in 0..200i64 {
        let root = random_tree(1000, &mut seed);
        for s in 0..400i64 {
            check = (check * 31 + amount_of_time(&root, 1 + (37 * s + t) % 1000)) % 1000000007;
        }
    }
    println!("200 trees of 1000, 400 starts each: checksum {check}");
}
