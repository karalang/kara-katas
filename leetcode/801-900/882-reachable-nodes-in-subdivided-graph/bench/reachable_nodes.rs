// LeetCode #882 bench: Rust mirror of reachable_nodes.kara (the ★ arm,
// Dijkstra with a priority queue) on the same 600 graphs.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn reachable_nodes(edges: &[Vec<i64>], max_moves: i64, n: i64) -> i64 {
    let n = n as usize;
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    for (e, edge) in edges.iter().enumerate() {
        adj[edge[0] as usize].push(e);
        adj[edge[1] as usize].push(e);
    }
    let mut dist = vec![max_moves + 1; n];
    dist[0] = 0;
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0i64, 0usize)));
    while let Some(Reverse((d, u))) = queue.pop() {
        if d > dist[u] {
            continue;
        }
        for &e in &adj[u] {
            let v = (edges[e][0] + edges[e][1]) as usize - u;
            let next = d + edges[e][2] + 1;
            if next < dist[v] {
                dist[v] = next;
                queue.push(Reverse((next, v)));
            }
        }
    }
    let mut seen = dist.iter().filter(|&&d| d <= max_moves).count() as i64;
    for edge in edges {
        let from_u = (max_moves - dist[edge[0] as usize]).max(0);
        let from_v = (max_moves - dist[edge[1] as usize]).max(0);
        seen += (from_u + from_v).min(edge[2]);
    }
    seen
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn below(seed: &mut i64, limit: i64) -> i64 {
    let x = next_random(seed);
    let y = next_random(seed);
    (x * 32768 + y) % limit
}

fn main() {
    let mut seed = 882;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..600 {
        let n = 2000 + below(&mut seed, 1001);
        let mut offsets: Vec<i64> = Vec::new();
        while offsets.len() < 3 {
            let d = 1 + below(&mut seed, n / 2 - 1);
            if !offsets.contains(&d) {
                offsets.push(d);
            }
        }
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for u in 0..n {
            for k in 0..3 {
                edges.push(vec![u, (u + offsets[k]) % n, below(&mut seed, 10001)]);
            }
        }
        let max_moves = below(&mut seed, 200000);
        let reached = reachable_nodes(&edges, max_moves, n);
        total += reached;
        check = (check * 131 + reached) % 1000000007;
    }
    println!("600 graphs of up to 3000 nodes: {} nodes reached, checksum {}", total, check);
}
