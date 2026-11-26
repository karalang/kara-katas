// LeetCode #1761: Minimum Degree of a Connected Trio in a Graph -- the bench
// in Rust, mirroring min_trio_degree.kara: an adjacency matrix, the degrees,
// and every edge (u, v) with each w above v.
fn min_trio_degree(n: i32, edges: &[Vec<i32>]) -> i32 {
    let n = n as usize;
    let mut joined = vec![vec![false; n + 1]; n + 1];
    let mut degree = vec![0i32; n + 1];
    for e in edges.iter() {
        let (u, v) = (e[0] as usize, e[1] as usize);
        joined[u][v] = true;
        joined[v][u] = true;
        degree[u] += 1;
        degree[v] += 1;
    }
    let mut best = i32::MAX;
    for u in 1..n + 1 {
        for v in u + 1..n + 1 {
            if !joined[u][v] {
                continue;
            }
            for w in v + 1..n + 1 {
                if joined[u][w] && joined[v][w] {
                    best = best.min(degree[u] + degree[v] + degree[w] - 6);
                }
            }
        }
    }
    if best == i32::MAX { -1 } else { best }
}

fn main() {
    let mut seed: i64 = 1761;
    let mut weights: Vec<(i32, i32, i64)> = Vec::new();
    for u in 1..401 {
        for v in u + 1..401 {
            seed = (seed * 1103515245 + 12345) % 2147483648;
            weights.push((u, v, seed / 65536 % 1000));
        }
    }
    let mut check: i64 = 0;
    for call in 0..40i64 {
        let threshold = 300 + (check + call * 7919) % 500;
        let edges: Vec<Vec<i32>> = weights.iter().filter(|&&(_, _, w)| w < threshold).map(|&(u, v, _)| vec![u, v]).collect();
        check = (check * 31 + min_trio_degree(400, &edges) as i64 + 1) % 1000000007;
    }
    println!("40 calls on 400 nodes: checksum {}", check);
}
