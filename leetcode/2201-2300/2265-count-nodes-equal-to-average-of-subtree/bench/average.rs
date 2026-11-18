// LeetCode #2265: Count Nodes Equal to Average of Subtree -- Rust mirror
// of the ★ arm (average.kara): the same random trees, each counted by one
// post-order walk returning (sum, size). The nodes are
// `Rc<RefCell<TreeNode>>`, LeetCode's and the model of Kāra's `shared
// struct`. Output is byte-identical to average.kara.
use std::cell::RefCell;
use std::rc::Rc;

type Link = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i32,
    left: Link,
    right: Link,
}

fn sum_and_size(node: &Link, matches: &mut i64) -> (i64, i64) {
    let Some(n) = node else {
        return (0, 0);
    };
    let n = n.borrow();
    let (left_sum, left_size) = sum_and_size(&n.left, matches);
    let (right_sum, right_size) = sum_and_size(&n.right, matches);
    let sum = left_sum + right_sum + n.val as i64;
    let size = left_size + right_size + 1;
    if sum / size == n.val as i64 {
        *matches += 1;
    }
    (sum, size)
}

fn average_of_subtree(root: &Link) -> i64 {
    let mut matches = 0;
    sum_and_size(root, &mut matches);
    matches
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: usize, top: i64, seed: &mut i64) -> Link {
    let nodes: Vec<Rc<RefCell<TreeNode>>> = (0..n)
        .map(|_| {
            let v = (next_random(seed) % (top + 1)) as i32;
            Rc::new(RefCell::new(TreeNode { val: v, left: None, right: None }))
        })
        .collect();
    for k in 1..n {
        let mut at = nodes[(next_random(seed) % k as i64) as usize].clone();
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
    let mut seed = 2265;
    let mut check = 0;
    for _ in 0..500 {
        let root = random_tree(1000, 1000, &mut seed);
        for _ in 0..20 {
            check = (check * 31 + average_of_subtree(&root)) % 1000000007;
        }
    }
    println!("500 trees of 1000, 20 times: checksum {check}");
}
