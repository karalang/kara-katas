// LeetCode #2137: Pour Water Between Buckets to Make Water Levels Equal --
// the benchmark, the same algorithm as water.kara.

fn equalize_water(buckets: &[i64], loss: i64) -> f64 {
    let keep = (100 - loss) as f64 / 100.0;
    let mut low = 0.0;
    let mut high = *buckets.iter().max().unwrap() as f64;
    for _ in 0..64 {
        let mid = (low + high) / 2.0;
        let mut spare = 0.0;
        let mut need = 0.0;
        for &b in buckets.iter() {
            let w = b as f64;
            if w > mid {
                spare += (w - mid) * keep;
            } else {
                need += mid - w;
            }
        }
        if spare >= need {
            low = mid;
        } else {
            high = mid;
        }
    }
    low
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2137;
    let mut lists: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut buckets = Vec::new();
        for _ in 0..100000 {
            buckets.push(next_random(&mut seed) % 100001);
        }
        lists.push(buckets);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for round in 0..10 {
        for l in 0..10 {
            let hi = next_random(&mut seed);
            let at = ((hi * 32768 + next_random(&mut seed)) % 100000) as usize;
            lists[l][at] = next_random(&mut seed) % 100001;
            let loss = next_random(&mut seed) % 100;
            let level = equalize_water(&lists[l], loss);
            let scaled = (level * 1048576.0 + 0.5).floor() as i64;
            total += scaled;
            check = (check * 31 + scaled + round) % 1000000007;
        }
    }
    println!("100 solves: {} in all, in steps of 2^-20, checksum {}", total, check);
}
