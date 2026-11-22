// LeetCode #2773: Height of Special Binary Tree -- the bench in Rust: the
// ★ arm over 20 random trees of 10^4 nodes, all drawn first, then each
// answered 200 times.

fn depth(u: i64, left: &[i64], right: &[i64]) -> i64 {
    let mut best = 0;
    let l = left[u as usize];
    if l >= 0 && right[l as usize] != u {
        best = best.max(depth(l, left, right) + 1);
    }
    let r = right[u as usize];
    if r >= 0 && left[r as usize] != u {
        best = best.max(depth(r, left, right) + 1);
    }
    best
}

fn height_of_tree(left: &[i64], right: &[i64], root: i64) -> i64 {
    depth(root, left, right)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn joined(left: &[i64], right: &[i64], root: i64) -> (Vec<i64>, Vec<i64>) {
    let mut leaves: Vec<i64> = Vec::new();
    let mut stack: Vec<i64> = vec![root];
    while let Some(u) = stack.pop() {
        let ui = u as usize;
        if left[ui] < 0 && right[ui] < 0 {
            leaves.push(u);
        }
        if right[ui] >= 0 {
            stack.push(right[ui]);
        }
        if left[ui] >= 0 {
            stack.push(left[ui]);
        }
    }
    let mut l = left.to_vec();
    let mut r = right.to_vec();
    let k = leaves.len();
    for i in 0..k {
        r[leaves[i] as usize] = leaves[(i + 1) % k];
        l[leaves[i] as usize] = leaves[(i + k - 1) % k];
    }
    (l, r)
}

fn grown(n: i64, reach: i64, seed: &mut i64) -> (Vec<i64>, Vec<i64>) {
    let mut left = vec![-1i64; n as usize];
    let mut right = vec![-1i64; n as usize];
    for k in 1..n {
        let mut p = (k - 1 - next_random(seed) % reach.min(k)) as usize;
        while left[p] >= 0 && right[p] >= 0 {
            p = (next_random(seed) % k) as usize;
        }
        let go_left = if left[p] >= 0 {
            false
        } else if right[p] >= 0 {
            true
        } else {
            next_random(seed) % 2 == 0
        };
        if go_left {
            left[p] = k;
        } else {
            right[p] = k;
        }
    }
    joined(&left, &right, 0)
}

fn main() {
    let count = 20;
    let rounds = 200;
    let mut seed: i64 = 2773;
    let mut trees: Vec<(Vec<i64>, Vec<i64>)> = Vec::new();
    for _ in 0..count {
        let reach = next_random(&mut seed) % 50 + 1;
        trees.push(grown(10000, reach, &mut seed));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (left, right) in trees.iter() {
            let h = height_of_tree(left, right, 0);
            total += h;
            check = (check * 31 + h + r) % 1000000007;
        }
    }
    println!("{} trees of 10^4, {} rounds: heights sum to {}, checksum {}", count, rounds, total, check);
}
