// LeetCode #915: Partition Array into Disjoint Intervals -- bench: Rust
// mirror of the largest on the left against the smallest on the right in
// partition_disjoint.kara.

fn partition_disjoint(nums: &[i64]) -> i64 {
    let n = nums.len();
    let mut least_after = vec![0i64; n];
    least_after[n - 1] = nums[n - 1];
    let mut i = n - 1;
    while i > 0 {
        i -= 1;
        least_after[i] = nums[i].min(least_after[i + 1]);
    }
    let mut most = nums[0];
    for k in 1..n {
        if most <= least_after[k] {
            return k as i64;
        }
        most = most.max(nums[k]);
    }
    n as i64
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn big(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    (high * 32768 + next_random(seed)) % 1000001
}

fn main() {
    let rounds = 2000;
    let n = 100000;
    let mut seed = 915;
    let mut nums: Vec<i64> = Vec::new();
    for i in 0..n {
        let v = big(&mut seed) % 500000;
        nums.push(if i < n / 2 { v } else { 500000 + v });
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        let i = (big(&mut seed) % n as i64) as usize;
        let old = nums[i];
        nums[i] = big(&mut seed);
        let k = partition_disjoint(&nums);
        total += k;
        check = (check * 1000003 + k) % 1000000007;
        nums[i] = old;
    }
    println!(
        "{} rounds over {} values: left sides summing to {}, checksum {}",
        rounds, n, total, check
    );
}
