// LeetCode #2285: Maximum Total Importance of Roads -- the bench, the ★
// arm's Rust twin. The degrees sorted, the k-th smallest valued k.

fn maximum_importance(n: usize, roads: &[(usize, usize)]) -> i64 {
    let mut degree = vec![0i64; n];
    for &(a, b) in roads.iter() {
        degree[a] += 1;
        degree[b] += 1;
    }
    degree.sort();
    let mut total: i64 = 0;
    for (i, d) in degree.iter().enumerate() {
        total += d * (i as i64 + 1);
    }
    total
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 2285;
    let mut graphs: Vec<Vec<(usize, usize)>> = Vec::new();
    for _ in 0..200 {
        let mut roads: Vec<(usize, usize)> = Vec::new();
        while roads.len() < 5000 {
            let a = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 5000;
            let b = (next_random(&mut seed) * 32768 + next_random(&mut seed)) % 5000;
            if a != b {
                roads.push((a as usize, b as usize));
            }
        }
        graphs.push(roads);
    }
    let mut check: i64 = 0;
    for _ in 0..20 {
        for roads in graphs.iter() {
            check = (check * 31 + maximum_importance(5000, roads)) % 1000000007;
        }
    }
    println!("20 passes over 200 graphs of 5000 cities: checksum {}", check);
}
