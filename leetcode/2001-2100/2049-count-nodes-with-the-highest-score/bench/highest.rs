// LeetCode #2049: Count Nodes With the Highest Score -- Rust mirror of the
// ★ arm's benchmark (highest.kara): the same 50 trees of 100000 nodes, the
// same explicit-stack preorder walked backwards.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn draw(n: usize, reach: i64, seed: &mut i64) -> Vec<i64> {
    let mut parents = vec![-1i64; n];
    let mut kids = vec![0i64; n];
    for i in 1..n {
        let mut at = i - (next_random(seed) % reach.min(i as i64) + 1) as usize;
        while kids[at] == 2 {
            at += 1;
        }
        parents[i] = at as i64;
        kids[at] += 1;
    }
    parents
}

fn count_highest_score_nodes(parents: &[i64]) -> i64 {
    let n = parents.len();
    let mut children: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut root = 0;
    for v in 0..n {
        if parents[v] == -1 {
            root = v;
        } else {
            children[parents[v] as usize].push(v);
        }
    }
    let mut order: Vec<usize> = Vec::new();
    let mut stack = vec![root];
    while let Some(v) = stack.pop() {
        order.push(v);
        for &c in &children[v] {
            stack.push(c);
        }
    }
    let mut size = vec![1i64; n];
    for &v in order.iter().rev() {
        if parents[v] != -1 {
            size[parents[v] as usize] += size[v];
        }
    }
    let (mut best, mut count) = (0i64, 0i64);
    for v in 0..n {
        let mut score = (n as i64 - size[v]).max(1);
        for &c in &children[v] {
            score *= size[c];
        }
        if score > best {
            best = score;
            count = 1;
        } else if score == best {
            count += 1;
        }
    }
    count
}

fn main() {
    let mut seed = 2049i64;
    let (mut sum, mut check) = (0i64, 0i64);
    for t in 0..50 {
        let count = count_highest_score_nodes(&draw(100000, 1 + t * 1000, &mut seed));
        sum += count;
        check = (check * 31 + count) % 1000000007;
    }
    println!("50 trees: sum {}, checksum {}", sum, check);
}
