// LeetCode #2444: Count Subarrays With Fixed Bounds -- the bench, the ★
// arm: one pass keeping the last value outside the bounds, the last
// `min_k` and the last `max_k`.

fn count_subarrays(nums: &[i64], min_k: i64, max_k: i64) -> i64 {
    let mut count = 0i64;
    let mut bad = -1i64;
    let mut last_min = -1i64;
    let mut last_max = -1i64;
    for i in 0..nums.len() {
        let x = nums[i];
        let k = i as i64;
        if x < min_k || x > max_k {
            bad = k;
        }
        if x == min_k {
            last_min = k;
        }
        if x == max_k {
            last_max = k;
        }
        count += (last_min.min(last_max) - bad).max(0);
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2444i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(1 + next_random(&mut seed) % 20);
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..100i64 {
        for c in 0..arrays.len() {
            let at = ((p * 7919 + c as i64 * 104729) % 100000) as usize;
            arrays[c][at] = 1 + next_random(&mut seed) % 20;
            check = (check * 31 + count_subarrays(&arrays[c], 3, 17) + p) % 1000000007;
        }
    }
    println!("100 passes over 10 arrays of 10^5 values: checksum {}", check);
}
