// LeetCode #2242: Maximum Score of a Node Sequence -- the benchmark's Rust
// mirror of score.kara: each node's neighbours sorted by score, largest
// first, and cut to three; every edge as the middle one tries the nine
// pairs, all four distinct.

fn maximum_score(scores: &[i64], edges: &[(usize, usize)]) -> i64 {
    let n = scores.len();
    let mut best3: Vec<Vec<usize>> = vec![Vec::new(); n];
    for &(a, b) in edges {
        best3[a].push(b);
        best3[b].push(a);
    }
    for list in best3.iter_mut() {
        list.sort_by(|&x, &y| scores[y].cmp(&scores[x]));
        list.truncate(3);
    }
    let mut best = -1i64;
    for &(b, c) in edges {
        for &a in &best3[b] {
            if a == c {
                continue;
            }
            for &d in &best3[c] {
                if d != a && d != b {
                    best = best.max(scores[a] + scores[b] + scores[c] + scores[d]);
                }
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    high * 32768 + next_random(seed)
}

fn main() {
    let n = 50000i64;
    let mut seed = 2242i64;
    let mut check = 0i64;
    for _ in 0..40 {
        let scores: Vec<i64> = (0..n).map(|_| wide_random(&mut seed) % 100000000 + 1).collect();
        let edges: Vec<(usize, usize)> = (0..n)
            .map(|j| (j as usize, ((j + 1 + wide_random(&mut seed) % (n / 2 - 2)) % n) as usize))
            .collect();
        check = (check * 31 + maximum_score(&scores, &edges)) % 1000000007;
    }
    println!("40 graphs of 50000 nodes: checksum {}", check);
}
