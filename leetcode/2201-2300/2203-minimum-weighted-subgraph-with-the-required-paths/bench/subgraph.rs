// benchmark's Rust mirror of subgraph.kara (LeetCode #2203, the ★ arm):
// three Dijkstras with a `BinaryHeap` of `Reverse` pairs, the last over the
// edges turned round, and the least sum over the meeting node.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn dijkstra(adj: &[Vec<(usize, i64)>], from: usize) -> Vec<i64> {
    let mut dist = vec![-1; adj.len()];
    let mut queue = BinaryHeap::new();
    queue.push(Reverse((0i64, from)));
    while let Some(Reverse((d, u))) = queue.pop() {
        if dist[u] >= 0 {
            continue;
        }
        dist[u] = d;
        for &(v, w) in &adj[u] {
            if dist[v] < 0 {
                queue.push(Reverse((d + w, v)));
            }
        }
    }
    dist
}

fn minimum_weight(n: usize, edges: &[[i64; 3]], src1: usize, src2: usize, dest: usize) -> i64 {
    let mut forward: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    let mut backward: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for e in edges {
        forward[e[0] as usize].push((e[1] as usize, e[2]));
        backward[e[1] as usize].push((e[0] as usize, e[2]));
    }
    let one = dijkstra(&forward, src1);
    let two = dijkstra(&forward, src2);
    let home = dijkstra(&backward, dest);
    let mut best = -1;
    for v in 0..n {
        if one[v] >= 0 && two[v] >= 0 && home[v] >= 0 {
            let total = one[v] + two[v] + home[v];
            if best < 0 || total < best {
                best = total;
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
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2203;
    let n: i64 = 20000;
    let mut graphs: Vec<Vec<[i64; 3]>> = Vec::new();
    for _ in 0..4 {
        let mut edges = Vec::new();
        while edges.len() < 60000 {
            let from = wide_random(&mut seed) % n;
            let to = wide_random(&mut seed) % n;
            if from != to {
                edges.push([from, to, wide_random(&mut seed) % 100000 + 1]);
            }
        }
        graphs.push(edges);
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for edges in &graphs {
            for t in 0..4 {
                let weight = minimum_weight(n as usize, edges, t * 3, t * 3 + 1, t * 3 + 2);
                check = (check * 31 + weight + 1) % 1000000007;
            }
        }
    }
    println!("5 passes over 4 graphs: checksum {}", check);
}
