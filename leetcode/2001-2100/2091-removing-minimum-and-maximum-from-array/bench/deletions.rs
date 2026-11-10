// LeetCode #2091: Removing Minimum and Maximum From Array -- Rust mirror of
// the ★ arm's benchmark (deletions.kara): the same 20 shuffled arrays, each
// answered 20 times by the same walk over a `Vec`.

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn minimum_deletions(nums: &[i64]) -> i64 {
    let n = nums.len();
    let (mut lo, mut hi) = (0usize, 0usize);
    for k in 1..n {
        if nums[k] < nums[lo] {
            lo = k;
        }
        if nums[k] > nums[hi] {
            hi = k;
        }
    }
    let (i, j) = (lo.min(hi), lo.max(hi));
    (j + 1).min(n - i).min(i + 1 + n - j) as i64
}

fn main() {
    let mut seed = 2091i64;
    let mut arrays: Vec<Vec<i64>> = Vec::new();
    for _ in 0..20 {
        let mut v: Vec<i64> = (0..100000i64).map(|i| 2 * i - 100000).collect();
        for i in (1..100000usize).rev() {
            let j = (next_random(&mut seed) % (i as i64 + 1)) as usize;
            v.swap(i, j);
        }
        arrays.push(v);
    }
    let (mut total, mut check) = (0i64, 0i64);
    for round in 0..20 {
        for t in 0..20 {
            let d = minimum_deletions(&arrays[(t + round) % 20]);
            total += d;
            check = (check * 31 + d) % 1000000007;
        }
    }
    println!("400 answers: sum {}, checksum {}", total, check);
}
