// LeetCode #956: Tallest Billboard -- Rust mirror of the Kara bench
// program (the shorter side by difference).

fn tallest_billboard(rods: &[i64]) -> i64 {
    let total: i64 = rods.iter().sum();
    let size = (total + 1) as usize;
    let mut best = vec![-1i64; size];
    best[0] = 0;
    for &r in rods {
        let prev = best.clone();
        for d in 0..=total {
            let short = prev[d as usize];
            if short < 0 {
                continue;
            }
            if d + r <= total && short > best[(d + r) as usize] {
                best[(d + r) as usize] = short;
            }
            let nd = (d - r).abs() as usize;
            let ns = short + d.min(r);
            if ns > best[nd] {
                best[nd] = ns;
            }
        }
    }
    best[0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 30;
    let count = 200;
    let n = 20;
    let mut seed = 956i64;
    let mut sets: Vec<Vec<i64>> = Vec::new();
    for _ in 0..count {
        let rods: Vec<i64> = (0..n).map(|_| 1 + next_random(&mut seed) % 250).collect();
        sets.push(rods);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for r in 0..rounds {
        for i in 0..count {
            let k = (r + i) % count;
            let h = tallest_billboard(&sets[k]);
            total += h;
            check = (check * 31 + h) % 1000000007;
        }
    }
    println!("{} rounds over {} sets of {} rods up to 250: heights adding to {}, checksum {}", rounds, count, n, total, check);
}
