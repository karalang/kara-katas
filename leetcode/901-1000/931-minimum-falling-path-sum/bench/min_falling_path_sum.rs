// LeetCode #931: Minimum Falling Path Sum -- bench: one row of sums at a
// time. Mirrors min_falling_path_sum.kara.

fn min_falling_path_sum(matrix: &[Vec<i64>]) -> i64 {
    let n = matrix.len();
    let mut prev = matrix[0].clone();
    for r in 1..n {
        let mut cur = vec![0i64; n];
        for c in 0..n {
            let mut best = prev[c];
            if c > 0 && prev[c - 1] < best {
                best = prev[c - 1];
            }
            if c + 1 < n && prev[c + 1] < best {
                best = prev[c + 1];
            }
            cur[c] = matrix[r][c] + best;
        }
        prev = cur;
    }
    let mut answer = prev[0];
    for &v in &prev {
        if v < answer {
            answer = v;
        }
    }
    answer
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let (rounds, count, n) = (150, 100, 100);
    let mut seed = 931;
    // count matrices of n x n values from -100 to 100, built once
    let mut matrices: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..count {
        let mut matrix: Vec<Vec<i64>> = Vec::new();
        for _ in 0..n {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..n {
                row.push(next_random(&mut seed) % 201 - 100);
            }
            matrix.push(row);
        }
        matrices.push(matrix);
    }
    let mut total: i64 = 0;
    let mut check: i64 = 0;
    for r in 0..rounds {
        // each round visits every matrix, starting from a different one
        for i in 0..count {
            let a = min_falling_path_sum(&matrices[(r + i) % count]);
            total += a;
            check = (check * 1000003 + a + 1000000) % 1000000007;
        }
    }
    println!("{rounds} rounds over {count} matrices of {n} x {n}: answers summing to {total}, checksum {check}");
}
