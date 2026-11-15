// benchmark's Rust mirror of top.kara (LeetCode #2202, the ★ arm): the
// first k - 1 numbers and the one at index k.

fn maximum_top(nums: &[i64], k: i64) -> i64 {
    let n = nums.len() as i64;
    if n == 1 {
        return if k % 2 == 1 { -1 } else { nums[0] };
    }
    let mut best = -1;
    for i in 0..(k - 1).min(n) {
        best = best.max(nums[i as usize]);
    }
    if k < n {
        best = best.max(nums[k as usize]);
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn wide_random(seed: &mut i64) -> i64 {
    let hi = next_random(seed);
    hi * 32768 + next_random(seed)
}

fn main() {
    let mut seed = 2202;
    let mut piles: Vec<Vec<i64>> = Vec::new();
    let mut ks: Vec<Vec<i64>> = Vec::new();
    for _ in 0..10 {
        piles.push(
            (0..100000)
                .map(|_| wide_random(&mut seed) % 1000000001)
                .collect(),
        );
        ks.push((0..10).map(|_| wide_random(&mut seed) % 100002).collect());
    }
    let mut check: i64 = 0;
    for _ in 0..50 {
        for p in 0..10 {
            for &k in &ks[p] {
                check = (check * 31 + maximum_top(&piles[p], k) + 1) % 1000000007;
            }
        }
    }
    println!("50 passes over 10 piles: checksum {}", check);
}
