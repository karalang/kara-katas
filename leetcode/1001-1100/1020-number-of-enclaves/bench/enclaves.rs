// LeetCode #1020: Number of Enclaves -- bench
// Mirrors ./enclaves.kara; see ../README.md § Benchmarks.

fn num_enclaves(grid: &Vec<Vec<i64>>) -> i64 {
    let m = grid.len() as i64;
    let n = grid[0].len() as i64;
    let mut land = grid.clone();
    let mut stack: Vec<(i64, i64)> = Vec::new();
    for i in 0..m {
        for j in 0..n {
            if (i == 0 || j == 0 || i == m - 1 || j == n - 1) && land[i as usize][j as usize] == 1 {
                land[i as usize][j as usize] = 0;
                stack.push((i, j));
            }
        }
    }
    let steps = [(1, 0), (-1, 0), (0, 1), (0, -1)];
    while let Some((i, j)) = stack.pop() {
        for (di, dj) in steps.iter() {
            let (a, b) = (i + di, j + dj);
            if a >= 0 && a < m && b >= 0 && b < n && land[a as usize][b as usize] == 1 {
                land[a as usize][b as usize] = 0;
                stack.push((a, b));
            }
        }
    }
    let mut left = 0;
    for row in land.iter() {
        for c in row.iter() {
            left += c;
        }
    }
    left
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let count = 100;
    let rounds = 20;
    let mut seed = 1020;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    let mut cells = 0;
    for _ in 0..count {
        let m = next_random(&mut seed) % 500 + 1;
        let n = next_random(&mut seed) % 500 + 1;
        let land = 2 + next_random(&mut seed) % 5;
        let mut grid: Vec<Vec<i64>> = Vec::new();
        for _ in 0..m {
            let mut row: Vec<i64> = Vec::new();
            for _ in 0..n {
                row.push(if next_random(&mut seed) % 8 < land { 1 } else { 0 });
            }
            grid.push(row);
        }
        cells += m * n;
        grids.push(grid);
    }
    let mut total = 0i64;
    let mut check = 0i64;
    for _ in 0..rounds {
        for grid in grids.iter() {
            let a = num_enclaves(grid);
            total += a;
            check = (check * 31 + a) % 1000000007;
        }
    }
    println!("{count} grids, {cells} cells, {rounds} rounds: {total} enclaves, checksum {check}");
}
