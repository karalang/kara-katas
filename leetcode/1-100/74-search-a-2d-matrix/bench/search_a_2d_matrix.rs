// Benchmark workload — Search a 2D Matrix (LeetCode #74).
// Rust mirror of bench/search_a_2d_matrix.kara. Flattened binary search over a
// 100×100 matrix built ONCE as a Vec<Vec<i64>> (double-indirection, matching
// Kāra's Vec[Vec[i64]]), then K=10_000_000 queries (targets k % 20000, ~half hit)
// folding each hit/miss bit into a rolling polynomial hash. The search is the
// measured work. See ../README.md § Benchmarks.

fn search_matrix(m: &Vec<Vec<i64>>, target: i64) -> bool {
    let rows = m.len();
    if rows == 0 {
        return false;
    }
    let cols = m[0].len();
    if cols == 0 {
        return false;
    }
    let mut lo: i64 = 0;
    let mut hi: i64 = (rows * cols) as i64 - 1;
    while lo <= hi {
        let mid = lo + (hi - lo) / 2;
        let v = m[(mid / cols as i64) as usize][(mid % cols as i64) as usize];
        if v == target {
            return true;
        } else if v < target {
            lo = mid + 1;
        } else {
            hi = mid - 1;
        }
    }
    false
}

fn main() {
    const ROWS: i64 = 100;
    const COLS: i64 = 100;
    const TOTAL: i64 = 10_000_000;
    const MODULUS: i64 = 1_000_000_007;
    let range = 2 * ROWS * COLS;

    let mut m: Vec<Vec<i64>> = Vec::new();
    for i in 0..ROWS {
        let mut row: Vec<i64> = Vec::new();
        for j in 0..COLS {
            row.push((i * COLS + j) * 2);
        }
        m.push(row);
    }

    let mut acc: i64 = 0;
    for k in 0..TOTAL {
        let target = k % range;
        let bit = if search_matrix(&m, target) { 1 } else { 0 };
        acc = (acc * 131 + bit) % MODULUS;
    }
    println!("{}", acc);
}
