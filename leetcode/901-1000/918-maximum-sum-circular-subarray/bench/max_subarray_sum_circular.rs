// LeetCode #918: Maximum Sum Circular Subarray -- bench: Rust mirror of
// Kadane for the largest and the smallest sum in
// max_subarray_sum_circular.kara.

fn max_subarray_sum_circular(nums: &[i64]) -> i64 {
    let mut total = 0;
    let mut best_here = 0;
    let mut best = nums[0];
    let mut worst_here = 0;
    let mut worst = nums[0];
    for &v in nums {
        total += v;
        best_here = v.max(best_here + v);
        best = best.max(best_here);
        worst_here = v.min(worst_here + v);
        worst = worst.min(worst_here);
    }
    if best < 0 {
        best
    } else {
        best.max(total - worst)
    }
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn value(seed: &mut i64) -> i64 {
    let high = next_random(seed);
    (high * 2 + next_random(seed) % 2) % 60001 - 30000
}

fn main() {
    let rounds = 4000;
    let n = 30000;
    let mut seed = 918;
    let mut nums: Vec<i64> = Vec::new();
    for _ in 0..n {
        nums.push(value(&mut seed));
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..rounds {
        let i = (next_random(&mut seed) % n) as usize;
        let old = nums[i];
        nums[i] = value(&mut seed);
        let r = max_subarray_sum_circular(&nums);
        total += r;
        check = (check * 1000003 + r) % 1000000007;
        nums[i] = old;
    }
    println!("{rounds} rounds over {n} values: answers summing to {total}, checksum {check}");
}
