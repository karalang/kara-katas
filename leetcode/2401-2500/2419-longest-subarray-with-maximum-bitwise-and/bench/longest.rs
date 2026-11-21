// LeetCode #2419: Longest Subarray With Maximum Bitwise AND -- the bench,
// the ★ arm in Rust: one scan keeping the largest value so far and the
// run of it ending here.

fn longest_subarray(nums: &[i64]) -> i64 {
    let (mut top, mut run, mut best) = (0, 0, 0);
    for &x in nums {
        if x > top {
            top = x;
            run = 0;
            best = 0;
        }
        if x == top {
            run += 1;
            best = best.max(run);
        } else {
            run = 0;
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2419;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for i in 0..10 {
        let mut nums: Vec<i64> = Vec::new();
        for k in 0..100000 {
            if k > 0 && next_random(&mut seed) % 2 == 0 {
                nums.push(nums[k - 1]);
            } else {
                nums.push(1 + next_random(&mut seed) % (2 + 100 * i));
            }
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for p in 0..500 {
        for nums in arrays.iter() {
            check = (check * 31 + longest_subarray(nums) + p) % 1000000007;
        }
    }
    println!("500 passes over 10 arrays of 10^5 values: checksum {}", check);
}
