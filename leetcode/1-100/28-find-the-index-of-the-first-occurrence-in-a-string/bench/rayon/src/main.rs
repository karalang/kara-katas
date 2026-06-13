// LeetCode #28 — rayon-parallel Rust mirror (par lane, brute_force).
// Same brute-force sliding-window str_str as ../brute_force.rs; the K-call
// reduction runs across a rayon pool. Hand-tuned-parallel comparator for
// Kāra's auto-par (which parallelizes the same K-loop from zero parallel
// source). Sink = 199998400 (K=100 × first-match index 1999984).
use rayon::prelude::*;

fn str_str(haystack: &[u8], needle: &[u8]) -> i64 {
    let hn = haystack.len() as i64;
    let nn = needle.len() as i64;
    if nn == 0 {
        return 0;
    }
    if nn > hn {
        return -1;
    }
    let mut i = 0i64;
    while i <= hn - nn {
        let mut j = 0i64;
        while j < nn && haystack[(i + j) as usize] == needle[j as usize] {
            j += 1;
        }
        if j == nn {
            return i;
        }
        i += 1;
    }
    -1
}

fn main() {
    const N: usize = 2_000_000;
    const M: usize = 16;

    let mut haystack = vec![b'a'; N];
    haystack[N - 1] = b'b';
    let mut needle = vec![b'a'; M];
    needle[M - 1] = b'b';

    let total: i64 = (0..100)
        .into_par_iter()
        .map(|_| str_str(&haystack, &needle))
        .sum();
    println!("{}", total);
}
