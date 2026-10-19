// LeetCode 795 — Number of Subarrays with Bounded Maximum: the bench, in
// Rust. Mirrors num_subarray_bounded_max.kara: one pass, keeping the
// last place of a number above right and of one in range.

fn num_subarray_bounded_max(nums: &[i64], left: i64, right: i64) -> i64 {
    let mut too_big: i64 = -1;
    let mut in_range: i64 = -1;
    let mut count = 0;
    for i in 0..nums.len() {
        if nums[i] > right {
            too_big = i as i64;
        } else if nums[i] >= left {
            in_range = i as i64;
        }
        if in_range > too_big {
            count += in_range - too_big;
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big_random(seed: &mut i64) -> i64 {
    let a = next_random(seed);
    let b = next_random(seed);
    (a * 32768 + b) % 1000000001
}

fn main() {
    let mut seed = 795;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..16 {
        let mut nums = Vec::new();
        for _ in 0..100000 {
            nums.push(big_random(&mut seed));
        }
        arrays.push(nums);
    }
    let rounds = 8000;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        let a = big_random(&mut seed);
        let b = big_random(&mut seed);
        let count = num_subarray_bounded_max(&arrays[r % 16], a.min(b), a.max(b));
        total += count;
        check = (check * 131 + count % 1000000007) % 1000000007;
    }
    println!("{rounds} rounds of 100000 numbers: {total} subarrays, checksum {check}");
}
