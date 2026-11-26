// LeetCode #1498: Number of Subsequences That Satisfy the Given Sum
// Condition -- the bench in Rust, mirroring num_subseq.kara: the values
// sorted, then two pointers.
const MOD: i64 = 1000000007;

fn num_subseq(nums: &[i32], target: i32) -> i32 {
    let mut sorted = nums.to_vec();
    sorted.sort();
    let n = sorted.len() as i64;
    let mut pow2 = vec![1i64; n as usize];
    for i in 1..n as usize {
        pow2[i] = pow2[i - 1] * 2 % MOD;
    }
    let mut count = 0i64;
    let mut lo: i64 = 0;
    let mut hi: i64 = n - 1;
    while lo <= hi {
        if sorted[lo as usize] + sorted[hi as usize] <= target {
            count = (count + pow2[(hi - lo) as usize]) % MOD;
            lo += 1;
        } else {
            hi -= 1;
        }
    }
    count as i32
}

fn main() {
    let mut seed: i64 = 1498;
    let mut nums: Vec<i32> = Vec::new();
    for _ in 0..100000 {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        nums.push((1 + seed / 65536 * 31 % 1000000) as i32);
    }
    let mut check: i64 = 0;
    for call in 0..200i64 {
        let at = ((check + call * 7919) % 100000) as usize;
        nums[at] = (1 + (check + call) % 1000000) as i32;
        let target = 1 + (check * 13 + call) % 1000000;
        check = (check * 31 + num_subseq(&nums, target as i32) as i64) % 1000000007;
    }
    println!("200 calls over 100000 values: checksum {}", check);
}
