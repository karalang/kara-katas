// LeetCode #2714: Find Shortest Path with K Hops -- the bench (hops.kara in
// Rust): Dijkstra's search over states of a node and the hops spent, a
// `BinaryHeap` of `Reverse((distance, node, hops))`.
use std::cmp::Reverse;
use std::collections::{BinaryHeap, HashSet};

fn shortest_path_with_hops(n: usize, edges: &Vec<Vec<i64>>, s: usize, d: usize, k: usize) -> i64 {
    let mut adjacent: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for e in edges.iter() {
        adjacent[e[0] as usize].push((e[1] as usize, e[2]));
        adjacent[e[1] as usize].push((e[0] as usize, e[2]));
    }
    let far = i64::MAX;
    let mut dist: Vec<Vec<i64>> = vec![vec![far; k + 1]; n];
    let mut queue: BinaryHeap<Reverse<(i64, usize, usize)>> = BinaryHeap::new();
    dist[s][0] = 0;
    queue.push(Reverse((0, s, 0)));
    while let Some(Reverse((here, u, hops))) = queue.pop() {
        if here > dist[u][hops] {
            continue;
        }
        if u == d {
            return here;
        }
        for &(v, w) in adjacent[u].iter() {
            if here + w < dist[v][hops] {
                dist[v][hops] = here + w;
                queue.push(Reverse((here + w, v, hops)));
            }
            if hops < k && here < dist[v][hops + 1] {
                dist[v][hops + 1] = here;
                queue.push(Reverse((here, v, hops + 1)));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let graphs = 50;
    let rounds = 10;
    let mut seed: i64 = 2714;
    let mut problems: Vec<(Vec<Vec<i64>>, i64, i64, i64)> = Vec::new();
    for _ in 0..graphs {
        let n: i64 = 500;
        let mut joined: HashSet<(i64, i64)> = HashSet::new();
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for v in 1..n {
            let u = next_random(&mut seed) % v;
            joined.insert((u, v));
            edges.push(vec![u, v, wide(&mut seed) % 1000000 + 1]);
        }
        for _ in 0..9501 {
            let a = next_random(&mut seed) % n;
            let b = next_random(&mut seed) % n;
            let (u, v) = (a.min(b), a.max(b));
            if u != v && joined.insert((u, v)) {
                edges.push(vec![v, u, wide(&mut seed) % 1000000 + 1]);
            }
        }
        let s = next_random(&mut seed) % n;
        let d = (s + 1 + next_random(&mut seed) % (n - 1)) % n;
        let k = next_random(&mut seed) % 50;
        problems.push((edges, s, d, k));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edges, s, d, k) in problems.iter() {
            let length = shortest_path_with_hops(500, edges, *s as usize, *d as usize, *k as usize);
            sum += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{} graphs of 500 nodes, {} rounds: lengths sum to {}, checksum {}", graphs, rounds, sum, check);
}
