// LeetCode #1254 bench, in Rust: the ★ arm (each island flooded to water
// by recursion from its first cell, and counted when no cell of it reached
// the edge) on 100 random 100 by 100 grids built once, each with its own
// share of land from 20 to 80 in 100; each copied and asked 40 times,
// every count folded into a checksum.

fn closed(grid: &mut Vec<Vec<i64>>, i: i64, j: i64) -> bool {
    if i < 0 || j < 0 || i >= grid.len() as i64 || j >= grid[0].len() as i64 {
        return false;
    }
    if grid[i as usize][j as usize] == 1 {
        return true;
    }
    grid[i as usize][j as usize] = 1;
    let up = closed(grid, i - 1, j);
    let down = closed(grid, i + 1, j);
    let left = closed(grid, i, j - 1);
    let right = closed(grid, i, j + 1);
    up && down && left && right
}

fn closed_island(mut grid: Vec<Vec<i64>>) -> i64 {
    let mut count = 0;
    for i in 0..grid.len() {
        for j in 0..grid[0].len() {
            if grid[i][j] == 0 && closed(&mut grid, i as i64, j as i64) {
                count += 1;
            }
        }
    }
    count
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 1254;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..100 {
        let land = next_random(&mut seed) % 61 + 20;
        let mut grid = Vec::new();
        for _ in 0..100 {
            let mut row = Vec::new();
            for _ in 0..100 {
                row.push(if next_random(&mut seed) % 100 < land { 0 } else { 1 });
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let mut check: i64 = 0;
    for _ in 0..40 {
        for grid in &grids {
            check = (check * 131 + closed_island(grid.clone())) % 1000000007;
        }
    }
    println!("40 rounds of 100 grids of 100 by 100: checksum {check}");
}
