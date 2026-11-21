// LeetCode #2435: Paths in Matrix Whose Sum Is Divisible by K -- the
// bench, the ★ arm: one row of counts by remainder, each cell's from
// above, still in place, and from the left, shifted by its value.

const MOD: i64 = 1000000007;

fn number_of_paths(grid: &[Vec<i64>], k: usize) -> i64 {
    let n = grid[0].len();
    let mut row: Vec<Vec<i64>> = vec![vec![0; k]; n];
    for i in 0..grid.len() {
        for j in 0..n {
            let mut came: Vec<i64> = vec![0; k];
            if i == 0 && j == 0 {
                came[0] = 1;
            }
            for r in 0..k {
                let left = if j > 0 { row[j - 1][r] } else { 0 };
                came[r] = (came[r] + row[j][r] + left) % MOD;
            }
            let v = grid[i][j] as usize;
            for r in 0..k {
                row[j][(r + v) % k] = came[r];
            }
        }
    }
    row[n - 1][0]
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2435;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..5 {
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..200 {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..250 {
                row.push(next_random(&mut seed) % 101);
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for p in 0..10i64 {
        for g in 0..grids.len() {
            grids[g][((p * 37) % 200) as usize][((p * 91) % 250) as usize] = p;
            check = (check * 31 + number_of_paths(&grids[g], 50) + p) % 1000000007;
        }
    }
    println!("10 passes over 5 grids of 200 by 250: checksum {}", check);
}
