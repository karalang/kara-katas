// LeetCode #724: Find Pivot Index -- the total, then one running sum.
// Benchmark mirror of the Kara star arm: the total once, then a walk
// from the left keeping the sum of the numbers passed, stopping at the
// first index whose left sum equals what is left on the right.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn pivot_index(nums: &[i64]) -> i64 {
    let mut total = 0;
    for x in nums.iter() {
        total += *x;
    }
    let mut left = 0;
    for i in 0..nums.len() {
        if left == total - left - nums[i] {
            return i as i64;
        }
        left += nums[i];
    }
    -1
}

fn main() {
    let mut seed: i64 = 724;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..50 {
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..4999 {
            nums.push(next_random(&mut seed) % 2001 - 1000);
        }
        nums.push(next_random(&mut seed) % 2001 - 1000);
        for j in 0..4999 {
            nums.push(nums[4998 - j]);
        }
        arrays.push(nums);
    }
    let mut sum = 0;
    for round in 0..1000 {
        for k in 0..50 {
            let p = (round * 7919 + k * 31) % 9999;
            arrays[k][p] = -arrays[k][p];
            sum += pivot_index(&arrays[k]);
        }
    }
    println!("1000 rounds of 50 arrays of 9999 numbers: sum {}", sum);
}
