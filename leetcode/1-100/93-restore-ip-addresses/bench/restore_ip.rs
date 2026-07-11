// Benchmark workload — Restore IP Addresses (LeetCode #93).
// Rust mirror of bench/restore_ip.kara. Folds the segment values of every valid
// four-segment quadruple through a rolling polynomial hash; digits computed inline from
// the iteration index (no array). Input length varies per iteration (n = 4 + iter%9) so
// the fixed-shape enumeration can't be vectorized away. K=6,500,000. Compiled with
// `rustc -O`. See ../README.md § Benchmarks.

fn digit(pos: i64, iter: i64) -> i64 {
    (pos * 7 + iter) % 10
}

fn seg_val(start: i64, len: i64, iter: i64) -> i64 {
    if len < 1 || len > 3 {
        return -1;
    }
    if len > 1 && digit(start, iter) == 0 {
        return -1;
    }
    let mut v = 0i64;
    let mut i = 0i64;
    while i < len {
        v = v * 10 + digit(start + i, iter);
        i += 1;
    }
    if v > 255 {
        return -1;
    }
    v
}

fn restore_fold(n: i64, iter: i64, seed: i64) -> i64 {
    let mut acc = seed;
    let mut a = 1i64;
    while a <= 3 && a < n {
        let v0 = seg_val(0, a, iter);
        if v0 >= 0 {
            let mut b = a + 1;
            while b <= a + 3 && b < n {
                let v1 = seg_val(a, b - a, iter);
                if v1 >= 0 {
                    let mut c = b + 1;
                    while c <= b + 3 && c < n {
                        let v2 = seg_val(b, c - b, iter);
                        let v3 = seg_val(c, n - c, iter);
                        if v2 >= 0 && v3 >= 0 {
                            acc = (acc * 131 + v0 * 1000000 + v1 * 10000 + v2 * 100 + v3 + 1)
                                % 1_000_000_007;
                        }
                        c += 1;
                    }
                }
                b += 1;
            }
        }
        a += 1;
    }
    acc
}

fn main() {
    const TOTAL: i64 = 6_500_000;
    const MODULUS: i64 = 1_000_000_007;
    let mut sum = 0i64;
    for iter in 0..TOTAL {
        let n = 4 + (iter % 9); // 4..12 — data-dependent length
        sum = (sum * 131 + restore_fold(n, iter, iter)) % MODULUS;
    }
    println!("{}", sum);
}
