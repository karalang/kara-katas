// LeetCode #1627: Graph Connectivity With Threshold -- the bench's Rust
// mirror: the ★ arm on 100 problems of 10000 cities, thresholds 0 to 99,
// each asked the same 100000 queries, all drawn first.

fn find(parent: &mut [i32], x: i32) -> i32 {
    let mut root = x;
    while parent[root as usize] != root {
        root = parent[root as usize];
    }
    let mut x = x;
    while parent[x as usize] != root {
        let next = parent[x as usize];
        parent[x as usize] = root;
        x = next;
    }
    root
}

fn are_connected(n: i32, threshold: i32, queries: &[Vec<i32>]) -> Vec<bool> {
    let mut parent: Vec<i32> = (0..=n).collect();
    for z in threshold + 1..=n {
        for m in (2 * z..=n).step_by(z as usize) {
            let (a, b) = (find(&mut parent, z), find(&mut parent, m));
            if a != b {
                parent[b as usize] = a;
            }
        }
    }
    queries.iter().map(|q| find(&mut parent, q[0]) == find(&mut parent, q[1])).collect()
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1627;
    let n: i64 = 10000;
    let thresholds: Vec<i32> = (0..100).map(|_| (next_random(&mut seed) % 100) as i32).collect();
    let mut queries: Vec<Vec<i32>> = Vec::new();
    for _ in 0..100000 {
        let a = next_random(&mut seed) % n + 1;
        let b = next_random(&mut seed) % n + 1;
        queries.push(vec![a as i32, b as i32]);
    }
    let mut check: i64 = 0;
    let mut total: i64 = 0;
    for &threshold in &thresholds {
        let yes = are_connected(n as i32, threshold, &queries).iter().filter(|&&a| a).count() as i64;
        total += yes;
        check = (check * 31 + yes + 1) % 1000000007;
    }
    println!("100 problems of 10000 cities and 100000 queries: {} connected, checksum {}", total, check);
}
