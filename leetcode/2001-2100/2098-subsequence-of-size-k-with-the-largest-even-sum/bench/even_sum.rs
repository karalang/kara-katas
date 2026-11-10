// LeetCode #2098: Subsequence of Size K With the Largest Even Sum -- Rust
// mirror of the ★ arm's benchmark (even_sum.kara): the same 200 lists of
// 100000 numbers, each sorted largest first and given the better swap.

fn largest_even_sum(nums: &[i64], k: usize) -> i64 {
    let mut sorted = nums.to_vec();
    sorted.sort_by(|a, b| b.cmp(a));
    let sum: i64 = sorted[..k].iter().sum();
    if sum % 2 == 0 {
        return sum;
    }
    let taken_odd = sorted[..k].iter().filter(|&&x| x % 2 == 1).min();
    let taken_even = sorted[..k].iter().filter(|&&x| x % 2 == 0).min();
    let left_odd = sorted[k..].iter().filter(|&&x| x % 2 == 1).max();
    let left_even = sorted[k..].iter().filter(|&&x| x % 2 == 0).max();
    let mut best = -1;
    if let (Some(&o), Some(&e)) = (taken_odd, left_even) {
        best = best.max(sum - o + e);
    }
    if let (Some(&e), Some(&o)) = (taken_even, left_odd) {
        best = best.max(sum - e + o);
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
    let mut seed = 2098;
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for _ in 0..200 {
        let nums: Vec<i64> = (0..100000).map(|_| wide_random(&mut seed) % 100001).collect();
        let k = (wide_random(&mut seed) % 100000 + 1) as usize;
        let got = largest_even_sum(&nums, k);
        total += got;
        check = (check * 31 + got + 1) % 1000000007;
    }
    println!("200 answers: sum {total}, checksum {check}");
}
