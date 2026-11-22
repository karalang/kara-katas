// LeetCode #2737: Find the Closest Marked Node -- the bench (closest.kara
// in Rust): Dijkstra from s with a `BinaryHeap` of `Reverse` entries,
// stopping at the first marked node taken off it.

use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn minimum_distance(n: usize, edges: &[Vec<i64>], s: usize, marked: &[i64]) -> i64 {
    let mut out: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for e in edges.iter() {
        out[e[0] as usize].push((e[1] as usize, e[2]));
    }
    let mut is_marked = vec![false; n];
    for &v in marked.iter() {
        is_marked[v as usize] = true;
    }
    let mut dist = vec![i64::MAX; n];
    let mut queue = BinaryHeap::new();
    dist[s] = 0;
    queue.push(Reverse((0i64, s)));
    while let Some(Reverse((d, u))) = queue.pop() {
        if d > dist[u] {
            continue;
        }
        if is_marked[u] {
            return d;
        }
        for &(v, w) in out[u].iter() {
            if d + w < dist[v] {
                dist[v] = d + w;
                queue.push(Reverse((d + w, v)));
            }
        }
    }
    -1
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let graphs = 50;
    let n: i64 = 500;
    let m = 10000;
    let rounds = 20;
    let mut seed: i64 = 2737;
    let mut problems: Vec<(Vec<Vec<i64>>, i64, Vec<i64>)> = Vec::new();
    for _ in 0..graphs {
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for _ in 0..m {
            let u = next_random(&mut seed) % n;
            let v = (u + 1 + next_random(&mut seed) % (n - 1)) % n;
            let hi = next_random(&mut seed);
            let w = (hi * 32768 + next_random(&mut seed)) % 1000000 + 1;
            edges.push(vec![u, v, w]);
        }
        let s = next_random(&mut seed) % n;
        let mut marked: Vec<i64> = Vec::new();
        let want = (next_random(&mut seed) % 3 + 1) as usize;
        while marked.len() < want {
            let v = next_random(&mut seed) % n;
            if v != s && !marked.contains(&v) {
                marked.push(v);
            }
        }
        problems.push((edges, s, marked));
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edges, s, marked) in problems.iter() {
            let distance = minimum_distance(n as usize, edges, *s as usize, marked);
            sum += distance;
            check = (check * 31 + distance + 1 + r) % 1000000007;
        }
    }
    println!("{} graphs of {} nodes and {} edges, {} rounds: distances sum to {}, checksum {}", graphs, n, m, rounds, sum, check);
}
