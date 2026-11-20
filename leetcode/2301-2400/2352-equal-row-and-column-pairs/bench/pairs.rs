// LeetCode #2352: Equal Row and Column Pairs -- the bench, the ★ arm in
// Rust: the rows counted in a `HashMap` keyed by the row, then each column
// built and looked up there.

use std::collections::HashMap;

fn equal_pairs(grid: &[Vec<i64>]) -> i64 {
    let n = grid.len();
    let mut rows: HashMap<Vec<i64>, i64> = HashMap::new();
    for row in grid {
        let count = rows.get(row).copied().unwrap_or(0);
        rows.insert(row.clone(), count + 1);
    }
    let mut total = 0i64;
    for j in 0..n {
        let column: Vec<i64> = (0..n).map(|i| grid[i][j]).collect();
        total += rows.get(&column).copied().unwrap_or(0);
    }
    total
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    // grid g is 200 x 200, cell (i, j) being (a i j + b) mod m, so that
    // rows repeat and match columns, with a in 1 to 5 and m in 2 to 10
    let mut seed = 2352i64;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..10 {
        let a = 1 + next_random(&mut seed) % 5;
        let b = next_random(&mut seed) % 10;
        let m = 2 + next_random(&mut seed) % 9;
        let grid: Vec<Vec<i64>> = (0..200i64)
            .map(|i| (0..200i64).map(|j| (a * i * j + b) % m).collect())
            .collect();
        grids.push(grid);
    }
    let mut check = 0i64;
    for p in 0..40i64 {
        for grid in &grids {
            check = (check * 31 + equal_pairs(grid) + p) % 1000000007;
        }
    }
    println!("40 passes over 10 grids of 200 x 200: checksum {}", check);
}
