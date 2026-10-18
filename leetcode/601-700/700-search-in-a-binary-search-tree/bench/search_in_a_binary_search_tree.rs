// LeetCode #700: Search in a Binary Search Tree -- bench program, Rust mirror of the loop arm.

struct TreeNode {
    val: i64,
    left: Option<Box<TreeNode>>,
    right: Option<Box<TreeNode>>,
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn search_bst(root: Option<&TreeNode>, val: i64) -> Option<&TreeNode> {
    let mut at = root;
    while let Some(n) = at {
        if val == n.val {
            return Some(n);
        }
        at = if val < n.val { n.left.as_deref() } else { n.right.as_deref() };
    }
    None
}

fn leaf(v: i64) -> Box<TreeNode> {
    Box::new(TreeNode { val: v, left: None, right: None })
}

fn insert(root: &mut TreeNode, v: i64) {
    let mut at = root;
    loop {
        let next = if v < at.val { &mut at.left } else { &mut at.right };
        match next {
            Some(child) => at = child,
            None => {
                *next = Some(leaf(v));
                return;
            }
        }
    }
}

fn main() {
    let mut seed = 700;
    let n: i64 = 50000;
    let mut trees: Vec<Box<TreeNode>> = Vec::new();
    for _ in 0..10 {
        let mut values: Vec<i64> = (0..n).map(|i| 2 * i).collect();
        for i in 1..n {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            let j = (hi * 32768 + lo) % (i + 1);
            values.swap(i as usize, j as usize);
        }
        let mut root = leaf(values[0]);
        for i in 1..n as usize {
            insert(&mut root, values[i]);
        }
        trees.push(root);
    }
    let searches = 40000;
    let mut queries: Vec<i64> = Vec::new();
    for _ in 0..searches {
        let hi = next_random(&mut seed);
        let lo = next_random(&mut seed);
        queries.push((hi * 32768 + lo) % (2 * n));
    }
    let rounds = 5;
    let mut found: i64 = 0;
    let mut checksum: i64 = 0;
    for _ in 0..rounds {
        for root in trees.iter() {
            for &q in queries.iter() {
                if let Some(hit) = search_bst(Some(root), q) {
                    found += 1;
                    checksum = (checksum * 31 + hit.val) % 1000000007;
                }
            }
        }
    }
    println!("{rounds} rounds of 10 trees of {n}, {searches} searches each: {found} found, checksum {checksum}");
}
