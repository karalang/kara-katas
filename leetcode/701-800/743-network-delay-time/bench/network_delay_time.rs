// LeetCode 743 — Network Delay Time, bench: the ★ arm (Dijkstra with a
// priority queue) on a 100-node graph of 6000 edges, every source, while
// edge times change. Mirrors network_delay_time.kara.
use std::cmp::Reverse;
use std::collections::BinaryHeap;

fn network_delay_time(times: &[(i64, i64, i64)], n: i64, k: i64) -> i64 {
    let mut adj: Vec<Vec<(i64, i64)>> = Vec::new();
    for _ in 0..n + 1 {
        adj.push(Vec::new());
    }
    for &(u, v, w) in times {
        adj[u as usize].push((v, w));
    }
    let mut heard: Vec<i64> = vec![-1; (n + 1) as usize];
    let mut queue: BinaryHeap<Reverse<(i64, i64)>> = BinaryHeap::new();
    queue.push(Reverse((0, k)));
    let mut settled = 0;
    let mut last = 0;
    while let Some(Reverse((d, u))) = queue.pop() {
        if heard[u as usize] != -1 {
            continue;
        }
        heard[u as usize] = d;
        settled += 1;
        last = d;
        for &(v, w) in &adj[u as usize] {
            if heard[v as usize] == -1 {
                queue.push(Reverse((d + w, v)));
            }
        }
    }
    if settled == n { last } else { -1 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_graph(seed: &mut i64, n: i64, m: i64, max_w: i64) -> Vec<(i64, i64, i64)> {
    let mut used = vec![false; ((n + 1) * (n + 1)) as usize];
    let mut times = Vec::new();
    while (times.len() as i64) < m {
        let u = 1 + next_random(seed) % n;
        let v = 1 + next_random(seed) % n;
        if u == v || used[(u * (n + 1) + v) as usize] {
            continue;
        }
        used[(u * (n + 1) + v) as usize] = true;
        let w = next_random(seed) % (max_w + 1);
        times.push((u, v, w));
    }
    times
}

fn main() {
    let rounds = 12;
    let mut seed = 743;
    let mut times = random_graph(&mut seed, 100, 6000, 100);
    let mut total = 0;
    for _ in 0..rounds {
        for _ in 0..50 {
            let i = (next_random(&mut seed) % times.len() as i64) as usize;
            let w = next_random(&mut seed) % 101;
            times[i].2 = w;
        }
        for k in 1..101 {
            total += network_delay_time(&times, 100, k);
        }
    }
    println!("{} rounds of 100 queries on 100 nodes and 6000 edges: answers sum to {}", rounds, total);
}
