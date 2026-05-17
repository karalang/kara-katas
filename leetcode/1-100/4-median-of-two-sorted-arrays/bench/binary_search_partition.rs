//! Benchmark workload — binary-search-partition O(log min(m, n)) Median of
//! Two Sorted Arrays.
//!
//! Algorithmic mirror of bench/binary_search_partition.kara and
//! bench/binary_search_partition.py. See ../README.md § Benchmarks for the
//! choice of M, N, R, K and the rotated-input shape.

fn middle_pair_off(
    a: &[i64], a_off: i64, a_len: i64,
    b: &[i64], b_off: i64, b_len: i64,
) -> (i64, i64) {
    if a_len > b_len {
        return middle_pair_off(b, b_off, b_len, a, a_off, a_len);
    }
    let half = (a_len + b_len + 1) / 2;
    let mut lo: i64 = 0;
    let mut hi: i64 = a_len;
    while lo <= hi {
        let i = (lo + hi) / 2;
        let j = half - i;
        let left_a  = if i > 0     { a[(a_off + i - 1) as usize] } else { i64::MIN };
        let right_a = if i < a_len { a[(a_off + i) as usize]     } else { i64::MAX };
        let left_b  = if j > 0     { b[(b_off + j - 1) as usize] } else { i64::MIN };
        let right_b = if j < b_len { b[(b_off + j) as usize]     } else { i64::MAX };
        if left_a > right_b {
            hi = i - 1;
        } else if left_b > right_a {
            lo = i + 1;
        } else {
            let lower = left_a.max(left_b);
            if (a_len + b_len) % 2 == 1 {
                return (lower, lower);
            }
            let upper = right_a.min(right_b);
            return (lower, upper);
        }
    }
    unreachable!()
}

fn main() {
    const M: i64 = 1_000_000;
    const N: i64 = 1_000_000;
    const R: i64 = 1_000;
    const K: i64 = 10_000_000;

    let base_a: Vec<i64> = (0..(M + R)).map(|p| 2 * p).collect();
    let base_b: Vec<i64> = (0..(N + R)).map(|p| 2 * p + 1).collect();

    let mut sum: i64 = 0;
    let mut k: i64 = 0;
    while k < K {
        let off = k % R;
        let (lower, upper) = middle_pair_off(&base_a, off, M, &base_b, off, N);
        sum += lower + upper;
        k += 1;
    }
    println!("{}", sum);
}
