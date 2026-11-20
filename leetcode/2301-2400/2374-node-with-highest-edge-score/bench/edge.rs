// LeetCode #2374: Node With Highest Edge Score -- the bench, the ★ arm in
// Rust: each node adds its label to the score of the node its edge points
// to, and the answer is the highest score's node, the smallest on a tie.

fn edge_score(edges: &[usize]) -> i64 {
    let n = edges.len();
    let mut score = vec![0i64; n];
    for i in 0..n {
        score[edges[i]] += i as i64;
    }
    let mut best = 0;
    for v in 1..n {
        if score[v] > score[best] {
            best = v;
        }
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // graph a: 10^5 nodes, each edge to one of the first 4^(a + 1) nodes
    // (at most all of them), another node than its own
    let n = 100000usize;
    let mut seed = 2374i64;
    let mut graphs: Vec<Vec<usize>> = Vec::new();
    let mut width = 4i64;
    for _ in 0..10 {
        let edges: Vec<usize> = (0..n)
            .map(|i| {
                let hi = next_random(&mut seed);
                let e = ((hi * 32768 + next_random(&mut seed)) % width.min(n as i64)) as usize;
                if e == i { (e + 1) % n } else { e }
            })
            .collect();
        graphs.push(edges);
        width *= 4;
    }
    let mut check = 0i64;
    for p in 0..50i64 {
        for edges in &graphs {
            check = (check * 31 + edge_score(edges) + p) % 1000000007;
        }
    }
    println!("50 passes over 10 graphs of 10^5 nodes: checksum {}", check);
}
