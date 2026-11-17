// LeetCode #1594: Maximum Non Negative Product in a Matrix
// -- the bench in Rust, mirroring product.kara: the largest and the
// smallest product of a path reaching each cell, in two Vec<Vec<i64>>
// tables, on 40000 grids of 15 by 15 cells from -4 to 4, all drawn first.

fn max_product_path(grid: &[Vec<i32>]) -> i32 {
    let rows = grid.len();
    let cols = grid[0].len();
    let mut hi = vec![vec![0i64; cols]; rows];
    let mut lo = vec![vec![0i64; cols]; rows];
    for r in 0..rows {
        for c in 0..cols {
            let v = grid[r][c] as i64;
            if r == 0 && c == 0 {
                hi[r][c] = v;
                lo[r][c] = v;
                continue;
            }
            let mut best = i64::MIN;
            let mut worst = i64::MAX;
            if r > 0 {
                best = best.max(hi[r - 1][c] * v).max(lo[r - 1][c] * v);
                worst = worst.min(hi[r - 1][c] * v).min(lo[r - 1][c] * v);
            }
            if c > 0 {
                best = best.max(hi[r][c - 1] * v).max(lo[r][c - 1] * v);
                worst = worst.min(hi[r][c - 1] * v).min(lo[r][c - 1] * v);
            }
            hi[r][c] = best;
            lo[r][c] = worst;
        }
    }
    let top = hi[rows - 1][cols - 1];
    if top < 0 { -1 } else { (top % 1000000007) as i32 }
}

fn main() {
    let mut seed: i64 = 1594;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let grids: Vec<Vec<Vec<i32>>> = (0..40000)
        .map(|_| (0..15).map(|_| (0..15).map(|_| (next_random() % 9 - 4) as i32).collect()).collect())
        .collect();
    let mut check: i64 = 0;
    let mut negative = 0;
    for grid in &grids {
        let answer = max_product_path(grid);
        if answer == -1 {
            negative += 1;
        }
        check = (check * 31 + answer as i64 + 1) % 1000000007;
    }
    println!("40000 grids of 15 by 15: {} only negative, checksum {}", negative, check);
}
