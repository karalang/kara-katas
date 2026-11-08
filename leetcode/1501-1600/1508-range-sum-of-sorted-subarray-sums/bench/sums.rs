// LeetCode #1508: Range Sum of Sorted Subarray Sums -- the bench: 40 arrays
// of 1000 numbers built once, then 25 ranges of places asked of each, by
// the ★ arm.

const MOD: i64 = 1000000007;

fn at_most(prefix: &[i64], twice: &[i64], bound: i64) -> (i64, i64) {
    let n = prefix.len() - 1;
    let (mut count, mut total, mut i) = (0i64, 0i64, 0usize);
    for j in 1..n + 1 {
        while prefix[j] - prefix[i] > bound {
            i += 1;
        }
        let w = (j - i) as i64;
        count += w;
        total += w * prefix[j] - (twice[j] - twice[i]);
    }
    (count, total)
}

fn smallest(prefix: &[i64], twice: &[i64], k: i64) -> i64 {
    if k == 0 {
        return 0;
    }
    let (mut lo, mut hi) = (1, prefix[prefix.len() - 1]);
    while lo < hi {
        let mid = (lo + hi) / 2;
        if at_most(prefix, twice, mid).0 >= k {
            hi = mid;
        } else {
            lo = mid + 1;
        }
    }
    let (count, total) = at_most(prefix, twice, lo);
    total - (count - k) * lo
}

fn range_sum(nums: &[i64], n: usize, left: i64, right: i64) -> i64 {
    let mut prefix = vec![0i64; n + 1];
    for i in 0..n {
        prefix[i + 1] = prefix[i] + nums[i];
    }
    let mut twice = vec![0i64; n + 1];
    for i in 0..n {
        twice[i + 1] = twice[i] + prefix[i];
    }
    (smallest(&prefix, &twice, right) - smallest(&prefix, &twice, left - 1)) % MOD
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1508;
    let arrays: Vec<Vec<i64>> = (0..40)
        .map(|_| (0..1000).map(|_| next_random(&mut seed) % 100 + 1).collect())
        .collect();
    let total = 1000 * 1001 / 2;
    let mut check: i64 = 0;
    for _ in 0..25 {
        for nums in &arrays {
            let a = next_random(&mut seed) % total + 1;
            let b = next_random(&mut seed) % total + 1;
            check = (check * 31 + range_sum(nums, 1000, a.min(b), a.max(b)) + 1) % 1000000007;
        }
    }
    println!("1000 ranges over 40 arrays of 1000 numbers: checksum {}", check);
}
