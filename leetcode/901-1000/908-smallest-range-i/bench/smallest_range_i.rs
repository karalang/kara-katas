// LeetCode #908: Smallest Range I -- bench program, Rust.
//
// The largest and smallest values, over 500,000 numbers up to 10^4 built
// once. Each round scores them with a k that changes from round to round,
// folds the score into a checksum and changes one number.

fn smallest_range_i(nums: &[i64], k: i64) -> i64 {
    let mut lo = nums[0];
    let mut hi = nums[0];
    for i in 1..nums.len() {
        lo = lo.min(nums[i]);
        hi = hi.max(nums[i]);
    }
    (hi - lo - 2 * k).max(0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 500000;
    let rounds: i64 = 500;
    let mut seed: i64 = 908;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(next_random(&mut seed) % 10001);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..rounds {
        let got = smallest_range_i(&nums, round * 37 % 5001);
        total += got;
        check = (check * 31 + got) % 1000000007;
        nums[(round as usize) * 7919 % n] = next_random(&mut seed) % 10001;
    }
    println!("{} rounds over {} numbers: scores summing to {}, checksum {}", rounds, n, total, check);
}
