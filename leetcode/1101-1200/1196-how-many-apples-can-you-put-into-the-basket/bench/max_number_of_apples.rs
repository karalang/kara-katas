// LeetCode #1196 bench: the ★ arm in Rust, over the same 200 baskets of
// 10^3 apples and 200 rounds as the Kāra bench; each call sorts its own
// copy with the standard `sort`.

fn max_number_of_apples(mut weight: Vec<i64>) -> i64 {
    weight.sort();
    let mut load = 0;
    for (i, &w) in weight.iter().enumerate() {
        load += w;
        if load > 5000 {
            return i as i64;
        }
    }
    weight.len() as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let lows = [1, 1, 300, 1];
    let highs = [1000, 20, 1000, 100];
    let mut seed = 1196;
    let mut baskets: Vec<Vec<i64>> = Vec::new();
    for k in 0..200 {
        let low = lows[k % 4];
        let high = highs[k % 4];
        let basket: Vec<i64> = (0..1000)
            .map(|_| low + next_random(&mut seed) % (high - low + 1))
            .collect();
        baskets.push(basket);
    }
    let mut check: i64 = 0;
    for _ in 0..200 {
        for basket in &baskets {
            let apples = max_number_of_apples(basket.clone());
            check = (check * 131 + apples + 1) % 1000000007;
        }
    }
    println!("200 rounds of 200 baskets of 1000 apples: checksum {}", check);
}
