// Benchmark workload — Minimum Window Substring (LeetCode #76).
// Rust mirror of bench/minimum_window_substring.kara. Sliding-window need/have
// algorithm over a fixed n=50000 sequence (alphabet {0,1,2,3}) built once, K=5000
// iterations against a k-cycled 3-symbol target, folding (start, len) into a
// rolling hash. The O(n) window scan is the measured work. See ../README.md.

fn min_window(s: &[i64], t: &[i64]) -> (i64, i64) {
    let n = s.len() as i64;
    let m = t.len() as i64;
    if m > n {
        return (-1, 0);
    }
    let mut need = [0i64; 4];
    let mut required = 0i64;
    for &c in t {
        if need[c as usize] == 0 {
            required += 1;
        }
        need[c as usize] += 1;
    }
    let mut have = [0i64; 4];
    let mut formed = 0i64;
    let mut l = 0i64;
    let mut best_start = -1i64;
    let mut best_len = 0i64;
    let mut r = 0i64;
    while r < n {
        let cr = s[r as usize] as usize;
        have[cr] += 1;
        if have[cr] == need[cr] {
            formed += 1;
        }
        while formed == required {
            let win = r - l + 1;
            if best_start == -1 || win < best_len {
                best_start = l;
                best_len = win;
            }
            let cl = s[l as usize] as usize;
            have[cl] -= 1;
            if have[cl] < need[cl] {
                formed -= 1;
            }
            l += 1;
        }
        r += 1;
    }
    (best_start, best_len)
}

fn main() {
    const N: i64 = 50000;
    const TOTAL: i64 = 5000;
    const MODULUS: i64 = 1_000_000_007;

    let mut s: Vec<i64> = Vec::new();
    for i in 0..N {
        s.push((i * 7) % 4);
    }
    let targets: [[i64; 3]; 6] = [
        [0, 1, 2], [1, 2, 3], [2, 3, 0], [3, 0, 1], [0, 2, 3], [1, 3, 0],
    ];

    let mut acc: i64 = 0;
    for k in 0..TOTAL {
        let t = &targets[(k % 6) as usize];
        let (start, len) = min_window(&s, t);
        acc = (acc * 131 + (start + 1)) % MODULUS;
        acc = (acc * 131 + len) % MODULUS;
    }
    println!("{}", acc);
}
