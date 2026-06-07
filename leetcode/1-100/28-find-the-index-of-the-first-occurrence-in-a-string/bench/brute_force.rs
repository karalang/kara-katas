//! Benchmark workload — brute-force sliding-window strStr.
//!
//! Algorithmic mirror of bench/brute_force.kara and bench/brute_force.py. See
//! ../README.md § Benchmarks for the adversarial input and N, M, K.

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

    let mut total: i64 = 0;
    for _ in 0..10 {
        total += str_str(&haystack, &needle);
    }
    println!("{}", total);
}
