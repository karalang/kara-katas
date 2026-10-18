// LeetCode 747 — Largest Number At Least Twice of Others, bench: the ★
// arm (one pass) on millions of 50-value lists cut from a random pool.
// Mirrors dominant_index.kara.

fn dominant_index(nums: &[i64]) -> i64 {
    let mut best = 0;
    let mut second = -1;
    for i in 1..nums.len() {
        if nums[i] > nums[best] {
            second = nums[best];
            best = i;
        } else if nums[i] > second {
            second = nums[i];
        }
    }
    if nums[best] >= 2 * second { best as i64 } else { -1 }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let queries = 2000000;
    let pool_len = 100000;
    let n = 50;
    let mut seed = 747;
    let mut pool: Vec<i64> = Vec::new();
    for _ in 0..pool_len {
        pool.push(next_random(&mut seed) % 52);
    }
    let mut nums: Vec<i64> = vec![0; n as usize];
    let mut found = 0;
    let mut total = 0;
    for q in 0..queries {
        let start = next_random(&mut seed) % (pool_len - n);
        for j in 0..n {
            nums[j as usize] = pool[(start + j) as usize];
        }
        nums[(q % n) as usize] = 100;
        let got = dominant_index(&nums);
        if got != -1 {
            found += 1;
            total += got;
        }
    }
    println!("{} lists of 50 values: {} have a dominant value, indices sum to {}", queries, found, total);
}
