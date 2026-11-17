// LeetCode #2245: Maximum Trailing Zeros in a Cornered Path -- the
// benchmark's Rust mirror of zeros.kara: prefix sums of the twos and
// fives of each row and column, every cell tried as the corner.

fn count_factor(value: i64, p: i64) -> i64 {
    let mut v = value;
    let mut count = 0;
    while v % p == 0 {
        v /= p;
        count += 1;
    }
    count
}

fn max_trailing_zeros(grid: &[Vec<i64>]) -> i64 {
    let m = grid.len();
    let n = grid[0].len();
    let mut row_twos = vec![vec![0i64; n + 1]; m];
    let mut row_fives = vec![vec![0i64; n + 1]; m];
    let mut col_twos = vec![vec![0i64; n]; m + 1];
    let mut col_fives = vec![vec![0i64; n]; m + 1];
    for i in 0..m {
        for j in 0..n {
            let t = count_factor(grid[i][j], 2);
            let f = count_factor(grid[i][j], 5);
            row_twos[i][j + 1] = row_twos[i][j] + t;
            row_fives[i][j + 1] = row_fives[i][j] + f;
            col_twos[i + 1][j] = col_twos[i][j] + t;
            col_fives[i + 1][j] = col_fives[i][j] + f;
        }
    }
    let mut best = 0;
    for i in 0..m {
        for j in 0..n {
            let left = (row_twos[i][j + 1], row_fives[i][j + 1]);
            let right = (row_twos[i][n] - row_twos[i][j], row_fives[i][n] - row_fives[i][j]);
            let up = (col_twos[i][j], col_fives[i][j]);
            let down = (col_twos[m][j] - col_twos[i + 1][j], col_fives[m][j] - col_fives[i + 1][j]);
            for (ht, hf) in [left, right] {
                for (vt, vf) in [up, down] {
                    best = best.max((ht + vt).min(hf + vf));
                }
            }
        }
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2245i64;
    let mut check = 0i64;
    for _ in 0..40 {
        let grid: Vec<Vec<i64>> = (0..250).map(|_| (0..400).map(|_| next_random(&mut seed) % 1000 + 1).collect()).collect();
        check = (check * 31 + max_trailing_zeros(&grid) + 1) % 1000000007;
    }
    println!("40 grids of 250 x 400: checksum {}", check);
}
