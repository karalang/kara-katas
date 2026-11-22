// LeetCode #2872: Maximum Number of K-Divisible Components -- the bench,
// as components.kara: 30 trees of 3 * 10^4 nodes, each answered 20 times
// by the breadth-first arm.

fn max_k_divisible_components(n: usize, edges: &[Vec<i64>], values: &[i64], k: i64) -> i64 {
    let mut adjacent: Vec<Vec<usize>> = vec![Vec::new(); n];
    for e in edges {
        adjacent[e[0] as usize].push(e[1] as usize);
        adjacent[e[1] as usize].push(e[0] as usize);
    }
    let mut parent: Vec<i64> = vec![-1; n];
    let mut order: Vec<usize> = vec![0];
    let mut head = 0;
    while head < order.len() {
        let u = order[head];
        head += 1;
        for &w in &adjacent[u] {
            if w as i64 != parent[u] {
                parent[w] = u as i64;
                order.push(w);
            }
        }
    }
    let mut rest: Vec<i64> = values.iter().map(|v| v % k).collect();
    let mut parts = 0;
    for &u in order.iter().rev() {
        if rest[u] == 0 {
            parts += 1;
        } else if parent[u] >= 0 {
            let p = parent[u] as usize;
            rest[p] = (rest[p] + rest[u]) % k;
        }
    }
    parts
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (30, 20, 30000i64);
    let mut seed = 2872;
    let mut cases: Vec<(Vec<Vec<i64>>, Vec<i64>, i64)> = Vec::new();
    for c in 0..count {
        let k = next_random(&mut seed) % 9 + 2;
        let mut edges: Vec<Vec<i64>> = Vec::new();
        for v in 1..n {
            let reach = if c % 2 == 1 { v.min(5) } else { v };
            edges.push(vec![v - 1 - wide(&mut seed) % reach, v]);
        }
        let mut values: Vec<i64> = (0..n).map(|_| wide(&mut seed) % 1000000001).collect();
        let sum: i64 = values.iter().sum();
        values[0] += (k - sum % k) % k;
        cases.push((edges, values, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (edges, values, k) in cases.iter() {
            let parts = max_k_divisible_components(n as usize, edges, values, *k);
            total += parts;
            check = (check * 31 + parts + r) % 1000000007;
        }
    }
    println!("{count} trees of {n}, {rounds} rounds: {total} components, checksum {check}");
}
