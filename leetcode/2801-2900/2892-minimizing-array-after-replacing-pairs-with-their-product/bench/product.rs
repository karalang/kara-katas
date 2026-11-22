// LeetCode #2892: Minimizing Array After Replacing Pairs With Their
// Product -- the bench, as
// product.kara: 50 arrays of 10^5 values, each with its k, answered 20
// times by the greedy arm.

fn min_array_length(nums: &[i64], k: i64) -> i64 {
    if nums.contains(&0) {
        return 1;
    }
    let mut runs = 1;
    let mut product = nums[0];
    for &x in &nums[1..] {
        if product * x <= k {
            product *= x;
        } else {
            runs += 1;
            product = x;
        }
    }
    runs
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide(seed: &mut i64) -> i64 {
    next_random(seed) * 32768 + next_random(seed)
}

fn main() {
    let (count, rounds, n) = (50usize, 20i64, 100000usize);
    let mut seed = 2892;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for c in 0..count {
        let mut nums: Vec<i64> = (0..n)
            .map(|_| {
                if next_random(&mut seed) % 2 == 0 {
                    1
                } else {
                    next_random(&mut seed) % 1000 + 1
                }
            })
            .collect();
        if c % 10 == 0 {
            nums[n - 1 - c] = 0;
        }
        let k = wide(&mut seed) % 1000000000 + 1;
        cases.push((nums, k));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, k) in cases.iter() {
            let length = min_array_length(nums, *k);
            total += length;
            check = (check * 31 + length + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: lengths total {total}, checksum {check}");
}
