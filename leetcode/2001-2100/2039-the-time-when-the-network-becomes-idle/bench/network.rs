// LeetCode #2039: The Time When the Network Becomes Idle -- the ★ arm in
// Rust, the same algorithm and workload as network.kara: breadth-first
// search from the master with a VecDeque, then each server's last message
// and its reply.
use std::collections::{HashSet, VecDeque};

fn network_becomes_idle(edges: &[Vec<i64>], patience: &[i64]) -> i64 {
    let n = patience.len();
    let mut adjacent: Vec<Vec<i64>> = vec![Vec::new(); n];
    for e in edges.iter() {
        adjacent[e[0] as usize].push(e[1]);
        adjacent[e[1] as usize].push(e[0]);
    }
    let mut hops: Vec<i64> = vec![-1; n];
    hops[0] = 0;
    let mut queue: VecDeque<i64> = VecDeque::new();
    queue.push_back(0);
    while let Some(u) = queue.pop_front() {
        for &v in adjacent[u as usize].iter() {
            if hops[v as usize] == -1 {
                hops[v as usize] = hops[u as usize] + 1;
                queue.push_back(v);
            }
        }
    }
    let mut idle = 0;
    for i in 1..n {
        let round_trip = 2 * hops[i];
        let last_sent = (round_trip - 1) / patience[i] * patience[i];
        idle = idle.max(last_sent + round_trip + 1);
    }
    idle
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn random_network(n: i64, reach: i64, extra: i64, top: i64, seed: &mut i64) -> (Vec<Vec<i64>>, Vec<i64>) {
    let mut edges: Vec<Vec<i64>> = Vec::new();
    let mut joined: HashSet<(i64, i64)> = HashSet::new();
    for v in 1..n {
        let hi = next_random(seed);
        let lo = next_random(seed);
        let u = v - 1 - (hi * 32768 + lo) % reach.min(v);
        edges.push(vec![u, v]);
        joined.insert((u, v));
    }
    let mut tries = 0;
    while (edges.len() as i64) < n - 1 + extra && tries < 4 * extra {
        tries += 1;
        let (h1, l1) = (next_random(seed), next_random(seed));
        let a = (h1 * 32768 + l1) % n;
        let (h2, l2) = (next_random(seed), next_random(seed));
        let b = (h2 * 32768 + l2) % n;
        let (u, v) = (a.min(b), a.max(b));
        if u != v && !joined.contains(&(u, v)) {
            joined.insert((u, v));
            edges.push(vec![u, v]);
        }
    }
    let mut patience = vec![0];
    for _ in 1..n {
        patience.push(next_random(seed) % top + 1);
    }
    (edges, patience)
}

fn main() {
    let mut seed = 2039;
    let mut networks: Vec<(Vec<Vec<i64>>, Vec<i64>)> = Vec::new();
    for r in 0..4 {
        let top = [100000, 3, 1000, 1][r];
        let reach = [100000, 2, 50, 1][r];
        networks.push(random_network(100000, reach, 1, top, &mut seed));
    }
    let mut calls = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..25 {
        for r in 0..4 {
            let at = (round * 7919 + r * 104729) % 99999 + 1;
            networks[r].1[at] = networks[r].1[at] % 7 + 1;
            let answer = network_becomes_idle(&networks[r].0, &networks[r].1);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
