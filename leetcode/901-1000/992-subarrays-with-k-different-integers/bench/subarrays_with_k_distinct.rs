// LeetCode #992: Subarrays with K Different Integers -- bench, the ★ arm
// (at most k, less at most k - 1), the same algorithm and workload as
// subarrays_with_k_distinct.kara.

fn at_most(nums: &[i64], k: i64) -> i64 {
    let mut count = vec![0i64; nums.len() + 1];
    let mut distinct = 0;
    let mut left = 0;
    let mut total: i64 = 0;
    for right in 0..nums.len() {
        if count[nums[right] as usize] == 0 {
            distinct += 1;
        }
        count[nums[right] as usize] += 1;
        while distinct > k {
            count[nums[left] as usize] -= 1;
            if count[nums[left] as usize] == 0 {
                distinct -= 1;
            }
            left += 1;
        }
        total += right as i64 - left as i64 + 1;
    }
    total
}

fn subarrays_with_k_distinct(nums: &[i64], k: i64) -> i64 {
    at_most(nums, k) - at_most(nums, k - 1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let rounds = 100;
    let mut seed = 992;
    let arrays: Vec<Vec<i64>> = (0..20).map(|_| (0..20000).map(|_| 1 + next_random(&mut seed) % 100).collect()).collect();
    let mut found: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for i in 0..20 {
            let k = 1 + ((r * 7 + i) % 60) as i64;
            let got = subarrays_with_k_distinct(&arrays[(r + i) % 20], k);
            found += got;
            check = (check * 31 + got + 1) % 1000000007;
        }
    }
    println!("{} rounds over 20 arrays of 20000 numbers: {} subarrays, checksum {}", rounds, found, check);
}
