// LeetCode #87 — rayon-parallel Rust mirror (par lane).
// Same batch of K=60000 independent memoized scramble decisions as
// ../scramble_string.rs; the associative sum reduction runs across a rayon pool.
// Hand-tuned-parallel comparator for Kāra's auto-par. Sink matches the seq mirrors.
use rayon::prelude::*;

fn scramble(s1: &[u8], i1: i64, s2: &[u8], i2: i64, len: i64, memo: &mut [i64], n: i64) -> bool {
    if len == 0 {
        return true;
    }
    let key = ((i1 * n + i2) * (n + 1) + len) as usize;
    if memo[key] != -1 {
        return memo[key] == 1;
    }
    let mut equal = true;
    for k in 0..len {
        if s1[(i1 + k) as usize] != s2[(i2 + k) as usize] {
            equal = false;
            break;
        }
    }
    if equal {
        memo[key] = 1;
        return true;
    }
    let mut counts = [0i64; 26];
    for k in 0..len {
        counts[(s1[(i1 + k) as usize] as i64 - 97) as usize] += 1;
        counts[(s2[(i2 + k) as usize] as i64 - 97) as usize] -= 1;
    }
    for c in 0..26 {
        if counts[c] != 0 {
            memo[key] = 0;
            return false;
        }
    }
    let mut split = 1;
    while split < len {
        if scramble(s1, i1, s2, i2, split, memo, n)
            && scramble(s1, i1 + split, s2, i2 + split, len - split, memo, n)
        {
            memo[key] = 1;
            return true;
        }
        if scramble(s1, i1, s2, i2 + len - split, split, memo, n)
            && scramble(s1, i1 + split, s2, i2, len - split, memo, n)
        {
            memo[key] = 1;
            return true;
        }
        split += 1;
    }
    memo[key] = 0;
    false
}

fn one(len: i64, seed: i64) -> i64 {
    let mut s1: Vec<u8> = Vec::with_capacity(len as usize);
    for j in 0..len {
        s1.push((97 + (j % 8)) as u8);
    }
    let mut s2: Vec<u8> = Vec::with_capacity(len as usize);
    for j in 0..len {
        s2.push(s1[((j * 5 + seed) % len) as usize]);
    }
    let cells = (len * len * (len + 1)) as usize;
    let mut memo = vec![-1i64; cells];
    let r = if scramble(&s1, 0, &s2, 0, len, &mut memo, len) { 1 } else { 0 };
    let mut h = r;
    for i in 0..cells {
        h = (h * 131 + (memo[i] + 2)) % 1_000_000_007;
    }
    h
}

fn main() {
    let sum: i64 = (0..60000_i64).into_par_iter().map(|k| one(12, k)).sum();
    println!("{}", sum);
}
