// LeetCode #2871: Split Array Into Maximum Number of Subarrays -- the
// bench, as split.kara: 50 arrays of 10^5 values, each answered 10 times
// by the greedy arm.

fn max_subarrays(nums: &[i64]) -> i64 {
    let mut parts = 0;
    let mut running = -1;
    for &v in nums {
        running &= v;
        if running == 0 {
            parts += 1;
            running = -1;
        }
    }
    parts.max(1)
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (50, 10, 100000);
    let mut seed = 2871;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for c in 0..count {
        let nums: Vec<i64> = (0..n)
            .map(|_| {
                if c % 2 == 0 {
                    wide(&mut seed) % 1000001
                } else {
                    (wide(&mut seed) | wide(&mut seed)) % 1000001
                }
            })
            .collect();
        arrays.push(nums);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let parts = max_subarrays(nums);
            total += parts;
            check = (check * 31 + parts + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: {total} subarrays, checksum {check}");
}
