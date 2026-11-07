// LeetCode #1060: Missing Element in Sorted Array -- the benchmark, the
// same algorithm as missing.kara.

fn missing_element(nums: &[i64], k: i64) -> i64 {
    let missing = |i: i64| nums[i as usize] - nums[0] - i;
    let last = nums.len() as i64 - 1;
    if missing(last) < k {
        return nums[last as usize] + k - missing(last);
    }
    // missing(lo) < k <= missing(hi)
    let mut lo = 0;
    let mut hi = last;
    while hi - lo > 1 {
        let mid = lo + (hi - lo) / 2;
        if missing(mid) < k {
            lo = mid;
        } else {
            hi = mid;
        }
    }
    nums[lo as usize] + k - missing(lo)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // 50 arrays of 50000 values, built once; 200000 values of k each
    let mut seed: i64 = 1060;
    let mut calls: i64 = 0;
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for a in 0..50 {
        let mut nums = vec![next_random(&mut seed) % 100 + 1];
        for _ in 1..50000 {
            let gap = 1 + next_random(&mut seed) % (2 + a * 3);
            nums.push(nums[nums.len() - 1] + gap);
        }
        let span = nums[49999] - nums[0] - 49999;
        for _ in 0..200000 {
            let hi = next_random(&mut seed) * 32768;
            let k = 1 + (hi + next_random(&mut seed)) % (span + 1000);
            let answer = missing_element(&nums, k);
            sum += answer;
            check = (check * 31 + answer % 1000003) % 1000000007;
            calls += 1;
        }
    }
    println!("{} calls: sum {}, checksum {}", calls, sum, check);
}
