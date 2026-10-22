// Benchmark for #847: Shortest Path Visiting All Nodes -- Rust twin of the
// Kāra ★ arm (breadth-first search over (visited set, node) states).
use std::collections::VecDeque;

fn shortest_path_length(graph: &[Vec<i64>]) -> i64 {
    let n = graph.len() as i64;
    let all = (1i64 << n) - 1;
    let mut seen = vec![false; (n << n) as usize];
    let mut queue: VecDeque<(i64, i64, i64)> = VecDeque::new();
    for v in 0..n {
        seen[((1i64 << v) * n + v) as usize] = true;
        queue.push_back((1 << v, v, 0));
    }
    while let Some((mask, v, steps)) = queue.pop_front() {
        if mask == all {
            return steps;
        }
        for &w in graph[v as usize].iter() {
            let next = mask | (1 << w);
            if !seen[(next * n + w) as usize] {
                seen[(next * n + w) as usize] = true;
                queue.push_back((next, w, steps + 1));
            }
        }
    }
    0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 64;
    let rounds = 4000;
    let n: i64 = 12;
    let mut seed: i64 = 847;
    let mut graphs: Vec<Vec<Vec<i64>>> = Vec::new();
    for g in 0..count {
        let mut edge = vec![false; (n * n) as usize];
        for v in 1..n {
            let w = next_random(&mut seed) % v;
            edge[(v * n + w) as usize] = true;
            edge[(w * n + v) as usize] = true;
        }
        for _ in 0..g % 16 * 3 {
            let v = next_random(&mut seed) % n;
            let w = next_random(&mut seed) % n;
            if v != w {
                edge[(v * n + w) as usize] = true;
                edge[(w * n + v) as usize] = true;
            }
        }
        let graph: Vec<Vec<i64>> =
            (0..n).map(|v| (0..n).filter(|&w| edge[(v * n + w) as usize]).collect()).collect();
        graphs.push(graph);
    }
    let mut total = 0;
    let mut checksum: i64 = 0;
    for round in 0..rounds {
        let length = shortest_path_length(&graphs[round % count]);
        total += length;
        checksum = (checksum * 31 + length) % 1000000007;
    }
    println!("{} rounds of {} graphs: lengths sum to {}, checksum {}", rounds, count, total, checksum);
}
