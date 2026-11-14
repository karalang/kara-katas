// LeetCode #1558: Minimum Numbers of Function Calls to Make Target Array --
// bench: the ★ arm (every value's 1 bits, and the widest value's length
// less one) over 20 arrays of 100000 values, built once, each asked 30
// times. Rust mirror of calls.kara.

fn min_operations(nums: &[i64]) -> i64 {
    let mut increments = 0i64;
    let mut widest = 0i64;
    for &x in nums {
        increments += x.count_ones() as i64;
        if x > 0 {
            widest = widest.max(64 - x.leading_zeros() as i64);
        }
    }
    increments + (widest - 1).max(0)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn mix(check: i64, x: i64) -> i64 {
    (check * 31 + x + 1) % 1000000007
}

fn main() {
    let mut seed = 1558;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            let bits = next_random(&mut seed) % 30 + 1;
            let draw = next_random(&mut seed) * 32768 + next_random(&mut seed);
            nums.push(draw % (1i64 << bits));
        }
        arrays.push(nums);
    }
    let mut check = 0;
    let mut total = 0;
    for _ in 0..30 {
        for nums in &arrays {
            let calls = min_operations(nums);
            total += calls;
            check = mix(check, calls);
        }
    }
    println!("30 passes over 20 arrays of 100000 values: {} calls, checksum {}", total, check);
}
