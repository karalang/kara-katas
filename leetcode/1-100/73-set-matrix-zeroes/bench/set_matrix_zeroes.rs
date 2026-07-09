// Benchmark workload — Set Matrix Zeroes (LeetCode #73).
// Rust mirror of bench/set_matrix_zeroes.kara. Faithful to the kata's Vec-of-Vec
// matrix: each row is a Vec<i64> grown by push and the matrix is a Vec<Vec<i64>>
// grown by push — NOT a fixed [[i64; N]; N] — so the comparison measures the same
// growing-dynamic-array discipline as Kāra's `Vec.new()+push` (the #72 fairness
// lesson). O(1)-space first-row/col marker algorithm, K=100_000 iters over a
// 20×20 matrix with three punched zeros.
// See ../README.md § Benchmarks.

fn set_zeroes(m: &mut Vec<Vec<i64>>) {
    let rows = m.len();
    if rows == 0 {
        return;
    }
    let cols = m[0].len();

    let mut first_row_zero = false;
    let mut first_col_zero = false;
    for j in 0..cols {
        if m[0][j] == 0 {
            first_row_zero = true;
        }
    }
    for i in 0..rows {
        if m[i][0] == 0 {
            first_col_zero = true;
        }
    }

    for i in 1..rows {
        for j in 1..cols {
            if m[i][j] == 0 {
                m[i][0] = 0;
                m[0][j] = 0;
            }
        }
    }

    for i in 1..rows {
        for j in 1..cols {
            if m[i][0] == 0 || m[0][j] == 0 {
                m[i][j] = 0;
            }
        }
    }

    if first_row_zero {
        for j in 0..cols {
            m[0][j] = 0;
        }
    }
    if first_col_zero {
        for i in 0..rows {
            m[i][0] = 0;
        }
    }
}

fn main() {
    const TOTAL: i64 = 100_000;
    const MODULUS: i64 = 1_000_000_007;
    const ROWS: i64 = 20;
    const COLS: i64 = 20;

    let mut acc: i64 = 0;
    for k in 0..TOTAL {
        let mut m: Vec<Vec<i64>> = Vec::new();
        for i in 0..ROWS {
            let mut row: Vec<i64> = Vec::new();
            for j in 0..COLS {
                row.push(1 + (i * 31 + j * 17 + k) % 9);
            }
            m.push(row);
        }
        m[(k % ROWS) as usize][(k % COLS) as usize] = 0;
        m[((k * 7) % ROWS) as usize][((k * 13) % COLS) as usize] = 0;
        m[((k * 3) % ROWS) as usize][((k * 11) % COLS) as usize] = 0;

        set_zeroes(&mut m);

        for i in 0..ROWS as usize {
            for j in 0..COLS as usize {
                acc = (acc * 131 + m[i][j]) % MODULUS;
            }
        }
    }
    println!("{}", acc);
}
