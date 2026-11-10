// LeetCode #2065: Maximum Path Quality of a Graph -- Rust mirror of the ★
// arm's benchmark (quality.kara): 1000 graphs of 1000 nodes, 2000 edges
// tried, each from a node to one of the next three and of time 10 or 11,
// and the time 100; a recursive search with a count of visits per node.
use std::collections::HashSet;

fn walk(adj: &[Vec<(usize, i64)>], values: &[i64], max_time: i64, node: usize, time: i64, quality: i64, visits: &mut Vec<i64>, best: &mut i64) {
    if node == 0 {
        *best = (*best).max(quality);
    }
    for &(next, t) in &adj[node] {
        if time + t <= max_time {
            visits[next] += 1;
            let gain = if visits[next] == 1 { values[next] } else { 0 };
            walk(adj, values, max_time, next, time + t, quality + gain, visits, best);
            visits[next] -= 1;
        }
    }
}

fn maximal_path_quality(values: &[i64], edges: &[(usize, usize, i64)], max_time: i64) -> i64 {
    let n = values.len();
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for &(u, v, t) in edges {
        adj[u].push((v, t));
        adj[v].push((u, t));
    }
    let mut visits = vec![0i64; n];
    visits[0] = 1;
    let mut best = 0;
    walk(&adj, values, max_time, 0, 0, values[0], &mut visits, &mut best);
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2065i64;
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..1000 {
        let n = 1000usize;
        let mut values = Vec::with_capacity(n);
        for _ in 0..n {
            let hi = next_random(&mut seed);
            values.push((hi * 32768 + next_random(&mut seed)) % 100000001);
        }
        let mut degree = vec![0; n];
        let mut seen: HashSet<(usize, usize)> = HashSet::new();
        let mut edges = Vec::new();
        for _ in 0..2000 {
            let u = (next_random(&mut seed) % n as i64) as usize;
            let v = (u + 1 + (next_random(&mut seed) % 3) as usize) % n;
            let t = next_random(&mut seed) % 2 + 10;
            let key = (u.min(v), u.max(v));
            if degree[u] < 4 && degree[v] < 4 && !seen.contains(&key) {
                seen.insert(key);
                degree[u] += 1;
                degree[v] += 1;
                edges.push((u, v, t));
            }
        }
        let a = maximal_path_quality(&values, &edges, 100);
        total += a;
        check = (check * 31 + a % 1000000007) % 1000000007;
    }
    println!("1000 graphs: sum {}, checksum {}", total, check);
}
