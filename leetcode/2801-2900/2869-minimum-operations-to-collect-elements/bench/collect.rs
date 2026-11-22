// LeetCode #2869: Minimum Operations to Collect Elements -- the bench,
// as collect.kara: 50000 arrays of 50 values, each answered 20 times by
// the bit-mask arm.

fn min_operations(nums: &[i64], k: i64) -> i64 {
    let full: i64 = (1 << k) - 1;
    let mut mask: i64 = 0;
    let n = nums.len();
    for i in (0..n).rev() {
        if nums[i] <= k {
            mask |= 1 << (nums[i] - 1);
        }
        if mask == full {
            return (n - i) as i64;
        }
    }
    n as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (count, rounds, n) = (50000, 20, 50i64);
    let mut seed = 2869;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let mut nums: Vec<i64> = (0..n).map(|_| next_random(&mut seed) % n + 1).collect();
        let at = (next_random(&mut seed) % n) as usize;
        nums[at] = 1;
        let mut reach = 1;
        while nums.contains(&(reach + 1)) {
            reach += 1;
        }
        let k = next_random(&mut seed) % reach + 1;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in cases.iter() {
            let ops = min_operations(nums, *k);
            total += ops;
            check = (check * 31 + ops + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: {total} operations, checksum {check}");
}
