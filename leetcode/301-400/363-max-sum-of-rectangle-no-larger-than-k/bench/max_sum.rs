// Benchmark for #363 -- mirror of max_sum.kara (the merge-sort arm).

fn best_pair(p: &mut [i64], lo: usize, hi: usize, k: i64, scratch: &mut [i64]) -> i64 {
    if hi - lo < 2 {
        return i64::MIN;
    }
    let mid = (lo + hi) / 2;
    let mut best = best_pair(p, lo, mid, k, scratch).max(best_pair(p, mid, hi, k, scratch));
    let mut j = mid;
    for i in lo..mid {
        while j < hi && p[j] <= p[i] + k {
            j += 1;
        }
        if j > mid {
            best = best.max(p[j - 1] - p[i]);
        }
    }
    let (mut a, mut b, mut out) = (lo, mid, lo);
    while a < mid || b < hi {
        if b == hi || (a < mid && p[a] <= p[b]) {
            scratch[out] = p[a];
            a += 1;
        } else {
            scratch[out] = p[b];
            b += 1;
        }
        out += 1;
    }
    p[lo..hi].copy_from_slice(&scratch[lo..hi]);
    best
}

fn max_sum_submatrix(matrix: &[Vec<i64>], k: i64) -> i64 {
    let rows = matrix.len();
    let cols = matrix[0].len();
    let mut best = i64::MIN;
    let mut scratch = vec![0i64; cols + 1];
    for top in 0..rows {
        let mut sums = vec![0i64; cols];
        for bottom in top..rows {
            for c in 0..cols {
                sums[c] += matrix[bottom][c];
            }
            let mut prefix = vec![0i64; cols + 1];
            for c in 0..cols {
                prefix[c + 1] = prefix[c] + sums[c];
            }
            best = best.max(best_pair(&mut prefix, 0, cols + 1, k, &mut scratch));
        }
    }
    best
}

fn main() {
    let mut seed: i64 = 363;
    let mut checksum: i64 = 0;
    for _ in 0..20 {
        let mut matrix: Vec<Vec<i64>> = Vec::new();
        let mut least = 100;
        for _ in 0..100 {
            let mut row = Vec::new();
            for _ in 0..100 {
                seed = (seed * 1103515245 + 12345) % 2147483648;
                let v = (seed / 65536) % 201 - 100;
                least = least.min(v);
                row.push(v);
            }
            matrix.push(row);
        }
        seed = (seed * 1103515245 + 12345) % 2147483648;
        let k = least.max((seed / 65536) % 20001 - 10000);
        checksum = (checksum * 31 + max_sum_submatrix(&matrix, k) + 1000000) % 1000000007;
    }
    println!("checksum {checksum}");
}
