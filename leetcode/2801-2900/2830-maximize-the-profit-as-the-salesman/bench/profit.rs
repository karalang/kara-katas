// LeetCode #2830: Maximize the Profit as the Salesman -- the bench's Rust
// mirror of the ★ arm: the offers filed by their last house, and best[i]
// the most gold from the first i houses.

fn maximize_the_profit(n: usize, offers: &[[i64; 3]]) -> i64 {
    let mut ending: Vec<Vec<(usize, i64)>> = vec![Vec::new(); n];
    for o in offers {
        ending[o[1] as usize].push((o[0] as usize, o[2]));
    }
    let mut best = vec![0i64; n + 1];
    for i in 0..n {
        best[i + 1] = best[i];
        for &(start, gold) in &ending[i] {
            best[i + 1] = best[i + 1].max(best[start] + gold);
        }
    }
    best[n]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    a * 32768 + next_random(seed)
}

fn main() {
    let count = 20;
    let rounds = 10;
    let n: i64 = 100000;
    let mut seed = 2830;
    let mut streets: Vec<Vec<[i64; 3]>> = Vec::new();
    for _ in 0..count {
        let offers: Vec<[i64; 3]> = (0..n)
            .map(|_| {
                let start = wide(&mut seed) % n;
                let end = (start + next_random(&mut seed) % 100).min(n - 1);
                [start, end, next_random(&mut seed) % 1000 + 1]
            })
            .collect();
        streets.push(offers);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for offers in &streets {
            let a = maximize_the_profit(n as usize, offers);
            total += a;
            check = (check * 31 + a + r) % 1000000007;
        }
    }
    println!("{} streets of {}, {} rounds: gold totals {}, checksum {}", count, n, rounds, total, check);
}
