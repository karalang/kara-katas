// LeetCode #701: Insert into a Binary Search Tree -- bench program, Rust mirror of the loop arm.

struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn insert_into_bst(mut root: Option<Box<TreeNode>>, val: i64) -> Option<Box<TreeNode>> {
    let fresh = Box::new(TreeNode { val, left: None, right: None });
    let mut at = match root.as_deref_mut() {
        None => return Some(fresh),
        Some(r) => r,
    };
    loop {
        let side = if val < at.val { &mut at.left } else { &mut at.right };
        match side {
            Some(child) => at = child,
            None => {
                *side = Some(fresh);
                return root;
            }
        }
    }
}

fn height(root: &Option<Box<TreeNode>>) -> i64 {
    let mut best = 0;
    let mut stack: Vec<(&TreeNode, i64)> = Vec::new();
    if let Some(r) = root {
        stack.push((r, 1));
    }
    while let Some((n, depth)) = stack.pop() {
        best = best.max(depth);
        if let Some(r) = &n.right {
            stack.push((r, depth + 1));
        }
        if let Some(l) = &n.left {
            stack.push((l, depth + 1));
        }
    }
    best
}

fn main() {
    let mut seed = 701;
    let n: i64 = 50000;
    let mut orders: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut values: Vec<i64> = (0..n).map(|i| 2 * i).collect();
        for i in 1..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let j = (hi * 32768 + lo) % (i + 1);
            values.swap(i as usize, j as usize);
        }
        orders.push(values);
    }
    let rounds = 5;
    let mut total: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for order in orders.iter() {
            let mut root: Option<Box<TreeNode>> = None;
            for &v in order.iter() {
                root = insert_into_bst(root, v);
            }
            let h = height(&root);
            total += h;
            checksum = (checksum * 31 + h) % 1000000007;
        }
    }
    println!("{rounds} rounds of 10 trees grown to {n}: heights sum to {total}, checksum {checksum}");
}
