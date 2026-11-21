// LeetCode #2458: Height of Binary Tree After Subtree Removal Queries --
// the bench, the ★ arm in Rust: every subtree's height, then a walk down
// carrying the height the tree keeps without each node, both kept in a
// `HashMap` by value. The nodes are `Rc<RefCell<TreeNode>>`, LeetCode's
// and the model of Kāra's `shared struct`.
use std::cell::RefCell;
use std::collections::HashMap;
use std::rc::Rc;

type Link = Option<Rc<RefCell<TreeNode>>>;

struct TreeNode {
    val: i32,
    left: Link,
    right: Link,
}

fn height(node: &Link, heights: &mut HashMap<i64, i64>) -> i64 {
    let Some(n) = node else {
        return -1;
    };
    let n = n.borrow();
    let h = 1 + height(&n.left, heights).max(height(&n.right, heights));
    heights.insert(n.val as i64, h);
    h
}

fn of(node: &Link, heights: &HashMap<i64, i64>) -> i64 {
    match node {
        None => -1,
        Some(n) => heights[&(n.borrow().val as i64)],
    }
}

fn walk(node: &Link, depth: i64, rest: i64, heights: &HashMap<i64, i64>, answers: &mut HashMap<i64, i64>) {
    if let Some(n) = node {
        let n = n.borrow();
        answers.insert(n.val as i64, rest);
        walk(&n.left, depth + 1, rest.max(depth + 1 + of(&n.right, heights)), heights, answers);
        walk(&n.right, depth + 1, rest.max(depth + 1 + of(&n.left, heights)), heights, answers);
    }
}

fn tree_queries(root: &Link, queries: &[i64]) -> Vec<i64> {
    let mut heights = HashMap::new();
    height(root, &mut heights);
    let mut answers = HashMap::new();
    walk(root, 0, 0, &heights, &mut answers);
    queries.iter().map(|q| answers[q]).collect()
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
    // 20 random trees of 10^4 nodes built once; then 60 passes, each
    // asking every tree about every value but the root's, pass p starting
    // its queries p * 101 values along
    let mut seed = 2458;
    let n = 10000i64;
    let trees: Vec<Link> = (0..20).map(|_| random_tree(n as usize, &mut seed)).collect();
    let mut check = 0i64;
    for p in 0..60i64 {
        for root in trees.iter() {
            let r = root.as_ref().unwrap().borrow().val as i64;
            let queries: Vec<i64> = (0..n).map(|i| 1 + (i + p * 101) % n).filter(|&v| v != r).collect();
            for a in tree_queries(root, &queries) {
                check = (check * 31 + a + p) % 1000000007;
            }
        }
    }
    println!("60 passes over 20 trees of 10^4: checksum {check}");
}
