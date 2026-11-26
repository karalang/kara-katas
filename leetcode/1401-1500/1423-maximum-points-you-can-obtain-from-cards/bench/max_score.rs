fn max_score(card_points: &[i32], k: i32) -> i32 {
    let n = card_points.len();
    let k = k as usize;
    let mut sum: i32 = card_points[..k].iter().sum();
    let mut best = sum;
    for i in 0..k {
        sum += card_points[n - 1 - i] - card_points[k - 1 - i];
        best = best.max(sum);
    }
    best
}

fn main() {
    let mut seed: i64 = 1423;
    let mut pool: Vec<i32> = Vec::with_capacity(1000000);
    for _ in 0..1000000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        pool.push((1 + seed / 65536 % 10000) as i32);
    }
    let mut check: i64 = 0;
    for _ in 0..50000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let start = (seed / 65536 % 900001) as usize;
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = (1 + seed / 65536 % 100000) as i32;
        check = (check * 131 + max_score(&pool[start..start + 100000], k) as i64) % 1000000007;
    }
    println!("5 * 10^4 windows of 10^5 cards: checksum {}", check);
}
