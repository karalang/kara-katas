// LeetCode #1493: Longest Subarray of 1's After Deleting One Element -- the
// bench in Rust, mirroring longest_subarray.kara: a sliding window holding
// at most one 0.

fn longest_subarray(nums: &[i32]) -> i32 {
    let mut best: i64 = 0;
    let mut zeros = 0;
    let mut left = 0usize;
    for right in 0..nums.len() {
        if nums[right] == 0 {
            zeros += 1;
        }
        while zeros > 1 {
            if nums[left] == 0 {
                zeros -= 1;
            }
            left += 1;
        }
        best = best.max(right as i64 - left as i64);
    }
    best as i32
}

fn main() {
    let mut seed: i64 = 1493;
    let mut nums: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums.push(if seed / 65536 % 10 == 0 { 0 } else { 1 });
    }
    let mut check: i64 = 0;
    for call in 0..1000i64 {
        let at = ((check + call * 7919) % 100000) as usize;
        nums[at] = 1 - nums[at];
        check = (check * 31 + longest_subarray(&nums) as i64 + 1) % 1000000007;
    }
    println!("1000 calls over 100000 digits: checksum {}", check);
}
