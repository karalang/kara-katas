// LeetCode #1074: Number of Submatrices That Sum to Target -- the
// benchmark's Rust mirror of submatrix_sum.kara: the same row pairs and a
// std `HashMap` (SipHash-1-3, as Kāra's `Map`) of running totals, over 30
// matrices of 100 by 100 built once, each counted for three targets.

use std::collections::HashMap;

fn num_submatrix_sum_target(matrix: &[Vec<i64>], target: i64) -> i64 {
    let m = matrix.len();
    let n = matrix[0].len();
    let mut count = 0;
    for top in 0..m {
        let mut column = vec![0i64; n];
        for bottom in top..m {
            for c in 0..n {
                column[c] += matrix[bottom][c];
            }
            let mut seen: HashMap<i64, i64> = HashMap::new();
            seen.insert(0, 1);
            let mut total = 0;
            for c in 0..n {
                total += column[c];
                count += seen.get(&(total - target)).copied().unwrap_or(0);
                let k = seen.get(&total).copied().unwrap_or(0) + 1;
                seen.insert(total, k);
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1074;
    let mut matrices: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..30 {
        let mut matrix = Vec::new();
        for _ in 0..100 {
            let mut row = Vec::new();
            for _ in 0..100 {
                row.push(next_random(&mut seed) % 7 - 3);
            }
            matrix.push(row);
        }
        matrices.push(matrix);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for matrix in &matrices {
        for target in [-5, 0, 7] {
            let x = num_submatrix_sum_target(matrix, target);
            total += x;
            check = (check * 31 + x) % 1000000007;
        }
    }
    println!("90 calls: {} submatrices, checksum {}", total, check);
}
