// LeetCode #2036: Maximum Alternating Subarray Sum -- the ★ arm in Rust,
// the same algorithm and workload as alternating.kara: the best sum ending
// here on a plus, and the one ending on a minus (none yet at the first
// value), stepped once per value.

fn maximum_alternating_subarray_sum(nums: &[i64]) -> i64 {
    let mut plus = nums[0];
    let mut minus: Option<i64> = None;
    let mut best = plus;
    for &x in nums.iter().skip(1) {
        let next_plus = match minus {
            Some(m) => x.max(m + x),
            None => x,
        };
        minus = Some(plus - x);
        plus = next_plus;
        best = best.max(plus);
        if let Some(m) = minus {
            best = best.max(m);
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2036;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for a in 0..4 {
        let top = [100000, 1000, 100000, 3][a];
        let mut nums: Vec<i64> = Vec::new();
        for _ in 0..100000 {
            let hi = next_random(&mut seed);
            let lo = next_random(&mut seed);
            nums.push((hi * 32768 + lo) % (2 * top + 1) - top);
        }
        arrays.push(nums);
    }
    let mut calls = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for round in 0..1000 {
        for a in 0..4 {
            let at = (round * 7919 + a * 104729) % 100000;
            arrays[a][at] = -arrays[a][at];
            let answer = maximum_alternating_subarray_sum(&arrays[a]);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer % 1000000007) % 1000000007;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
