// LeetCode #2017: Grid Game -- the ★ arm's benchmark, a mirror of grid.kara.

fn grid_game(grid: &[Vec<i64>]) -> i64 {
    let mut top: i64 = grid[0].iter().sum();
    let mut bottom = 0i64;
    let mut best = i64::MAX;
    for i in 0..grid[0].len() {
        top -= grid[0][i];
        best = best.min(top.max(bottom));
        bottom += grid[1][i];
    }
    best
}

fn next_random(seed: &mut i64) -> i64 {
    *seed = (*seed * 1103515245 + 12345) % 2147483648;
    *seed / 65536
}

fn main() {
    let mut seed = 2017i64;
    let mut grids: Vec<Vec<Vec<i64>>> = Vec::new();
    for _ in 0..200 {
        let mut grid = Vec::new();
        for _ in 0..2 {
            let mut row = Vec::new();
            for _ in 0..50000 {
                row.push(next_random(&mut seed) * 3 % 100000 + 1);
            }
            grid.push(row);
        }
        grids.push(grid);
    }
    let (mut calls, mut sum, mut check) = (0i64, 0i64, 0i64);
    for _ in 0..10 {
        for grid in &grids {
            let answer = grid_game(grid);
            calls += 1;
            sum += answer;
            check = (check * 31 + answer) % 1000000007;
        }
    }
    println!("{calls} calls: sum {sum}, checksum {check}");
}
