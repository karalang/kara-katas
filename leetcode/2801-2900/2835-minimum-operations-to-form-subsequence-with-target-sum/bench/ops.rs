// LeetCode #2835: Minimum Operations to Form Subsequence With Target Sum
// -- the bench, mirrored from ops.kara: counts by bit, low to high.

fn min_operations(nums: &[i64], target: i64) -> i64 {
    if nums.iter().sum::<i64>() < target {
        return -1;
    }
    let mut count: Vec<i64> = vec![0; 32];
    for &x in nums.iter() {
        count[x.trailing_zeros() as usize] += 1;
    }
    let mut ops = 0;
    for i in 0..31 {
        if (target >> i) & 1 == 1 {
            if count[i] > 0 {
                count[i] -= 1;
            } else {
                let mut j = i + 1;
                while count[j] == 0 {
                    j += 1;
                }
                ops += (j - i) as i64;
                count[j] -= 1;
                for k in i..j {
                    count[k] += 1;
                }
            }
        }
        count[i + 1] += count[i] / 2;
    }
    ops
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 2000;
    let rounds = 200;
    let n = 1000;
    let mut seed = 2835;
    let mut cases: Vec<(Vec<i64>, i64)> = Vec::new();
    for _ in 0..count {
        let nums: Vec<i64> = (0..n).map(|_| 1i64 << (next_random(&mut seed) % 15 + 16)).collect();
        let hi = next_random(&mut seed);
        let target = (hi * 32768 + next_random(&mut seed)) % 2147483647 + 1;
        cases.push((nums, target));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for (nums, target) in cases.iter() {
            let ops = min_operations(nums, *target);
            total += ops;
            check = (check * 31 + ops + 1 + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n}, {rounds} rounds: operations total {total}, checksum {check}");
}
