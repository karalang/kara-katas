// LeetCode #2401: Longest Nice Subarray -- the bench, the ★ arm in Rust: a
// sliding window keeping the OR of its values, values leaving from the
// left by XOR until the new one fits.

fn longest_nice_subarray(nums: &[i64]) -> i64 {
    let (mut used, mut left, mut best) = (0i64, 0usize, 0usize);
    for right in 0..nums.len() {
        while used & nums[right] != 0 {
            used ^= nums[left];
            left += 1;
        }
        used |= nums[right];
        best = best.max(right - left + 1);
    }
    best as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2401;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let mut x = 1i64 << (next_random(&mut seed) % 30);
            if next_random(&mut seed) % 2 == 0 {
                x |= 1i64 << (next_random(&mut seed) % 30);
            }
            nums.push(x);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..20 {
        for nums in &arrays {
            check = (check * 31 + longest_nice_subarray(nums) + p) % 1000000007;
        }
    }
    println!("20 passes over 20 arrays of 10^5 values: checksum {}", check);
}
