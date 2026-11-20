// LeetCode #1245 bench, in Rust: the ★ arm (two breadth-first searches
// over an adjacency list) on 100 random trees of 10000 nodes built once,
// each asked 5 times; every diameter folded into a checksum.

use std::collections::VecDeque;

fn farthest(adj: &[Vec<i64>], from: i64) -> (i64, i64) {
    let mut dist = vec![-1i64; adj.len()];
    let mut queue: VecDeque<i64> = VecDeque::new();
    dist[from as usize] = 0;
    queue.push_back(from);
    let mut last = from;
    while let Some(node) = queue.pop_front() {
        last = node;
        for &next in &adj[node as usize] {
            if dist[next as usize] < 0 {
                dist[next as usize] = dist[node as usize] + 1;
                queue.push_back(next);
            }
        }
    }
    (last, dist[last as usize])
}

fn tree_diameter(edges: &[Vec<i64>]) -> i64 {
    let n = edges.len() + 1;
    let mut adj: Vec<Vec<i64>> = vec![Vec::new(); n];
    for e in edges {
        adj[e[0] as usize].push(e[1]);
        adj[e[1] as usize].push(e[0]);
    }
    let (end, _) = farthest(&adj, 0);
    let (_, diameter) = farthest(&adj, end);
    diameter
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_tree(n: i64, shape: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut label: Vec<i64> = (0..n).collect();
    for i in (1..n).rev() {
        let j = next_random(seed) % (i + 1);
        label.swap(i as usize, j as usize);
    }
    let mut edges: Vec<Vec<i64>> = Vec::new();
    for v in 1..n {
        let parent = match shape {
            0 => next_random(seed) % v,
            1 => v - 1 - next_random(seed) % v.min(3),
            _ => next_random(seed) % v.min(4),
        };
        edges.push(vec![label[parent as usize], label[v as usize]]);
    }
    edges
}

fn main() {
    let mut seed = 1245;
    let mut trees: Vec<Vec<Vec<i64>>> = Vec::new();
    for t in 0..100 {
        trees.push(random_tree(10000, t % 3, &mut seed));
    }
    let mut check = 0;
    for _ in 0..5 {
        for edges in &trees {
            check = (check * 131 + tree_diameter(edges)) % 1000000007;
        }
    }
    println!("5 rounds of 100 trees of 10000 nodes: checksum {check}");
}
