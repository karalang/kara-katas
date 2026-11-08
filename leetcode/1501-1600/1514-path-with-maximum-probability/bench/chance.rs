// LeetCode #1514: Path with Maximum Probability -- the bench: 10 graphs of
// 50000 nodes and 100000 edges built once, then 5 questions asked of each
// by the ★ arm: Dijkstra for the largest product, the chance ordered by
// `total_cmp` in the heap.
use std::cmp::Ordering;
use std::collections::BinaryHeap;

#[derive(PartialEq)]
struct Entry(f64, i64);
impl Eq for Entry {}
impl PartialOrd for Entry {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}
impl Ord for Entry {
    fn cmp(&self, other: &Self) -> Ordering {
        self.0.total_cmp(&other.0).then(self.1.cmp(&other.1))
    }
}

fn max_probability(n: i64, edges: &[(i64, i64)], succ_prob: &[f64], start: i64, end: i64) -> f64 {
    let mut adjacent: Vec<Vec<(i64, f64)>> = vec![Vec::new(); n as usize];
    for (i, &(a, b)) in edges.iter().enumerate() {
        adjacent[a as usize].push((b, succ_prob[i]));
        adjacent[b as usize].push((a, succ_prob[i]));
    }
    let mut best = vec![0.0f64; n as usize];
    best[start as usize] = 1.0;
    let mut queue = BinaryHeap::new();
    queue.push(Entry(1.0, start));
    while let Some(Entry(chance, node)) = queue.pop() {
        if node == end {
            return chance;
        }
        if chance < best[node as usize] {
            continue;
        }
        for &(next, p) in &adjacent[node as usize] {
            let through = chance * p;
            if through > best[next as usize] {
                best[next as usize] = through;
                queue.push(Entry(through, next));
            }
        }
    }
    0.0
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1514;
    let n: i64 = 50000;
    let mut graphs: Vec<(Vec<(i64, i64)>, Vec<f64>)> = Vec::new();
    for _ in 0..10 {
        let mut edges = Vec::new();
        let mut probs = Vec::new();
        for _ in 0..100000 {
            let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let b = (a + 1 + (next_random(&mut seed) * 32768 + next_random(&mut seed)) % (n - 1)) % n;
            edges.push((a, b));
            probs.push((next_random(&mut seed) % 21 + 80) as f64 / 100.0);
        }
        graphs.push((edges, probs));
    }
    let mut check: i64 = 0;
    for _ in 0..5 {
        for (edges, probs) in &graphs {
            let start = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let end = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % n;
            let p = max_probability(n, edges, probs, start, end);
            check = (check * 31 + (p * 1000000000000.0 + 0.5).floor() as i64 + 1) % 1000000007;
        }
    }
    println!("50 questions over 10 graphs of 50000 nodes: checksum {}", check);
}
