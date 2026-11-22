// LeetCode #2875: Minimum Size Subarray in Infinite Array -- the bench,
// as infinite.kara: 50 arrays of 10^5 values, each with its target,
// answered 20 times by the sliding-window arm.

fn min_size_subarray(nums: &[i64], target: i64) -> i64 {
    let n = nums.len();
    let total: i64 = nums.iter().sum();
    let whole = target / total * n as i64;
    let rest = target % total;
    if rest == 0 {
        return whole;
    }
    let mut best: i64 = -1;
    let mut sum = 0;
    let mut left = 0;
    for right in 0..2 * n {
        sum += nums[right % n];
        while sum > rest {
            sum -= nums[left % n];
            left += 1;
        }
        let length = (right - left + 1) as i64;
        if sum == rest && (best < 0 || length < best) {
            best = length;
        }
    }
    if best < 0 {
        -1
    } else {
        whole + best
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (50, 20i64, 100000);
    let mut seed = 2875;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for c in 0..count {
        let top = if c % 2 == 1 { 10 } else { 100000 };
        let nums: Vec<i64> = (0..n).map(|_| wide(&mut seed) % top + 1).collect();
        let target = wide(&mut seed) % 1000000000 + 1;
        cases.push((nums, target));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, target) in cases.iter() {
            let length = min_size_subarray(nums, *target);
            total += length;
            check = (check * 31 + length + 1 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}");
}
