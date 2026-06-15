//! Benchmark workload — KMP strStr, same adversarial input as brute_force.rs.
//!
//! Algorithmic mirror of bench/kmp.kara and bench/kmp.py. See ../README.md.

fn build_lps(pat: &[u8], m: i64) -> Vec<i64> {
    let mut lps = vec![0i64; m as usize];
    let mut len = 0i64;
    let mut i = 1i64;
    while i < m {
        if pat[i as usize] == pat[len as usize] {
            len += 1;
            lps[i as usize] = len;
            i += 1;
        } else if len > 0 {
            len = lps[(len - 1) as usize];
        } else {
            lps[i as usize] = 0;
            i += 1;
        }
    }
    lps
}

fn str_str(haystack: &[u8], needle: &[u8]) -> i64 {
    let hn = haystack.len() as i64;
    let nn = needle.len() as i64;
    if nn == 0 {
        return 0;
    }
    if nn > hn {
        return -1;
    }
    let lps = build_lps(needle, nn);
    let mut i = 0i64;
    let mut j = 0i64;
    while i < hn {
        if haystack[i as usize] == needle[j as usize] {
            i += 1;
            j += 1;
            if j == nn {
                return i - nn;
            }
        } else if j > 0 {
            j = lps[(j - 1) as usize];
        } else {
            i += 1;
        }
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

    let mut total: i64 = 0;
    for _ in 0..100 {
        total += str_str(&haystack, &needle);
    }
    println!("{}", total);
}
