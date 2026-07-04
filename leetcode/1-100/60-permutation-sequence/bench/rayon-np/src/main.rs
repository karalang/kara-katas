// LeetCode #60 — rayon-parallel Rust mirror (par lane, NEXT-PERM solver).
// Same next_permutation-iterate generator + position-weighted checksum as
// ../../permutation_sequence_nextperm.rs; the K=333 reduction runs across a
// rayon pool. Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches
// the kara/rust/c/go mirrors.

fn next_permutation(a: &mut [i64]) {
    let len = a.len() as i64;
    let mut i = len - 2;
    while i >= 0 && a[i as usize] >= a[(i + 1) as usize] {
        i -= 1;
    }
    if i >= 0 {
        let mut j = len - 1;
        while a[j as usize] <= a[i as usize] {
            j -= 1;
        }
        a.swap(i as usize, j as usize);
    }
    let mut lo = i + 1;
    let mut hi = len - 1;
    while lo < hi {
        a.swap(lo as usize, hi as usize);
        lo += 1;
        hi -= 1;
    }
}

fn get_permutation(n: i64, k: i64) -> Vec<i64> {
    let mut a: Vec<i64> = (1..=n).collect();
    for _ in 0..(k - 1) {
        next_permutation(&mut a);
    }
    a
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
    let k_iters: i64 = 333;

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
