// LeetCode #2270: Number of Ways to Split Array -- the bench, the ★ arm.

fn ways_to_split_array(nums: &[i64]) -> i64 {
    let total: i64 = nums.iter().sum();
    let mut left = 0;
    let mut ways = 0;
    for i in 0..nums.len() - 1 {
        left += nums[i];
        if left >= total - left {
            ways += 1;
        }
    }
    ways
}

// ---- bench harness ---------------------------------------------------------

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2270;
    let mut check = 0;
    for _ in 0..100 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            nums.push(next_random(&mut seed) % 200001 - 100000);
        }
        check = (check * 31 + ways_to_split_array(&nums)) % 1000000007;
    }
    println!("100 arrays of 10^5: checksum {check}");
}
