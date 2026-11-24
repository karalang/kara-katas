// LeetCode #1330 bench, Rust mirror of the Kāra bench: the ★ arm (the
// prefix, suffix and inside reversals' best gains in one pass) on 20 arrays
// of 3 * 10^4 values, the constraints' longest, within 30000 of 0, built
// once. Then 75 passes, each setting one value of every array from the
// checksum so far, answering it and folding the answer plus the pass into
// the checksum.

fn max_value_after_reverse(nums: &[i32]) -> i32 {
    let n = nums.len();
    let mut total: i32 = 0;
    let mut gain: i32 = 0;
    let mut high_low = i32::MIN;
    let mut low_high = i32::MAX;
    for i in 0..n - 1 {
        let a = nums[i];
        let b = nums[i + 1];
        let d = (a - b).abs();
        total += d;
        gain = gain.max((nums[0] - b).abs() - d);
        gain = gain.max((nums[n - 1] - a).abs() - d);
        high_low = high_low.max(a.min(b));
        low_high = low_high.min(a.max(b));
    }
    if n > 1 {
        gain = gain.max(2 * (high_low - low_high));
    }
    total + gain
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let n: usize = 30000;
    let mut seed: i64 = 1330;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..20 {
        let mut nums: Vec<i32> = Vec::new();
        for _ in 0..n {
            nums.push((next_random(&mut seed) % 60001 - 30000) as i32);
        }
        arrays.push(nums);
    }
    let mut check: i64 = 0;
    for pass in 0..75 {
        for t in 0..20 {
            let at = (check % n as i64) as usize;
            arrays[t][at] = ((check / 7) % 60001 - 30000) as i32;
            let got = max_value_after_reverse(&arrays[t]);
            check = (check * 31 + got as i64 + pass) % 1000000007;
        }
    }
    println!("75 passes over 20 arrays of 3 * 10^4: checksum {check}");
}
