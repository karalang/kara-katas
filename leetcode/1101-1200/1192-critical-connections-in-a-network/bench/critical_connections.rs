// LeetCode #1192 bench: the ★ arm in Rust, over the same 4 networks and 10
// rounds as the Kāra bench.

use std::collections::HashSet;

fn critical_connections(n: usize, connections: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for (id, c) in connections.iter().enumerate() {
        adj[c[0] as usize].push((c[1] as usize, id as i64));
        adj[c[1] as usize].push((c[0] as usize, id as i64));
    }
    let mut disc = vec![-1i64; n];
    let mut low = vec![0i64; n];
    let mut bridges: Vec<Vec<i64>> = Vec::new();
    disc[0] = 0;
    let mut time = 1;
    let mut stack: Vec<(usize, i64, usize)> = vec![(0, -1, 0)];
    while !stack.is_empty() {
        let top = stack.len() - 1;
        let (u, via, next) = stack[top];
        if next < adj[u].len() {
            stack[top] = (u, via, next + 1);
            let (v, id) = adj[u][next];
            if id == via {
                continue;
            }
            if disc[v] == -1 {
                disc[v] = time;
                low[v] = time;
                time += 1;
                stack.push((v, id, 0));
            } else {
                low[u] = low[u].min(disc[v]);
            }
        } else {
            stack.pop();
            if let Some(&(p, _, _)) = stack.last() {
                low[p] = low[p].min(low[u]);
                if low[u] > disc[p] {
                    bridges.push(vec![p as i64, u as i64]);
                }
            }
        }
    }
    bridges
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_network(seed: &mut i64, n: i64, extra: i64) -> Vec<Vec<i64>> {
    let mut joined: HashSet<(i64, i64)> = HashSet::new();
    let mut edges: Vec<Vec<i64>> = Vec::new();
    for v in 1..n {
        let u = next_random(seed) % v;
        joined.insert((u, v));
        edges.push(vec![u, v]);
    }
    for _ in 0..extra {
        let a = next_random(seed) % n;
        let b = next_random(seed) % n;
        let key = (a.min(b), a.max(b));
        if a != b && !joined.contains(&key) {
            joined.insert(key);
            edges.push(vec![a, b]);
        }
    }
    edges
}

fn main() {
    let mut seed = 1192;
    let path: Vec<Vec<i64>> = (0..99999).map(|i| vec![i, i + 1]).collect();
    let mut ring = path.clone();
    ring.push(vec![99999, 0]);
    let networks = [
        (50000, random_network(&mut seed, 50000, 50001)),
        (100000, random_network(&mut seed, 100000, 0)),
        (100000, path),
        (100000, ring),
    ];
    let mut check: i64 = 0;
    for _ in 0..10 {
        for (n, edges) in &networks {
            let bridges = critical_connections(*n, edges);
            check = (check * 131 + bridges.len() as i64) % 1000000007;
            for b in &bridges {
                check = (check * 131 + b[0] * 100003 + b[1]) % 1000000007;
            }
        }
    }
    println!("10 rounds of 4 networks of up to 100000 servers: checksum {check}");
}
