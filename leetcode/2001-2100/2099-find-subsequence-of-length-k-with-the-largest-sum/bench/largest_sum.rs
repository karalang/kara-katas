// LeetCode #2099: Find Subsequence of Length K With the Largest Sum -- Rust
// mirror of the ★ arm's benchmark (largest_sum.kara): the same 20000 lists
// of 1000 numbers, the positions sorted by value and the chosen put back
// in order.

fn max_subsequence(nums: &[i64], k: usize) -> Vec<i64> {
    let mut order: Vec<usize> = (0..nums.len()).collect();
    order.sort_by(|&a, &b| nums[b].cmp(&nums[a]).then(a.cmp(&b)));
    let mut chosen = order[..k].to_vec();
    chosen.sort();
    chosen.iter().map(|&i| nums[i]).collect()
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
    let mut seed = 2099;
    let mut total = 0;
    let mut check: i64 = 0;
    for _ in 0..20000 {
        let nums: Vec<i64> = (0..1000).map(|_| wide_random(&mut seed) % 200001 - 100000).collect();
        let k = (next_random(&mut seed) % 1000 + 1) as usize;
        let got = max_subsequence(&nums, k);
        total += got.len();
        for &x in &got {
            check = (check * 31 + x + 100000) % 1000000007;
        }
    }
    println!("20000 answers: {total} numbers, checksum {check}");
}
