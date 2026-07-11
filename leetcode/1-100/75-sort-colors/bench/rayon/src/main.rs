// LeetCode #75 — rayon-parallel Rust mirror (par lane).
// Same batch of K=2000 independent Dutch National Flag sorts as ../sort_colors.rs;
// the associative sum reduction runs across a rayon pool. Hand-tuned-parallel
// comparator for Kāra's auto-par. Sink matches the seq mirrors.
use rayon::prelude::*;

const N: i64 = 59999;

fn sort_and_hash(seed: i64) -> i64 {
    let mut a: Vec<i64> = Vec::new();
    for j in 0..N {
        a.push((j * 7 + seed) % 3);
    }
    let mut low: usize = 0;
    let mut mid: usize = 0;
    let mut high: i64 = N - 1;
    while mid as i64 <= high {
        if a[mid] == 0 {
            a.swap(low, mid);
            low += 1;
            mid += 1;
        } else if a[mid] == 1 {
            mid += 1;
        } else {
            a.swap(mid, high as usize);
            high -= 1;
        }
    }
    let mut acc: i64 = 0;
    for j in 0..N as usize {
        acc = (acc * 131 + a[j]) % 1_000_000_007;
    }
    acc
}

fn main() {
    let sum: i64 = (0..2000_i64).into_par_iter().map(sort_and_hash).sum();
    println!("{}", sum);
}
