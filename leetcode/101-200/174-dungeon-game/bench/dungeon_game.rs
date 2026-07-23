fn max_i64(a: i64, b: i64) -> i64 { if a > b { a } else { b } }
fn min_i64(a: i64, b: i64) -> i64 { if a < b { a } else { b } }

fn calculate_minimum_hp(grid: &[i64], dp: &mut [i64], m: i64, n: i64) -> i64 {
    for i in (0..m).rev() {
        let base = i * n;
        for j in (0..n).rev() {
            let cell = grid[(base + j) as usize];
            let need;
            if i == m - 1 && j == n - 1 {
                need = max_i64(1, 1 - cell);
            } else if i == m - 1 {
                need = max_i64(1, dp[(base + j + 1) as usize] - cell);
            } else if j == n - 1 {
                need = max_i64(1, dp[(base + n + j) as usize] - cell);
            } else {
                let ahead = min_i64(dp[(base + n + j) as usize], dp[(base + j + 1) as usize]);
                need = max_i64(1, ahead - cell);
            }
            dp[(base + j) as usize] = need;
        }
    }
    dp[0]
}

fn main() {
    let m: i64 = 200;
    let n: i64 = 200;
    let passes: i64 = 2000;
    let total = (m * n) as usize;
    let mut grid = vec![0i64; total];
    let mut state: i64 = 12345;
    for c in 0..total {
        state = (state * 1103515245 + 12345) & 2147483647;
        grid[c] = (state % 121) - 100;
    }
    let mut dp = vec![0i64; total];
    let mut sink: i64 = 0;
    for p in 0..passes {
        let idx = ((p * 131 + 7) % (m * n)) as usize;
        grid[idx] = -grid[idx];
        sink += calculate_minimum_hp(&grid, &mut dp, m, n);
    }
    println!("{}", sink);
}
