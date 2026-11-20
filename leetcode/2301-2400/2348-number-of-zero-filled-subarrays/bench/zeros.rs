// LeetCode #2348: Number of Zero-Filled Subarrays -- the bench, the ★ arm
// in Rust: the length of the run of zeros ending at each place, summed.

fn zero_filled_subarray(nums: &[i64]) -> i64 {
    let mut run = 0i64;
    let mut total = 0i64;
    for &x in nums {
        if x == 0 {
            run += 1;
        } else {
            run = 0;
        }
        total += run;
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // array a holds a value that is not zero with a chance of 1 in a + 2
    let mut seed = 2348i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..10i64 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let r = next_random(&mut seed);
            nums.push(if r % (a + 2) == 0 { r + 1 } else { 0 });
        }
        arrays.push(nums);
    }
    let mut check = 0i64;
    for p in 0..60i64 {
        for nums in &arrays {
            check = (check * 31 + zero_filled_subarray(nums) + p) % 1000000007;
        }
    }
    println!("60 passes over 10 arrays of 10^5 values: checksum {}", check);
}
