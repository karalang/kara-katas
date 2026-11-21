// LeetCode #2482: Difference Between Ones and Zeros in Row and Column --
// bench, Rust mirror of diff.kara.

fn ones_minus_zeros(grid: &[Vec<i64>]) -> Vec<Vec<i64>> {
    let m = grid.len();
    let n = grid[0].len();
    let mut row_ones = vec![0i64; m];
    let mut col_ones = vec![0i64; n];
    for i in 0..m {
        for j in 0..n {
            row_ones[i] += grid[i][j];
            col_ones[j] += grid[i][j];
        }
    }
    let mut diff = Vec::new();
    for i in 0..m {
        let mut row = Vec::new();
        for j in 0..n {
            row.push(2 * row_ones[i] + 2 * col_ones[j] - m as i64 - n as i64);
        }
        diff.push(row);
    }
    diff
}

fn main() {
    let mut seed: i64 = 2482;
    let mut next_random = || {
        seed = (seed * 1103515245 + 12345) % 2147483648;
        seed / 65536
    };
    let mut grids: Vec<Vec<Vec<i64>>> = (0..20).map(|_| (0..100).map(|_| (0..100).map(|_| next_random() % 2).collect()).collect()).collect();
    let mut check: i64 = 0;
    for p in 0..180 {
        for g in 0..20 {
            let (i, j) = ((check % 100) as usize, (check / 100 % 100) as usize);
            grids[g][i][j] = 1 - grids[g][i][j];
            let diff = ones_minus_zeros(&grids[g]);
            for row in &diff {
                for &v in row {
                    check = (check * 31 + v + 200 + p) % 1000000007;
                }
            }
        }
    }
    println!("180 passes over 20 grids of 100 by 100: checksum {}", check);
}
