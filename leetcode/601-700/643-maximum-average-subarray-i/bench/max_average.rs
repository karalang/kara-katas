// Benchmark for #643: mirror of max_average.kara (the ★ arm: a sliding
// sum) on the same workload.

fn find_max_average(nums: &[i64], k: usize) -> f64 {
    let mut sum: i64 = 0;
    for i in 0..k {
        sum += nums[i];
    }
    let mut best = sum;
    for i in k..nums.len() {
        sum += nums[i] - nums[i - k];
        if sum > best {
            best = sum;
        }
    }
    best as f64 / k as f64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed: i64 = 643;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(next_random(&mut seed) % 20001 - 10000);
        }
        arrays.push(nums);
    }
    let rounds = 4000;
    let mut total = 0.0;
    for r in 0..rounds {
        let k = 1 + (r * 7919) % 100000;
        total += find_max_average(&arrays[r % 20], k);
    }
    println!("{} rounds over 20 arrays of 100000 values: answers adding to {:.5}", rounds, total);
}
