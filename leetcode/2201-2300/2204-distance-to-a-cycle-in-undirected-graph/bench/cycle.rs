// benchmark's Rust mirror of cycle.kara (LeetCode #2204, the ★ arm):
// leaves peeled by degree, then one breadth-first search from the cycle.
use std::collections::VecDeque;

fn distance_to_cycle(n: usize, edges: &[[usize; 2]]) -> Vec<i64> {
    let mut adj: Vec<Vec<usize>> = vec![Vec::new(); n];
    let mut degree = vec![0i64; n];
    for e in edges {
        adj[e[0]].push(e[1]);
        adj[e[1]].push(e[0]);
        degree[e[0]] += 1;
        degree[e[1]] += 1;
    }
    let mut leaves: VecDeque<usize> = (0..n).filter(|&v| degree[v] == 1).collect();
    let mut peeled = vec![false; n];
    while let Some(v) = leaves.pop_front() {
        peeled[v] = true;
        for &u in &adj[v] {
            degree[u] -= 1;
            if degree[u] == 1 {
                leaves.push_back(u);
            }
        }
    }
    let mut dist = vec![-1i64; n];
    let mut frontier = VecDeque::new();
    for v in 0..n {
        if !peeled[v] {
            dist[v] = 0;
            frontier.push_back(v);
        }
    }
    while let Some(v) = frontier.pop_front() {
        for &u in &adj[v] {
            if dist[u] < 0 {
                dist[u] = dist[v] + 1;
                frontier.push_back(u);
            }
        }
    }
    dist
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn random_graph(n: usize, ring: usize, seed: &mut i64) -> Vec<[usize; 2]> {
    let mut order: Vec<usize> = (0..n).collect();
    for i in (1..n).rev() {
        let j = (wide_random(seed) % (i as i64 + 1)) as usize;
        order.swap(i, j);
    }
    let mut edges = Vec::new();
    for i in 0..ring {
        edges.push([order[i], order[(i + 1) % ring]]);
    }
    for i in ring..n {
        edges.push([order[i], order[(wide_random(seed) % i as i64) as usize]]);
    }
    for i in (1..n).rev() {
        let j = (wide_random(seed) % (i as i64 + 1)) as usize;
        edges.swap(i, j);
    }
    for e in edges.iter_mut() {
        if next_random(seed) % 2 == 1 {
            e.swap(0, 1);
        }
    }
    edges
}

fn main() {
    let mut seed = 2204;
    let graphs: Vec<Vec<[usize; 2]>> = [3, 10, 100, 1000, 10000, 100000]
        .iter()
        .map(|&ring| random_graph(100000, ring, &mut seed))
        .collect();
    let mut check: i64 = 0;
    for _ in 0..5 {
        for edges in &graphs {
            let dist = distance_to_cycle(100000, edges);
            let sum: i64 = dist.iter().sum();
            check = (check * 31 + sum + dist[dist.len() / 2]) % 1000000007;
        }
    }
    println!("5 passes over 6 graphs: checksum {}", check);
}
