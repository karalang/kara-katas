// benchmark's Rust mirror of minimal.kara (LeetCode #2195, the ★ arm): the
// gaps walked, each a series.

fn run_sum(from: i64, to: i64) -> i64 {
    (from + to) * (to - from + 1) / 2
}

fn minimal_k_sum(nums: &[i64], k: i64) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let mut wanted = k;
    let mut sum = 0;
    let mut last = 0;
    for &x in &sorted {
        if x > last + 1 && wanted > 0 {
            let take = if x - last - 1 < wanted { x - last - 1 } else { wanted };
            sum += run_sum(last + 1, last + take);
            wanted -= take;
        }
        if x > last {
            last = x;
        }
    }
    if wanted > 0 {
        sum += run_sum(last + 1, last + wanted);
    }
    sum
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2195;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..100000 {
        let a = next_random(&mut seed);
        let b = next_random(&mut seed);
        nums.push((a * 32768 + b) % 1000000000 + 1);
    }
    let mut check: i64 = 0;
    for i in 0..300 {
        let k = 100000000 - i * 1000;
        check = (check * 31 + minimal_k_sum(&nums, k) % 1000000007) % 1000000007;
    }
    println!("300 solves over {} numbers: checksum {}", nums.len(), check);
}
