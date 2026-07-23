fn max_side(grid: &[i64], dp: &mut [i64], rows: i64, cols: i64) -> i64 {
    for j in 0..cols { dp[j as usize] = 0; }
    let mut best = 0i64;
    for i in 0..rows {
        let base = i * cols;
        let mut prev_diag = 0i64;
        for j in 0..cols {
            let ju = j as usize;
            let temp = dp[ju];
            if grid[(base + j) as usize] == 1 {
                let mut v = 1i64;
                if i != 0 && j != 0 {
                    let mut m = dp[ju];
                    if dp[ju - 1] < m { m = dp[ju - 1]; }
                    if prev_diag < m { m = prev_diag; }
                    v = m + 1;
                }
                dp[ju] = v;
                if v > best { best = v; }
            } else {
                dp[ju] = 0;
            }
            prev_diag = temp;
        }
    }
    best
}

fn main() {
    let rows: i64 = 800;
    let cols: i64 = 800;
    let passes: i64 = 150;
    let total = (rows * cols) as usize;
    let mut grid = vec![0i64; total];
    let mut state: i64 = 12345;
    for c in 0..total {
        state = (state * 1103515245 + 12345) & 2147483647;
        grid[c] = if state % 100 < 62 { 1 } else { 0 };
    }
    let mut dp = vec![0i64; cols as usize];
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p % rows) * cols + ((p * 131 + 7) % cols)) as usize;
        grid[idx] = 1 - grid[idx];
        sink += max_side(&grid, &mut dp, rows, cols);
    }
    println!("{}", sink);
}
