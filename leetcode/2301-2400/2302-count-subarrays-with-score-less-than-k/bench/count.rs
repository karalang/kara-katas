// LeetCode #2302: Count Subarrays With Score Less Than K -- the bench,
// the ★ arm in Rust. A sliding window, narrowed at the left while its
// score is `k` or more, counting every subarray ending at its right end.

fn count_subarrays(nums: &[i64], k: i64) -> i64 {
    let mut count = 0i64;
    let mut sum = 0i64;
    let mut left = 0usize;
    for right in 0..nums.len() {
        sum += nums[right];
        while sum * (right - left + 1) as i64 >= k {
            sum -= nums[left];
            left += 1;
        }
        count += (right - left + 1) as i64;
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2302;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            nums.push((hi * 32768 + next_random(&mut seed)) % 100000 + 1);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..30i64 {
        for a in 0..20usize {
            check = (check * 31 + count_subarrays(&arrays[a], 1000000000 * (a as i64 + 1) + pass)) % 1000000007;
        }
    }
    println!("30 passes over 20 arrays of 10^5: checksum {}", check);
}
