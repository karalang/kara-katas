// LeetCode #1712: Ways to Split Array Into Three Subarrays -- the Rust
// mirror of the bench (split.kara): prefix sums, and for each end of the
// left part two `partition_point` searches, on 20 random arrays of 100000
// values, each answered 10 times.

fn ways_to_split(nums: &[i32]) -> i32 {
    let n = nums.len();
    let mut prefix: Vec<i64> = vec![0];
    for &x in nums.iter() {
        prefix.push(prefix[prefix.len() - 1] + x as i64);
    }
    let total = prefix[n];
    let mut ways: i64 = 0;
    for i in 1..n - 1 {
        let left = prefix[i];
        let lo = prefix.partition_point(|&p| p < 2 * left).max(i + 1);
        let hi = prefix.partition_point(|&p| 2 * p <= total + left).min(n);
        if hi > lo {
            ways += (hi - lo) as i64;
        }
    }
    (ways % 1000000007) as i32
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 20;
    let rounds: i64 = 10;
    let n = 100000;
    let mut seed: i64 = 1712;
    let mut arrays: Vec<Vec<i32>> = Vec::new();
    for _ in 0..count {
        arrays.push((0..n).map(|_| (next_random(&mut seed) % 10001) as i32).collect());
    }
    let mut sum: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        for nums in arrays.iter() {
            let answer = ways_to_split(nums) as i64;
            sum += answer;
            check = (check * 31 + answer + r) % 1000000007;
        }
    }
    println!("{count} arrays of {n} values, {rounds} rounds: answers sum to {sum}, checksum {check}");
}
