// LeetCode #60 — rayon-parallel Rust mirror (par lane, FACTORIAL solver).
// Same factorial-number-system generator + position-weighted checksum as
// ../../permutation_sequence.rs; the K=500k reduction runs across a rayon
// pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches the
// kara/rust/c/go mirrors.

fn get_permutation(n: i64, k: i64) -> Vec<i64> {
    let mut fact: Vec<i64> = vec![1];
    for i in 1..=n {
        fact.push(fact[(i - 1) as usize] * i);
    }
    let mut digits: Vec<i64> = (1..=n).collect();
    let mut kk = k - 1;
    let mut result: Vec<i64> = Vec::new();
    for pos in 0..n {
        let block = fact[(n - 1 - pos) as usize];
        let idx = kk / block;
        kk %= block;
        result.push(digits.remove(idx as usize));
    }
    result
}

fn checksum(perm: &[i64], n: i64) -> i64 {
    let mut s = 0i64;
    for i in 0..n {
        s += perm[i as usize] * (i + 1);
    }
    s
}

fn main() {
    use rayon::prelude::*;
    const NTAB: [i64; 9] = [9, 8, 9, 7, 8, 9, 6, 7, 9];
    const KTAB: [i64; 9] = [362880, 40320, 181440, 5040, 20160, 300000, 720, 2520, 250000];
    let m: i64 = 9;
    let k_iters: i64 = 500_000;

    let total: i64 = (0..k_iters)
        .into_par_iter()
        .map(|k| {
            let idx = (k % m) as usize;
            let perm = get_permutation(NTAB[idx], KTAB[idx]);
            checksum(&perm, NTAB[idx])
        })
        .sum();
    println!("{}", total);
}
