// LeetCode #2331: Evaluate Boolean Binary Tree -- the bench, the ★ arm in
// Rust. A leaf is its own truth, and an OR or an AND node its two
// subtrees evaluated recursively and joined by `||` or `&&`, which stop
// at the first child that settles it. O(n). The tree is
// `Option<Box<TreeNode>>`.

struct TreeNode {
    val: i32,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn evaluate_tree(root: &Option<Box<TreeNode>>) -> bool {
    let node = match root {
        Some(node) => node,
        None => return false,
    };
    match node.val {
        0 => false,
        1 => true,
        2 => evaluate_tree(&node.left) || evaluate_tree(&node.right),
        _ => evaluate_tree(&node.left) && evaluate_tree(&node.right),
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(seed: &mut i64, depth: i64) -> Option<Box<TreeNode>> {
    if depth == 0 || next_random(seed) % 8 == 0 {
        return Some(Box::new(TreeNode { val: (next_random(seed) % 2) as i32, left: None, right: None }));
    }
    let op = (next_random(seed) % 2 + 2) as i32;
    let left = random_tree(seed, depth - 1);
    let right = random_tree(seed, depth - 1);
    Some(Box::new(TreeNode { val: op, left, right }))
}

fn main() {
    let mut seed: i64 = 2331;
    let trees: Vec<Option<Box<TreeNode>>> = (0..200).map(|_| random_tree(&mut seed, 14)).collect();
    let mut check: i64 = 0;
    for p in 0..500i64 {
        for k in 0..200 {
            let truth = if evaluate_tree(&trees[k]) { 1 } else { 2 };
            check = (check * 3 + truth + p) % 1000000007;
        }
    }
    println!("500 passes over 200 trees of depth up to 14: checksum {}", check);
}
