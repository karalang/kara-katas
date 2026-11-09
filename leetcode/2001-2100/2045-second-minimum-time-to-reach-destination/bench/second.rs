// LeetCode #2045: Second Minimum Time to Reach Destination -- the ★ arm in
// Rust, the same algorithm and workload as second.kara: a breadth-first
// search keeping each vertex's two smallest walk lengths, then the lights.
use std::collections::{HashSet, VecDeque};

fn travel(steps: i64, time: i64, change: i64) -> i64 {
    let mut t = 0;
    for _ in 0..steps {
        if t / change % 2 == 1 {
            t = (t / change + 1) * change;
        }
        t += time;
    }
    t
}

fn second_minimum(n: i64, edges: &[Vec<i64>], time: i64, change: i64) -> i64 {
    let n = n as usize;
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n + 1];
    for e in edges {
        adjacent[e[0] as usize].push(e[1] as usize);
        adjacent[e[1] as usize].push(e[0] as usize);
    }
    let mut first = vec![-1i64; n + 1];
    let mut second = vec![-1i64; n + 1];
    first[1] = 0;
    let mut queue: VecDeque<(usize, i64)> = VecDeque::new();
    queue.push_back((1, 0));
    while let Some((u, d)) = queue.pop_front() {
        for &v in &adjacent[u] {
            if first[v] == -1 {
                first[v] = d + 1;
                queue.push_back((v, d + 1));
            } else if second[v] == -1 && first[v] < d + 1 {
                second[v] = d + 1;
                queue.push_back((v, d + 1));
            }
        }
    }
    travel(second[n], time, change)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn graph(n: i64, reach: i64, extra: i64, seed: &mut i64) -> Vec<Vec<i64>> {
    let mut edges: Vec<Vec<i64>> = Vec::new();
    let mut seen: HashSet<i64> = HashSet::new();
    for v in 2..n + 1 {
        let u = v - 1 - next_random(seed) % reach.min(v - 1);
        edges.push(vec![u, v]);
        seen.insert(u * (n + 1) + v);
    }
    let mut tries = 0;
    while (edges.len() as i64) < n - 1 + extra && tries < 4 * extra {
        tries += 1;
        let a = next_random(seed) % n + 1;
        let b = next_random(seed) % n + 1;
        let (u, v) = (a.min(b), a.max(b));
        if u != v && !seen.contains(&(u * (n + 1) + v)) {
            seen.insert(u * (n + 1) + v);
            edges.push(vec![u, v]);
        }
    }
    edges
}

fn main() {
    let mut seed = 2045i64;
    let mut graphs: Vec<Vec<Vec<i64>>> = Vec::new();
    for r in 0..4 {
        let reach = [10000, 3, 2, 1][r];
        graphs.push(graph(10000, reach, 10001, &mut seed));
    }
    let mut calls = 0i64;
    let mut sum = 0i64;
    let mut check = 0i64;
    for round in 0..250i64 {
        for r in 0..4usize {
            let time = (round * 7 + r as i64) % 1000 + 1;
            let change = (round * 13 + r as i64 * 5) % 1000 + 1;
            let answer = second_minimum(10000, &graphs[r], time, change);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
