// LeetCode #1786: Number of Restricted Paths From First to Last Node -- the
// bench in Rust, mirroring count_restricted_paths.kara: Dijkstra from node
// n, then the paths summed in the order the nodes settled.
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashSet};

fn count_restricted_paths(n: i32, edges: &[Vec<i32>]) -> i32 {
    let n = n as usize;
    let mut adj: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n + 1];
    for e in edges {
        adj[e[0] as usize].push((e[1] as usize, e[2] as i64));
        adj[e[1] as usize].push((e[0] as usize, e[2] as i64));
    }
    let mut dist: Vec<i64> = vec![-1; n + 1];
    let mut order: Vec<usize> = Vec::new();
    let mut queue: BinaryHeap<Reverse<(i64, usize)>> = BinaryHeap::new();
    queue.push(Reverse((0, n)));
    while let Some(Reverse((d, u))) = queue.pop() {
        if dist[u] != -1 {
            continue;
        }
        dist[u] = d;
        order.push(u);
        for &(v, w) in &adj[u] {
            if dist[v] == -1 {
                queue.push(Reverse((d + w, v)));
            }
        }
    }
    let mut ways: Vec<i64> = vec![0; n + 1];
    ways[n] = 1;
    for &u in &order {
        for &(v, _) in &adj[u] {
            if dist[v] < dist[u] {
                ways[u] = (ways[u] + ways[v]) % 1000000007;
            }
        }
    }
    ways[1] as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_graph(seed: &mut i64, n: i64, extra: i64) -> Vec<Vec<i32>> {
    let mut edges: Vec<Vec<i32>> = Vec::new();
    let mut joined: HashSet<(i64, i64)> = HashSet::new();
    for v in 2..n + 1 {
        let u = 1 + next_random(seed) % (v - 1);
        let w = 1 + next_random(seed) % 100000;
        joined.insert((u, v));
        edges.push(vec![u as i32, v as i32, w as i32]);
    }
    for _ in 0..extra {
        let a = 1 + next_random(seed) % n;
        let b = 1 + next_random(seed) % n;
        let (u, v) = if a < b { (a, b) } else { (b, a) };
        if u == v || joined.contains(&(u, v)) {
            continue;
        }
        let w = 1 + next_random(seed) % 100000;
        joined.insert((u, v));
        edges.push(vec![u as i32, v as i32, w as i32]);
    }
    edges
}

fn main() {
    let mut seed: i64 = 1786;
    let mut graphs: Vec<Vec<Vec<i32>>> = Vec::new();
    for _ in 0..200 {
        graphs.push(random_graph(&mut seed, 2000, 2001));
    }
    let mut check: i64 = 0;
    for call in 0..1000i64 {
        let edges = &graphs[((check + call) % 200) as usize];
        check = (check * 31 + count_restricted_paths(2000, edges) as i64) % 1000000007;
    }
    println!("1000 calls over 200 graphs: checksum {}", check);
}
